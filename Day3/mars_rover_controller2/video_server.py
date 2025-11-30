# video_server.py
from flask import Flask, Response
import cv2

app = Flask(__name__)

front = cv2.VideoCapture(0)
back = cv2.VideoCapture(1)

def gen(cam):
    while True:
        ret, frame = cam.read()
        if not ret:
            continue
        ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video/front')
def front_feed(): return Response(gen(front), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video/back')
def back_feed(): return Response(gen(back), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)