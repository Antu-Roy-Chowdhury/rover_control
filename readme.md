# Rover Control Panel (Ubuntu)

## Features
- Joystick (Arrow / 360° modes)
- Keyboard control (WASD / Arrows)
- Optional speed slider
- USB webcam live feed
- YOLO object detection on video feed
- Robot stops automatically when idle

## Setup

1. Install Python3 & Tkinter:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```
2. 
```bash
pip install -r requirements.txt
python3 main_gui.py
```

```bash
sudo apt install python3-venv python3-dev

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

deactivate

```