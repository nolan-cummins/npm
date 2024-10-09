# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainTtoprf.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QLCDNumber, QLabel, QLayout,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QStatusBar, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(810, 603)
        MainWindow.setMinimumSize(QSize(810, 603))
        MainWindow.setMaximumSize(QSize(810, 603))
        self.save = QAction(MainWindow)
        self.save.setObjectName(u"save")
        self.save.setEnabled(True)
        icon = QIcon()
        if QIcon.hasThemeIcon(QIcon.ThemeIcon.DocumentSave):
            icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave)
        else:
            icon.addFile(u"../../../../.designer/save_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)

        self.save.setIcon(icon)
        self.save.setIconVisibleInMenu(True)
        self.load = QAction(MainWindow)
        self.load.setObjectName(u"load")
        icon1 = QIcon()
        if QIcon.hasThemeIcon(QIcon.ThemeIcon.DocumentOpen):
            icon1 = QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen)
        else:
            icon1.addFile(u"../../../../.designer/load_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)

        self.load.setIcon(icon1)
        self.load.setIconVisibleInMenu(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(130, 21, 421, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.length_input = QSpinBox(self.horizontalLayoutWidget)
        self.length_input.setObjectName(u"length_input")
        self.length_input.setMaximum(100000)

        self.gridLayout.addWidget(self.length_input, 1, 0, 1, 1)

        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_3 = QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_4 = QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.width_input = QSpinBox(self.horizontalLayoutWidget)
        self.width_input.setObjectName(u"width_input")
        self.width_input.setMaximum(100000)

        self.gridLayout.addWidget(self.width_input, 1, 1, 1, 1)

        self.height_input = QSpinBox(self.horizontalLayoutWidget)
        self.height_input.setObjectName(u"height_input")
        self.height_input.setMaximum(100000)

        self.gridLayout.addWidget(self.height_input, 1, 2, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.speed = QSlider(self.centralwidget)
        self.speed.setObjectName(u"speed")
        self.speed.setGeometry(QRect(70, 90, 41, 421))
        self.speed.setMaximum(100)
        self.speed.setOrientation(Qt.Orientation.Vertical)
        self.speed.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.speed.setTickInterval(10)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 40, 61, 41))
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(680, 110, 101, 401))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.save_point = QPushButton(self.verticalLayoutWidget_2)
        self.save_point.setObjectName(u"save_point")

        self.verticalLayout_2.addWidget(self.save_point)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.horizontalSpacer)

        self.sp1 = QPushButton(self.verticalLayoutWidget_2)
        self.sp1.setObjectName(u"sp1")

        self.verticalLayout_2.addWidget(self.sp1)

        self.sp2 = QPushButton(self.verticalLayoutWidget_2)
        self.sp2.setObjectName(u"sp2")

        self.verticalLayout_2.addWidget(self.sp2)

        self.sp3 = QPushButton(self.verticalLayoutWidget_2)
        self.sp3.setObjectName(u"sp3")

        self.verticalLayout_2.addWidget(self.sp3)

        self.sp4 = QPushButton(self.verticalLayoutWidget_2)
        self.sp4.setObjectName(u"sp4")

        self.verticalLayout_2.addWidget(self.sp4)

        self.sp5 = QPushButton(self.verticalLayoutWidget_2)
        self.sp5.setObjectName(u"sp5")

        self.verticalLayout_2.addWidget(self.sp5)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_6 = QLabel(self.verticalLayoutWidget_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(91, 19))

        self.verticalLayout.addWidget(self.label_6)

        self.step_size = QSpinBox(self.verticalLayoutWidget_2)
        self.step_size.setObjectName(u"step_size")
        self.step_size.setMaximum(999999)
        self.step_size.setStepType(QAbstractSpinBox.StepType.DefaultStepType)

        self.verticalLayout.addWidget(self.step_size)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.step_mode = QPushButton(self.verticalLayoutWidget_2)
        self.step_mode.setObjectName(u"step_mode")
        self.step_mode.setCheckable(True)
        self.step_mode.setAutoExclusive(False)

        self.verticalLayout_2.addWidget(self.step_mode)

        self.free_mode = QPushButton(self.verticalLayoutWidget_2)
        self.free_mode.setObjectName(u"free_mode")
        self.free_mode.setCheckable(True)
        self.free_mode.setAutoExclusive(False)

        self.verticalLayout_2.addWidget(self.free_mode)

        self.set_zero = QPushButton(self.verticalLayoutWidget_2)
        self.set_zero.setObjectName(u"set_zero")

        self.verticalLayout_2.addWidget(self.set_zero)

        self.origin = QPushButton(self.verticalLayoutWidget_2)
        self.origin.setObjectName(u"origin")

        self.verticalLayout_2.addWidget(self.origin)

        self.main_plot = PlotWidget(self.centralwidget)
        self.main_plot.setObjectName(u"main_plot")
        self.main_plot.setGeometry(QRect(129, 89, 421, 421))
        self.z_axis = PlotWidget(self.centralwidget)
        self.z_axis.setObjectName(u"z_axis")
        self.z_axis.setGeometry(QRect(570, 90, 81, 421))
        self.horizontalLayoutWidget_3 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(20, 80, 42, 441))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.horizontalLayoutWidget_3)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_3.addWidget(self.label_8)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_28 = QLabel(self.horizontalLayoutWidget_3)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_3.addWidget(self.label_28, 13, 0, 1, 1)

        self.label_30 = QLabel(self.horizontalLayoutWidget_3)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_3.addWidget(self.label_30, 14, 0, 1, 1)

        self.label_16 = QLabel(self.horizontalLayoutWidget_3)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_3.addWidget(self.label_16, 7, 0, 1, 1)

        self.label_31 = QLabel(self.horizontalLayoutWidget_3)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_3.addWidget(self.label_31, 15, 0, 1, 1)

        self.label_24 = QLabel(self.horizontalLayoutWidget_3)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_3.addWidget(self.label_24, 11, 0, 1, 1)

        self.label_20 = QLabel(self.horizontalLayoutWidget_3)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_3.addWidget(self.label_20, 9, 0, 1, 1)

        self.label_14 = QLabel(self.horizontalLayoutWidget_3)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_3.addWidget(self.label_14, 16, 0, 1, 1)

        self.label_32 = QLabel(self.horizontalLayoutWidget_3)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_3.addWidget(self.label_32, 12, 0, 1, 1)

        self.label_18 = QLabel(self.horizontalLayoutWidget_3)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_3.addWidget(self.label_18, 4, 0, 1, 1)

        self.label_22 = QLabel(self.horizontalLayoutWidget_3)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_3.addWidget(self.label_22, 10, 0, 1, 1)

        self.label_33 = QLabel(self.horizontalLayoutWidget_3)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_3.addWidget(self.label_33, 8, 0, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout_3)

        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(660, 20, 41, 81))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_3.addWidget(self.label_9)

        self.label_7 = QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.label_10 = QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_3.addWidget(self.label_10)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(700, 20, 93, 83))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.x_display = QLCDNumber(self.verticalLayoutWidget_3)
        self.x_display.setObjectName(u"x_display")
        self.x_display.setEnabled(True)
        self.x_display.setFrameShape(QFrame.Shape.WinPanel)
        self.x_display.setFrameShadow(QFrame.Shadow.Sunken)
        self.x_display.setSmallDecimalPoint(False)
        self.x_display.setDigitCount(8)
        self.x_display.setMode(QLCDNumber.Mode.Dec)
        self.x_display.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.verticalLayout_4.addWidget(self.x_display)

        self.y_display = QLCDNumber(self.verticalLayoutWidget_3)
        self.y_display.setObjectName(u"y_display")
        self.y_display.setEnabled(True)
        self.y_display.setFrameShape(QFrame.Shape.WinPanel)
        self.y_display.setFrameShadow(QFrame.Shadow.Sunken)
        self.y_display.setDigitCount(8)
        self.y_display.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.verticalLayout_4.addWidget(self.y_display)

        self.z_display = QLCDNumber(self.verticalLayoutWidget_3)
        self.z_display.setObjectName(u"z_display")
        self.z_display.setEnabled(True)
        self.z_display.setFrameShape(QFrame.Shape.WinPanel)
        self.z_display.setFrameShadow(QFrame.Shadow.Sunken)
        self.z_display.setDigitCount(8)
        self.z_display.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.verticalLayout_4.addWidget(self.z_display)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(570, 60, 81, 22))
        self.connection = QLabel(self.centralwidget)
        self.connection.setObjectName(u"connection")
        self.connection.setGeometry(QRect(20, 489, 761, 61))
        self.print = QLabel(self.centralwidget)
        self.print.setObjectName(u"print")
        self.print.setGeometry(QRect(20, 510, 761, 61))
        self.stop = QPushButton(self.centralwidget)
        self.stop.setObjectName(u"stop")
        self.stop.setGeometry(QRect(30, 10, 81, 31))
        self.stop.setAutoFillBackground(False)
        icon2 = QIcon(QIcon.fromTheme(u"media-playback-stop"))
        self.stop.setIcon(icon2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.connection.raise_()
        self.horizontalLayoutWidget.raise_()
        self.speed.raise_()
        self.label.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.main_plot.raise_()
        self.z_axis.raise_()
        self.horizontalLayoutWidget_3.raise_()
        self.verticalLayoutWidget.raise_()
        self.verticalLayoutWidget_3.raise_()
        self.label_11.raise_()
        self.print.raise_()
        self.stop.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 810, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSerial = QMenu(self.menubar)
        self.menuSerial.setObjectName(u"menuSerial")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.speed, self.save_point)
        QWidget.setTabOrder(self.save_point, self.sp1)
        QWidget.setTabOrder(self.sp1, self.sp2)
        QWidget.setTabOrder(self.sp2, self.sp3)
        QWidget.setTabOrder(self.sp3, self.sp4)
        QWidget.setTabOrder(self.sp4, self.sp5)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSerial.menuAction())
        self.menuFile.addAction(self.save)
        self.menuFile.addAction(self.load)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.load.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Length (mm)</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Width (mm)</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Height (mm)</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Speed</span></p></body></html>", None))
        self.save_point.setText(QCoreApplication.translate("MainWindow", u"Save Point", None))
        self.sp1.setText(QCoreApplication.translate("MainWindow", u"Save Point 1", None))
        self.sp2.setText(QCoreApplication.translate("MainWindow", u"Save Point 2", None))
        self.sp3.setText(QCoreApplication.translate("MainWindow", u"Save Point 3", None))
        self.sp4.setText(QCoreApplication.translate("MainWindow", u"Save Point 4", None))
        self.sp5.setText(QCoreApplication.translate("MainWindow", u"Save Point 5", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Step Size</p></body></html>", None))
        self.step_mode.setText(QCoreApplication.translate("MainWindow", u"Step Mode", None))
        self.free_mode.setText(QCoreApplication.translate("MainWindow", u"Free Mode", None))
        self.set_zero.setText(QCoreApplication.translate("MainWindow", u"Set Zero", None))
        self.origin.setText(QCoreApplication.translate("MainWindow", u"Origin", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">%</p></body></html>", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">30</p></body></html>", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">20</p></body></html>", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">90</p></body></html>", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">10</p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">50</p></body></html>", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">70</p></body></html>", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">0</p></body></html>", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">40</p></body></html>", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">100</p></body></html>", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">60</p></body></html>", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\">80</p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"X (um)", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Y (um)", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Z (um)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Z</span></p></body></html>", None))
        self.connection.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">Status: Disconnected</span></p></body></html>", None))
        self.print.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">[]</span></p></body></html>", None))
        self.stop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSerial.setTitle(QCoreApplication.translate("MainWindow", u"Serial", None))
    # retranslateUi

