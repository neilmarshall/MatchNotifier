import os
import smtplib
from email.message import EmailMessage


def send_email(subject, body, recipient):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = recipient

    email_account_address = os.environ["EmailAccountAddress"]
    msg["from"] = email_account_address
    email_account_password = os.environ["EmailAccountPassword"]

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_account_address, email_account_password)

    server.send_message(msg)

    server.quit()


