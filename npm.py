import sys
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
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
        print(self.comboBox.currentText()+'                    ', end='\r')
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

        self.save_point.clicked.connect(self.on_save_point)
        self.save_point.setFocusPolicy(Qt.NoFocus)
        self.set_zero.clicked.connect(self.on_set_zero)
        self.set_zero.setFocusPolicy(Qt.NoFocus)
        self.step_mode.clicked.connect(self.on_step_mode)
        self.step_mode.setFocusPolicy(Qt.NoFocus)
        self.origin.clicked.connect(self.on_origin)
        self.origin.setFocusPolicy(Qt.NoFocus)

        self.sp1.clicked.connect(self.on_sp1)
        self.sp1.setFocusPolicy(Qt.NoFocus)
        self.sp2.clicked.connect(self.on_sp2)
        self.sp2.setFocusPolicy(Qt.NoFocus)
        self.sp3.clicked.connect(self.on_sp3)
        self.sp3.setFocusPolicy(Qt.NoFocus)
        self.sp4.clicked.connect(self.on_sp4)
        self.sp4.setFocusPolicy(Qt.NoFocus)
        self.sp5.clicked.connect(self.on_sp5)
        self.sp5.setFocusPolicy(Qt.NoFocus)

        self.sp1_xyz=[]
        self.sp2_xyz=[]
        self.sp3_xyz=[]
        self.sp4_xyz=[]
        self.sp5_xyz=[]
        self.sp_vars=[self.sp1_xyz,self.sp2_xyz,self.sp3_xyz,self.sp4_xyz,self.sp5_xyz,]

        self.points=[self.sp1.text(),self.sp2.text(),self.sp3.text(),self.sp4.text(),self.sp5.text()]
        self.sp_buttons=[self.sp1,self.sp2,self.sp3,self.sp4,self.sp5]
        
        self.length_input.setValue(300)
        self.width_input.setValue(300)
        self.height_input.setValue(100)
        self.length_input.textChanged.connect(self.on_lwh_input)
        self.width_input.textChanged.connect(self.on_lwh_input)
        self.height_input.textChanged.connect(self.on_lwh_input)

        self.step_size.setValue(100)
        self.step_size.textChanged.connect(self.on_step_size)

        self.speed.setValue(100)
        self.speed.valueChanged.connect(self.on_speed)

        self.main_plot.setMouseEnabled(x=False, y=False)  # Disable mouse panning & zooming
        self.main_plot.setFocusPolicy(QtCore.Qt.NoFocus.StrongFocus)
        self.main_plot.hideButtons()  # Disable corner auto-scale button
        self.main_plot.showGrid(x=True, y=True)
        self.main_plot.setLabel("left", "Y (um)")
        self.main_plot.setLabel("bottom", "X (um)")
        self.x=0
        self.y=0
        self.z=0

        self.z_axis.setFocusPolicy(QtCore.Qt.NoFocus.StrongFocus)
        self.z_axis.hideButtons()  # Disable corner auto-scale button
        self.z_axis.hideAxis('bottom')
        self.z_axis.showGrid(x=False, y=True)
        self.z_axis.setLabel("left", "Z (um)")

        self.is_key_W_pressed = False
        self.is_key_A_pressed = False
        self.is_key_S_pressed = False
        self.is_key_D_pressed = False

        self.is_key_SHIFT_pressed=False
        self.is_key_SPACE_pressed=False
        
        self.z_axis.setMouseEnabled(x=False, y=False)  # Disable mouse panning & zooming
        self.z_axis.hideButtons()  # Disable corner auto-scale button

        self.l = 300000
        self.w = 300000
        self.h = 100000

        self.main_plot.setXRange(0, self.l)
        self.main_plot.setYRange(0, self.w)
        self.z_axis.setXRange(0, 1)
        self.z_axis.setYRange(0, self.h)

        self.step=100
        self.is_step_mode=False

        self.timer = QTimer()
        self.zero=[0,0,0]

    def on_sp1(self):
        try:
            self.x=self.sp1_xyz[0]
            self.y=self.sp1_xyz[1]
            self.z=self.sp1_xyz[2]
        except:
            pass
        finally:
            self.main_plot.clear()
            self.z_axis.clear()
            self.x_display.display(self.x)
            self.y_display.display(self.y)
            self.z_display.display(self.z)
            self.z_axis.plot([0], [self.z], pen=None, symbol='o')
            self.main_plot.plot([self.x], [self.y], pen=None, symbol='o')  # setting pen=None disables line drawing
       
    def on_sp2(self):
        try:
            self.x=self.sp2_xyz[0]
            self.y=self.sp2_xyz[1]
            self.z=self.sp2_xyz[2]
        except:
            pass
        finally:
            self.main_plot.clear()
            self.z_axis.clear()
            self.x_display.display(self.x)
            self.y_display.display(self.y)
            self.z_display.display(self.z)
            self.z_axis.plot([0], [self.z], pen=None, symbol='o')
            self.main_plot.plot([self.x], [self.y], pen=None, symbol='o')  # setting pen=None disables line drawing
       
    def on_sp3(self):
        try:
            self.x=self.sp3_xyz[0]
            self.y=self.sp3_xyz[1]
            self.z=self.sp3_xyz[2]
        except:
            pass
        finally:
            self.main_plot.clear()
            self.z_axis.clear()
            self.x_display.display(self.x)
            self.y_display.display(self.y)
            self.z_display.display(self.z)
            self.z_axis.plot([0], [self.z], pen=None, symbol='o')
            self.main_plot.plot([self.x], [self.y], pen=None, symbol='o')  # setting pen=None disables line drawing
       
    def on_sp4(self):
        try:
            self.x=self.sp4_xyz[0]
            self.y=self.sp4_xyz[1]
            self.z=self.sp4_xyz[2]
        except:
            pass
        finally:
            self.main_plot.clear()
            self.z_axis.clear()
            self.x_display.display(self.x)
            self.y_display.display(self.y)
            self.z_display.display(self.z)
            self.z_axis.plot([0], [self.z], pen=None, symbol='o')
            self.main_plot.plot([self.x], [self.y], pen=None, symbol='o')  # setting pen=None disables line drawing
       
    def on_sp5(self):
        try:
            self.x=self.sp5_xyz[0]
            self.y=self.sp5_xyz[1]
            self.z=self.sp5_xyz[2]
        except:
            pass
        finally:
            self.main_plot.clear()
            self.z_axis.clear()
            self.x_display.display(self.x)
            self.y_display.display(self.y)
            self.z_display.display(self.z)
            self.z_axis.plot([0], [self.z], pen=None, symbol='o')
            self.main_plot.plot([self.x], [self.y], pen=None, symbol='o')  # setting pen=None disables line drawing
            
    def on_origin(self):
        self.main_plot.clear()
        self.z_axis.clear()
        self.x=0
        self.y=0
        self.z=0
        self.x_display.display(self.x)
        self.y_display.display(self.y)
        self.z_display.display(self.z)
        self.z_axis.plot([0], [self.z], pen=None, symbol='o')
        self.main_plot.plot([self.x], [self.y], pen=None, symbol='o')  # setting pen=None disables line drawing
    
    def start_move(self):
        # Check if the timer is already running
        if not self.timer.isActive():
            # Connect the timeout signal to the function only if it's not already connected
            # This prevents multiple connections if start_move is called multiple times
            self.timer.timeout.connect(self.WASDMove)
            # Start the timer with an interval of 1000 milliseconds (1 second)
            self.timer.start(33)
            
    def stop_move(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Failed to disconnect")
            # .. your divide-by-zero code ..
            # Stop the timer
            # Disconnect the signal to prevent a potential memory leak
            try:
                self.timer.stop()
                self.timer.timeout.disconnect(self.WASDMove)
            except:
                # No connection to disconnect, pass
                pass
            
    def on_save_point(self):
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
            print(self.Dialog.selection+' changed to: '+self.Dialog.name_input.text()+'                                                                                ',
                  end='\r')
        else:
            print('canceled                                                   ',end='\r')
        self.is_key_W_pressed=False
        self.is_key_A_pressed=False
        self.is_key_S_pressed=False
        self.is_key_D_pressed=False
        self.is_key_SHIFT_pressed=False
        self.is_key_SPACE_pressed=False

    def on_set_zero(self):
        self.zero=[self.x,self.y,self.z]
        print(str([self.x,self.y,self.z])+'                    ', end='\r')   

    def on_step_mode(self, checked):
        self.is_step_mode=checked
        print('step mode '+str(checked)+'                    ', end='\r') 

    def on_lwh_input(self):
        self.l = int(self.length_input.text())*1000
        self.w = int(self.width_input.text())*1000
        self.h = int(self.height_input.text())*1000
        dim = [self.l,self.w,self.h]
        self.main_plot.setXRange(0, self.l)
        self.main_plot.setYRange(0, self.w)
        self.z_axis.setXRange(0, 1)
        self.z_axis.setYRange(0, self.h)
        self.main_plot.clear()
        self.z_axis.clear()
        self.x=0
        self.y=0
        self.z=0
        self.z_axis.plot([0], [self.z], pen=None, symbol='o')
        self.main_plot.plot([self.x], [self.y], pen=None, symbol='o')  # setting pen=None disables line drawing
        print(str(dim)+'                    ', end='\r')

    def on_speed(self):
        print(str(self.speed.value()/100)+'                    ', end='\r')

    def on_step_size(self):
        self.step=int(self.step_size.text())
        print(str(self.step)+'                    ', end='\r')

    def keyPressEvent(self, event):
        if self.is_step_mode:
            self.is_key_W_pressed = False
            self.is_key_A_pressed = False
            self.is_key_S_pressed = False
            self.is_key_D_pressed = False
            self.is_key_SHIFT_pressed=False
            self.is_key_SPACE_pressed=False
            self.stop_move()
            if event.key() == QtCore.Qt.Key_W and not event.isAutoRepeat():
                if self.y>=self.l:
                    pass
                else:
                    self.y+=self.step
            elif event.key() == QtCore.Qt.Key_A and not event.isAutoRepeat():
                if self.x<=0:
                    pass
                else:
                    self.x-=self.step
            elif event.key() == QtCore.Qt.Key_S and not event.isAutoRepeat():
                if self.y<=0:
                    pass
                else:
                    self.y-=self.step
            elif event.key() == QtCore.Qt.Key_D and not event.isAutoRepeat():
                if self.x>=self.w:
                    pass
                else:
                    self.x+=self.step
            elif event.key() == QtCore.Qt.Key_Shift and not event.isAutoRepeat():
                if self.z<=0:
                    pass
                else:
                    self.z-=self.step
            elif event.key() == QtCore.Qt.Key_Space and not event.isAutoRepeat():
                if self.z>=self.h:
                    pass
                else:
                    self.z+=self.step
            elif event.key() == QtCore.Qt.Key_R:
                self.x=self.zero[0]
                self.y=self.zero[1]
                self.z=self.zero[2]
                self.x_display.display(self.x)
                self.y_display.display(self.y)
                self.z_display.display(self.z)
                self.main_plot.clear()
                self.z_axis.clear()
                self.z_axis.plot([0], [self.zero[2]], pen=None, symbol='o')
                self.main_plot.plot([self.zero[0]], [self.zero[1]], pen=None, symbol='o')  # setting pen=None disables line drawing
            print(f'({self.x}, {self.y})', end='\r')
            self.x_display.display(self.x)
            self.y_display.display(self.y)
            self.z_display.display(self.z)
            self.z_axis.clear()
            self.main_plot.clear()
            self.z_axis.plot([0], [self.z], pen=None, symbol='o')
            self.main_plot.plot([self.x], [self.y], pen=None, symbol='o')  # setting pen=None disables line drawing
        else:
            if event.key() == QtCore.Qt.Key_W and not event.isAutoRepeat():
                self.is_key_W_pressed = True
            elif event.key() == QtCore.Qt.Key_A and not event.isAutoRepeat():
                self.is_key_A_pressed = True
            elif event.key() == QtCore.Qt.Key_S and not event.isAutoRepeat():
                self.is_key_S_pressed = True
            elif event.key() == QtCore.Qt.Key_D and not event.isAutoRepeat():
                self.is_key_D_pressed = True
            elif event.key() == QtCore.Qt.Key_Space and not event.isAutoRepeat():
                self.is_key_SPACE_pressed = True
            elif event.key() == QtCore.Qt.Key_Shift and not event.isAutoRepeat():
                self.is_key_SHIFT_pressed = True
            elif event.key() == QtCore.Qt.Key_R:
                self.x=self.zero[0]
                self.y=self.zero[1]
                self.z=self.zero[2]
                self.x_display.display(self.x)
                self.y_display.display(self.y)
                self.z_display.display(self.z)
                self.z_axis.clear()
                self.z_axis.plot([0], [self.zero[2]], pen=None, symbol='o')
                self.main_plot.clear()
                self.main_plot.plot([self.zero[0]], [self.zero[1]], pen=None, symbol='o')  # setting pen=None disables line drawing
            super(MainWindow, self).keyPressEvent(event)
            if any([self.is_key_W_pressed, self.is_key_A_pressed, self.is_key_S_pressed, self.is_key_D_pressed,
                       self.is_key_SHIFT_pressed, self.is_key_SPACE_pressed]):
                self.start_move()

    def keyReleaseEvent(self, event):
        if self.is_step_mode:
            pass
        else:
            if event.key() == QtCore.Qt.Key_W and not event.isAutoRepeat():
                self.is_key_W_pressed = False
            elif event.key() == QtCore.Qt.Key_A and not event.isAutoRepeat():
                self.is_key_A_pressed = False
            elif event.key() == QtCore.Qt.Key_S and not event.isAutoRepeat():
                self.is_key_S_pressed = False
            elif event.key() == QtCore.Qt.Key_D and not event.isAutoRepeat():
                self.is_key_D_pressed = False
            elif event.key() == QtCore.Qt.Key_Space and not event.isAutoRepeat():
                self.is_key_SPACE_pressed = False
            elif event.key() == QtCore.Qt.Key_Shift and not event.isAutoRepeat():
                self.is_key_SHIFT_pressed = False
            super(MainWindow, self).keyReleaseEvent(event)
            if not any([self.is_key_W_pressed, self.is_key_A_pressed, self.is_key_S_pressed, self.is_key_D_pressed,
                       self.is_key_SHIFT_pressed, self.is_key_SPACE_pressed]):
                self.stop_move()
 
    def WASDMove(self):
        if self.is_step_mode:
            pass
        else:
            self.max = (self.l+self.w)/200
            step = int(self.max*self.speed.value()/100)
            step_z = int(self.h*self.speed.value()/10000)
            if self.is_key_W_pressed:
                if self.y>=self.l or self.y+step>=self.l:
                    self.y=self.l
                else:
                    self.y+=step
            if self.is_key_A_pressed:
                if self.x<=0 or self.x-step<=0:
                    self.x=0
                else:
                    self.x-=step
            if self.is_key_S_pressed:
                if self.y<=0 or self.y-step<=0:
                    self.y=0
                else:
                    self.y-=step
            if self.is_key_D_pressed:
                if self.x>=self.w or self.x+step>=self.w:
                    self.x=self.w
                else:
                    self.x+=step
            if self.is_key_SHIFT_pressed:
                if self.z<=0  or self.z-step_z<=0:
                    self.z=0
                else:
                    self.z-=step_z
            if self.is_key_SPACE_pressed:
                if self.z>=self.h or self.z+step_z>=self.h:
                    self.z=self.h
                else:
                    self.z+=step_z
            if any([self.is_key_W_pressed, self.is_key_A_pressed, self.is_key_S_pressed, self.is_key_D_pressed,
                       self.is_key_SHIFT_pressed, self.is_key_SPACE_pressed]):
                print(f'({self.x}, {self.y}, {self.z})', end='\r')
                self.x_display.display(self.x)
                self.y_display.display(self.y)
                self.z_display.display(self.z)
                self.z_axis.clear()
                self.z_axis.plot([0], [self.z], pen=None, symbol='o')
                self.main_plot.clear()
                self.main_plot.plot([self.x], [self.y], pen=None, symbol='o')  # setting pen=None disables line drawing
            pass

if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()

if __name__ == '__main__':
    window = MainWindow()
    app.setStyle('Windows')
    window.show()
    app.exec()