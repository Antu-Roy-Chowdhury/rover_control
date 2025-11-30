# video_feed.py ← FINAL 100% WORKING VERSION
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer, Qt, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
import cv2
import numpy as np


class VideoFeedWidget(QWidget):
    def __init__(self, title, stream_url):
        super().__init__()
        self.title = title
        self.stream_url = stream_url        # ← THIS WAS MISSING BEFORE!

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("""
            color: #ff4b1f; font-size: 30px; font-weight: bold;
            background: rgba(0,0,0,180); border-radius: 15px; padding: 12px;
        """)
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # Video area
        self.video_display = QLabel("NO SIGNAL")
        self.video_display.setStyleSheet("background: black; color: #666; border-radius: 15px;")
        self.video_display.setMinimumSize(450, 340)
        self.video_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_display)

        # Network + timer
        self.manager = QNetworkAccessManager(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_frame)
        self.timer.start(60)  # ~16 FPS — smooth & safe

    def fetch_frame(self):
        req = QNetworkRequest(QUrl(self.stream_url))
        reply = self.manager.get(req)
        reply.finished.connect(lambda r=reply: self.show_frame(r))

    def show_frame(self, reply):
        if reply.error():
            self.video_display.setText("NO SIGNAL\nCamera offline")
            return

        data = reply.readAll().data()
        if not data:
            return

        arr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        qimg = QImage(frame.data, w, h, w * ch, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        scaled = pixmap.scaled(
            self.video_display.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.video_display.setPixmap(scaled)