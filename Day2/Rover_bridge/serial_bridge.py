import serial
import time

SRC = "/dev/ttyUSB0"    # ESP-B (LoRa RX)
DST = "/dev/ttyUSB1"    # ESP-C (Motor controller)

baud = 115200

ser_in = serial.Serial(SRC, baud, timeout=0.1)
ser_out = serial.Serial(DST, baud, timeout=0.1)

print("LoRa RX -> Motor Bridge Active")

while True:
    try:
        line = ser_in.readline().decode().strip()
        if line:
            print("RX:", line)
            ser_out.write((line + "\n").encode())
            ser_out.flush()
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
