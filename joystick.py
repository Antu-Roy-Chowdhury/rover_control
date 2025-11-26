import tkinter as tk
import serial
import math

# ==== SERIAL SETUP ====
SERIAL_PORT = "COM4"     # Change to your Arduino port
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print("Arduino connected")
except:
    arduino = None
    print("Arduino NOT connected")


# ==== SEND COMMAND ====
def send_cmd(cmd):
    print("CMD:", cmd)
    if arduino:
        arduino.write(cmd.encode())


# ==== JOYSTICK WINDOW ====
root = tk.Tk()
root.title("LoRa Robot Joystick Controller")
root.geometry("400x500")
root.configure(bg="#222")

canvas = tk.Canvas(root, width=300, height=300, bg="#333", highlightthickness=0)
canvas.pack(pady=20)

# Draw outer circle (joystick area)
canvas.create_oval(50, 50, 250, 250, fill="#555", outline="#777", width=4)

# Center position
center_x, center_y = 150, 150

# Create joystick knob
knob = canvas.create_oval(130, 130, 170, 170, fill="#0f0")


# ==== JOYSTICK LOGIC ====
def move_knob(event):
    dx = event.x - center_x
    dy = event.y - center_y

    distance = math.sqrt(dx*dx + dy*dy)

    # Limit movement to radius
    if distance > 70:
        angle = math.atan2(dy, dx)
        dx = 70 * math.cos(angle)
        dy = 70 * math.sin(angle)

    canvas.coords(knob, center_x + dx - 20, center_y + dy - 20,
                         center_x + dx + 20, center_y + dy + 20)

    # Determine direction
    if abs(dx) < 20 and abs(dy) < 20:
        send_cmd("S")  # STOP
        return

    if abs(dx) > abs(dy):
        if dx > 0:
            send_cmd("R")
        else:
            send_cmd("L")
    else:
        if dy > 0:
            send_cmd("B")
        else:
            send_cmd("F")


def return_center(event):
    canvas.coords(knob, 130, 130, 170, 170)
    send_cmd("S")


# Bind movement
canvas.bind("<B1-Motion>", move_knob)
canvas.bind("<ButtonRelease-1>", return_center)


# ==== UI LABEL ====
label = tk.Label(root, text="Drag the joystick to control the robot",
                 bg="#222", fg="white", font=("Arial", 14))
label.pack()

root.mainloop()
