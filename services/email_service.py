import os
import smtplib
from email.message import EmailMessage

import streamlit as st


def _setting(name, default=""):
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except Exception:
        return os.getenv(name, default)


def send_email_report(
    recipients,
    subject,
    body,
    attachment_bytes=None,
    attachment_filename=None,
    attachment_mime="application/pdf"
):
    smtp_host = _setting("SMTP_HOST")
    smtp_port = int(_setting("SMTP_PORT", "587"))
    smtp_username = _setting("SMTP_USERNAME")
    smtp_password = _setting("SMTP_PASSWORD")
    email_from = _setting("EMAIL_FROM", smtp_username)

    if not smtp_host or not smtp_username or not smtp_password:
        raise ValueError("SMTP email settings are missing. Check .streamlit/secrets.toml.")

    if isinstance(recipients, str):
        recipients = [
            email.strip()
            for email in recipients.replace("\n", ",").split(",")
            if email.strip()
        ]

    if not recipients:
        raise ValueError("No recipient email address provided.")

    msg = EmailMessage()
    msg["From"] = email_from
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment_bytes and attachment_filename:
        maintype, subtype = attachment_mime.split("/", 1)

        msg.add_attachment(
            attachment_bytes,
            maintype=maintype,
            subtype=subtype,
            filename=attachment_filename
        )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

    return True