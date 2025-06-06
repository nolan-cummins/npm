import cv2
import numpy as np

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

def applyFilters(frame, settings):
    boxes, centers, boxes2D = [], [], []

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
    return frame, boxes, centers, boxes2D

def trackObject(frame, settings, coord, M, hovering, track, tracked_box, tracked_center, setpoint):
    if frame is not None:
        h, w = frame.shape[:2]
        original = frame.copy()
        frame, boxes, centers, boxes2D = applyFilters(frame, settings)

        if settings["showOriginal"]:
            frame = original
        zoom_scale = 1+settings["zoomSlider"]/20
        if len(boxes) > 0:
            x, y, p_w, p_h = coord
            x *= w/p_w
            y *= h/p_h
            if M is not None:
                M_inv = cv2.invertAffineTransform(M)
                pts = np.array([[[x, y]]], dtype=np.float32)
                x, y = cv2.transform(pts, M_inv)[0,0]
            box_to_track = None
            box_center = None
            hovering = False
            for i, box in enumerate(boxes):
                if cv2.pointPolygonTest(box, (x, y), False) >= 0:
                    boxes.pop(i)
                    box_to_track = box
                    box2D_to_track = boxes2D[i]
                    box_center = centers[i]
                    hovering = True
                    break

            skip_once = False
            if box_to_track is not None:
                if track and tracked_box is None:
                    tracked_box = box2D_to_track
                    setpoint = box_center
                    skip_once = True
                elif not track:
                    cv2.drawContours(frame,[box_to_track],-1,(0, 255, 0),2)
                    print(f'Selecting object at: ({x:.2f}, {y:.2f})'.ljust(200), end='\r')
            if track and not skip_once:
                if tracked_box is None:
                    track = False
                else:
                    match = False
                    distances = np.sum((np.array(centers) - tracked_box[0]) ** 2, axis=1)
                    closest_box2D = boxes2D[np.argmin(distances)]
                    closest_box = np.intp(cv2.boxPoints(closest_box2D))
                    itype, _ = cv2.rotatedRectangleIntersection(tracked_box, closest_box2D)
                    if itype != cv2.INTERSECT_NONE:
                        tracked_center = np.intp(closest_box2D[0])
                        cv2.drawContours(frame,[closest_box],-1,(0, 255, 0),2)
                        cv2.line(frame,setpoint,tracked_center,(0,0,0),1)
                        cv2.circle(frame,setpoint,5,(0,255,0))
                        cv2.circle(frame,tracked_center,5,(0,0,255))
                        tracked_box = closest_box2D

                        if zoom_scale > 0:
                            cx, cy = setpoint

                            crop_h = int(h/zoom_scale)
                            crop_w = int(w/zoom_scale)
                            half_h = crop_h // 2
                            half_w = crop_w // 2
                            
                            x1 = int(cx - half_w)
                            y1 = int(cy - half_h)
                            
                            x1 = max(0, min(x1, w - crop_w))
                            y1 = max(0, min(y1, h - crop_h))
                            x2 = x1 + crop_w
                            y2 = y1 + crop_h
                            
                            crop_frame = np.array(frame[y1:y2, x1:x2])
                            frame = cv2.resize(crop_frame, (w, h))
                        match = True
                track = match
                if not match:
                    setpoint=None
                    tracked_box=None
                    tracked_center=None
    return frame, M, hovering, track, tracked_box, tracked_center, setpoint, boxes, zoom_scale