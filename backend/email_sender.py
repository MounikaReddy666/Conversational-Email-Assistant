
#smtp automation

import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def send_email_smtp(email_content):
    sender_email = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        raise Exception("Missing sender email or app password.")

    # Parse email content
    lines = email_content.split('\n')
    to_line = next((line for line in lines if line.startswith("To: ")), None)
    subject_line = next((line for line in lines if line.startswith("Subject: ")), None)
    body = '\n'.join(lines[2:]).strip() if len(lines) > 2 else "No body provided."

    if not to_line or not subject_line:
        raise Exception("Invalid email format: Missing To or Subject.")

    recipient_email = to_line.replace("To: ", "").strip()
    subject = subject_line.replace("Subject: ", "").strip()

    msg = MIMEText(body)
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"\u2705 Email sent to {recipient_email}")
        return True, [f"mock_screenshot_{datetime.now().strftime('%H%M%S')}.png"]
    except Exception as e:
        print(f"\u274C Failed to send email: {str(e)}")
        return False, []