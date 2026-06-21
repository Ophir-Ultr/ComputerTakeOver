
from pynput import keyboard, mouse
from PIL import Image
import socket
import io
import pyautogui
import threading
import cv2
import struct
import numpy
import time
def client_connection():
    server = socket.socket()
    server.bind(("0.0.0.0", 9999))
    server.listen(1)
    print("Waiting for connection...")
    conn, addr = server.accept()
    print("Connected from: ", addr)
    send_lock = threading.Lock()
    def receive_screen():
        cv2.namedWindow("screen", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            try:
                data = b""
                while len(data) < 4:

                    data += conn.recv(4)
                size = struct.unpack(">L", data)[0]
                data = b""
                while len(data) < size:
                    data += conn.recv(size - len(data))
                frame = cv2.imdecode(numpy.frombuffer(data, numpy.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow("screen", frame)
                cv2.waitKey(1)
            except Exception as e:
                print(f"Error in on_move: {e}")
            
    ctrl_width, ctrl_height = pyautogui.size()    

    def on_press(key):
        try:    
            command = (f"key,{key.char}".encode())
            print("sending:", command)
            with send_lock:
                conn.sendall(struct.pack(">L", len(command)))
                conn.sendall(command)
        except AttributeError:
            pass
 
    def on_move(x, y):
        try:
            rel_x = x / ctrl_width
            rel_y = y / ctrl_height
            command  = (f"move,{rel_x},{rel_y}".encode())
            print("sending:", command)
            with send_lock:
                conn.sendall(struct.pack(">L", len(command)))
                conn.sendall(command)
            time.sleep(0.01)
        except AttributeError:
            pass
        except Exception as e:
            print(f"Error in on_move: {e}")

    def on_click(x, y, button, pressed):
        rel_x = x / ctrl_width
        rel_y = y / ctrl_height
        command = (f"click,{rel_x},{rel_y},{button},{pressed}".encode())
        print("sending:", command)
        with send_lock:
            conn.sendall(struct.pack(">L", len(command)))
            conn.sendall(command)

    def on_scroll(x, y, dx, dy):
        command = (f"scroll,{x},{y},{dx},{dy}".encode())
        print("sending:", command)
        with send_lock:
            conn.sendall(struct.pack(">L", len(command)))
            conn.sendall(command)

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
