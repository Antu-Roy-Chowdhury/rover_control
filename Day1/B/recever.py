import os
os.environ["QT_QPA_PLATFORM"] = "xcb"   # <--- FIX GUI CRASH

import cv2
import socket
import pickle
import struct

host_ip = "0.0.0.0"
port = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host_ip, port))
server_socket.listen(5)

print("Waiting for connection...")
conn, addr = server_socket.accept()
print("Connected:", addr)

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = conn.recv(4096)
        if not packet:
            print("No data received, exiting.")
            break
        data += packet

    if len(data) < payload_size:
        break

    print("Header received")  # DEBUG
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    print("Message size:", msg_size)  # DEBUG

    while len(data) < msg_size:
        packet = conn.recv(4096)
        if not packet:
            print("No frame data, exiting.")
            break
        data += packet

    frame_data = data[:msg_size]
    data = data[msg_size:]
    print("Frame received")  # DEBUG

    frame = pickle.loads(frame_data)
    cv2.imshow("Streaming", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

conn.close()
cv2.destroyAllWindows()
print("Connection closed")
