import cv2
import socket
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 12346))

while True:
    data = b''
    while len(data) < 4:
        packet = s.recv(4 - len(data))
        if not packet:
            break
        data += packet
    size = int.from_bytes(data, byteorder='big')
    data = b''
    while len(data) < size:
        packet = s.recv(size - len(data))
        if not packet:
            break
        data += packet
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow('Video', img)
    if cv2.waitKey(1) == ord('q'):
        break

s.close()
cv2.destroyAllWindows()

