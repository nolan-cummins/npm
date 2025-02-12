import sys
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import QIODevice, QByteArray
from PySide6.QtCore import QTime, QTimer, Slot
import pyqtgraph as pg
import numpy as np
from time import *
import warnings

import ctypes
myappid = 'nil.npm.pyqt.1' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from importlib import reload

import ui_main
reload(ui_main)
from ui_main import *

import ui_dialog
reload(ui_dialog)
from ui_dialog import *

from serial import *
import serial.tools.list_ports

class Dialog(QDialog, Ui_Dialog):
    def __init__(self, points, parent=None):
        QDialog.__init__(self, parent)
        self.points = points
        self.setupUi(self)
        self.setWindowTitle("Save Current Position")
        self.setWindowIcon(QtGui.QIcon('save_icon.png'))
        self.buttonBox.accepted.connect(self.on_save)
        self.comboBox.activated.connect(self.on_activate)
        self.comboBox.clear()
        self.comboBox.addItems(self.points)
        self.comboBox.setPlaceholderText('Select Save Point')
        self.selection=self.comboBox.itemText(0)
        self.index=0
        self.save=False
        comboBox=[]
        for i in range(0,self.comboBox.count()):
            comboBox.append(self.comboBox.itemText(i))
        print(str(comboBox), end='\r') 

    def on_activate(self):
        print(self.comboBox.currentText().ljust*(200), end='\r')
        self.selection=self.comboBox.currentText()
        self.index=self.comboBox.currentIndex()
    
    def on_save(self):
        self.comboBox.setItemText(self.index, self.name_input.text())
        self.save=True
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon('nanopen_icon.png'))
        self.setWindowTitle("Nanopen Manipulator")

        buttons = [
            (self.save_point, self.on_save_point), (self.set_zero, self.on_set_zero),
            (self.home, self.on_home), (self.step_mode, self.on_step_mode),
            (self.origin, self.on_origin), (self.free_mode, self.on_free_mode),
            (self.stop, self.on_stop)
        ]
        for btn, handler in buttons:
            btn.clicked.connect(handler)
            btn.setFocusPolicy(Qt.NoFocus)
        
        actions = [(self.actionum, self.on_unit_um), (self.actionsteps, self.on_unit_step)]
        for action, handler in actions:
            action.triggered.connect(handler)
        
        self.sp_vars = [[] for _ in range(5)]
        self.sp_buttons = [self.sp1, self.sp2, self.sp3, self.sp4, self.sp5]
        self.points = [btn.text() for btn in self.sp_buttons]
        
        for sp in self.sp_buttons:
            sp.clicked.connect(self.on_sp)
            sp.setFocusPolicy(Qt.NoFocus)
        
        inputs = [self.length_input, self.width_input, self.height_input]
        for inp in inputs:
            inp.editingFinished.connect(self.on_lwh_input)
        
        self.step_size.editingFinished.connect(self.on_step_size)
        self.speed.setValue(100)
        self.speed.valueChanged.connect(self.on_speed)
        
        self.main_plot.setMouseEnabled(x=True, y=True)
        self.main_plot.setFocusPolicy(QtCore.Qt.NoFocus.StrongFocus)
        self.main_plot.hideButtons()
        self.main_plot.showGrid(x=True, y=True)
        self.main_plot.setLabel("left", "Y (um)")
        self.main_plot.setLabel("bottom", "X (um)")
        
        self.z_axis.setFocusPolicy(QtCore.Qt.NoFocus.StrongFocus)
        self.z_axis.hideButtons()
        self.z_axis.hideAxis('bottom')
        self.z_axis.showGrid(x=False, y=True)
        self.z_axis.setLabel("left", "Z (um)")
        self.z_axis.setMouseEnabled(x=False, y=True)
        
        self.x = self.y = self.z = 0
        self.step_x = self.step_y = self.step_z = 0
        self.plot_x = self.plot_y = self.plot_z = self.x
        self.plot_x_actual = self.plot_y_actual = self.plot_z_actual = self.x
        
        self.is_key_W_pressed = self.is_key_A_pressed = self.is_key_S_pressed = self.is_key_D_pressed = False
        self.is_key_SHIFT_pressed = self.is_key_SPACE_pressed = False
        
        self.step_factor = 2.7662
        self.step = 36
        self.step_size.setValue(self.step * self.step_factor)
        self.is_step_mode = False
        for inp in inputs:
            inp.setSingleStep(round(self.step_factor, 0))
        
        self.l, self.w, self.h, self.unit = 100000, 300000, 300000, "um"
        self.on_lwh_input()
        
        self.timer, self.serial_timer, self.precisionTimer = QTimer(), QTimer(), QTimer()
        self.serialTimerDelay = 33
        self.precisionRunning = False
        
        self.serial = QSerialPort(self)
        self.serial.readyRead.connect(self.read_serial_data)
        self.buffer, self.com_port, self.serial_port = b'', '', ''
        self.ports = sorted(serial.tools.list_ports.comports())
        
        for port in self.ports:
            com_port = QAction(port[0], self, checkable=True)
            com_port.triggered.connect(self.on_serial)
            self.menuSerial.addAction(com_port)
            self.serial.setPortName(port[0])
            self.serial.close()
        
        self.zero = [0, 0, 0]
        self.i, self.x_runs, self.y_runs, self.z_runs, self.num_runs = 0, 0, 0, 0, 10
        self.initial_xyz, self.lastData = [], [0, 0, 0]
        self.sync, self.is_free_mode = False, False
    
    def changeUnit(self, unit):
        self.unit = unit
        self.x_display_label.setText(QCoreApplication.translate("MainWindow", f"X ({unit})", None))
        self.y_display_label.setText(QCoreApplication.translate("MainWindow", f"Y ({unit})", None))
        self.z_display_label.setText(QCoreApplication.translate("MainWindow", f"Z ({unit})", None))
        self.height_label.setText(QCoreApplication.translate("MainWindow", 
                                                             f"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Height ({unit})</span></p></body></html>",
                                                             None))
        self.width_label.setText(QCoreApplication.translate("MainWindow", 
                                                             f"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Width ({unit})</span></p></body></html>",
                                                             None))
        self.length_label.setText(QCoreApplication.translate("MainWindow", 
                                                             f"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Length ({unit})</span></p></body></html>",
                                                             None))
        self.step_size_label.setText(QCoreApplication.translate("MainWindow", f"<html><head/><body><p align=\"center\">Step Size ({unit})</p><p align=\"center\"><br/></p></body></html>", None))

        if self.unit == "um":
            l = self.length_input.value() * self.step_factor
            w = self.width_input.value() * self.step_factor
            h = self.height_input.value() * self.step_factor
            self.step_size.setValue(self.step*self.step_factor)
            self.length_input.setSingleStep(np.round(self.step_factor,0))
            self.width_input.setSingleStep(np.round(self.step_factor,0))
            self.height_input.setSingleStep(np.round(self.step_factor,0))
        elif self.unit == "steps":
            l = self.length_input.value() / self.step_factor
            w = self.width_input.value() / self.step_factor
            h = self.height_input.value() / self.step_factor
            self.step_size.setValue(self.step)
            self.length_input.setSingleStep(1)
            self.width_input.setSingleStep(1)
            self.height_input.setSingleStep(1)

        self.length_input.setValue(l)
        self.width_input.setValue(w)
        self.height_input.setValue(h)        
        self.plotFactor()
        self.on_lwh_input()
    
    def on_unit_um(self):
        self.actionsteps.setChecked(not self.actionum.isChecked())
        self.changeUnit("um")

    def on_unit_step(self):
        self.actionum.setChecked(not self.actionsteps.isChecked())
        self.changeUnit("steps")
    
    def plotFactor(self):
        if self.actionum.isChecked():
            self.plot_x=self.x*self.step_factor
            self.plot_y=self.y*self.step_factor
            self.plot_z=self.z*self.step_factor
            try:
                if self.serial.isOpen():
                    self.plot_x_actual=self.x_actual*self.step_factor
                    self.plot_y_actual=self.y_actual*self.step_factor
                    self.plot_z_actual=self.z_actual*self.step_factor
            except Exception as e:
                if "has no attribute" in str(e):
                    print("No active port!", end='\r')
                    pass
                else:
                    print(e)
                    pass
        else:
            self.plot_x=self.x
            self.plot_y=self.y
            self.plot_z=self.z
            try:
                if self.serial.isOpen():
                    self.plot_x_actual=self.x_actual
                    self.plot_y_actual=self.y_actual
                    self.plot_z_actual=self.z_actual
            except Exception as e:
                if "has no attribute" in str(e):
                    print("No active port!\r", end='\r')
                    pass
                else:
                    print(e)
                    pass
        
        self.x_display.display(self.plot_x)
        self.y_display.display(self.plot_y)
        self.z_display.display(self.plot_z)
        self.z_axis.clear()
        self.main_plot.clear()
        self.z_axis.plot([0], [self.plot_z], pen=None, symbol='o')
        self.main_plot.plot([self.plot_x], [self.plot_y], pen=None, symbol='o')

        try:
            if self.serial.isOpen():
                self.main_plot.plot([self.plot_x_actual], [self.plot_y_actual], pen=None, symbol='x')
                self.z_axis.plot([0], [self.plot_z_actual], pen=None, symbol='x')
        except:
            print("Error plotting feedback!")
            pass

        print(f'step: {self.step}, (x, l): {(self.x, self.l)}, (y, w): {(self.y, self.w)}, (z, h): {(self.z, self.h)}'.ljust(200), end='\r')
    
    def on_serial(self):
        for port in self.menuSerial.actions():
            try:
                if port.isChecked():
                    self.com_port = port.text()
                    self.serial.setPortName(self.com_port) 
                    self.serial.setBaudRate(QSerialPort.Baud9600)
                    self.serial.setDataBits(QSerialPort.Data8)
                    self.serial.setParity(QSerialPort.NoParity)
                    self.serial.setStopBits(QSerialPort.OneStop)
                    self.serial.setFlowControl(QSerialPort.NoFlowControl)
                if not self.serial.open(QIODevice.ReadWrite) or not port.isChecked():
                    self.sync = False
                    self.serial_timer.stop()
                    self.serial_timer.timeout.disconnect(self.start_Serial_Move)
                    port.setChecked(False)
                    self.serial.close()
                    print(f"Closed port: {self.com_port}".ljust(200))
                    self.connection.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">Status: Disconnected</span></p></body></html>", None))
                else:
                    if not self.serial_timer.isActive():
                        self.serial.write(f'C{self.x};{self.y};{self.z}\n'.encode('utf_8'))
                        self.serial_timer.timeout.connect(self.start_Serial_Move)
                        self.serial_timer.start(self.serialTimerDelay)
                        print(f"Opened port: {self.com_port}".ljust(200))
                        self.connection.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">Status: Connected</span></p></body></html>", None))
                        self.sync = True
                    break
            except Exception as e:
                port.setChecked(False)
                self.connection.setText(QCoreApplication.translate("MainWindow", f'<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">Status: {str(e)}</span></p></body></html>', None))
                print(str(e) + ' '*200, end='\r')

    def read_serial_data(self):
        try:
            incoming_data = self.serial.readAll().data()
            if not incoming_data:
                return
            self.buffer += incoming_data
            while b'\n' in self.buffer:
                line, self.buffer = self.buffer.split(b'\n', 1)
                decoded_data = line.decode('utf_8')
                print(f'ARDUINO: {decoded_data.strip()}'.ljust(200), end='\r')
                self.print.setText(QCoreApplication.translate("MainWindow", f'<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">{decoded_data.strip()}</span></p></body>'))
                if "C" in decoded_data:
                    coords = decoded_data[1:].split(';',3)
                    if len(coords)==3:
                        try:
                            self.x_actual=int(coords[0])
                            self.y_actual=int(coords[1])
                            self.z_actual=int(coords[2])
                        except:
                            pass
                        try:
                            self.plotFactor()
                        except ValueError as ve:
                            print(f"Error converting coordinates: {ve}")
                if "L" in decoded_data:
                    limit = decoded_data[1:].split(';',3)
                    self.l=int(limit[0].split('.',1)[0])
                    self.w=int(limit[1].split('.',1)[0])
                    self.h=int(limit[2].split('.',1)[0])
                    self.x=0
                    self.y=0
                    self.z=0
                    self.on_lwh_input()
        except Exception as e:
            print(f"Error reading serial data: {e}")

    def on_free_mode(self, checked):
        self.is_free_mode=checked

    def on_stop(self):
        try:
            if self.serial.isOpen() and self.sync:
                self.serial.write('s\n'.encode('utf_8'))
        except Exception as e: print(str(e).ljust(200), end='\r')        

    def on_sp(self):
        button = self.sender().objectName()
        try:
            if button == 'sp1':
                self.x, self.y, self.z =self.sp1_xyz   
            elif button == 'sp2':
                self.x, self.y, self.z =self.sp2_xyz      
            elif button == 'sp3':
                self.x, self.y, self.z =self.sp3_xyz     
            elif button == 'sp4':
                self.x, self.y, self.z =self.sp4_xyz     
            elif button == 'sp5':
                self.x, self.y, self.z =self.sp5_xyz
        except:
            pass
        finally:
            self.plotFactor()       
            
    def on_origin(self): # origin
        self.x=0
        self.y=0
        self.z=0

        self.plotFactor()
    
    def start_move(self):
        if not self.timer.isActive():
            self.timer.timeout.connect(self.WASDMove)
            self.timer.start(33)
        
    def stop_move(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Failed to disconnect")
            try:
                self.timer.stop()
                self.timer.timeout.disconnect(self.WASDMove)              
            except:
                pass

    def start_Serial_Move(self):
        try:
            if self.serial.isOpen() and self.sync:
                if self.x_actual != self.x or self.y_actual != self.y or self.z_actual != self.z:
                    if self.x != self.lastData[0] or self.y != self.lastData[1] or self.z != self.lastData[2]:
                        self.serial.write(f'P{self.x};{self.y};{self.z}\n'.encode('utf_8'))
                        self.lastData = [self.x, self.y, self.z]
                    if self.i == 0:
                        self.i+=1
                    elif self.i == 1:
                        self.i+=1
                    elif self.i == 2:
                        self.i=0
        except Exception as e: print(str(e).ljust(200), end='\r')

    def sendSerialPositions(self):
        try:
            if self.serial.isOpen() and self.sync:
                self.serial.write(f'P{self.x};{self.y};{self.z}\n'.encode('utf_8'))
        except Exception as e: print(str(e).ljust(200), end='\r')
    
    def on_save_point(self): # save point
        self.points=[self.sp1.text(),self.sp2.text(),self.sp3.text(),self.sp4.text(),self.sp5.text()]
        self.stop_move()
        self.Dialog = Dialog(self.points)
        self.Dialog.exec()
        if self.Dialog.save:
            self.sp_buttons[self.Dialog.index].setText(QCoreApplication.translate("MainWindow", self.Dialog.name_input.text(), None))
            self.sp_vars[self.Dialog.index]=[self.x,self.y,self.z]
            print(self.Dialog.index)
            if self.Dialog.index == 0:
                self.sp1_xyz=[self.x,self.y,self.z]
            elif self.Dialog.index == 1:
                self.sp2_xyz=[self.x,self.y,self.z]
            elif self.Dialog.index == 2:
                self.sp3_xyz=[self.x,self.y,self.z]
            elif self.Dialog.index == 3:
                self.sp4_xyz=[self.x,self.y,self.z]
            elif self.Dialog.index == 4:
                self.sp5_xyz=[self.x,self.y,self.z]
            print(self.Dialog.selection+' changed to: '+self.Dialog.name_input.text().ljust(200),end='\r')
        else:
            print('canceled'.ljust(200),end='\r')
        self.is_key_W_pressed=False
        self.is_key_A_pressed=False
        self.is_key_S_pressed=False
        self.is_key_D_pressed=False
        self.is_key_SHIFT_pressed=False
        self.is_key_SPACE_pressed=False

    def on_home(self):
        if self.serial.isOpen() and self.sync:
            self.serial.write("H\n".encode('utf_8')) 

    def on_set_zero(self):
        self.x=0
        self.y=0
        self.z=0
        if self.serial.isOpen() and self.sync:
            self.sync = False
            self.serial.write(f'C{self.x};{self.y};{self.z}\n'.encode('utf_8'))   
            self.sync = True
            
        self.plotFactor()

    def on_step_mode(self, checked):
        self.is_step_mode=checked
        print('step mode '+str(checked).ljust(200), end='\r') 

    def on_lwh_input(self):
        if self.actionum.isChecked():
            l = int(np.round(np.round(self.length_input.value()/self.step_factor/2,0)*self.step_factor,0))
            w = int(np.round(np.round(self.width_input.value()/self.step_factor/2,0)*self.step_factor,0))
            h = int(np.round(np.round(self.height_input.value()/self.step_factor/2,0)*self.step_factor,0))
            self.l, self.w, self.h = np.array([l, w, h])/self.step_factor
            self.length_input.setValue(l*2)
            self.width_input.setValue(w*2)
            self.height_input.setValue(h*2)
        else:
            self.l = int(np.round(self.length_input.value()/2,0))
            self.w = int(np.round(self.width_input.value()/2,0))
            self.h = int(np.round(self.height_input.value()/2,0))
            l, w, h = (self.l, self.w, self.h)

        self.main_plot.setLimits(xMax=l, xMin=-l, yMin=-w, yMax=w)
        self.z_axis.setLimits(yMin=-h, yMax=h)
        self.main_plot.setXRange(-l, l)
        self.main_plot.setYRange(-w, w)
        self.z_axis.setXRange(0, 1)
        self.z_axis.setYRange(-h, h)
        print(str([l,w,h]).ljust(200), end='\r')

    def on_speed(self):
        print(str(self.speed.value()/100).ljust(200), end='\r')

    def on_step_size(self):
        if self.actionum.isChecked():
            self.step=int(np.round(np.round(self.step_size.value()/self.step_factor,0),0))
            self.step_size.setValue(self.step*self.step_factor)
        else:
            self.step=int(np.round(self.step_size.value(),0))
            self.step_size.setValue(self.step)

    def non_blocking_delay(self, ms):
        loop = QEventLoop()
        QTimer.singleShot(ms, loop.quit)
        loop.exec()

    def runPrecision(self):
        delay = 1000
        if self.x_runs == self.num_runs * 2 and self.y_runs == 0:
            self.non_blocking_delay(delay)
        if self.x_runs < self.num_runs * 2:
            self.non_blocking_delay(delay)
            if self.x_actual == self.initial_xyz[0]:
                if self.x_runs < self.num_runs:
                    self.x = self.initial_xyz[0] + self.step
                else:
                    self.x = self.initial_xyz[0] - self.step
            elif self.x_actual == self.x:
                self.x = self.initial_xyz[0]
                self.x_runs += 1
                print(f'X_runs left: {self.num_runs*2 - self.x_runs}'.ljust(200))
        elif self.y_runs < self.num_runs * 2:
            self.non_blocking_delay(delay)
            if self.y_actual == self.initial_xyz[1]:
                if self.y_runs < self.num_runs:
                    self.y = self.initial_xyz[1] + self.step
                else:
                    self.y = self.initial_xyz[1] - self.step
            elif self.y_actual == self.y:
                self.y = self.initial_xyz[1]
                self.y_runs += 1
                print(f'Y_runs left: {self.num_runs*2 - self.y_runs}'.ljust(200))


        if self.x_runs == self.num_runs * 2 and self.y_runs == self.num_runs * 2:
            self.x = self.initial_xyz[0]
            self.y = self.initial_xyz[1]
            self.precisionTimer.stop()
            self.precisionTimer.timeout.disconnect(self.runPrecision)     

    def moveW(self, step):
        if self.is_free_mode:
            self.y+=step
        elif self.y>=self.w or self.y+step>=self.w:
            self.y=self.w
        else:
            self.y+=step

    def moveA(self, step):
        if self.is_free_mode:
            self.x-=step
        elif self.x<=-self.l or self.x-step<=-self.l: # 
            self.x=-self.l
        else:
            self.x-=step

    def moveS(self, step):
        if self.is_free_mode:
            self.y-=step
        elif self.y<=-self.w or self.y-step<=-self.w:
            self.y=-self.w
        else:
            self.y-=step

    def moveD(self, step):
        if self.is_free_mode:
            self.x+=step
        elif self.x>=self.l or self.x+step>=self.l:
            self.x=self.l
        else:
            self.x+=step

    def moveSpace(self, step):
        if self.is_free_mode:
            self.z+=step
        elif self.z>=self.h or self.z+step>=self.h:
            self.z=self.h
        else:
            self.z+=step

    def moveShift(self, step):
        if self.is_free_mode:
            self.z-=step
        elif self.z<=-self.h or self.z-step<=-self.h:
            self.z=-self.h
        else:
            self.z-=self.step

    def precisionScript(self):
        self.precisionRunning = not self.precisionRunning
        if self.precisionRunning:
            self.x_runs=0
            self.y_runs=0
            print("Running precision. . .")
            self.initial_xyz = [self.x, self.y, self.z]
            self.precisionTimer.timeout.connect(self.runPrecision)
            self.precisionTimer.start(33)
        else:
            self.x_runs=0
            self.y_runs=0
            print("Stopping precision.")
            self.x = self.initial_xyz[0]
            self.y = self.initial_xyz[1]
            self.precisionTimer.stop()
            self.precisionTimer.timeout.disconnect(self.runPrecision)   

    def stepModeScript(self, key):
        self.is_key_W_pressed = False
        self.is_key_A_pressed = False
        self.is_key_S_pressed = False
        self.is_key_D_pressed = False
        self.is_key_SHIFT_pressed=False
        self.is_key_SPACE_pressed=False
        self.stop_move()
        if key == QtCore.Qt.Key_W:
            self.moveW(self.step)
        elif key == QtCore.Qt.Key_A:
            self.moveA(self.step)
        elif key == QtCore.Qt.Key_S:
            self.moveS(self.step)
        elif key == QtCore.Qt.Key_D:
            self.moveD(self.step)
        elif key == QtCore.Qt.Key_Shift:
            self.moveShift(self.step)
        elif key == QtCore.Qt.Key_Space:
            self.moveSpace(self.step)
        self.start_Serial_Move()
        self.plotFactor()
        
    def keyPressEvent(self, event): 
        if not event.isAutoRepeat():
            key = event.key()
            if key == QtCore.Qt.Key_H:
                self.serial.write("H\n".encode('utf_8'))
            if key == QtCore.Qt.Key_R:
                try:
                    if self.serial.isOpen():
                        self.serial.write('s\n'.encode('utf_8'))
                except Exception as e: print(str(e).ljust(200), end='\r')
            if key == QtCore.Qt.Key_P:
                self.precisionScript()
            if self.is_step_mode:
                self.stepModeScript(key)      
            else:
                self.sendSerialPositions()
                if key == QtCore.Qt.Key_W:
                    self.is_key_W_pressed = True             
                if key == QtCore.Qt.Key_A:
                    self.is_key_A_pressed = True             
                if key == QtCore.Qt.Key_S:
                    self.is_key_S_pressed = True               
                if key == QtCore.Qt.Key_D:
                    self.is_key_D_pressed = True              
                if key == QtCore.Qt.Key_Space:
                    self.is_key_SPACE_pressed = True              
                if key == QtCore.Qt.Key_Shift:
                    self.is_key_SHIFT_pressed = True 

            super(MainWindow, self).keyPressEvent(event)
            if any([self.is_key_W_pressed, self.is_key_A_pressed, self.is_key_S_pressed, self.is_key_D_pressed,
                       self.is_key_SHIFT_pressed, self.is_key_SPACE_pressed]):
                self.start_move() 

    def keyReleaseEvent(self, event):
        if not self.is_step_mode and not event.isAutoRepeat():
            key = event.key()
            if key in [QtCore.Qt.Key_W, QtCore.Qt.Key_A, QtCore.Qt.Key_S, QtCore.Qt.Key_D, QtCore.Qt.Key_Space, QtCore.Qt.Key_Shift]:
                self.sendSerialPositions()
            if key == QtCore.Qt.Key_W:
                self.is_key_W_pressed = False
            if key == QtCore.Qt.Key_A:
                self.is_key_A_pressed = False
            if key == QtCore.Qt.Key_S:
                self.is_key_S_pressed = False
            if key == QtCore.Qt.Key_D:
                self.is_key_D_pressed = False
            if key == QtCore.Qt.Key_Space:
                self.is_key_SPACE_pressed = False
            if key == QtCore.Qt.Key_Shift:
                self.is_key_SHIFT_pressed = False
            super(MainWindow, self).keyReleaseEvent(event)
            if not any([self.is_key_W_pressed, self.is_key_A_pressed, self.is_key_S_pressed, self.is_key_D_pressed,
                       self.is_key_SHIFT_pressed, self.is_key_SPACE_pressed]):
                self.stop_move()
                try:
                    if self.serial.isOpen():
                        self.serial.write(f'P{self.x};{self.y};{self.z}\n'.encode('utf_8'))
                except Exception as e: print(str(e).ljust(200), end='\r')                  
 
    def WASDMove(self):
        if not self.is_step_mode:
            step = int(self.step*self.speed.value()/100)

            if self.is_key_W_pressed:
                self.moveW(step)
            if self.is_key_S_pressed:
                self.moveS(step)
            if self.is_key_D_pressed:
                self.moveD(step)
            if self.is_key_A_pressed:
                self.moveA(step)
            if self.is_key_SPACE_pressed:
                self.moveSpace(step)
            if self.is_key_SHIFT_pressed:
                self.moveShift(step)

            self.plotFactor()

    def closeEvent(self, event):
        try:
            self.serial.close()
            print(f"Closed port: {self.com_port}".ljust(200))  # Confirm port is closed
        except:
            pass
        print('\nExited')

if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()

if __name__ == '__main__':
    window = MainWindow()
    app.setStyle('Windows')
    window.show()
    print('Running\n')
    app.exec()