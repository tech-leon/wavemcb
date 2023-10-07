from decouple import config
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

SMTP = config("SMTP")
SMTP_PORT = config("SMTP_PORT")
EMAIL = config("EMAIL")
# EMAIL_NAME = config("EMAIL_NAME")
EMAIL_PWD = config("EMAIL_PWD")

conf = ConnectionConfig(
    MAIL_USERNAME =EMAIL,
    MAIL_PASSWORD = EMAIL_PWD,
    MAIL_FROM = EMAIL,
    MAIL_PORT = SMTP_PORT,
    MAIL_SERVER = SMTP,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def connect_smtp(user_email:str, subject: str, message: str):
    
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=user_email,
        body=message,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})    
    
    
    # msg = EmailMessage()
    # msg['Subject'] = subject
    # msg['From'] = f"{EMAIL_NAME} <{EMAIL}>"
    # msg['To'] = f"Customer <{user_email}>"
    # msg.set_content(message)
    
    # # Create a secure SSL context
    # context = ssl.create_default_context()
    
    # try:
    #     with sm.SMTP(SMTP) as server:
    #         # server.ehlo()
    #         server.starttls()
    #         # server.ehlo()
    #         server.login(user=EMAIL, password=EMAIL_PWD)
    #         server.sendmail(
    #             from_addr=f"{EMAIL_NAME} <{EMAIL}>",
    #             to_addrs=[user_email],
    #             msg=str(msg)
    #         )
    # except Execption as e:
    #     print(e)
    #     return e
    # finally:
    #     return msg






# import smtplib as sm
# import ssl
# from email.message import EmailMessage
# from decouple import config


# SMTP = config("SMTP")
# SMTP_PORT = config("SMTP_PORT")
# EMAIL = config("EMAIL")
# EMAIL_NAME = config("EMAIL_NAME")
# EMAIL_PWD = config("EMAIL_PWD")

# def connect_smtp(user_email, subject, message):
    
#     msg = EmailMessage()
#     msg['Subject'] = subject
#     msg['From'] = f"{EMAIL_NAME} <{EMAIL}>"
#     msg['To'] = f"Customer <{user_email}>"
#     msg.set_content(message)
    
#     # Create a secure SSL context
#     context = ssl.create_default_context()
    
#     try:
#         with sm.SMTP(SMTP) as server:
#             # server.ehlo()
#             server.starttls()
#             # server.ehlo()
#             server.login(user=EMAIL, password=EMAIL_PWD)
#             server.sendmail(
#                 from_addr=f"{EMAIL_NAME} <{EMAIL}>",
#                 to_addrs=[user_email],
#                 msg=str(msg)
#             )
#     except Execption as e:
#         print(e)
#         return e
#     finally:
#         return msg

