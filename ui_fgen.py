# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fgenhgwmEs.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
    QLabel, QProgressBar, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QTabWidget, QToolButton, QVBoxLayout, QWidget)

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
        font = QFont()
        font.setPointSize(15)
        self.progressBar.setFont(font)
        self.progressBar.setValue(0)

        self.horizontalLayout_10.addWidget(self.progressBar)

        self.label_18 = QLabel(self.horizontalLayoutWidget_10)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_18)

        self.timeRemainingPanel = QLCDNumber(self.horizontalLayoutWidget_10)
        self.timeRemainingPanel.setObjectName(u"timeRemainingPanel")
        self.timeRemainingPanel.setMinimumSize(QSize(130, 0))
        self.timeRemainingPanel.setMaximumSize(QSize(130, 40))
        self.timeRemainingPanel.setSmallDecimalPoint(True)
        self.timeRemainingPanel.setDigitCount(8)
        self.timeRemainingPanel.setMode(QLCDNumber.Mode.Dec)
        self.timeRemainingPanel.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.timeRemainingPanel.setProperty("value", 99199199.000000000000000)

        self.horizontalLayout_10.addWidget(self.timeRemainingPanel)

        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(730, 410, 261, 221))
        self.horizontalLayout_12 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_14 = QLabel(self.layoutWidget)
        self.label_14.setObjectName(u"label_14")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_14.setFont(font1)
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

        self.showExposure = QCheckBox(self.layoutWidget)
        self.showExposure.setObjectName(u"showExposure")
        self.showExposure.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.showExposure.setChecked(True)

        self.verticalLayout_7.addWidget(self.showExposure)

        self.showPosition = QCheckBox(self.layoutWidget)
        self.showPosition.setObjectName(u"showPosition")
        self.showPosition.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.verticalLayout_7.addWidget(self.showPosition)

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
        self.label_16.setFont(font1)
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

        self.layoutWidget1 = QWidget(Dialog)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(730, 19, 261, 381))
        self.verticalLayout_9 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_15 = QLabel(self.layoutWidget1)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_15)

        self.line_3 = QFrame(self.layoutWidget1)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_9.addWidget(self.line_3)

        self.tabWidget = QTabWidget(self.layoutWidget1)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(-1, 0, 259, 311))
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 248, 394))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_6 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.label_6)

        self.experimentSelect = QComboBox(self.scrollAreaWidgetContents_2)
        self.experimentSelect.addItem("")
        self.experimentSelect.addItem("")
        self.experimentSelect.setObjectName(u"experimentSelect")

        self.horizontalLayout_14.addWidget(self.experimentSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_9 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.label_9)

        self.exposureTimeSlider = QSlider(self.scrollAreaWidgetContents_2)
        self.exposureTimeSlider.setObjectName(u"exposureTimeSlider")
        self.exposureTimeSlider.setMinimum(100)
        self.exposureTimeSlider.setMaximum(20000)
        self.exposureTimeSlider.setOrientation(Qt.Orientation.Horizontal)
        self.exposureTimeSlider.setTickInterval(10)

        self.horizontalLayout_13.addWidget(self.exposureTimeSlider)

        self.exposureTimeValue = QSpinBox(self.scrollAreaWidgetContents_2)
        self.exposureTimeValue.setObjectName(u"exposureTimeValue")
        self.exposureTimeValue.setMinimumSize(QSize(80, 0))
        self.exposureTimeValue.setMinimum(100)
        self.exposureTimeValue.setMaximum(20000)

        self.horizontalLayout_13.addWidget(self.exposureTimeValue)


        self.verticalLayout_6.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.stepIncrementLabel = QLabel(self.scrollAreaWidgetContents_2)
        self.stepIncrementLabel.setObjectName(u"stepIncrementLabel")
        self.stepIncrementLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.stepIncrementLabel)

        self.stepIncrementSelect = QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.stepIncrementSelect.setObjectName(u"stepIncrementSelect")
        self.stepIncrementSelect.setMinimumSize(QSize(100, 0))
        self.stepIncrementSelect.setDecimals(4)
        self.stepIncrementSelect.setMinimum(-10000.000000000000000)
        self.stepIncrementSelect.setMaximum(10000.000000000000000)

        self.horizontalLayout_2.addWidget(self.stepIncrementSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_13 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_13)

        self.numberIncrementsSelect = QSpinBox(self.scrollAreaWidgetContents_2)
        self.numberIncrementsSelect.setObjectName(u"numberIncrementsSelect")
        self.numberIncrementsSelect.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_9.addWidget(self.numberIncrementsSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_11 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_11)

        self.waveformSelect = QComboBox(self.scrollAreaWidgetContents_2)
        self.waveformSelect.addItem("")
        self.waveformSelect.addItem("")
        self.waveformSelect.setObjectName(u"waveformSelect")
        self.waveformSelect.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_7.addWidget(self.waveformSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.voltageLabel = QLabel(self.scrollAreaWidgetContents_2)
        self.voltageLabel.setObjectName(u"voltageLabel")
        self.voltageLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.voltageLabel)

        self.voltageSelect = QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.voltageSelect.setObjectName(u"voltageSelect")
        self.voltageSelect.setMinimumSize(QSize(100, 0))
        self.voltageSelect.setDecimals(7)
        self.voltageSelect.setMaximum(20.000000000000000)

        self.horizontalLayout_3.addWidget(self.voltageSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.frequencyLabel = QLabel(self.scrollAreaWidgetContents_2)
        self.frequencyLabel.setObjectName(u"frequencyLabel")
        self.frequencyLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.frequencyLabel)

        self.frequencySelect = QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.frequencySelect.setObjectName(u"frequencySelect")
        self.frequencySelect.setMinimumSize(QSize(100, 0))
        self.frequencySelect.setMaximumSize(QSize(125, 16777215))
        self.frequencySelect.setDecimals(7)
        self.frequencySelect.setMaximum(10000000.000000000000000)

        self.horizontalLayout_6.addWidget(self.frequencySelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.periodLabel = QLabel(self.scrollAreaWidgetContents_2)
        self.periodLabel.setObjectName(u"periodLabel")
        self.periodLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.periodLabel)

        self.periodSelect = QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.periodSelect.setObjectName(u"periodSelect")
        self.periodSelect.setMinimumSize(QSize(100, 0))
        self.periodSelect.setMaximumSize(QSize(125, 16777215))
        self.periodSelect.setDecimals(7)
        self.periodSelect.setMaximum(10000000.000000000000000)

        self.horizontalLayout_5.addWidget(self.periodSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_12 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_12)

        self.phaseSelect = QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.phaseSelect.setObjectName(u"phaseSelect")
        self.phaseSelect.setMinimumSize(QSize(100, 0))
        self.phaseSelect.setDecimals(7)
        self.phaseSelect.setMaximum(180.000000000000000)

        self.horizontalLayout_8.addWidget(self.phaseSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.fpsSelect = QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.fpsSelect.setObjectName(u"fpsSelect")
        self.fpsSelect.setMinimumSize(QSize(100, 0))
        self.fpsSelect.setDecimals(0)
        self.fpsSelect.setMinimum(1.000000000000000)
        self.fpsSelect.setMaximum(169.000000000000000)
        self.fpsSelect.setValue(100.000000000000000)

        self.horizontalLayout.addWidget(self.fpsSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_8)

        self.recordingTimeSelect = QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.recordingTimeSelect.setObjectName(u"recordingTimeSelect")
        self.recordingTimeSelect.setMinimumSize(QSize(100, 0))
        self.recordingTimeSelect.setDecimals(6)
        self.recordingTimeSelect.setMaximum(10000.000000000000000)
        self.recordingTimeSelect.setValue(30.000000000000000)

        self.horizontalLayout_4.addWidget(self.recordingTimeSelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_19 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(16777215, 15))
        self.label_19.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.label_19.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_19)

        self.saveDirectorySelect = QToolButton(self.scrollAreaWidgetContents_2)
        self.saveDirectorySelect.setObjectName(u"saveDirectorySelect")
        self.saveDirectorySelect.setMinimumSize(QSize(125, 0))

        self.horizontalLayout_11.addWidget(self.saveDirectorySelect)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.applyButton = QPushButton(self.scrollAreaWidgetContents_2)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setMinimumSize(QSize(0, 25))

        self.verticalLayout_6.addWidget(self.applyButton)


        self.verticalLayout_8.addLayout(self.verticalLayout_6)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.scrollArea_2 = QScrollArea(self.tab_2)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setGeometry(QRect(0, 0, 259, 311))
        self.scrollArea_2.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, -60, 247, 371))
        self.verticalLayout_18 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.blurTitle_2 = QLabel(self.scrollAreaWidgetContents_3)
        self.blurTitle_2.setObjectName(u"blurTitle_2")
        font2 = QFont()
        font2.setPointSize(9)
        self.blurTitle_2.setFont(font2)
        self.blurTitle_2.setFrameShape(QFrame.Shape.NoFrame)
        self.blurTitle_2.setFrameShadow(QFrame.Shadow.Raised)
        self.blurTitle_2.setTextFormat(Qt.TextFormat.RichText)
        self.blurTitle_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_30.addWidget(self.blurTitle_2)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.showOriginalLabel = QLabel(self.scrollAreaWidgetContents_3)
        self.showOriginalLabel.setObjectName(u"showOriginalLabel")
        self.showOriginalLabel.setEnabled(True)
        self.showOriginalLabel.setMinimumSize(QSize(0, 0))
        self.showOriginalLabel.setMaximumSize(QSize(80, 16777215))
        self.showOriginalLabel.setFont(font2)
        self.showOriginalLabel.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.showOriginalLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.showOriginalLabel.setFrameShadow(QFrame.Shadow.Raised)
        self.showOriginalLabel.setTextFormat(Qt.TextFormat.RichText)
        self.showOriginalLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_29.addWidget(self.showOriginalLabel)

        self.showOriginal = QCheckBox(self.scrollAreaWidgetContents_3)
        self.showOriginal.setObjectName(u"showOriginal")
        self.showOriginal.setEnabled(True)
        self.showOriginal.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_29.addWidget(self.showOriginal)


        self.horizontalLayout_30.addLayout(self.horizontalLayout_29)


        self.verticalLayout_16.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.blurToggle = QCheckBox(self.scrollAreaWidgetContents_3)
        self.blurToggle.setObjectName(u"blurToggle")
        self.blurToggle.setFont(font1)

        self.horizontalLayout_16.addWidget(self.blurToggle)

        self.blurSlider = QSlider(self.scrollAreaWidgetContents_3)
        self.blurSlider.setObjectName(u"blurSlider")
        self.blurSlider.setEnabled(False)
        self.blurSlider.setMaximum(100)
        self.blurSlider.setOrientation(Qt.Orientation.Horizontal)
        self.blurSlider.setInvertedAppearance(False)
        self.blurSlider.setInvertedControls(False)
        self.blurSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.blurSlider.setTickInterval(10)

        self.horizontalLayout_16.addWidget(self.blurSlider)

        self.blurValue = QSpinBox(self.scrollAreaWidgetContents_3)
        self.blurValue.setObjectName(u"blurValue")
        self.blurValue.setEnabled(False)
        self.blurValue.setMinimumSize(QSize(100, 0))
        self.blurValue.setFont(font2)
        self.blurValue.setMaximum(100)
        self.blurValue.setDisplayIntegerBase(10)

        self.horizontalLayout_16.addWidget(self.blurValue)


        self.verticalLayout_16.addLayout(self.horizontalLayout_16)


        self.verticalLayout_17.addLayout(self.verticalLayout_16)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.contrast_2 = QLabel(self.scrollAreaWidgetContents_3)
        self.contrast_2.setObjectName(u"contrast_2")
        self.contrast_2.setFont(font2)
        self.contrast_2.setFrameShape(QFrame.Shape.NoFrame)
        self.contrast_2.setFrameShadow(QFrame.Shadow.Raised)
        self.contrast_2.setTextFormat(Qt.TextFormat.RichText)
        self.contrast_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_19.addWidget(self.contrast_2)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.invertLabel = QLabel(self.scrollAreaWidgetContents_3)
        self.invertLabel.setObjectName(u"invertLabel")
        self.invertLabel.setEnabled(True)
        self.invertLabel.setMinimumSize(QSize(0, 0))
        self.invertLabel.setMaximumSize(QSize(50, 16777215))
        self.invertLabel.setFont(font2)
        self.invertLabel.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.invertLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.invertLabel.setFrameShadow(QFrame.Shadow.Raised)
        self.invertLabel.setTextFormat(Qt.TextFormat.RichText)
        self.invertLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_22.addWidget(self.invertLabel)

        self.invertToggle = QCheckBox(self.scrollAreaWidgetContents_3)
        self.invertToggle.setObjectName(u"invertToggle")
        self.invertToggle.setEnabled(True)
        self.invertToggle.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_22.addWidget(self.invertToggle)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_22)


        self.verticalLayout_10.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.adaptToggle = QCheckBox(self.scrollAreaWidgetContents_3)
        self.adaptToggle.setObjectName(u"adaptToggle")
        self.adaptToggle.setFont(font1)

        self.horizontalLayout_25.addWidget(self.adaptToggle)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.adaptSliderArea = QSlider(self.scrollAreaWidgetContents_3)
        self.adaptSliderArea.setObjectName(u"adaptSliderArea")
        self.adaptSliderArea.setEnabled(False)
        self.adaptSliderArea.setMinimum(0)
        self.adaptSliderArea.setMaximum(99)
        self.adaptSliderArea.setSingleStep(3)
        self.adaptSliderArea.setValue(21)
        self.adaptSliderArea.setOrientation(Qt.Orientation.Horizontal)
        self.adaptSliderArea.setInvertedAppearance(False)
        self.adaptSliderArea.setInvertedControls(False)
        self.adaptSliderArea.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.adaptSliderArea.setTickInterval(9)

        self.horizontalLayout_23.addWidget(self.adaptSliderArea)

        self.adaptValueArea = QSpinBox(self.scrollAreaWidgetContents_3)
        self.adaptValueArea.setObjectName(u"adaptValueArea")
        self.adaptValueArea.setEnabled(False)
        self.adaptValueArea.setMinimumSize(QSize(80, 0))
        self.adaptValueArea.setMaximumSize(QSize(80, 16777215))
        self.adaptValueArea.setFont(font2)
        self.adaptValueArea.setMinimum(3)
        self.adaptValueArea.setMaximum(99)
        self.adaptValueArea.setSingleStep(2)
        self.adaptValueArea.setValue(21)

        self.horizontalLayout_23.addWidget(self.adaptValueArea)


        self.verticalLayout_13.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.adaptSliderC = QSlider(self.scrollAreaWidgetContents_3)
        self.adaptSliderC.setObjectName(u"adaptSliderC")
        self.adaptSliderC.setEnabled(False)
        self.adaptSliderC.setMinimum(-25)
        self.adaptSliderC.setMaximum(25)
        self.adaptSliderC.setValue(4)
        self.adaptSliderC.setOrientation(Qt.Orientation.Horizontal)
        self.adaptSliderC.setInvertedAppearance(False)
        self.adaptSliderC.setInvertedControls(False)
        self.adaptSliderC.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.adaptSliderC.setTickInterval(10)

        self.horizontalLayout_24.addWidget(self.adaptSliderC)

        self.adaptValueC = QSpinBox(self.scrollAreaWidgetContents_3)
        self.adaptValueC.setObjectName(u"adaptValueC")
        self.adaptValueC.setEnabled(False)
        self.adaptValueC.setMinimumSize(QSize(80, 0))
        self.adaptValueC.setFont(font2)
        self.adaptValueC.setMinimum(-25)
        self.adaptValueC.setMaximum(25)
        self.adaptValueC.setValue(4)

        self.horizontalLayout_24.addWidget(self.adaptValueC)


        self.verticalLayout_13.addLayout(self.horizontalLayout_24)


        self.horizontalLayout_25.addLayout(self.verticalLayout_13)


        self.horizontalLayout_15.addLayout(self.horizontalLayout_25)


        self.verticalLayout_10.addLayout(self.horizontalLayout_15)


        self.verticalLayout_17.addLayout(self.verticalLayout_10)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.dilationTitle_3 = QLabel(self.scrollAreaWidgetContents_3)
        self.dilationTitle_3.setObjectName(u"dilationTitle_3")
        self.dilationTitle_3.setFont(font2)
        self.dilationTitle_3.setFrameShape(QFrame.Shape.NoFrame)
        self.dilationTitle_3.setFrameShadow(QFrame.Shadow.Raised)
        self.dilationTitle_3.setTextFormat(Qt.TextFormat.RichText)
        self.dilationTitle_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_14.addWidget(self.dilationTitle_3)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.dilationToggle = QCheckBox(self.scrollAreaWidgetContents_3)
        self.dilationToggle.setObjectName(u"dilationToggle")
        self.dilationToggle.setFont(font1)

        self.horizontalLayout_17.addWidget(self.dilationToggle)

        self.dilationSlider = QSlider(self.scrollAreaWidgetContents_3)
        self.dilationSlider.setObjectName(u"dilationSlider")
        self.dilationSlider.setEnabled(False)
        self.dilationSlider.setMinimum(0)
        self.dilationSlider.setMaximum(5)
        self.dilationSlider.setPageStep(1)
        self.dilationSlider.setOrientation(Qt.Orientation.Horizontal)
        self.dilationSlider.setInvertedAppearance(False)
        self.dilationSlider.setInvertedControls(False)
        self.dilationSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.dilationSlider.setTickInterval(1)

        self.horizontalLayout_17.addWidget(self.dilationSlider)

        self.dilationValue = QSpinBox(self.scrollAreaWidgetContents_3)
        self.dilationValue.setObjectName(u"dilationValue")
        self.dilationValue.setEnabled(False)
        self.dilationValue.setMinimumSize(QSize(100, 0))
        self.dilationValue.setFont(font2)
        self.dilationValue.setMinimum(0)
        self.dilationValue.setMaximum(5)
        self.dilationValue.setDisplayIntegerBase(10)

        self.horizontalLayout_17.addWidget(self.dilationValue)


        self.verticalLayout_14.addLayout(self.horizontalLayout_17)


        self.verticalLayout_17.addLayout(self.verticalLayout_14)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.threshold_3 = QLabel(self.scrollAreaWidgetContents_3)
        self.threshold_3.setObjectName(u"threshold_3")
        self.threshold_3.setFont(font2)
        self.threshold_3.setFrameShape(QFrame.Shape.NoFrame)
        self.threshold_3.setFrameShadow(QFrame.Shadow.Raised)
        self.threshold_3.setTextFormat(Qt.TextFormat.RichText)
        self.threshold_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.threshold_3)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.frameDiffToggle = QCheckBox(self.scrollAreaWidgetContents_3)
        self.frameDiffToggle.setObjectName(u"frameDiffToggle")
        self.frameDiffToggle.setFont(font1)

        self.horizontalLayout_28.addWidget(self.frameDiffToggle)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.frameDiffSlider = QSlider(self.scrollAreaWidgetContents_3)
        self.frameDiffSlider.setObjectName(u"frameDiffSlider")
        self.frameDiffSlider.setEnabled(False)
        self.frameDiffSlider.setMinimum(0)
        self.frameDiffSlider.setMaximum(1000)
        self.frameDiffSlider.setValue(25)
        self.frameDiffSlider.setOrientation(Qt.Orientation.Horizontal)
        self.frameDiffSlider.setInvertedAppearance(False)
        self.frameDiffSlider.setInvertedControls(False)
        self.frameDiffSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.frameDiffSlider.setTickInterval(100)

        self.horizontalLayout_26.addWidget(self.frameDiffSlider)

        self.frameDiffValue = QSpinBox(self.scrollAreaWidgetContents_3)
        self.frameDiffValue.setObjectName(u"frameDiffValue")
        self.frameDiffValue.setEnabled(False)
        self.frameDiffValue.setMinimumSize(QSize(80, 0))
        self.frameDiffValue.setMaximumSize(QSize(80, 16777215))
        self.frameDiffValue.setFont(font2)
        self.frameDiffValue.setMinimum(0)
        self.frameDiffValue.setMaximum(999)
        self.frameDiffValue.setValue(25)

        self.horizontalLayout_26.addWidget(self.frameDiffValue)


        self.verticalLayout_15.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.frameDiffSliderMax = QSlider(self.scrollAreaWidgetContents_3)
        self.frameDiffSliderMax.setObjectName(u"frameDiffSliderMax")
        self.frameDiffSliderMax.setEnabled(False)
        self.frameDiffSliderMax.setMinimum(0)
        self.frameDiffSliderMax.setMaximum(1000)
        self.frameDiffSliderMax.setValue(25)
        self.frameDiffSliderMax.setOrientation(Qt.Orientation.Horizontal)
        self.frameDiffSliderMax.setInvertedAppearance(False)
        self.frameDiffSliderMax.setInvertedControls(False)
        self.frameDiffSliderMax.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.frameDiffSliderMax.setTickInterval(100)

        self.horizontalLayout_27.addWidget(self.frameDiffSliderMax)

        self.frameDiffValueMax = QSpinBox(self.scrollAreaWidgetContents_3)
        self.frameDiffValueMax.setObjectName(u"frameDiffValueMax")
        self.frameDiffValueMax.setEnabled(False)
        self.frameDiffValueMax.setMinimumSize(QSize(80, 0))
        self.frameDiffValueMax.setFont(font2)
        self.frameDiffValueMax.setMinimum(0)
        self.frameDiffValueMax.setMaximum(999)
        self.frameDiffValueMax.setValue(100)

        self.horizontalLayout_27.addWidget(self.frameDiffValueMax)


        self.verticalLayout_15.addLayout(self.horizontalLayout_27)


        self.horizontalLayout_28.addLayout(self.verticalLayout_15)


        self.horizontalLayout_18.addLayout(self.horizontalLayout_28)


        self.verticalLayout_11.addLayout(self.horizontalLayout_18)


        self.verticalLayout_17.addLayout(self.verticalLayout_11)

        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.zoomTitle = QLabel(self.scrollAreaWidgetContents_3)
        self.zoomTitle.setObjectName(u"zoomTitle")
        self.zoomTitle.setFont(font2)
        self.zoomTitle.setFrameShape(QFrame.Shape.NoFrame)
        self.zoomTitle.setFrameShadow(QFrame.Shadow.Raised)
        self.zoomTitle.setTextFormat(Qt.TextFormat.RichText)
        self.zoomTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_19.addWidget(self.zoomTitle)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.zoomSlider = QSlider(self.scrollAreaWidgetContents_3)
        self.zoomSlider.setObjectName(u"zoomSlider")
        self.zoomSlider.setEnabled(True)
        self.zoomSlider.setMinimum(0)
        self.zoomSlider.setMaximum(100)
        self.zoomSlider.setPageStep(1)
        self.zoomSlider.setOrientation(Qt.Orientation.Horizontal)
        self.zoomSlider.setInvertedAppearance(False)
        self.zoomSlider.setInvertedControls(True)
        self.zoomSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.zoomSlider.setTickInterval(10)

        self.horizontalLayout_20.addWidget(self.zoomSlider)

        self.zoomValue = QSpinBox(self.scrollAreaWidgetContents_3)
        self.zoomValue.setObjectName(u"zoomValue")
        self.zoomValue.setEnabled(True)
        self.zoomValue.setMinimumSize(QSize(100, 0))
        self.zoomValue.setFont(font2)
        self.zoomValue.setMinimum(0)
        self.zoomValue.setMaximum(100)
        self.zoomValue.setDisplayIntegerBase(10)

        self.horizontalLayout_20.addWidget(self.zoomValue)


        self.verticalLayout_19.addLayout(self.horizontalLayout_20)


        self.verticalLayout_17.addLayout(self.verticalLayout_19)


        self.verticalLayout_18.addLayout(self.verticalLayout_17)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_9.addWidget(self.tabWidget)


        self.retranslateUi(Dialog)

        self.playButton.setDefault(False)
        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
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
        self.showExposure.setText(QCoreApplication.translate("Dialog", u"Exposure", None))
        self.showPosition.setText(QCoreApplication.translate("Dialog", u"Position", None))
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
        self.label_15.setText(QCoreApplication.translate("Dialog", u"Settings", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Experiment", None))
        self.experimentSelect.setItemText(0, QCoreApplication.translate("Dialog", u"Z-Axis Offset", None))
        self.experimentSelect.setItemText(1, QCoreApplication.translate("Dialog", u"Voltage", None))

        self.label_9.setText(QCoreApplication.translate("Dialog", u"Exposure (ms)", None))
        self.stepIncrementLabel.setText(QCoreApplication.translate("Dialog", u"Step Increment (um)", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Number of Increments", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Waveform", None))
        self.waveformSelect.setItemText(0, QCoreApplication.translate("Dialog", u"SQU", None))
        self.waveformSelect.setItemText(1, QCoreApplication.translate("Dialog", u"SIN", None))

        self.voltageLabel.setText(QCoreApplication.translate("Dialog", u"Voltage (Vpp)", None))
        self.frequencyLabel.setText(QCoreApplication.translate("Dialog", u"Frequency (Hz)", None))
        self.periodLabel.setText(QCoreApplication.translate("Dialog", u"Period (s)", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Phase Angle (\u00b0)", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"FPS", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Recording Time (s)", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Save Directory", None))
        self.saveDirectorySelect.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.applyButton.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Experiments", None))
        self.blurTitle_2.setText(QCoreApplication.translate("Dialog", u"Gaussian Blur", None))
        self.showOriginalLabel.setText(QCoreApplication.translate("Dialog", u"Hide Filters", None))
        self.showOriginal.setText("")
        self.blurToggle.setText("")
        self.contrast_2.setText(QCoreApplication.translate("Dialog", u"Adaptive Threshold", None))
        self.invertLabel.setText(QCoreApplication.translate("Dialog", u"Invert", None))
        self.invertToggle.setText("")
        self.adaptToggle.setText("")
        self.dilationTitle_3.setText(QCoreApplication.translate("Dialog", u"Dilation", None))
        self.dilationToggle.setText("")
        self.threshold_3.setText(QCoreApplication.translate("Dialog", u"Frame Differencing", None))
        self.frameDiffToggle.setText("")
        self.zoomTitle.setText(QCoreApplication.translate("Dialog", u"Zoom", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Video", None))
    # retranslateUi

