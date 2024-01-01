import os
import uvicorn
from fastapi import FastAPI, Body, Depends, Request, Header
from pydantic import Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import json as js
from datetime import date

from .model import User_signup, User_login, Add_emotions, Update_emotions, User_checking, User_password, User_infomation, Reset_email_checking, Reset_password, Share_emotions
from .auth.auth_bearer import JWTBearer, One_time_JWTBearer
from .auth.auth_handler import signJWT, get_password_hash, verify_password, decodeJWT
from .auth.auth_reset import one_time_signJWT, one_time_decodeJWT
from .email import messenger
from .database import db


app = FastAPI(redoc_url=None)
# Define the origins that are allowed to access API 
origins = ["https://wavemocards.com",
           "https://www.wavemocards.com",
           "https://frontendtesting.wavemocards.com",]
# Add CORS middleware with the specified configuration.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# route handlers
# get emotions informations
@app.get("/emoinfo/{query}/", tags=["emotion informations"])
async def get_emotions(query: str):
    if query == "about":
        return db.about_emotions()
    if query == "cards":
        return db.emotion_cards()
    return {"error": "Something went wrong! Contact the server administrator."}

# signup
@app.post("/user/signup", tags=["user"])
async def create_user(user: User_signup):
    # replace with db call, making sure to hash the password first
    user.password = get_password_hash(user.password)
    if user.day_of_birth == "":
        user.day_of_birth = '0-0-0'
    result = db.register_new_user(user)
    if result == 1:
        return {"message": "The user was successfully registered."}
    if result == 0:
        return {"message": "The user exists."}
    return {"error": "Something went wrong! Contact the server administrator."}

# login
@app.post("/user/login", tags=["user"])
async def user_login(user: User_login): 
    if db.check_user(user.user_name)["user_name"] == True:
        hashed_password = db.get_user_hashed_password(user.user_name)
        if verify_password(user.password, hashed_password):
            user_info = db.get_user_info(user.user_name)
            user_token = signJWT(user.user_name)["access_token"]  # get access token
            return {"access_token": user_token, "user_info": user_info}
    return {"error": "Wrong login details!"}


# user update password
@app.put("/user/password", dependencies=[Depends(JWTBearer())], tags=["user"])
async def update_password(password: User_password, request: Request):
    user_auth = request.headers.get('Authorization')
    current_user = decodeJWT(user_auth[7:])
    hashed_password = db.get_user_hashed_password(current_user["user_name"])
    if not verify_password(password.current_password, hashed_password):
        return {"error": "Wrong password! Please try again."}
    if password.new_password != password.confirm_password:
        return {"error": "Please check your new passwords!"}
    if password.current_password == password.new_password:
        return {"error": \
            "The new password should not be the same as the current password!"}
    new_password_hashed = get_password_hash(password.new_password)
    db.update_user_password(current_user["user_name"], new_password_hashed)
    return { "message": "The password was successfully updated."}


# update user info
@app.put("/user/info", dependencies=[Depends(JWTBearer())], tags=["user"])
async def update_user_info(user_info: User_infomation, request: Request):
    user_auth = request.headers.get('Authorization')
    current_user = decodeJWT(user_auth[7:])
    result = db.update_user_info(current_user["user_name"], user_info)
    if result == 1:
        return { "message": "The info was successfully updated."}
    if result == 0:
        return {"message": "Nothing changed."}
    return {"error": "Something went wrong! Contact the server administrator."}


# user checking
@app.post("/user/checking", tags=["user"])
async def user_checking(check: User_checking):
    if check.user_name == None and check.email == None:
        return {"error": "One of the fields must be provided."}
    return {"message": db.check_user(check.user_name, check.email)}


# get user emo records
@app.get("/emotions", dependencies=[Depends(JWTBearer())], tags=["emotions"])
async def get_emotions(user_name: str = 'john2024'):
    result = db.get_user_emos(db.get_user_id(user_name))
    if result == False:
        return {"message": "No emotions were found."}
    return {"message": result}


# emo shares
@app.post("/emotions/share", dependencies=[Depends(JWTBearer())], tags=["emotions"])
async def share_emotions(share_emo: Share_emotions, request: Request):
    result = db.share_user_emo(share_emo)
    if result == 1:
        return {"message": "The emotion was shared successfully."}
    if result == 2:
        return {"message": "The user did not exist."}
    if result == 3:
        return {"warning": "The same emotion couldn't be shared with the same person twice!"}
    print(result)
    return {"error": "Something went wrong! Contact the server administrator."}


# emo unshares
@app.post("/emotions/unshare", dependencies=[Depends(JWTBearer())], tags=["emotions"])
async def unshare_emotions(share_emo: Share_emotions, request: Request):
    result = db.unshare_user_emo(share_emo)
    if result == 1:
        return {"message": "The shared emotion was deleted successfully."}
    if result == 2:
        return {"error": "The ID and Name did not match."}
    return {"error": "Something went wrong! Contact the server administrator."}


# add emo records
@app.post("/emotions/add", dependencies=[Depends(JWTBearer())], tags=["emotions"])
async def add_emotions(emo: Add_emotions):
    result = db.create_emo(emo)
    if result == 1:
        return {"message": "The emotion was added successfully."}
    return {"error": "Something went wrong! Contact the server administrator."}


# update user emo records
@app.put("/emotions/update", dependencies=[Depends(JWTBearer())], tags=["emotions"])
async def update_emotions(emo: Update_emotions):
    result = db.update_user_emo(emo)
    if result == 0:
        return {"error": "No such emo ID was found."}
    if result == 1:
        return {"message": "The emotion was updated successfully."}
    return { "message": f"{result}"}


# delete user emo records
@app.delete("/emotions/delete/{emo_id}", dependencies=[Depends(JWTBearer())], tags=["emotions"])
async def delete_emotions(emo_id: int):
    result = db.delete_user_emo(emo_id)
    if result == 0:
        return {"error": "No such emo ID was found."}
    return {"message": f"The emotion {emo_id} was deleted."}


# get emotion analysis
@app.get("/emotions/analysis", dependencies=[Depends(JWTBearer())], tags=["emotions"])
async def analysis_emotions(user_name: str = "john2024", \
                      start_day: date = "2023-09-24", \
                      end_day: date = "2023-09-25"):
    user_id = db.get_user_id(user_name)
    analysed = db.analysis_by_days(user_id, start_day, end_day)
    if len(analysed) == 0:
        return {"message": "No emotion records were found."}
    return analysed


# email checking and send email for reset password
@app.post("/reset/send/email", tags=["resets"])
async def send_email(email: Reset_email_checking):
    if not db.check_user(email=email.email)["email"]:
        return {"message": "None of email addresses were found."}
    hashed_pwd = db.get_pwd_by_email(email.email)
    reset_pwd_token = one_time_signJWT(email.email, hashed_pwd)
    result = await messenger.send(email.email, reset_pwd_token)
    return {"message": "The email was sent."}


# reset user password
@app.put("/reset/password", 
        dependencies=[Depends(One_time_JWTBearer())], 
        tags=["resets"])
async def reset_password(user_resets: Reset_password):
    if user_resets.new_password != user_resets.confirm_password:
        return {"error": "Please check your new passwords!"}
    user_name = db.get_user_name_by_email(user_resets.email)
    new_password_hashed = get_password_hash(user_resets.new_password)
    
    result = db.update_user_password(user_name, new_password_hashed)
    return { "message": "The password was successfully updated."}


@app.get("/", response_class=RedirectResponse, status_code=301, tags=["redirect"])
async def redirect_to_home_page():
    return "https://wavemocards.com"



#TODO1: remove email checking responses to reset password.
#TODO2: remove the example of model.
