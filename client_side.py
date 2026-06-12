from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from PIL import ImageGrab
import socket
import io
def Get_server_ip():
    return input("Enter the server's ip: ")

def server_connection():
    client = socket.socket()
    ip = Get_server_ip()
    while True:
        try:
            client.connect((ip, 9999))
            break
        except ConnectionError:
            ip = Get_server_ip()

    keyboard = KeyboardController()
    mouse = MouseController()
    while True:
        image_bytes = get_image_in_bytes()
        size = len(image_bytes)
        client.send(size.to_bytes(4, 'big'))
        client.send(image_bytes)
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

def get_image_in_bytes():
    screen_shot = ImageGrab.grab()
    buffer = io.BytesIO()
    screen_shot.save(buffer, 'PNG')
    image_bytes = buffer.getvalue()
    return image_bytes

if __name__ == "__main__":
    server_connection()