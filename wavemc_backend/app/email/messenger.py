# import random as rd
from .email_sender import connect_smtp

# def get_random_keys():
#     random_keys = []
#     for i in range(0, 4):
#         random_keys.append(rd.randint(0, 9))
#     return random_keys


# def forget_password(user_email: str, reset_token: str):
#     keys = get_random_keys()
#     subject = "Reset forgotten Wavemocards account password"        
#     message = f"""\
# Dear Customer,

# You have used the 'forgotten password' option to reset your \
# Wavemocards account password.
# Please use the following pin code on the Wavemocards forgotten \
# password page to reset your password.

# {keys[0]} {keys[1]} {keys[2]} {keys[3]}

# This pin code vaild for 15 mins and can be used only once.
# Yours sincerely
# Wavemocards
# ------
# Wavemocards will never send you an unsolicited email asking for 
# your password, credit card details or account information.
# """
#     # send_email.connect_smtp(user_email, subject, message)
    
#     return connect_smtp(
#                 user_email, 
#                 subject, 
#                 message)
    
def forgot_password(user_email: str, reset_token: str):
    subject = "Reset forgotten Wavemocards account password"        
    message = """\
    <!DOCTYPE html>
    <html>
    <title>Reset Password</title>
    <body>
    <div style="width:100%; front-family: monospase;">
        <h1>Hello, {0:}</h1>
        <a href="https://wavemocards.com/resetPassword?reset_token={1:}&email={0:}" style="box-sizing:border-box;>link</a>
        <p>If you didn't request this...</p>
    </div>
    </body>
    </html>
    """.format(user_email, reset_token)
    
    return connect_smtp(
                    user_email, 
                    subject, 
                    message)
    
def forget_user_name(user_email):
    pass
