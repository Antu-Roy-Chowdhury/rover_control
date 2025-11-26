# main_gui.py
import tkinter as tk
import serial
import math
from video_feed import VideoFeed
import torch

# ---------------- SERIAL SETUP -----------------
SERIAL_PORT = "/dev/ttyUSB0"  # change to your Arduino port
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print("Arduino connected")
except:
    arduino = None
    print("Arduino NOT connected")

def send(cmd):
    print("SEND:", cmd)
    if arduino:
        arduino.write(cmd.encode())

# ---------------- MAIN WINDOW -----------------
root = tk.Tk()
root.title("Rover Control Panel")
root.geometry("800x550")
root.configure(bg="#1e1e1e")

title = tk.Label(root, text="LOOP ROVER CONTROL PANEL",
                 font=("Arial", 16, "bold"), fg="white", bg="#1e1e1e")
title.pack(pady=5)

# ---------------- MODE SWITCH -----------------
mode = tk.StringVar(value="ARROW")

def set_mode_arrow():
    mode.set("ARROW")
    mode_label.config(text="MODE: ARROW (F/B/L/R)", fg="#00d4ff")

def set_mode_360():
    mode.set("360")
    mode_label.config(text="MODE: 360° VECTOR", fg="#00ff88")

mode_frame = tk.Frame(root, bg="#1e1e1e")
mode_frame.pack(pady=5)

tk.Button(mode_frame, text="Arrow Mode", command=set_mode_arrow,
          font=("Arial", 12), width=12).grid(row=0, column=0, padx=10)
tk.Button(mode_frame, text="360 Mode", command=set_mode_360,
          font=("Arial", 12), width=12).grid(row=0, column=1, padx=10)

mode_label = tk.Label(root, text="MODE: ARROW (F/B/L/R)",
                      font=("Arial", 12), fg="#00d4ff", bg="#1e1e1e")
mode_label.pack(pady=3)

# ---------------- JOYSTICK CANVAS -----------------
canvas = tk.Canvas(root, width=350, height=350, bg="#222", highlightthickness=0)
canvas.pack(side="left", padx=10, pady=10)

canvas.create_oval(50, 50, 300, 300, outline="#555", width=5)
center_x, center_y = 175, 175
radius = 100
knob = canvas.create_oval(center_x-25, center_y-25, center_x+25, center_y+25, fill="#00ff66", outline="")

last_cmd = "S"

# Speed slider
speed_var = tk.IntVar(value=255)
speed_label = tk.Label(root, text="Speed:", font=("Arial", 12), fg="white", bg="#1e1e1e")
speed_label.pack()
speed_slider = tk.Scale(root, from_=50, to=255, orient=tk.HORIZONTAL, variable=speed_var,
                        bg="#1e1e1e", fg="white", troughcolor="#555", width=15)
speed_slider.pack(pady=5)

# ---------------- JOYSTICK LOGIC -----------------
def move_knob(event):
    global last_cmd
    dx = event.x - center_x
    dy = event.y - center_y
    distance = math.sqrt(dx*dx + dy*dy)
    if distance > radius:
        angle = math.atan2(dy, dx)
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)

    canvas.coords(knob, center_x + dx - 25, center_y + dy - 25,
                         center_x + dx + 25, center_y + dy + 25)

    if distance < 20:
        if last_cmd != "S":
            send("S")
            last_cmd = "S"
        return

    if mode.get() == "ARROW":
        if abs(dx) > abs(dy):
            cmd = "R" if dx > 0 else "L"
        else:
            cmd = "B" if dy > 0 else "F"
        if cmd != last_cmd:
            send(cmd)
            last_cmd = cmd
    else:
        angle_deg = int((math.degrees(math.atan2(-dy, dx)) + 360) % 360)
        speed = speed_var.get()
        packet = f"<{angle_deg},{speed}>"
        if packet != last_cmd:
            send(packet)
            last_cmd = packet

def reset_knob(event):
    global last_cmd
    canvas.coords(knob, center_x-25, center_y-25,
                         center_x+25, center_y+25)
    send("S")
    last_cmd = "S"

canvas.bind("<B1-Motion>", move_knob)
canvas.bind("<ButtonRelease-1>", reset_knob)

# ---------------- KEYBOARD CONTROL -----------------
def key_press(event):
    global last_cmd
    key = event.keysym
    mapping = {
        "w": "F", "W": "F",
        "s": "B", "S": "B",
        "a": "L", "A": "L",
        "d": "R", "D": "R",
        "Up": "F",
        "Down": "B",
        "Left": "L",
        "Right": "R",
        "space": "S"
    }
    if key in mapping:
        cmd = mapping[key]
        if cmd != last_cmd:
            send(cmd)
            last_cmd = cmd

root.bind("<KeyPress>", key_press)

# ---------------- VIDEO FEED WITH YOLO -----------------
video_frame = tk.Frame(root, bg="#111")
video_frame.pack(side="right", padx=10)
video_label = tk.Label(video_frame)
video_label.pack()

yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
cam = VideoFeed(source=0, yolo_model=yolo_model)

def update_video_gui():
    cam.read_frame()
    img = cam.process_frame()
    if img:
        video_label.imgtk = img
        video_label.configure(image=img)
    root.after(30, update_video_gui)

root.after(0, update_video_gui)

# ---------------- R
