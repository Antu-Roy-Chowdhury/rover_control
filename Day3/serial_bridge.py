#!/usr/bin/env python3
import serial
import time
import re

# CHANGE THESE TWO LINES ONLY
RECEIVER_PORT = '/dev/ttyUSB0'   # LoRa ESP32
MOTOR_PORT    = '/dev/ttyUSB1'   # Motor ESP32

BAUD = 115200

print("Starting LoRa → Motor bridge...")
print(f"LoRa receiver  → {RECEIVER_PORT}")
print(f"Motor driver   → {MOTOR_PORT}")
print("Press Ctrl+C to stop\n")

# Open both ports
lora_ser = serial.Serial(RECEIVER_PORT, BAUD, timeout=1)
motor_ser = serial.Serial(MOTOR_PORT, BAUD, timeout=0)  # non-blocking for motor

time.sleep(2)  # wait for ESP32 reset message

# Pattern to catch "Raw: LF:60" or "Raw: f:150 etc.
pattern = re.compile(r'Raw:\s*([A-Za-z]+):(\d+)', re.IGNORECASE)

while True:
    try:
        if lora_ser.in_waiting:
            line = lora_ser.readline().decode('utf-8', errors='ignore').strip()
            if "Raw:" in line:
                print(f"Received ← {line}")

                match = pattern.search(line)
                if match:
                    dir_part = match.group(1).strip().lower()
                    speed = match.group(2).strip()

                    # Convert full words to short (optional, your code already supports both)
                    dir_map = {
                        'forward': 'f', 'f': 'f',
                        'backward': 'b', 'b': 'b',
                        'left': 'l', 'l': 'l',
                        'right': 'r', 'r': 'r',
                        'lf': 'lf', 'rf': 'rf', 'lb': 'lb', 'rb': 'rb',
                        'stop': 'stop'
                    }
                    cmd = dir_map.get(dir_part, dir_part)
                    full_command = f"{cmd}:{speed}"

                    print(f"Sending → {full_command}")
                    motor_ser.write((full_command + "\n").encode())
                else:
                    # Fallback: send raw text after "Raw:"
                    if "Raw:" in line:
                        raw = line.split("Raw:", 1)[1].strip()
                        print(f"Sending raw → {raw}")
                        motor_ser.write((raw + "\n").encode())

    except KeyboardInterrupt:
        print("\nBridge stopped by user")
        break
    except Exception as e:
        print("Error:", e)
        time.sleep(1)

lora_ser.close()
motor_ser.close()