import uvicorn
from fastapi import FastAPI, Body, Depends
from pydantic import Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


from .model import PostSchema, User, UserLogin, Add_emotions, Get_emotions, Update_emotions
from .auth.auth_bearer import JWTBearer
from .auth.auth_handler import signJWT, get_password_hash, verify_password
from .database import db


app = FastAPI(redoc_url=None)
# Define the origins that are allowed to access API 
origins = ["https://wavemocards.com"]
# Add CORS middleware with the specified configuration.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# route handlers

@app.get("/", response_class=RedirectResponse, status_code=302, tags=["redirect"])
async def redirect_docs():
    return "http://api.wavemocards.com/docs"
    # return "http://api2.wavemocards.com/docs"


# get emotions informations
@app.get("/emoinfo/{query}/", tags=["emotion informations"])
async def get_emotions(query: str):
    if query == "about":
        return db.about_emotions()
    elif query == "cards":
        return db.emotion_cards()


# get user emo records
@app.get("/emotions", dependencies=[Depends(JWTBearer())], tags=["emotions"])
def get_emotions(user_name: str = 'john2024', limit: int = 5):
    return db.get_user_emos(db.get_user_id(user_name))[:limit]


# add emo records
@app.post("/emotions/add", dependencies=[Depends(JWTBearer())], tags=["emotions"])
def add_emotions(emo: Add_emotions):
    return {"data": f"{db.create_emo(emo)} emo has been added."}


# update user emo records
@app.put("/emotions/update", dependencies=[Depends(JWTBearer())], tags=["emotions"])
def update_emotions(emo: Update_emotions):
    result = db.update_user_emo(emo)
    if result == 0:
        return {"error": "No such emo ID was found."}
    return { "message": f"{result}"}


# delete user emo records
@app.delete("/emotions/delete/{emo_id}", dependencies=[Depends(JWTBearer())], tags=["emotions"])
def delete_emotions(emo_id: int):
    result = db.delete_user_emo(emo_id)
    if result == 0:
        return {"error": "No such emo ID was found."}
    return {"message": f"The emotion recard {emo_id} was deleted."}


# signup
@app.post("/user/signup", tags=["user"])
def create_user(user: User):  # = Body(...)):
    # replace with db call, making sure to hash the password first
    user.password = get_password_hash(user.password)
    if user.day_of_birth == "":
        user.day_of_birth = '0-0-0'
    return {"data": f"{db.register_new_user(user)} new user created."}

# login
@app.post("/user/login", tags=["user"])
def user_login(user: UserLogin):  # = Body(...)):
    if db.check_user(user.user_name):
        hashed_password = db.get_user_hashed_password(user.user_name)
        if verify_password(user.password, hashed_password):
            return signJWT(user.user_name)  # get access token
    return {"error": "Wrong login details!"}
