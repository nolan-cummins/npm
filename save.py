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

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from importlib import reload

import ui_dialog
reload(ui_dialog)
from ui_dialog import Ui_Dialog as Ui_Save

class SaveDialog(QDialog, Ui_Save):
    def __init__(self, points, parent=None):
        QDialog.__init__(self, parent)
        self.points = points
        self.setupUi(self)
        self.setWindowTitle("Save Current Position")
        self.setWindowIcon(QtGui.QIcon('save_icon.png'))
        QApplication.setWindowIcon(QIcon('save_icon.png'))
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