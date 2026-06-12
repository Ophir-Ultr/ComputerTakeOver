from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from PIL import ImageGrab
import socket

def Server_connection():
    client = socket.socket()
    client.connect(("127.0.0.1", 9999))
    keyboard = KeyboardController()
    mouse = MouseController()
    while True:
        data = client.recv(1024).decode()
        for action in data.split("\n"):
            if action:
                parts = action.split(",")
                if parts[0]== "key":
                    keyboard.press(parts[1])
                    keyboard.release(parts[1])
                elif parts[0] == "move":
                    mouse.position = (int(parts[1]), int(parts[2]))
                elif parts[0] == "click":
                    button = Button.left if parts[3] == "Button.left" else Button.right
                    mouse.press(button)
                    mouse.release(button)
                elif parts[0] == "scroll":
                    mouse.scroll(int(parts[3]), int(parts[4]))

if __name__ == "__main__":
    Server_connection()