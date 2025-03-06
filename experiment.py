from main import *

class Experiment(QThread):
    def __init__(self, autoDia):
        super().__init__()
        self.autoDia = autoDia

    @Slot(object)
    def updateAutoDia(self, autoDia):
        self.autoDia = autoDia
    
    def stoppable_delay(self, ms):
        self.delay_loop = QEventLoop()
        QTimer.singleShot(ms, self.delay_loop.quit)
        self.delay_loop.exec()

    def stop_stoppable_delay(self):
        if hasattr(self, "delay_loop") and self.delay_loop.isRunning():
            self.delay_loop.quit()
    
    def singleRun(self, relay, button, inst, fgen_name, position, direction):
        filename = f'{direction}_{position}_{self.autoDia.voltageSelect.value()}V'
        save_directory = self.autoDia.saveDirectory
        print("Reset waveform")
        resetWaveform(inst)
        relay("ON")
        self.stoppable_delay(1000)
        if not button.isChecked(): # Before and after each delay, must check if button is still toggled, otherwise, may continue
            return
        outputSignal(inst, fgen_name, True)
        if self.autoDia.recordButton.isChecked():
            print(f"Start recording at {self.autoDia.fpsSelect.value()} fps for {direction}")
            self.autoDia.active_dictionary={}
            self.autoDia.captureCamera.startRecord(filename=filename,
                                                   save_directory=save_directory)
        self.stoppable_delay(self.autoDia.recordingTimeSelect.value()*1e3)
        if not button.isChecked():
            return
        print("Stop recording")
        if self.autoDia.recordButton.isChecked():
            self.autoDia.captureCamera.stopRecord()
            raw = np.array(list(self.autoDia.active_dictionary.items()), dtype=float)
            raw[:, 0] -= raw[0, 0]
            data = pd.DataFrame(raw, columns=["timestamp (s)", "voltage"])
            data.to_csv(f'{save_directory}/{filename}.csv', index=False)
        outputSignal(inst, fgen_name, False)
        relay("OFF")

    def shutoffInstruments(self, inst, fgen_name, relays):
        outputSignal(inst, fgen_name, False)
        for relay in relays:
            relay("OFF")
    
    @Slot()
    def runExperiment(self, checked):
        playButton = self.autoDia.playButton
        runs = self.autoDia.numberIncrementsSelect.value()
        increment = self.autoDia.stepIncrementSelect.value() // self.step_factor
        position = self.z
        total_time = 2*(1+self.autoDia.recordingTimeSelect.value())*runs
        timer = countdownTimer(total_time, self.autoDia.timeRemainingPanel, self.autoDia.progressBar)
        inst = self.autoDia.functionGenerator
        try:
            if inst is not None:
                fgen_name = self.autoDia.functionGeneratorSelect.currentText()
                if checked:
                    timer.start()
                    print("\nStarting. . .")
                    run=1
                    while run < runs+1 and playButton.isChecked():
                        if self.autoDia.pauseButton.isChecked():
                            print(f"Paused on run {run} out of {runs}.", end='\r')
                            self.stoppable_delay(100)
                            timer.pause()
                        else:
                            timer.resume()
                            if self.z != self.z_actual:
                                print(f"Waiting for position: {self.z_actual*self.step_factor} -> {self.z*self.step_factor}", end='\r') 
                                self.z=position
                                self.stoppable_delay(100)
                            else:
                                print(f"\nBeginning run {run} of {runs}")
                                if not playButton.isChecked(): # Before, in-between, and after each run, must check if button is still toggled, otherwise, may continue
                                    break
                                self.autoDia.direction = 'X'
                                self.singleRun(self.toggleX, playButton, inst, fgen_name, position, "X")
                                if not playButton.isChecked():
                                    self.stop_stoppable_delay()
                                    break
                                self.autoDia.direction = 'Y'
                                self.singleRun(self.toggleY, playButton, inst, fgen_name, position, "Y")
                                if not playButton.isChecked():
                                    break
                                print(f"Move up {self.autoDia.stepIncrementSelect.value()} um")
                                position+=increment
                                self.z=position
                                print(f"Current position: {position*self.step_factor} um\n")
                                run+=1
                    timer.stop()
                    playButton.setChecked(False)
                    print("Finished")
                else:
                    timer.stop()
                    self.stop_stoppable_delay()
                    self.shutoffInstruments(inst, fgen_name, [self.toggleX, self.toggleY])
                    print("Stopped")
            else:
                playButton.setChecked(False)
        except:
            timer.stop()
            self.stop_stoppable_delay()
            self.shutoffInstruments(inst, fgen_name, [self.toggleX, self.toggleY])
            print("Stopped")

    def run(self):
      self.exec_()
              
    def stop(self):
        self.quit()
        self.wait()