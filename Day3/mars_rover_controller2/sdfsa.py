# joystick.py ← FINAL CLEAN & COMPACT VERSION (NO OVERLAY, SMALLER CIRCLE)
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
import math

class JoystickWidget(QWidget):
    command_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(320, 380)  # Compact but elegant
        self.setStyleSheet("background: rgba(25,8,8,240); border-radius: 35px;")

        # Title
        self.title = QLabel("Motor Joystick", self)
        self.title.setStyleSheet("color: #ff4b1f; font-size: 32px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Joystick settings
        self.radius = 100          # ← Smaller, clean circle
        self.knob_radius = 15
        self.center = QPoint(0, 0)
        self.pos = QPoint(0, 0)
        self.dragging = False

    def resizeEvent(self, event):
        # Always perfect center + title
        w, h = self.width(), self.height()
        self.center = QPoint(w // 2, h // 2 )
        self.title.setGeometry(0, 15, w, 60)
        if not self.dragging:
            self.pos = self.center
        self.update()
        super().resizeEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx, cy = self.center.x(), self.center.y()

        # === Outer ring (boundary) ===
        p.setBrush(QBrush(QColor(40, 10, 10, 240)))
        p.setPen(QPen(QColor(255, 80, 30), 8))
        p.drawEllipse(cx - self.radius - 8, cy - self.radius - 8,
                      (self.radius + 8)*2, (self.radius + 8)*2)

        # === Main circle (filled) ===
        p.setBrush(QBrush(QColor(25, 5, 5, 220)))
        p.setPen(QPen(QColor(255, 100, 50), 4))
        p.drawEllipse(cx - self.radius, cy - self.radius,
                      self.radius*2, self.radius*2)

        # === 8-direction subtle lines ===
        p.setPen(QPen(QColor(255, 100, 50, 150), 2, Qt.PenStyle.DashLine))
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = cx + int(self.radius * 0.8 * math.cos(rad))
            y = cy + int(self.radius * 0.8 * math.sin(rad))
            p.drawLine(cx, cy, x, y)

        # === Center glow ===
        p.setBrush(QBrush(QColor(255, 150, 80, 100)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(cx - 12, cy - 12, 24, 24)

        # === Joystick Knob (beautiful glow) ===
        # Outer glow
        p.setBrush(QBrush(QColor(255, 75, 31)))
        p.drawEllipse(self.pos.x() - self.knob_radius - 5,
                      self.pos.y() - self.knob_radius - 5,
                      (self.knob_radius + 5)*2, (self.knob_radius + 5)*2)

        # Main knob
        p.setBrush(QBrush(QColor(255, 75, 31)))
        p.setPen(QPen(QColor(255, 200, 100), 5))
        p.drawEllipse(self.pos.x() - self.knob_radius,
                      self.pos.y() - self.knob_radius,
                      self.knob_radius*2, self.knob_radius*2)

        # Highlight dot
        # p.setBrush(QBrush(QColor(255, 255, 200)))
        # p.drawEllipse(self.pos.x() - 8, self.pos.y() - 12, 16, 16)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.update_knob(e.position().toPoint())

    def mouseMoveEvent(self, e):
        if self.dragging:
            self.update_knob(e.position().toPoint())

    def mouseReleaseEvent(self, e):
        self.dragging = False
        self.pos = self.center
        self.update()
        self.command_signal.emit("STOP:0")

    def update_knob(self, mouse_pos):
        dx = mouse_pos.x() - self.center.x()
        dy = mouse_pos.y() - self.center.y()
        dist = math.hypot(dx, dy)

        # Clamp to circle
        if dist > self.radius:
            angle = math.atan2(dy, dx)
            dx = self.radius * math.cos(angle)
            dy = self.radius * math.sin(angle)

        self.pos = QPoint(int(self.center.x() + dx), int(self.center.y() + dy))
        self.update()

        # === 8-DIRECTION LOGIC ===
        speed = int((dist / self.radius) * 255)
        if speed < 35:
            self.command_signal.emit("STOP:0")
            return

        angle_deg = (math.degrees(math.atan2(dy, dx)) + 360) % 360

        if   angle_deg < 22.5  or angle_deg >= 337.5:  cmd = "F"
        elif angle_deg < 67.5:                        cmd = "RF"
        elif angle_deg < 112.5:                       cmd = "R"
        elif angle_deg < 157.5:                       cmd = "RB"
        elif angle_deg < 202.5:                       cmd = "B"
        elif angle_deg < 247.5:                       cmd = "LB"
        elif angle_deg < 292.5:                       cmd = "L"
        else:                                         cmd = "LF"

        self.command_signal.emit(f"{cmd}:{speed}")