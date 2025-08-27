########## Modules ##########
import asyncio

from aiosmtplib import SMTP

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.config import settings

from services.smtp.temps import template_routes, get_html
from services.smtp.credentials import credentials

########## Queue ##########
email_queue = asyncio.Queue()

########## Send email worker ##########
async def send_mail_worker():
    while True:
        email_data = await email_queue.get()

        email_user = credentials[email_data["type"]]["email"]
        email_pass = credentials[email_data["type"]]["pass"]

        msg = MIMEMultipart("alternative")
        msg["Subject"] = email_data["subject"]
        msg["From"] = email_user
        msg["To"] = email_data["to_email"]
        msg.attach(MIMEText(email_data["html"], "html"))

        try:
            smtp = SMTP(hostname=settings.EMAIL_HOST, port=settings.EMAIL_PORT, start_tls=True)
            await smtp.connect()
            await smtp.login(email_user, email_pass)
            await smtp.send_message(msg)
        except Exception as e:
            print(e)
        finally:
            await smtp.quit()


########## New email ##########
async def send_mail(type: str, subject: str, to_email: str, html: str):
    await email_queue.put({
        "type": type,
        "subject": subject,
        "to_email": to_email,
        "html": html
    })
