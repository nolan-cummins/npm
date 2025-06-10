from main import *
import cv2
import pypylon.pylon as py
from time import sleep

class captureCamera(QThread):
    timestamp = Signal(float)
    frame_out = Signal(tuple)
    display_out = Signal(tuple)

    def __init__(self, camera=None, fps=100, name='Unknown Camera', tlf=py.TlFactory.GetInstance()):
        super().__init__()
        if camera is None:
            try:
                py.TlFactory.GetInstance().EnumerateDevices()[0]
            except:
                print("No pylon cameras detected!")
        self.running = True
        self.desired_fps = fps
        self.name = name
        self.tlf = tlf
        self.cameraDevice = camera
        self.exposure=100
        self.frame_size=(1280, 1024)
        self.out=None
        self.record=False
        self.camera=None
        self.start_time = 0
        try:
            self.camera = py.InstantCamera(self.tlf.CreateDevice(self.cameraDevice)) 
            if self.camera is not None:
                self.camera.Open()
                
                self.camera.PixelFormat.Value = "Mono8"
                self.camera.ExposureAuto.Value = "Off"
                self.camera.Gain.Value = 0
                
                self.max_exposure = 20000
                self.min_exposure = 100
                self.camera.ExposureTime.Value=100
                self.w = self.camera.Width.Max
                self.h = self.camera.Height.Max
                self.frame_size = (self.w, self.h)
                
                self.camera.AcquisitionFrameRateEnable.Value = False
                self.camera.AcquisitionFrameRate.Value = 100
            else:
                print("No camera object!")
        except Exception as e:
            print(f"Invalid camera object: {e}")
        
        self.frame_duration = 1.0 / self.desired_fps

    def startCamera(self):
        if self.camera is not None:
            print(f"Starting frame collection: {self.name}")
            self.camera.StartGrabbing(py.GrabStrategy_LatestImageOnly)
        else:
            print(f"No camera object found: {self.camera}")

    def stopCamera(self):
        self.camera.StopGrabbing()

    def setExposure(self, exposure):
        if self.camera is not None:
            self.exposure=exposure
            self.camera.ExposureTime.Value=exposure

    @Slot()
    def pingCoords(self, coords):
        pass
        #print(coords)
        
    def run(self):
        camera = self.camera
        previous_frame = None
        converter = py.ImageFormatConverter()
        converter.OutputPixelFormat = py.PixelType_Mono8
        converter.OutputBitAlignment = py.OutputBitAlignment_MsbAligned
        accumulator=0
        acc_ratio = 30/self.desired_fps
        while self.running and camera is not None:
            try:
                if camera.IsGrabbing():
                    grabResult = camera.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
                    if grabResult.GrabSucceeded():
                        accumulator+=acc_ratio
                        image = converter.Convert(grabResult)
                        frame = image.GetArray()
                        if previous_frame is None:
                            previous_frame = frame.copy()
                        current_fps = camera.ResultingFrameRate.Value
                            
                        if current_fps < self.desired_fps:
                            camera.AcquisitionFrameRateEnable.SetValue(False)
                            self.exposure = camera.ExposureTime.Value
                            diff = np.abs(current_fps-self.desired_fps-1)
                            step = diff/2
                            if current_fps < self.desired_fps and self.exposure > self.min_exposure:
                                camera.ExposureTime.Value-=step
                            elif current_fps > self.desired_fps and self.exposure < self.max_exposure:
                                camera.ExposureTime.Value+=step
                        else:
                            camera.AcquisitionFrameRateEnable.SetValue(True)
                            camera.AcquisitionFrameRate.SetValue(self.desired_fps)

                        if frame is None or frame.size == 0:
                            print("Invalid frame received! Passing previous.")
                            frame = previous_frame
                        else:
                            previous_frame = frame.copy()
                        
                        if self.record and self.out.isOpened():
                            try:
                                self.frame_out.emit((frame, self.out))
                            except Exception as e:
                                print(f'Error emitting write frame: {e}')
                            self.timestamp.emit(time.time()-self.start_time)
                            
                        if accumulator >= 1.0:
                            try: # update display
                                exposure = camera.ExposureTime.Value
                                self.display_out.emit((frame, current_fps, exposure, self.record))
                            except Exception as e:
                                print(f'Error emitting display frame: {e}')
                            
                            accumulator -= 1.0
                            
            except Exception as e:
                print(f"Error grabbing frames: {e}")
                grabResult.Release()
                break

    def startRecord(self, filename, save_directory):
        if self.out is not None:
            self.out.release()
        output_filename = f'{save_directory}/{filename}.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(output_filename, fourcc, self.desired_fps, self.frame_size, isColor=False)
        self.start_time = time.time()
        self.record = True
        return

    def stopRecord(self):
        self.record = False
        if self.out is not None:
            self.out.release()
            self.out = None
    
    def stop(self):
        if self.out is not None:
            self.out.release()
        self.running = False
        self.camera.Close()
        self.quit()
        self.wait()