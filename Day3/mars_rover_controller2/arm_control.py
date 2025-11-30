# arm_control.py ← FINAL CLEAN & PROFESSIONAL VERSION
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import serial_handler as serial

class ArmControlWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: rgba(30, 10, 10, 240); border-radius: 35px;")

        # Main layout with perfect spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(35, 40, 35, 40)   # Perfect padding
        main_layout.setSpacing(25)

        # === TITLE - Always visible even in fullscreen ===
        lbl_title = QLabel("ARM CONTROL")
        lbl_title.setStyleSheet("""
            color: #ff4b1f;
            font-size: 30px;
            font-weight: bold;
            background: rgba(0,0,0,180); border-radius: 15px; padding: 10px;
        """)
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setMinimumHeight(50)
        main_layout.addWidget(lbl_title)

        # === 3 Intuitive Sliders ===
        sliders_info = [
            ("LEFT ← → RIGHT", -100, 100),
            ("DOWN ↓ ↑ UP",     -100, 100),
            ("BACK ← → FORWARD",-100, 100),
        ]

        self.sliders = []
        for text, min_val, max_val in sliders_info:
            row = QHBoxLayout()
            row.setSpacing(15)

            label = QLabel(text)
            label.setStyleSheet("color: #ff8c42; font-size: 26px; font-weight: bold;")
            label.setFixedWidth(280)
            row.addWidget(label)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(0)
            slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    background: #7c3e15; height: 18px; border-radius: 50px;
                }
                QSlider::handle:horizontal {
                    background: #ff4b1f; width: 15px; border-radius: 90px;
                    margin: -14px 0;
                    border: 3px solid #ff8c42;
                }
            """)
            
            slider.valueChanged.connect(self.update_arm)
            row.addWidget(slider, stretch=1)

            value_label = QLabel("0")
            value_label.setStyleSheet("color: #ff4b1f; font-size: 22px; font-weight: bold; min-width: 50px;")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.addWidget(value_label)

            main_layout.addLayout(row)
            self.sliders.append((slider, value_label))

        # === SINGLE TOGGLE BUTTON - CAPTURE / RELEASE ===
        self.capture_btn = QPushButton("CAPTURE")
        self.capture_btn.setCheckable(True)
        self.capture_btn.setStyleSheet("""
            QPushButton {
                background: #ff3333; color: white; font-size: 15px; font-weight: bold;
                border-radius: 50px; padding: 7px; min-height: 30px;
            }
            QPushButton:checked {
                background: #00aa00; color: white;
            }
            QPushButton:pressed {
                background: white; color: #ff3333;
            }
        """)
        self.capture_btn.clicked.connect(self.toggle_gripper)
        main_layout.addWidget(self.capture_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add stretch so button stays at bottom
        main_layout.addStretch()

    def update_arm(self):
        lr = self.sliders[0][0].value()
        ud = self.sliders[1][0].value()
        fb = self.sliders[2][0].value()

        # Smooth, realistic arm movement
        base       = int(lr * 1.8)
        shoulder   = int(90 + ud * 0.9 - fb * 0.4)
        elbow      = int(90 - ud * 0.8 + fb * 0.6)
        wrist_p    = int(-ud * 0.5)
        wrist_r    = int(lr * 0.6)
        gripper    = 180 if self.capture_btn.isChecked() else 0

        # Clamp values
        vals = [base, shoulder, elbow, wrist_p, wrist_r, gripper]
        vals = [max(min(v, 180), 0) for v in vals]

        cmd = f"ARM:({','.join(map(str, vals))})"
        serial.send_command(cmd)

        # Update value labels
        for i, (slider, label) in enumerate(self.sliders):
            label.setText(str(slider.value()))

    def toggle_gripper(self):
        if self.capture_btn.isChecked():
            self.capture_btn.setText("RELEASE")
            self.capture_btn.setStyleSheet(self.capture_btn.styleSheet().replace("#ff4b1f", "#34a734"))
        else:
            self.capture_btn.setText("CAPTURE")
            self.capture_btn.setStyleSheet(self.capture_btn.styleSheet().replace("#34a734", "#ff4b1f"))
            
        self.update_arm()  # Send new gripper state immediately