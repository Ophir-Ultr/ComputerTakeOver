from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import pyautogui
import socket
import io
import struct
import threading
import time
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
    def send_screen():
        while True:
            try: 
                image_bytes = get_image_in_bytes()
                size = len(image_bytes)
                client.sendall(struct.pack(">L", size))
                client.sendall(image_bytes)
                time.sleep(0.05)
            except  Exception as e:
                print(f"Error sending: {e}")
                break
    def receive_commands():
        while True:
            try:
                size_data = recvall(client, 4)
                if not size_data:
                    print("Disconnected before size")
                    break
                size = struct.unpack(">L", size_data)[0]
                data = b""
                data = recvall(client,size)
                action = data.decode()
                if action:
                        try:
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
                                if parts[4] == "True":
                                    mouse.press(button)
                                else:
                                    mouse.release(button)
                            elif parts[0] == "scroll":
                                mouse.scroll(float(parts[3]), float(parts[4]))
                        except Exception as e:
                            print(f"Error: {e}, action: {action}")
                            continue
            except Exception as e:
                print(f"Error recieving: {e}")
                break
    send_thread = threading.Thread(target=send_screen)
    recv_thread = threading.Thread(target=receive_commands)
    send_thread.start()
    recv_thread.start()

def get_image_in_bytes():
    screen_shot = pyautogui.screenshot()
    buffer = io.BytesIO()
    screen_shot.save(buffer, 'JPEG')
    image_bytes = buffer.getvalue()
    return image_bytes

def recvall(sock, size):
    data = b""
    while len(data) < size:
       packet = sock.recv(size - len(data))
       if not packet:
           return None
       data+= packet
    return data
    

if __name__ == "__main__":
    server_connection()