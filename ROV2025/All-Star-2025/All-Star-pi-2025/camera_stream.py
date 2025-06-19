import cv2
import socket
import pickle
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8485))  # Listen on all interfaces, port 8485
server_socket.listen(1)
print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected to: {addr}")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Compress frame as JPEG
    ret, buffer = cv2.imencode('.jpg', frame)
    data = pickle.dumps(buffer)
    size = struct.pack("!I", len(data))

    try:
        conn.sendall(size + data)
    except:
        break

cap.release()
conn.close()
