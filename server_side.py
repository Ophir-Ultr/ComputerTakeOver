
from pynput import keyboard, mouse
from PIL import Image
import socket
import io
import threading
def client_connection():
    server = socket.socket()
    server.bind(("0.0.0.0", 9999))
    server.listen(1)
    print("Waiting for connection...")
    conn, addr = server.accept()
    print("Connected from: ", addr)
    def receive_screen():
        while True:
            size = int.from_bytes(conn.recv(4), 'big')
            data = b""
            while len(data) < size:
                data += conn.recv(65536)
            image = Image.open(io.BytesIO(data))
            image.show()

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
        keyboard.Listener(on_press=on_press).join()
    
    def run_mouse():
        mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll).join()
    
    screen_thread = threading.Thread(target=receive_screen)
    k_thread = threading.Thread(target=run_keyboard)
    m_thread = threading.Thread(target=run_mouse)
    screen_thread.start()
    k_thread.start()
    m_thread.start()

if __name__ == "__main__":
    client_connection()
