import cv2
import numpy as np
import socket
import pickle
import struct
import pygame
import threading
import time

class CameraClient:
    def __init__(self, host='192.168.1.50', camera_number =0):
        port = 8485 + camera_number
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client_socket.connect((host, port))
        for _ in range(20):  # Try for ~10 seconds
            try:
                print(f"Attempting to connect to camera {camera_number}...")
                self.client_socket.connect((host, port))
                print(f"camera {camera_number} connected!")
                break
            except ConnectionRefusedError:
                time.sleep(0.5)
        else:
            raise ConnectionRefusedError(f"Could not connect to {host}:{port} after multiple attempts.")
        
        self.payload_size = struct.calcsize("!I")
        self.data = b""
        self.latest_surface = None
        self.running = True

        # Start frame receiving thread
        self.thread = threading.Thread(target=self._receive_frames, daemon=True)
        self.thread.start()

    def _receive_frames(self):
        while self.running:
            try:
                while len(self.data) < self.payload_size:
                    self.data += self.client_socket.recv(4096)

                packed_msg_size = self.data[:self.payload_size]
                self.data = self.data[self.payload_size:]
                msg_size = struct.unpack("!I", packed_msg_size)[0]

                while len(self.data) < msg_size:
                    self.data += self.client_socket.recv(4096)

                frame_data = self.data[:msg_size]
                self.data = self.data[msg_size:]

                frame = pickle.loads(frame_data)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = np.rot90(frame)  # Pygame expects (w,h) order
                self.latest_surface = pygame.surfarray.make_surface(frame)

            except Exception as e:
                print("Error receiving frame:", e)
                break

    def get_surface(self):
        return self.latest_surface

    def close(self):
        self.running = False
        self.client_socket.close()
