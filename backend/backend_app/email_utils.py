import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_email(to_email: str, subject: str, html_body: str):
    print("=== EMAIL DEBUG START ===")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body preview: {html_body[:150]}...")
    print("=== EMAIL DEBUG END ===")
    return True

  