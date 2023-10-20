import os
import re
from bs4 import BeautifulSoup as soup

from .email_sender import send_email


RESET_HTML_MEG = soup(open(os.getenv("RESET_HTML_MEG")),"html.parser")
USERNAME_HTML_MEG = soup(open(os.getenv("USERNAME_HTML_MEG")),"html.parser")


async def send_reset_pwd(user_email: str, reset_token: str):
    link = "https://wavemocards.com/resetPassword" \
           "?reset_token={0:}&email={1:}".format(reset_token, user_email)
    RESET_HTML_MEG.a['href'] = link
    subject = "Reset forgotten Wave Emotion Cards account password"
    
    # Attempt to send the email
    result = await send_email(user_email, subject, str(RESET_HTML_MEG))
    
    if result is not None:
        # Email sent successfully
        return "Email sent successfully"
    else:
        # Handle the error here, e.g., return an error message
        return "Email sending failed"


async def send_user_name(user_name: str, user_email: str):
    # Find the specific <p> tag and change its text
    target_tag = USERNAME_HTML_MEG.find('p', id='username')
    target_tag.string = f"This is your Wave Emotion Cards username: {user_name}"
    
    subject = "The user name of Wave Emotion Cards"
    
    result = await send_email(user_email, subject, str(USERNAME_HTML_MEG))

    if result is not None:
        # Email sent successfully
        return "Email sent successfully"
    else:
        # Handle the error here, e.g., return an error message
        return "Email sending failed"
