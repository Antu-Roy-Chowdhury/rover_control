# serial_handler.py ← FINAL BULLETPROOF VERSION
import serial
import serial.tools.list_ports
from datetime import datetime

# Global serial object
ser = None

def auto_detect_arduino():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        desc = p.description.lower()
        if any(k in desc for k in ["arduino", "ch340", "cp210x","esp", "usb serial", "usb-serial"]):
            return p.device
    return None

# Try to connect ONCE at startup
port = auto_detect_arduino()
if port:
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Arduino AUTO DETECTED & CONNECTED on {port}")
    except Exception as e:
        print(f"Arduino found but failed to connect: {e}")
        ser = None
else:
    print("No Arduino detected → Commands will print only")

def send_command(cmd: str):
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Pretty print
    if cmd.startswith("ARM:("):
        print(f"[{timestamp}] ARM 6DOF → {cmd[4:]}")
    elif ":" in cmd:
        parts = cmd.split(":", 1)
        direction = parts[0]
        speed = parts[1] if len(parts) > 1 else "0"
        arrows = {
            "F": "Forward", "B": "Backward", "L": "Left", "R": "Right",
            "RF": "Right-Forward", "LF": "Left-Forward",
            "RB": "Right-Backward", "LB": "Left-Backward", "STOP": "STOP"
        }
        print(f"[{timestamp}] Motor → {arrows.get(direction, direction):15} | Speed: {speed:>3}")
    else:
        print(f"[{timestamp}] → {cmd}")

    # Send to Arduino if connected
    global ser
    if ser and ser.is_open:
        try:
            ser.write((cmd + "\n").encode())
            ser.flush()
        except:
            print("Serial disconnected!")
            ser = None