import cv2
import socket

cap = cv2.VideoCapture(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 12346))
s.listen(1)

conn, addr = s.accept()
print('Connection from:', addr)

while True:
    ret, frame = cap.read()
    data = cv2.imencode('.jpg', frame)[1].tostring()
    conn.sendall(data)

conn.close()
cap.release()

