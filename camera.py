from main import *
import cv2 as cv

class captureCamera(QThread):
    frame_signal = Signal(QImage)

    def __init__(self, camera=0):
        super().__init__()
        self.running = True
        self.camera = camera
        
    def run(self):
        cap = cv.VideoCapture(self.camera)
        
        while self.running:
            ret, frame = cap.read()
            if ret:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.frame_signal.emit(q_image)
        
        cap.release()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
