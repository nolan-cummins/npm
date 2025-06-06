from main import *
from comms import *
from camera import captureCamera
from video_loader import processVideo, nearestOdd
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

class cameraFrameMouseTracking(QLabel):
    coords = Signal(tuple)
    clicked = Signal()
    wheelScrolled = Signal(int)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def mouseMoveEvent(self, event: QMouseEvent):
        x, y = event.pos().x(), event.pos().y()
        self.coords.emit((x, y))
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            event.accept()
        else:
            super().mousePressEvent(event)
            
    def wheelEvent(self, event):
        # 120 units per notch
        steps = event.angleDelta().y() // 120
        if steps:
            self.wheelScrolled.emit(int(steps))
            event.accept()
        else:
            super().wheelEvent(event)
        
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

        self.cameraFrame = cameraFrameMouseTracking(self)
        self.cameraFrame.setGeometry(QRect(10, 10, 710, 568))
        self.p_shape=(710, 568)
        self.cameraFrame.coords.connect(self.pollCoords)
        self.cameraFrame.clicked.connect(self.startTracking)
        self.cameraFrame.wheelScrolled.connect(lambda notches: self.zoomSlider.setValue(self.zoomSlider.value() + notches * 3))
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
        self.timestamp=0
        for widget in self.findChildren(QObject):
            if "Select" in widget.objectName() and not widget.objectName() == "numberIncrementsSelect":
                widget.textFromValue = lambda value: str(value).rstrip("0").rstrip(".")

        self.saveDirectorySelect.clicked.connect(self.selectSaveDir)
        self.saveDirectory=os.getcwd()
        self.setSaveDir(self.saveDirectory)


        actions = [(self.blurToggle.toggled, [self.blurSlider.setEnabled, self.blurValue.setEnabled]),
                   (self.adaptToggle.toggled, [self.adaptSliderArea.setEnabled, self.adaptValueArea.setEnabled, self.adaptSliderC.setEnabled, self.adaptValueC.setEnabled]),
                   (self.dilationToggle.toggled, [self.dilationSlider.setEnabled, self.dilationValue.setEnabled]),
                   (self.frameDiffToggle.toggled, [self.frameDiffSlider.setEnabled, self.frameDiffValue.setEnabled, self.frameDiffSliderMax.setEnabled, self.frameDiffValueMax.setEnabled]),
                   (self.blurSlider.valueChanged, [self.blurValue.setValue]),
                   (self.blurValue.editingFinished, [lambda: self.blurSlider.setValue(self.blurValue.value())]),
                   (self.adaptSliderArea.valueChanged, [self.adaptValueArea.setValue]),
                   (self.adaptValueArea.editingFinished, [lambda: self.adaptSliderArea.setValue(self.adaptValueArea.value())]),
                   (self.adaptSliderC.valueChanged, [self.adaptValueC.setValue]),
                   (self.adaptValueC.editingFinished, [lambda: self.adaptSliderC.setValue(self.adaptValueC.value())]),
                   (self.dilationSlider.valueChanged, [self.dilationValue.setValue]),
                   (self.dilationValue.editingFinished, [lambda: self.dilationSlider.setValue(self.dilationValue.value())]),
                   (self.frameDiffSlider.valueChanged, [self.frameDiffValue.setValue]),
                   (self.frameDiffValue.editingFinished, [lambda: self.frameDiffSlider.setValue(self.frameDiffValue.value())]),
                   (self.frameDiffSliderMax.valueChanged, [self.frameDiffValueMax.setValue]),
                   (self.frameDiffValueMax.editingFinished, [lambda: self.frameDiffSliderMax.setValue(self.frameDiffValueMax.value())]),
                   (self.zoomSlider.valueChanged, [self.zoomValue.setValue]),
                   (self.zoomValue.editingFinished, [lambda: self.zoomSlider.setValue(self.zoomValue.value())])]
        for action, handlers in actions:
            for handler in handlers:
                action.connect(handler)
                if "editingFinished" not in str(action):
                    action.connect(self.passVideoSettings)
        self.showOriginal.toggled.connect(self.passVideoSettings)
        self.invertToggle.toggled.connect(self.passVideoSettings)
        
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
        self.experimentSelect.currentIndexChanged.connect(self.switchExperiments)
        self.stepIncrementSelect.editingFinished.connect(partial(self.syncIncrement, "step"))
        self.numberIncrementsSelect.editingFinished.connect(partial(self.syncIncrement, "number"))
        self.voltageSelect.editingFinished.connect(partial(self.syncIncrement, "voltage"))
        self.switchExperiments()

        self.settings={"blurToggle": False,
                       "blurSlider": 0,
                       "adaptToggle": False,
                       "adaptSliderArea": 21,
                       "adaptSliderC": 4,
                       "invertToggle": False,
                       "dilationToggle": False,
                       "dilationSlider": 0,
                       "frameDiffToggle": False,
                       "frameDiffSlider": 25,
                       "frameDiffSliderMax": 100,
                       "showOriginal": False,
                       "zoomSlider": 0}
        
        for selectBox in self.selectBoxes:
            for dev, name in self.devices.items():
                if "04638827" in name:
                    name = "KEITHLEY (X)"
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
        
        self.cameraSelectionSelect.textActivated.connect(self.getCamera)
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
        self.cameraSelectionSelect.addItem("Open Video")

        if len(cameras) == 1:
            camera = cameras[0]
            name = camera.GetModelName()
            self.cameraSelectionSelect.setCurrentText(name)
            self.startCamera(camera, name)

        self.videoLoader = None
        self.tracking_info = None

    @Slot()
    def pollCoords(self, coords):
        x, y = coords
        p_w, p_h = self.p_shape
        margin_x = (self.cameraFrame.width() - p_w) / 2
        margin_y = (self.cameraFrame.height() - p_h) / 2
        x -= margin_x
        y -= margin_y
        if self.videoLoader is not None:
            self.videoLoader.pingCoords((x, y, p_w, p_h))
        if self.captureCamera is not None:
            self.captureCamera.pingCoords((x, y, p_w, p_h))

    @Slot()
    def startTracking(self):
        if self.videoLoader is not None:
            self.videoLoader.startTracking()
        
    @Slot()
    def getCamera(self, name):
        if self.captureCamera is not None:
            self.captureCamera.stop()
        index = self.cameraSelectionSelect.currentIndex()
        print(f'Selecting camera: {name}')
        if name == "Open Video":
            self.tracking_info = None
            self.openVideo()
        else:
            if self.videoLoader is not None:
                self.videoLoader.stop()
                self.tracking_info = None
                self.videoLoader = None
            camera = self.cameraSelectionSelect.itemData(index)
            print(f"Starting {name}...")
            self.cameraFrame.setPixmap(self.blank)
            self.startCamera(camera, name)

    def openVideo(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Video Files (*.avi;*.mp4;*.mov;*.mkv;*.wmv;*.flv;*.mpeg;*.mpg)",
            options=options
        )
        if file:
            if self.videoLoader is not None:
                self.videoLoader.stop()
            self.videoLoader = processVideo()
            self.videoLoader.display_out.connect(self.updateFrame)
            self.videoLoader.settings = self.settings
            self.videoLoader.start()
            self.videoLoader.loadVideo(file)

    def passVideoSettings(self, value):
        name = self.sender().objectName()
        if name == "adaptSliderArea":
            value = nearestOdd(value)
            self.adaptSliderArea.setValue(value)
            self.adaptValueArea.setValue(value)
        if self.videoLoader is not None:
            self.videoLoader.applySettings(name, value)
        self.settings[name] = value
            
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
        elif camera == 0 or camera is None:
            pass
        else:
            print(f"{camera} is not PyPylon compatible!")
    
    def updateFrame(self, data):
        if self.videoLoader is not None:
            frame, fps, time, center, setpoint = data
            if center is not None and setpoint is not None:
                self.tracking_info = (center, setpoint)
            exposure = 0
            record_state = False
        elif self.captureCamera is not None:
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
                    (self.showVoltage.isChecked(), f'Y: {self.voltage_y} V'),
                    (self.showTimestamp.isChecked(), time)]

        if self.tracking_info is not None:
            center, setpoint = self.tracking_info
            dx, dy = np.array(setpoint) - np.array(center)
            messages.append((self.showPosition.isChecked(), f'({dx:.0f}, {dy:.0f})'))
        
        total_height = 0
        for checkbox, msg in messages:
            if checkbox:
                rect, pos = textBackground(msg, fontScale, thickness, (5, total_height))
                cv2.rectangle(frame, rect[0], rect[1], color=(255, 255, 255), thickness=-1)
                cv2.putText(frame, msg, pos, cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0,0,0), thickness, lineType=cv2.LINE_AA)
                total_height += 5+rect[1][1]-rect[0][1]

        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image).scaled(self.cameraFrame.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.p_shape = (pixmap.width(), pixmap.height()) 
        self.cameraFrame.setPixmap(pixmap)
        
    def dataAcquisition(self, time):
        if self.direction == "X":
            volt = self.voltage_x
        elif self.direction == "Y":
            volt = self.voltage_y
        else:
            volt = np.nan
        self.timestamp = time
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

        if inst is None:
            print("No function generator connected!")
            return
        if self.experimentSelect.currentText() == "Voltage":
            if self.stepIncrementSelect.value() == 0:
                self.syncIncrement("number")
            elif self.numberIncrementsSelect.value() == 0:
                self.syncIncrement("step")
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

    def switchExperiments(self):
        experiment = self.experimentSelect.currentText()
        if experiment == "Z-Axis Offset":
            self.stepIncrementLabel.setText(QCoreApplication.translate("Dialog", u"Step Increment (um)", None))
            self.voltageLabel.setText(QCoreApplication.translate("Dialog", u"Voltage (Vpp)", None))
        elif experiment == "Voltage":
            self.stepIncrementLabel.setText(QCoreApplication.translate("Dialog", u"Step Increment (V)", None))
            self.voltageLabel.setText(QCoreApplication.translate("Dialog", u"Max Voltage (V)", None))

    def syncIncrement(self, sender):
        if self.experimentSelect.currentText() == "Voltage":
            max_voltage = self.voltageSelect.value()
            increments = self.numberIncrementsSelect.value()
            step = self.stepIncrementSelect.value()
            if sender == "voltage" and increments == 0 and step == 0:
                return
            if step > 0:
                if step > max_voltage:
                    self.stepIncrementSelect.setValue(max_voltage)
                    max_increments = 1
                else:
                    max_increments = max_voltage//step
            elif sender == "step":
                return                
            if increments > 0:
                min_step = max_voltage/increments
            elif sender == "number":
                return
            if sender == "step":
                self.numberIncrementsSelect.setValue(max_increments)
            elif sender == "number":
                self.stepIncrementSelect.setValue(min_step)
            elif sender == "voltage":
                if step == 0 and increments > 0:
                    self.stepIncrementSelect.setValue(min_step)
                elif increments == 0 and step > 0:
                    self.numberIncrementsSelect.setValue(max_increments)
                elif increments > 0 and step > 0:
                    self.numberIncrementsSelect.setValue(max_increments)
    
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
        if self.videoLoader is not None:
            self.videoLoader.restartVideo()
            print(f"Refreshing {self.videoLoader.name}")
        else:
            print(f"Refreshing {self.captureCamera.name}...")
            self.captureCamera.stop()
            self.statusMessage.setText(QCoreApplication.translate("Dialog", u"Status: Disconnected", None))
            index = self.cameraSelectionSelect.currentIndex()
            name = self.cameraSelectionSelect.currentText()
            camera = self.cameraSelectionSelect.itemData(index)
            self.cameraFrame.setPixmap(self.blank)
            self.startCamera(camera, name)

    def closeEvent(self, event):
        threads = [self.captureCamera, self.multimeterX, self.multimeterY, self.videoSaver, self.videoLoader]
        for thread in threads:
            if thread is not None:
                thread.stop()
        event.accept()