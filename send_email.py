import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

load_dotenv()
def send_email_notification(subject, body, attachments=[]):
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_RECEIVER")

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = receiver
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    for file_path in attachments:
        part = MIMEBase('application', 'octet-stream')
        with open(file_path, 'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        msg.attach(part)

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your SMTP server
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {receiver}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
