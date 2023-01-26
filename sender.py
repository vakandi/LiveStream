import pyaudio
import socket
import daemon

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 12345))
s.listen(1)

conn, addr = s.accept()
print('Connection from:', addr)

with daemon.DaemonContext():
    while True:
        data = stream.read(CHUNK)
        conn.sendall(data)

conn.close()
stream.stop_stream()
stream.close()
p.terminate()


