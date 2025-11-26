# video_feed.py
import cv2
from PIL import Image, ImageTk

class VideoFeed:
    def __init__(self, source=0, yolo_model=None):
        """
        source: camera index (default 0)
        yolo_model: optional preloaded YOLO model
        """
        self.cap = cv2.VideoCapture(source)
        self.yolo = yolo_model
        self.frame = None

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        self.frame = frame
        return frame

    def process_frame(self):
        """
        Process frame (YOLO detection if available)
        Returns: ImageTk.PhotoImage for Tkinter
        """
        if self.frame is None:
            return None

        frame = self.frame.copy()

        # YOLO object detection
        if self.yolo:
            results = self.yolo(frame)
            for result in results.xyxy[0]:
                x1, y1, x2, y2, conf, cls = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, f"{int(cls)} {conf:.2f}", (x1, y1-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk

    def release(self):
        self.cap.release()
