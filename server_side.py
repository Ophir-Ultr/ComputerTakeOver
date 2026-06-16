
from pynput import keyboard, mouse
from PIL import Image
import socket
import io
import threading
import cv2
import struct
import numpy
def client_connection():
    server = socket.socket()
    server.bind(("0.0.0.0", 9999))
    server.listen(1)
    print("Waiting for connection...")
    conn, addr = server.accept()
    print("Connected from: ", addr)
    def receive_screen():
        while True:
            data = b""
            while len(data) < 4:

                data += conn.recv(4)
            size = struct.unpack(">L", data)[0]
            data = b""
            while len(data) < size:
                data += conn.recv(size)
            frame = cv2.imdecode(numpy.frombuffer(data, numpy.uint8), cv2.IMREAD_COLOR)
            cv2.imshow("screen", frame)
            cv2.waitKey(1)
            conn.send("\n".encode())

        

    def on_press(key):
        try:    
            conn.send(f"key,{key.char}\n".encode())
        except AttributeError:
            pass
 
    def on_move(x, y):
        try:
            conn.send(f"move,{x},{y}\n".encode())
        except AttributeError:
            pass

    def on_click(x, y, button, pressed):
        conn.send(f"click,{x},{y},{button},{pressed}\n".encode())

    def on_scroll(x, y, dx, dy):
        conn.send(f"scroll,{x},{y},{dx},{dy}\n".encode())

    def run_keyboard():
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    
    def run_mouse():
        with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
            listener.join()
    
    screen_thread = threading.Thread(target=receive_screen)
    k_thread = threading.Thread(target=run_keyboard)
    m_thread = threading.Thread(target=run_mouse)
    screen_thread.start()
    k_thread.start()
    m_thread.start()

if __name__ == "__main__":
    client_connection()
