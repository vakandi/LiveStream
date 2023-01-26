import subprocess
import cv2
import pyaudio
import numpy as np
from threading import Thread
from flask import Flask, render_template, Response, request

# Start PHP server on port 8055
subprocess.call(["php", "-S", "localhost:8055"])

app = Flask(__name__)

cap = cv2.VideoCapture(0)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

@app.route('/livestream')
def index():
    return render_template('index.html')

def webcam_stream():
    global cap
    while True:
        ret, frame = cap.read()
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def microphone_stream():
    global stream
    while True:
        data = stream.read(1024)
        yield data

@app.route('/video_feed')
def video_feed():
    if request.args.get('state') == 'on':
        return Response(webcam_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response(status=204)

@app.route('/audio_feed')
def audio_feed():
    if request.args.get('state') == 'on':
        return Response(microphone_stream(), mimetype='audio/x-wav')
    else:
        return Response(status=204)

if __name__ == '__main__':
    app.run(host='localhost',port=8055)

