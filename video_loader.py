from main import *
import cv2

def nearestOdd(n):
    return n if n % 2 == 1 else n + 1

def frameDifferencing(frame, area_min: int=25, area_max: int=100):
    boxes, boxes2D, centers = [], [], []
    
    contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < area_min or area > area_max * 3:
            continue
        box2D = cv2.minAreaRect(contour)
        box = cv2.boxPoints(box2D)
        box = np.intp(box)
        boxes.append(box)
        boxes2D.append(box2D)
        centers.append(np.intp(box2D[0]))
        
    return boxes, centers, boxes2D

class processVideo(QThread):
    display_out = Signal(tuple)
    
    def __init__(self):
        super().__init__()

        self.cap = None
        self.fps = 1
        self.running = True
        self.pause = False
        self.display_fps = 30
        self.name = ''
        self.file = ''
        self.init_mutex = QMutex()
        self.pause_mutex = QMutex()
        self.settings_mutex = QMutex()
        self.coord_mutex = QMutex()
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
        self.coord = None
        self.tracked_box = None
        self.tracked_center = None
        self.setpoint = None
        self.track = False
        self.M = None
        self.hovering = False

    @Slot()
    def applySettings(self, name, value):
        with QMutexLocker(self.settings_mutex):
            self.settings[name] = value
            print(f"Changed {name} to {value}".ljust(200), end='\r')
            
    @Slot()
    def loadVideo(self, file):
        try:
            with QMutexLocker(self.init_mutex):
                self.cap = cv2.VideoCapture(file)
                self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.name = os.path.basename(file)
                self.file = file
            print(f"Loading video: {self.name}")
        except Exception as e:
            print(f"Error loading video {self.name}: {e}")

    @Slot()
    def clearVideo(self):
        with QMutexLocker(self.init_mutex):
            self.cap = None

    def capExists(self):
        with QMutexLocker(self.init_mutex):
            return self.cap is not None
    
    def videoState(self, paused):
        with QMutexLocker(self.pause_mutex):
            self.pause = paused

    @Slot()
    def pingCoords(self, coord):
        with QMutexLocker(self.coord_mutex):
            self.coord = coord
    
    @Slot()
    def restartVideo(self):
        with QMutexLocker(self.init_mutex):
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def applyFilters(self, frame):
        boxes, centers, boxes2D = [], [], []
        with QMutexLocker(self.settings_mutex):
            settings = self.settings

        if len(frame.shape) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
        if settings["blurToggle"]:
            blurVal = nearestOdd(int(31*settings["blurSlider"]/100))
            frame = cv2.GaussianBlur(frame, (blurVal, blurVal), 0)
        
        if settings["adaptToggle"]:
            frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                          settings["adaptSliderArea"], settings["adaptSliderC"])
            frame = cv2.bitwise_not(frame)
        
        if settings["invertToggle"]:
            frame = cv2.bitwise_not(frame)
        
        if settings["dilationToggle"]:
            frame = cv2.dilate(frame, None, iterations=settings["dilationSlider"])
            kernel = np.ones((3, 3), np.uint8)
            frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

        if settings["frameDiffToggle"]:
            boxes, centers, boxes2D = frameDifferencing(frame, settings["frameDiffSlider"], settings["frameDiffSliderMax"])
        
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        return frame, boxes, centers, boxes2D, settings

    @Slot()
    def startTracking(self):
        if self.hovering:
            self.track = not self.track
        else:
            self.track = False
        self.setpoint = None
        self.tracked_box = None
        self.tracked_center = None
    
    def run(self):
        tick_freq = cv2.getTickFrequency()
        fps_tick = 0
        last_tick = 0
        frame_num = 0
        run_once = True
        while self.running:
            if self.cap is not None:
                with QMutexLocker(self.init_mutex):
                    cap = self.cap
                    display_time = 1/self.display_fps
                    frame_time = 1/self.fps
                try:
                    start_tick = cv2.getTickCount()
                    ret, frame = cap.read()
                    if not ret:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    if fps_tick == 0:
                        fps_tick = cv2.getTickCount()
                    if last_tick == 0:
                        last_tick = cv2.getTickCount()

                    if frame is not None:
                        h, w = frame.shape[:2]
                        original = frame.copy()
                        frame, boxes, centers, boxes2D, settings = self.applyFilters(frame)
    
                        current_tick = cv2.getTickCount()
                        if (current_tick - fps_tick) / tick_freq >= display_time:
                            fps_tick = current_tick
                            if frame is not None:
                                if settings["showOriginal"]:
                                    frame = original
                                zoom_scale = 1+settings["zoomSlider"]/20
                                if len(boxes) > 0:
                                    with QMutexLocker(self.coord_mutex):
                                        coord = self.coord
                                        x, y, p_w, p_h = coord
                                        x *= w/p_w
                                        y *= h/p_h
                                        if self.M is not None:
                                            M_inv = cv2.invertAffineTransform(self.M)
                                            pts = np.array([[[x, y]]], dtype=np.float32)
                                            x, y = cv2.transform(pts, M_inv)[0,0]
                                    box_to_track = None
                                    box_center = None
                                    all_boxes = boxes.copy()
                                    self.hovering = False
                                    for i, box in enumerate(boxes):
                                        if cv2.pointPolygonTest(box, (x, y), False) >= 0:
                                            boxes.pop(i)
                                            box_to_track = box
                                            box2D_to_track = boxes2D[i]
                                            box_center = centers[i]
                                            self.hovering = True
                                            break

                                    if box_to_track is not None:
                                        if self.track and self.tracked_box is None:
                                            self.tracked_box = box2D_to_track
                                            self.setpoint = box_center
                                        elif not self.track:
                                            cv2.drawContours(frame,[box_to_track],-1,(0, 255, 0),2)
                                            print(f'Selecting object at: ({x:.2f}, {y:.2f})'.ljust(200), end='\r')
                                    if self.track:
                                        if self.tracked_box is None:
                                            self.track = False
                                        else:
                                            match = False
                                            for i, box2D in enumerate(boxes2D):
                                                itype, _ = cv2.rotatedRectangleIntersection(self.tracked_box, box2D)
                                                if itype != cv2.INTERSECT_NONE:
                                                    self.tracked_center = centers[i]
                                                    cv2.drawContours(frame,[all_boxes[i]],-1,(0, 255, 0),2)
                                                    cv2.line(frame,self.setpoint,self.tracked_center,(0,0,0),1)
                                                    cv2.circle(frame,self.setpoint,5,(0,255,0))
                                                    cv2.circle(frame,self.tracked_center,5,(0,0,255))
                                                    self.tracked_box = box2D

                                                    if zoom_scale > 0:
                                                        cx, cy = self.setpoint

                                                        half_w = w / (2.0 * zoom_scale)
                                                        half_h = h / (2.0 * zoom_scale)
                                                    
                                                        cx = min(max(cx, half_w), w - half_w)
                                                        cy = min(max(cy, half_h), h - half_h)
                                                        self.M = cv2.getRotationMatrix2D((float(cx), float(cy)), angle=0, scale=zoom_scale)
                                                        frame = cv2.warpAffine(frame, self.M, (w, h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
                                                    
                                                    match = True
                                                    break
                                        self.track = match
                                        if not match:
                                            self.setpoint=None
                                            self.tracked_box=None
                                            self.tracked_center=None
                                            
                                    if not self.track:
                                        cv2.drawContours(frame,boxes,-1,(0, 0, 255),2)
                                        
                                if zoom_scale > 0:
                                    if not self.track:
                                        cx, cy = (w/2, h/2)
                                        self.M = cv2.getRotationMatrix2D((float(cx), float(cy)), angle=0, scale=zoom_scale)
                                        frame = cv2.warpAffine(frame, self.M, (w, h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
                                if current_tick - last_tick > 0:
                                    fps = tick_freq / (current_tick - last_tick);

                                try:
                                    ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
                                    minutes = ms // 60000
                                    seconds = (ms % 60000) // 1000
                                    hundredths = (ms % 1000) // 10
                                    timestamp = f"{minutes:02d}:{seconds:02d}:{hundredths:02d}"
                                    self.display_out.emit((frame, fps, timestamp, self.tracked_center, self.setpoint))
                                except Exception as e:
                                    print(f'Error emitting display frame: {e}')
                        last_tick = cv2.getTickCount()
                        
                    process_time = (cv2.getTickCount() - start_tick) / tick_freq
                    sleep_time = max(frame_time - process_time, 0)
                    sleep(sleep_time)
                except Exception as e:
                    print(e)

    @Slot()
    def stop(self):
        self.running = False
        self.quit()
        self.wait()