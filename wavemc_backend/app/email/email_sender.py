import smtplib as sm
import ssl
from email.message import EmailMessage
from decouple import config
from aiosmtplib import send

SMTP = config("SMTP")
SMTP_PORT = config("SMTP_PORT")
EMAIL = config("EMAIL")
EMAIL_NAME = config("EMAIL_NAME")
EMAIL_PWD = config("EMAIL_PWD")


async def send_email(user_email: str, subject: str, message: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"{EMAIL_NAME} <{EMAIL}>"
    msg['To'] = f"Customer <{user_email}>"
    msg.set_content(message, subtype='html')

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
 
    try:
        await send(
            msg,
            hostname=SMTP,
            port=SMTP_PORT,
            username=EMAIL,
            password=EMAIL_PWD,
            use_tls=True,
            tls_context=context,
        )
        return "The email was sent."
    except Exception as e:
        print(e)
        return None
