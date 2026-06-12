
from pynput import keyboard, mouse
from PIL import ImageGrab
import socket

def Client_connection():
    server = socket.socket()
    server.bind(("0.0.0.0", 9999))
    server.listen(1)
    print("Waiting for connection...")
    conn, addr = server.accept()
    print("Connected from: ", addr)

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

    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()
    
    with keyboard.Listener(on_press= on_press):
        listener.join()

if __name__ == "__main__":
    Client_connection()
