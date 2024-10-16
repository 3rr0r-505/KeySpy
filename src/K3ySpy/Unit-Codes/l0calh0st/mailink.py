import smtplib
from email.mime.text import MIMEText
import requests

def get_flask_link():
    try:
        ngrok_url = requests.get('http://localhost:4040/api/tunnels').json()['tunnels'][0]['public_url']
        return ngrok_url
    except Exception as e:
        print("Error getting Flask link:", e)
        return None

def send_email(receiver_email, link):
    sender_email = "<fake@mail.com>"  # Replace with your email address
    sender_password = "<FakePassword>"  # Replace with your email password

    msg = MIMEText(f"Link to Flask application: {link}")
    msg['Subject'] = "Flask Application Link"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

if __name__ == '__main__':
    flask_link = get_flask_link()
    if flask_link:
        receiver_email = "<getmail@mail.com>"  # Replace with recipient's email address
        send_email(receiver_email, flask_link)
    else:
        print("Flask link not available.")
