from main import *
from comms import *
from camera import captureCamera
from functools import partial

import ui_fgen
reload(ui_fgen)
from ui_fgen import Ui_Dialog as Ui_Auto

class AutomationDialog(QDialog, Ui_Auto):
    run_experiment = Signal(bool)
    
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("Automation")
        self.setWindowIcon(QtGui.QIcon('automation_icon.png'))
        QApplication.setWindowIcon(QIcon('automation_icon.png'))
        self.refreshButton.clicked.connect(self.refresh)
        self.applyButton.clicked.connect(self.applySettings)
        self.playButton.clicked.connect(self.emitStart)

        self.cameraFrame = QLabel(self)
        self.cameraFrame.setGeometry(QRect(10, 10, 710, 568))
        self.blank = QPixmap("automation_icon.png").scaled(self.cameraFrame.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.cameraFrame.setPixmap(self.blank)
        self.cameraFrame.setAlignment(Qt.AlignCenter)
        self.captureCamera = None
        self.startCamera(0)

        self.periodSelect.editingFinished.connect(self.syncPer)
        self.periodValue=0.0
        self.frequencySelect.editingFinished.connect(self.syncFreq)
        self.frequencyValue=0.0
        self.frequencyFactor=1
        self.periodFactor=1
        for widget in self.findChildren(QObject):
            if "Select" in widget.objectName() and not widget.objectName() == "numberIncrementsSelect":
                widget.textFromValue = lambda value: str(value).rstrip("0").rstrip(".")

        self.saveDirectorySelect.clicked.connect(self.selectSaveDir)
        self.saveDirectory=os.getcwd()
        self.setSaveDir(self.saveDirectory)

        
        self.devices = getInstruments()

        self.selectBoxes = [self.cameraSelectionSelect,
                            self.functionGeneratorSelect,
                            self.multimeterXSelect,
                            self.multimeterYSelect]

        self.camera, self.functionGenerator, self.multimeterX, self.multimeterY = None, None, None, None

        self.setting_options = ['STEP', 'INC', 'WAVE', 'VOLT', 'FREQ', 'PER', 'PHASE', 
                                'FPS', 'REC', 'SHOW_FPS', 'SHOW_DIR', 'SHOW_VOLT', 'SHOW_TIME', 'SHOW_SCALEBAR']
        
        self.setting_variables = [self.stepIncrementSelect, self.numberIncrementsSelect, self.waveformSelect,
                                  self.voltageSelect, self.frequencySelect, self.periodSelect, self.phaseSelect,
                                  self.fpsSelect, self.recordingTimeSelect, self.showFPS, self.showDirection,
                                  self.showVoltage, self.showTimestamp, self.showScalebar]

        
        for selectBox in self.selectBoxes:
            for dev, name in self.devices.items():
                selectBox.addItem(name)
                selectBox.setItemData(selectBox.count() - 1, dev)
            selectBox.currentIndexChanged.connect(partial(self.connectInstrument, selectBox))

    def startCamera(self, camera):
        self.captureCamera = captureCamera(camera)
        self.captureCamera.frame_signal.connect(self.updateFrame)
        if not self.captureCamera.isRunning():
            self.captureCamera.running = True
            self.captureCamera.start()
    
    def updateFrame(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        self.cameraFrame.setPixmap(pixmap)
    
    def emitStart(self, checked):
        self.run_experiment.emit(checked)
    
    def selectSaveDir(self):
        selected_directory = QFileDialog.getExistingDirectory(self, "Select a Save Directory")
        if selected_directory:
            self.saveDirectory = selected_directory
            self.setSaveDir(selected_directory)
            print(f'Setting save directory to: {selected_directory}')

    def setSaveDir(self, directory):
        fm = QFontMetrics(self.saveDirectorySelect.font())
        elided_text = fm.elidedText(directory, Qt.ElideRight, self.saveDirectorySelect.width() - 10) 
        self.saveDirectorySelect.setText(QCoreApplication.translate("Dialog", directory, None))
        self.saveDirectorySelect.setToolTip(directory)
        
    def syncFreq(self, press=True):
        if press and self.frequencySelect.value() != 0:
            self.frequencyValue = self.frequencySelect.value()*self.frequencyFactor

        if self.frequencyValue < 1:
            self.frequencyFactor=1e-3
            self.frequencyLabel.setText(QCoreApplication.translate("Dialog", u"Frequency (mHz)", None))
        if self.frequencyValue >= 1:
            self.frequencyFactor=1
            self.frequencyLabel.setText(QCoreApplication.translate("Dialog", u"Frequency (Hz)", None))
        if self.frequencyValue >= 1e3:
            self.frequencyFactor=1e3
            self.frequencyLabel.setText(QCoreApplication.translate("Dialog", u"Frequency (kHz)", None))
        if self.frequencyValue >= 1e6:
            self.frequencyFactor=1e6
            self.frequencyLabel.setText(QCoreApplication.translate("Dialog", u"Frequency (MHz)", None))

        if press and self.frequencyValue != 0:
            self.periodValue=1/self.frequencyValue
            self.syncPer(False)
        print(f'Synchronizing frequency to {self.frequencyValue/self.frequencyFactor}')
        self.frequencySelect.setValue(self.frequencyValue/self.frequencyFactor)

    
    def syncPer(self, press=True):
        if press and self.periodSelect.value() != 0:
            self.periodValue = self.periodSelect.value()*self.periodFactor

        if self.periodValue < 1:
            self.periodFactor=1e-3
            self.periodLabel.setText(QCoreApplication.translate("Dialog", u"Period (ms)", None))
        if self.periodValue >= 1:
            self.periodFactor=1
            self.periodLabel.setText(QCoreApplication.translate("Dialog", u"Period (s)", None))
        if self.periodValue >= 60:
            self.periodFactor=60
            self.periodLabel.setText(QCoreApplication.translate("Dialog", u"Period (min)", None))
        if self.periodValue >= 3600:
            self.periodFactor=3600
            self.periodLabel.setText(QCoreApplication.translate("Dialog", u"Period (hrs)", None))

        if press and self.periodValue != 0:
            self.frequencyValue=1/self.periodValue
            self.syncFreq(False)
        print(f'Synchronizing period to {self.periodValue/self.periodFactor}')
        self.periodSelect.setValue(self.periodValue/self.periodFactor)

    def connectInstrument(self, selectBox, index):
        #printDevice(selectBox, index)
        idn = selectBox.itemData(index)
        name = selectBox.objectName()
        inst = rm.open_resource(idn)
        try:
            if "camera" in name:
                self.camera = inst
                print(f"Setting camera to: {inst.query('*IDN?').strip()}")
            if "functionGenerator" in name:
                self.functionGenerator = inst
                print(f"Setting function generator to: {inst.query('*IDN?').strip()}")
            if "multimeterX" in name:
                self.multimeterX = inst
                print(f"Setting multimeter (X) to: {inst.query('*IDN?').strip()}")
            if "multimeterY" in name:
                self.multimeterY = inst
                print(f"Setting multimeter (Y) to: {inst.query('*IDN?').strip()}")
        except:
            print(f'Error connecting to {selectBox.currentText()}')

    def applySettings(self):
        inst = self.functionGenerator
        wave = self.waveformSelect.currentText()
        volt = self.voltageSelect.value()
        freq = self.frequencyValue
        fgen_name = self.functionGeneratorSelect.currentText()
        
        setVoltage(inst, fgen_name, volt)
        setFrequency(inst, freq)
        setWaveform(inst, wave)

    def applyLoadedSettings(self, settings):
        for option in self.setting_options:
            if option in settings.keys():
                setting_object = self.setting_variables[self.setting_options.index(option)]
                setting = settings[option].iloc[0]
                name = setting_object.objectName()
                objtype = type(setting_object)
                if isinstance(setting_object, QDoubleSpinBox) or isinstance(setting_object, QSpinBox):
                    setting = float(setting)
                    if name == "periodSelect":
                        self.periodValue = setting
                        self.syncPer()
                    elif name == "frequencySelect":
                        self.frequencyValue = setting
                        self.syncFreq()
                    else:
                        setting_object.setValue(setting)
                    print(f'Setting {objtype}, {name} to {type(setting)}, {setting}')
                    
                elif isinstance(setting_object, QComboBox):
                    setting = str(setting)
                    print(f'Setting {objtype}, {name} to {type(setting)}, {setting}')
                    index = setting_object.findText(setting)
                    if index != -1:
                        setting_object.setCurrentIndex(index)
                        
                elif isinstance(setting_object, QCheckBox):
                    setting = str(setting).strip().lower() == "true"
                    print(f'Setting {type(setting_object)}, {name} to {type(setting)}, {setting}')
                    setting_object.setChecked(setting)
                else:
                    print(f'Could not find {name} of type {objtype}')

    def saveSettings(self, file_path):
        settings={}
        for option, variable in zip(self.setting_options, self.setting_variables) :
            setting=None
            if isinstance(variable, QDoubleSpinBox) or isinstance(variable, QSpinBox):
                setting = variable.value()
            elif isinstance(variable, QComboBox):
                setting = variable.currentText()
            elif isinstance(variable, QCheckBox):
                setting = variable.isChecked()
            settings[option] = setting
        df_settings = pd.DataFrame([settings])
        df_settings.to_csv(file_path, index=False)
        print(f'Saving {df_settings}\n to {file_path}')
            
    def refresh(self):
        print("Refreshing camera feed...")
        self.captureCamera.stop()
        self.startCamera(0)

    def closeEvent(self, event):
        self.captureCamera.stop()
        event.accept()