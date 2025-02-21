# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fgenrpyGEn.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDoubleSpinBox, QFrame, QHBoxLayout, QLCDNumber,
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QToolButton, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1000, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QSize(1000, 700))
        self.verticalLayoutWidget_6 = QWidget(Dialog)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(730, 10, 261, 351))
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_15 = QLabel(self.verticalLayoutWidget_6)
        self.label_15.setObjectName(u"label_15")
        font = QFont()
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_15)

        self.line_3 = QFrame(self.verticalLayoutWidget_6)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.verticalLayoutWidget_6)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.stepIncrementSelect = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.stepIncrementSelect.setObjectName(u"stepIncrementSelect")
        self.stepIncrementSelect.setMinimumSize(QSize(100, 0))
        self.stepIncrementSelect.setDecimals(4)
        self.stepIncrementSelect.setMinimum(-10000.000000000000000)
        self.stepIncrementSelect.setMaximum(10000.000000000000000)

        self.horizontalLayout_2.addWidget(self.stepIncrementSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_13 = QLabel(self.verticalLayoutWidget_6)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_13)

        self.numberIncrementsSelect = QSpinBox(self.verticalLayoutWidget_6)
        self.numberIncrementsSelect.setObjectName(u"numberIncrementsSelect")
        self.numberIncrementsSelect.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_9.addWidget(self.numberIncrementsSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_11 = QLabel(self.verticalLayoutWidget_6)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_11)

        self.waveformSelect = QComboBox(self.verticalLayoutWidget_6)
        self.waveformSelect.addItem("")
        self.waveformSelect.addItem("")
        self.waveformSelect.setObjectName(u"waveformSelect")
        self.waveformSelect.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_7.addWidget(self.waveformSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(self.verticalLayoutWidget_6)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_7)

        self.voltageSelect = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.voltageSelect.setObjectName(u"voltageSelect")
        self.voltageSelect.setMinimumSize(QSize(100, 0))
        self.voltageSelect.setDecimals(7)
        self.voltageSelect.setMaximum(20.000000000000000)

        self.horizontalLayout_3.addWidget(self.voltageSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.frequencyLabel = QLabel(self.verticalLayoutWidget_6)
        self.frequencyLabel.setObjectName(u"frequencyLabel")
        self.frequencyLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.frequencyLabel)

        self.frequencySelect = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.frequencySelect.setObjectName(u"frequencySelect")
        self.frequencySelect.setMinimumSize(QSize(100, 0))
        self.frequencySelect.setDecimals(7)
        self.frequencySelect.setMaximum(10000000.000000000000000)

        self.horizontalLayout_6.addWidget(self.frequencySelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.periodLabel = QLabel(self.verticalLayoutWidget_6)
        self.periodLabel.setObjectName(u"periodLabel")
        self.periodLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.periodLabel)

        self.periodSelect = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.periodSelect.setObjectName(u"periodSelect")
        self.periodSelect.setMinimumSize(QSize(100, 0))
        self.periodSelect.setDecimals(7)
        self.periodSelect.setMaximum(10000000.000000000000000)

        self.horizontalLayout_5.addWidget(self.periodSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_12 = QLabel(self.verticalLayoutWidget_6)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_12)

        self.phaseSelect = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.phaseSelect.setObjectName(u"phaseSelect")
        self.phaseSelect.setMinimumSize(QSize(100, 0))
        self.phaseSelect.setDecimals(7)
        self.phaseSelect.setMaximum(180.000000000000000)

        self.horizontalLayout_8.addWidget(self.phaseSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.verticalLayoutWidget_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.fpsSelect = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.fpsSelect.setObjectName(u"fpsSelect")
        self.fpsSelect.setMinimumSize(QSize(100, 0))
        self.fpsSelect.setDecimals(5)
        self.fpsSelect.setMaximum(1000.000000000000000)
        self.fpsSelect.setValue(100.000000000000000)

        self.horizontalLayout.addWidget(self.fpsSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(self.verticalLayoutWidget_6)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_8)

        self.recordingTimeSelect = QDoubleSpinBox(self.verticalLayoutWidget_6)
        self.recordingTimeSelect.setObjectName(u"recordingTimeSelect")
        self.recordingTimeSelect.setMinimumSize(QSize(100, 0))
        self.recordingTimeSelect.setDecimals(6)
        self.recordingTimeSelect.setMaximum(10000.000000000000000)
        self.recordingTimeSelect.setValue(30.000000000000000)

        self.horizontalLayout_4.addWidget(self.recordingTimeSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_19 = QLabel(self.verticalLayoutWidget_6)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(16777215, 15))
        self.label_19.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_19)

        self.saveDirectorySelect = QToolButton(self.verticalLayoutWidget_6)
        self.saveDirectorySelect.setObjectName(u"saveDirectorySelect")
        self.saveDirectorySelect.setMinimumSize(QSize(125, 0))

        self.horizontalLayout_11.addWidget(self.saveDirectorySelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.applyButton = QPushButton(self.verticalLayoutWidget_6)
        self.applyButton.setObjectName(u"applyButton")

        self.verticalLayout_6.addWidget(self.applyButton)

        self.playButton = QPushButton(Dialog)
        self.playButton.setObjectName(u"playButton")
        self.playButton.setGeometry(QRect(20, 590, 41, 41))
        icon = QIcon(QIcon.fromTheme(u"media-playback-start"))
        self.playButton.setIcon(icon)
        self.playButton.setCheckable(True)
        self.playButton.setChecked(False)
        self.playButton.setFlat(True)
        self.pauseButton = QPushButton(Dialog)
        self.pauseButton.setObjectName(u"pauseButton")
        self.pauseButton.setGeometry(QRect(70, 590, 41, 41))
        icon1 = QIcon(QIcon.fromTheme(u"media-playback-pause"))
        self.pauseButton.setIcon(icon1)
        self.pauseButton.setCheckable(True)
        self.pauseButton.setFlat(True)
        self.stopButton = QPushButton(Dialog)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(230, 590, 41, 41))
        icon2 = QIcon(QIcon.fromTheme(u"media-playback-stop"))
        self.stopButton.setIcon(icon2)
        self.stopButton.setCheckable(False)
        self.stopButton.setFlat(True)
        self.recordButton = QPushButton(Dialog)
        self.recordButton.setObjectName(u"recordButton")
        self.recordButton.setGeometry(QRect(180, 590, 41, 41))
        icon3 = QIcon(QIcon.fromTheme(u"media-record"))
        self.recordButton.setIcon(icon3)
        self.recordButton.setCheckable(True)
        self.recordButton.setChecked(False)
        self.recordButton.setFlat(True)
        self.refreshButton = QPushButton(Dialog)
        self.refreshButton.setObjectName(u"refreshButton")
        self.refreshButton.setGeometry(QRect(670, 590, 41, 41))
        icon4 = QIcon(QIcon.fromTheme(u"view-refresh"))
        self.refreshButton.setIcon(icon4)
        self.refreshButton.setFlat(True)
        self.screenshotButton = QPushButton(Dialog)
        self.screenshotButton.setObjectName(u"screenshotButton")
        self.screenshotButton.setGeometry(QRect(120, 590, 41, 41))
        icon5 = QIcon(QIcon.fromTheme(u"camera-photo"))
        self.screenshotButton.setIcon(icon5)
        self.screenshotButton.setFlat(True)
        self.statusMessage = QLabel(Dialog)
        self.statusMessage.setObjectName(u"statusMessage")
        self.statusMessage.setGeometry(QRect(270, 600, 401, 20))
        self.statusMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayoutWidget_10 = QWidget(Dialog)
        self.horizontalLayoutWidget_10.setObjectName(u"horizontalLayoutWidget_10")
        self.horizontalLayoutWidget_10.setGeometry(QRect(20, 640, 971, 51))
        self.horizontalLayout_10 = QHBoxLayout(self.horizontalLayoutWidget_10)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.progressBar = QProgressBar(self.horizontalLayoutWidget_10)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximumSize(QSize(710, 16777215))
        font1 = QFont()
        font1.setPointSize(15)
        self.progressBar.setFont(font1)
        self.progressBar.setValue(0)

        self.horizontalLayout_10.addWidget(self.progressBar)

        self.label_18 = QLabel(self.horizontalLayoutWidget_10)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font1)

        self.horizontalLayout_10.addWidget(self.label_18)

        self.timeRemainingPanel = QLCDNumber(self.horizontalLayoutWidget_10)
        self.timeRemainingPanel.setObjectName(u"timeRemainingPanel")
        self.timeRemainingPanel.setMinimumSize(QSize(130, 0))
        self.timeRemainingPanel.setMaximumSize(QSize(130, 40))
        self.timeRemainingPanel.setSmallDecimalPoint(True)
        self.timeRemainingPanel.setDigitCount(8)
        self.timeRemainingPanel.setMode(QLCDNumber.Mode.Dec)
        self.timeRemainingPanel.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.timeRemainingPanel.setProperty(u"value", 99199199.000000000000000)

        self.horizontalLayout_10.addWidget(self.timeRemainingPanel)

        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(730, 370, 261, 261))
        self.horizontalLayout_12 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_14 = QLabel(self.layoutWidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_14)

        self.line = QFrame(self.layoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line)

        self.showFPS = QCheckBox(self.layoutWidget)
        self.showFPS.setObjectName(u"showFPS")
        self.showFPS.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout_7.addWidget(self.showFPS)

        self.showDirection = QCheckBox(self.layoutWidget)
        self.showDirection.setObjectName(u"showDirection")
        self.showDirection.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.showDirection.setChecked(True)

        self.verticalLayout_7.addWidget(self.showDirection)

        self.showVoltage = QCheckBox(self.layoutWidget)
        self.showVoltage.setObjectName(u"showVoltage")
        self.showVoltage.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.showVoltage.setChecked(True)

        self.verticalLayout_7.addWidget(self.showVoltage)

        self.showTimestamp = QCheckBox(self.layoutWidget)
        self.showTimestamp.setObjectName(u"showTimestamp")
        self.showTimestamp.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.showTimestamp.setChecked(True)

        self.verticalLayout_7.addWidget(self.showTimestamp)

        self.showScalebar = QCheckBox(self.layoutWidget)
        self.showScalebar.setObjectName(u"showScalebar")
        self.showScalebar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout_7.addWidget(self.showScalebar)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)


        self.horizontalLayout_12.addLayout(self.verticalLayout_7)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_16 = QLabel(self.layoutWidget)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_16)

        self.line_2 = QFrame(self.layoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 15))
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_3)

        self.multimeterXSelect = QComboBox(self.layoutWidget)
        self.multimeterXSelect.setObjectName(u"multimeterXSelect")
        self.multimeterXSelect.setEditable(False)

        self.verticalLayout_3.addWidget(self.multimeterXSelect)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 15))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.multimeterYSelect = QComboBox(self.layoutWidget)
        self.multimeterYSelect.setObjectName(u"multimeterYSelect")
        self.multimeterYSelect.setEditable(False)

        self.verticalLayout_2.addWidget(self.multimeterYSelect)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 15))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.functionGeneratorSelect = QComboBox(self.layoutWidget)
        self.functionGeneratorSelect.setObjectName(u"functionGeneratorSelect")
        self.functionGeneratorSelect.setEditable(False)

        self.verticalLayout.addWidget(self.functionGeneratorSelect)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 15))
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_4)

        self.cameraSelectionSelect = QComboBox(self.layoutWidget)
        self.cameraSelectionSelect.setObjectName(u"cameraSelectionSelect")
        self.cameraSelectionSelect.setEditable(False)

        self.verticalLayout_5.addWidget(self.cameraSelectionSelect)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.horizontalLayout_12.addLayout(self.verticalLayout_4)


        self.retranslateUi(Dialog)

        self.playButton.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Settings", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Step Increment (um)", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Number of Increments", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Waveform", None))
        self.waveformSelect.setItemText(0, QCoreApplication.translate("Dialog", u"SQU", None))
        self.waveformSelect.setItemText(1, QCoreApplication.translate("Dialog", u"SIN", None))

        self.label_7.setText(QCoreApplication.translate("Dialog", u"Voltage (Vpp)", None))
        self.frequencyLabel.setText(QCoreApplication.translate("Dialog", u"Frequency (Hz)", None))
        self.periodLabel.setText(QCoreApplication.translate("Dialog", u"Period (s)", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Phase Angle (\u00b0)", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"FPS", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Recording Time (s)", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Save Directory", None))
        self.saveDirectorySelect.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.applyButton.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.playButton.setText("")
        self.pauseButton.setText("")
        self.stopButton.setText("")
        self.recordButton.setText("")
        self.refreshButton.setText("")
        self.screenshotButton.setText("")
        self.statusMessage.setText(QCoreApplication.translate("Dialog", u"Status: Disconnected", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Time Remaining (HH:MM:SS):", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Overlay", None))
        self.showFPS.setText(QCoreApplication.translate("Dialog", u"FPS", None))
        self.showDirection.setText(QCoreApplication.translate("Dialog", u"Direction (X/Y)", None))
        self.showVoltage.setText(QCoreApplication.translate("Dialog", u"Voltage", None))
        self.showTimestamp.setText(QCoreApplication.translate("Dialog", u"Timestamp", None))
        self.showScalebar.setText(QCoreApplication.translate("Dialog", u"Scalebar", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Instruments", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Multimeter (X)", None))
        self.multimeterXSelect.setCurrentText("")
        self.multimeterXSelect.setPlaceholderText(QCoreApplication.translate("Dialog", u"Select", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Multimeter (Y)", None))
        self.multimeterYSelect.setCurrentText("")
        self.multimeterYSelect.setPlaceholderText(QCoreApplication.translate("Dialog", u"Select", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Function Generator", None))
        self.functionGeneratorSelect.setCurrentText("")
        self.functionGeneratorSelect.setPlaceholderText(QCoreApplication.translate("Dialog", u"Select", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Camera", None))
        self.cameraSelectionSelect.setCurrentText("")
        self.cameraSelectionSelect.setPlaceholderText(QCoreApplication.translate("Dialog", u"Select", None))
    # retranslateUi

