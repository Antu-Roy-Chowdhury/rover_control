# main.py ← FINAL BEAUTIFUL LAYOUT
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

from joystick import JoystickWidget
from arm_control import ArmControlWidget  # ← New intuitive version
from video_feed import VideoFeedWidget
import serial_handler as serial

class MarsRoverController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Team Zenith Controller")
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.setStyleSheet("background: black;")

        # Background
        self.bg = QLabel(self)
        self.bg.lower()
        self.bg.setScaledContents(True)
        self.load_bg()

        container = QWidget()
        container.setStyleSheet("background: rgba(20,0,0,160); border-radius: 35px;")
        self.setCentralWidget(container)

        outer = QVBoxLayout(container)
        outer.setContentsMargins(50, 70, 50, 50)
        outer.setSpacing(30)

        title = QLabel("Team Zenith Controller")
        title.setStyleSheet("color: #ff4b1f; font-size: 80px; font-weight: bold;")
        title.setFont(QFont("Orbitron", 80, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(35)
        outer.addLayout(grid)

        # All 4 panels — EQUAL SIZE!
        self.joystick = JoystickWidget()
        self.arm = ArmControlWidget()
        self.front = VideoFeedWidget("Front Camera", "http://localhost:5000/video/front")
        self.back = VideoFeedWidget("Back Camera", "http://localhost:5000/video/back")

        grid.addWidget(self.joystick, 0, 0)
        grid.addWidget(self.front, 0, 1)
        grid.addWidget(self.arm, 1, 0)
        grid.addWidget(self.back, 1, 1)

        # Make all cells same size
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.joystick.command_signal.connect(serial.send_command)

# ...existing code...
    def load_bg(self):
        p = QPixmap("mars_bg.jpg")
        if p.isNull():
            p = QPixmap(1920, 1080)
            p.fill(Qt.GlobalColor.darkRed)
        self.bg.setPixmap(p.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        self.bg.setGeometry(0, 0, self.width(), self.height())
# ...existing code...

    def resizeEvent(self, event):
        self.load_bg()
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MarsRoverController()
    window.show()
    sys.exit(app.exec())