import random
import re
import ssl
from secret import EmailPassword
from email.message import EmailMessage
from flask import Flask, jsonify, abort
import smtplib

app = Flask(__name__, )


def send_email(to_email, message, email_subject):
    sender_email = "islamdoodoo@gmail.com"
    email_password = EmailPassword
    smtp_port = 587
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    server = smtplib.SMTP(smtp_server, smtp_port)
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = email_subject
    msg.set_content(message)
    try:
        server.starttls(context=context)
        server.login(sender_email, email_password)
        server.sendmail(sender_email, to_email, msg.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()


def is_valid_email(email_):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, str(email_))
    return bool(match)


def generate_random_code():
    random_int = random.randint(100000, 999999)
    random_int_str = '{:06d}'.format(random_int)
    return random_int_str


# the email code will be set in place of "___code___"
@app.route('/email_verification/<toemail>/<email_message>/<email_subject>')
def email_conformation(toemail, email_message, email_subject):
    code = generate_random_code()
    if is_valid_email(toemail):
        message = str(email_message).replace("___code___", code)
        send_email(to_email=toemail, message=message, email_subject=email_subject)
        return jsonify(code)
    else:
        abort(code=500)


app.run(host="0.0.0.0", port=8080)
