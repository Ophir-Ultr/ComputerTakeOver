from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import pyautogui
import socket
import io
import struct
def Get_server_ip():
    return input("Enter the server's ip: ")

def server_connection():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = Get_server_ip()
    while True:
        try:
            client.connect((ip, 9999))
            break
        except ConnectionError:
            ip = Get_server_ip()

    keyboard = KeyboardController()
    mouse = MouseController()
    target_width, target_height = pyautogui.size()
    while True:
        image_bytes = get_image_in_bytes()
        size = len(image_bytes)
        client.sendall(struct.pack(">L", size))
        client.sendall(image_bytes)
        data = client.recv(1024).decode() 
        for action in data.split("\n"):
            if action:
                parts = action.split(",")
                if parts[0]== "key":
                    keyboard.press(parts[1])
                    keyboard.release(parts[1])
                elif parts[0] == "move":
                    real_x = float(parts[1]) * target_width
                    real_y = float(parts[2]) * target_height
                    mouse.position = (int(real_x), int(real_y))
                elif parts[0] == "click":
                    real_x = float(parts[1]) * target_width
                    real_y = float(parts[2]) * target_height
                    mouse.position = (int(real_x), int(real_y))
                    button = Button.left if parts[3] == "Button.left" else Button.right
                    mouse.press(button)
                    mouse.release(button)
                elif parts[0] == "scroll":
                    mouse.scroll(int(parts[3]), int(parts[4]))

def get_image_in_bytes():
    screen_shot = pyautogui.screenshot()
    buffer = io.BytesIO()
    screen_shot.save(buffer, 'JPEG')
    image_bytes = buffer.getvalue()
    return image_bytes
    

if __name__ == "__main__":
    server_connection()