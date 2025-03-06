from main import *
from comms import *
from camera import captureCamera
from functools import partial
import pypylon.pylon as py
import cv2

import ui_fgen
reload(ui_fgen)
from ui_fgen import Ui_Dialog as Ui_Auto

def textBackground(text, fontScale, thickness, pos):
    (textWidth, textHeight), baseline = cv2.getTextSize(str(text), cv2.FONT_HERSHEY_SIMPLEX, fontScale, thickness)
    rect = [(pos[0], pos[1]), (pos[0] + textWidth, pos[1] + textHeight+baseline)]
    textPos = (pos[0], pos[1] + textHeight + baseline // 2)
    
    return (rect, textPos)

class videoSaver(QThread):
    def __init__(self):
        super().__init__()
        
    def run(self):
      self.exec_()

    @Slot(tuple)
    def saveFrame(self, frame_out):
        frame, out = frame_out
        if out is not None and frame is not None:
            try:
                out.write(frame)
            except Exception as e:
                print(f"Error reading frame from camera thread: {e}")
              
    def stop(self):
        self.quit()
        self.wait()    

class pollMultimeter(QThread):
    voltage = Signal(float)

    def __init__(self, inst):
        super().__init__()

        self.inst = inst
        self.running = True
    
    def run(self):
        while self.running:
            try:
                volt = getVoltage(self.inst)
                self.voltage.emit(volt)
            except Exception as e:
                print(e)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        
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
        self.direction = ''
        self.active_voltage = 0
        self.voltage_x = 0
        self.voltage_y = 0
        self.videoSaver = videoSaver()

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

        self.selectBoxes = [self.functionGeneratorSelect,
                            self.multimeterXSelect,
                            self.multimeterYSelect]

        self.camera, self.functionGenerator, self.multimeterX, self.multimeterY = None, None, None, None

        self.setting_options = ['STEP', 'INC', 'WAVE', 'VOLT', 'FREQ', 'PER', 'PHASE', 
                                'FPS', 'REC', 'SHOW_FPS', 'SHOW_DIR', 'SHOW_VOLT', 'SHOW_TIME', 'SHOW_SCALEBAR']
        
        self.setting_variables = [self.stepIncrementSelect, self.numberIncrementsSelect, self.waveformSelect,
                                  self.voltageSelect, self.frequencySelect, self.periodSelect, self.phaseSelect,
                                  self.fpsSelect, self.recordingTimeSelect, self.showFPS, self.showDirection,
                                  self.showVoltage, self.showTimestamp, self.showScalebar]

        self.exposureTimeSlider.valueChanged.connect(self.exposureTimeValue.setValue)
        self.exposureTimeValue.valueChanged.connect(self.exposureTimeSlider.setValue)
        self.exposureTimeValue.valueChanged.connect(self.onExposure)
        self.fpsSelect.editingFinished.connect(self.onFPS)
        self.recordButton.clicked.connect(self.onRecord)
        
        for selectBox in self.selectBoxes:
            for dev, name in self.devices.items():
                autodetect = False
                if "04638827" in name:
                    name = "KEITHLEY (X)"
                    autodetect = True
                elif "04611760" in name:
                    name = "KEITHLEY (Y)"
                elif "33220A" in name:
                    name = "AGILENT (33220A)"
                elif "No IDN" in name:
                    continue
                selectBox.addItem(name)
                selectBox.setItemData(selectBox.count() - 1, dev)
                    
            selectBox.currentIndexChanged.connect(partial(self.connectInstrument, selectBox))

        self.tlf = py.TlFactory.GetInstance()
        cameras = self.tlf.EnumerateDevices()
        
        self.cameraSelectionSelect.currentIndexChanged.connect(self.getCamera)
        for c in cameras:
            name = c.GetModelName()
            self.cameraSelectionSelect.addItem(name)
            self.cameraSelectionSelect.setItemData(self.cameraSelectionSelect.count() - 1, c)

            try:
                cam = py.InstantCamera(self.tlf.CreateDevice(c))
                cam.Close()
                print(f"Closed: {name}")
            except Exception as e:
                print(f"Error checking camera device {c}")


        if len(cameras) == 1:
            camera = cameras[0]
            name = camera.GetModelName()
            self.cameraSelectionSelect.setCurrentText(name)
            self.startCamera(camera, name)
            
    @property
    def getCamera(self):
        if self.captureCamera is not None:
            self.captureCamera.stop()
        index = self.cameraSelectionSelect.currentIndex()
        name = self.cameraSelectionSelect.currentText()
        camera = self.cameraSelectionSelect.itemData(index)
        print(f"Starting {name}...")
        self.cameraFrame.setPixmap(self.blank)
        self.startCamera(camera, name)

    def onRecord(self):
        if self.captureCamera is not None:
            if self.playButton.isChecked() and not self.captureCamera.record:
                if self.recordButton.isChecked():
                    self.captureCamera.startRecord()
                else:
                    self.captureCamera.stopRecord()
        else:
            print("No camera to record!")
        
    def startCamera(self, camera=None, name='Unknown Camera'):
        if camera.__class__.__name__ == "DeviceInfo":
            self.captureCamera = captureCamera(camera, self.fpsSelect.value(), name, self.tlf)
            self.captureCamera.timestamp.connect(self.dataAcquisition)
            self.captureCamera.frame_out.connect(self.videoSaver.saveFrame)
            self.captureCamera.display_out.connect(self.updateFrame)
            self.videoSaver.start()
            self.captureCamera.start()
            if not self.captureCamera.isRunning():
                self.captureCamera.running = True
            self.captureCamera.startCamera()
            if self.captureCamera.isRunning():
                self.statusMessage.setText(QCoreApplication.translate("Dialog", u"Status: Connected", None))
        elif camera == 0:
            pass
        else:
            print(f"{camera} is not PyPylon compatible!")
    
    def updateFrame(self, data):
        frame, fps, exposure, record_state = data
        if self.exposureTimeValue.value() != exposure:
            self.exposureTimeValue.setValue(exposure)

        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        h, w, ch = frame.shape
        bytes_per_line = w * ch
        
        if record_state:
            circle_center = (w - 50, 50)
            circle_radius = 15
            circle_color = (0, 0, 255)
            circle_thickness = -1
            cv2.circle(frame, circle_center, circle_radius, circle_color, circle_thickness)

        fontScale = 1.5
        thickness = 1
        fpsHeight = 0

        if not self.playButton.isChecked():
            self.direction = 'None'
        
        messages = [(self.showFPS.isChecked(), f"FPS: {fps:.2f}"),
                    (self.showDirection.isChecked(), f'DIR: {self.direction}'),
                    (self.showExposure.isChecked(), f'Exp: {exposure:.2f}'),
                    (self.showVoltage.isChecked(), f'X: {self.voltage_x} V'),
                    (self.showVoltage.isChecked(), f'Y: {self.voltage_y} V')]

        total_height = 0
        for checkbox, msg in messages:
            if checkbox:
                rect, pos = textBackground(msg, fontScale, thickness, (5, total_height))
                cv2.rectangle(frame, rect[0], rect[1], color=(255, 255, 255), thickness=-1)
                cv2.putText(frame, msg, pos, cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0,0,0), thickness, lineType=cv2.LINE_AA)
                total_height += 5+rect[1][1]-rect[0][1]

        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image).scaled(self.cameraFrame.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.cameraFrame.setPixmap(pixmap)
        
    def dataAcquisition(self, time):
        if self.direction == "X":
            volt = self.voltage_x
        elif self.direction == "Y":
            volt = self.voltage_y
        else:
            volt = np.nan

        self.active_voltage = volt
        self.active_dictionary[time] = volt
        
    def onExposure(self):
        value = self.exposureTimeValue.value()
        if self.captureCamera is not None:
            self.captureCamera.setExposure(value)

    def onFPS(self):
        if self.captureCamera is not None:
            self.captureCamera.desired_fps = self.fpsSelect.value()
    
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

        multimeter_reset_cmd = """
                               *RST
                               :SENS:FUNC "VOLT:DC"
                               """
        try:
            inst_id = inst.query('*IDN?').strip()
            if "camera" in name:
                self.camera = inst
                print(f"Setting camera to: {inst_id}")
            if "functionGenerator" in name:
                self.functionGenerator = inst
                print(f"Setting function generator to: {inst_id}")
            if "multimeterX" in name:
                if self.multimeterX is not None:
                    self.multimeterX.stop()
                print(f"Setting multimeter (X) to: {inst_id}")
                print(f"Resetting {inst_id}...")
                inst.write(multimeter_reset_cmd)
                self.multimeterX = pollMultimeter(inst)
                self.multimeterX.voltage.connect(self.onMultiX)
                self.multimeterX.start()
            if "multimeterY" in name:
                if self.multimeterY is not None:
                    self.multimeterY.stop()
                print(f"Setting multimeter (Y) to: {inst_id}")
                print(f"Resetting {inst_id}...")
                inst.write(multimeter_reset_cmd)
                self.multimeterY = pollMultimeter(inst)
                self.multimeterY.voltage.connect(self.onMultiY)
                self.multimeterY.start()
        except Exception as e:
            print(f'Error connecting to {selectBox.currentText()}: {e}')

    def onMultiX(self, voltage):
        self.voltage_x = voltage
        #print(f"X: {voltage}")

    def onMultiY(self, voltage):
        self.voltage_y = voltage
        #print(f"Y: {voltage}")
            
    def applySettings(self):
        inst = self.functionGenerator
        wave = self.waveformSelect.currentText()
        volt = self.voltageSelect.value()
        freq = self.frequencyValue
        fgen_name = self.functionGeneratorSelect.currentText()

        # self.onExposure()
        # self.captureCamera.desired_fps = self.fpsSelect.value()
        setVoltage(inst, fgen_name, volt)
        setFrequency(inst, freq)
        setWaveform(inst, wave)
        
        self.onFPS()
        self.onExposure()

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
        print(f"Refreshing {self.captureCamera.name}...")
        self.captureCamera.stop()
        self.statusMessage.setText(QCoreApplication.translate("Dialog", u"Status: Disconnected", None))
        index = self.cameraSelectionSelect.currentIndex()
        name = self.cameraSelectionSelect.currentText()
        camera = self.cameraSelectionSelect.itemData(index)
        self.cameraFrame.setPixmap(self.blank)
        self.startCamera(camera, name)
        

    def closeEvent(self, event):
        threads = [self.captureCamera, self.multimeterX, self.multimeterY, self.videoSaver]
        for thread in threads:
            if thread is not None:
                thread.stop()
        event.accept()