import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025

SENDER_ADDRESS = "donotreply@hms.com"


def send_email(to_address, subject, message):

    msg = MIMEMultipart()

    msg['From'] = SENDER_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)

    s.send_message(msg)

    s.quit()

    return True