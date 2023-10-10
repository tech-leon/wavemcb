import os
from bs4 import BeautifulSoup

from .email_sender import send_email


RESET_HTML_MEG = BeautifulSoup(open(os.getenv("RESET_HTML_MEG")),"html.parser")

async def send(user_email: str, reset_token: str):
    link = "https://wavemocards.com/resetPassword" \
           "?reset_token={0:}&email={1:}".format(reset_token, user_email)
    RESET_HTML_MEG.a['href'] = link
    subject = "Reset forgotten Wavemocards account password"
    
    # Attempt to send the email
    result = await send_email(user_email, subject, str(RESET_HTML_MEG))
    
    if result is not None:
        # Email sent successfully
        return "Email sent successfully"
    else:
        # Handle the error here, e.g., return an error message
        return "Email sending failed"
