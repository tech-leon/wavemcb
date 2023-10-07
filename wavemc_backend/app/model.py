from pydantic import BaseModel, Field
from datetime import date


class PostSchema(BaseModel):
    # id: int = Field(default=None)
    # title: str = Field(...)
    # content: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }


class User_signup(BaseModel):
    title: str = Field(None)
    email: str
    user_name: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    day_of_birth: date = Field(None)
    gender: str = Field(None)
    addr_street: str = Field(None)
    addr_city: str = Field(None)
    addr_postcode: int = Field(None)
    phone: int = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "student",
                "email": "johnwick@wavemocards.com",
                "user_name": "john2024",
                "password": "vEryStrongPassword",
                "first_name": "John",
                "last_name": "Wick",
                "day_of_birth": "1964-09-02",
                "gender": "M",
                "addr_street": "101 Hollywood Street",
                "addr_city": "Los Angeles",
                "addr_postcode": 90001,
                "phone": 2028638426
            }
        }


class User_login(BaseModel):
    user_name: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "user_name": "john2024",
                "password": "vEryStrongPassword",
            }
        }


class User_password(BaseModel):
    current_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "<PASSWORD>",
                "new_password": "<NEW_PASSWORD>",
                "confirm_password": "<NEW_PASSWORD>"
            }

        }


class User_infomation(BaseModel):
    title: str = Field(None)
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    day_of_birth: date
    # gender: str = Field(None)
    # addr_street: str = Field(None)
    # addr_city: str = Field(None)
    # addr_postcode: int = Field(None)
    # phone: int = Field(None, le=15)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "student",
                "first_name": "John",
                "last_name": "Wick",
                "day_of_birth": "1964-09-02",
                # "gender": "M",
                # "addr_street": "101 Hollywood Street",
                # "addr_city": "Los Angeles",
                # "addr_postcode": 90001,
                # "phone": 2028638426
            }
        }


class User_checking(BaseModel):
    email: str = Field(None)
    user_name: str = Field(None, min_length=3, max_length=20)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "johnwick@wavemocards.com",
                "user_name": "john2024"
            }
        }


class Add_emotions(BaseModel):
    user_name: str = Field(min_length=3, max_length=20)
    story: str = Field(None)
    reaction: str = Field(None)
    results: str = Field(None)
    feelings: str = Field(None)
    expect: int = Field(None)
    actions: str = Field(None)
    emotion_card_1: int = Field(ge=1, le=65)
    emotion_card_2: int = Field(None, ge=1, le=65)
    emotion_card_3: int = Field(None, ge=1, le=65)
    before_emo_level_1: int = Field(ge=1, le=5)
    before_emo_level_2: int = Field(None, ge=1, le=5)
    before_emo_level_3: int = Field(None, ge=1, le=5)
    after_emo_level_1: int = Field(None, ge=1, le=5)
    after_emo_level_2: int = Field(None, ge=1, le=5)
    after_emo_level_3: int = Field(None, ge=1, le=5)

    class Config:
        json_schema_extra = {
            "example": {
                "user_name": "john2024",
                "story": "雖然我盡力了，但我考試的分數還是不理想，讓我感到沮喪、難過和挫敗。",
                "reaction": "我開始更加努力地讀書，找老師請教問題，並參加補習班。",
                "results": "我的成績開始逐漸進步，我變得更有信心。",
                "feelings": "這讓我感到非常開心和驕傲，因為我證明了努力付出是有成果的。",
                "expect": 1,
                "actions": "雖然遇到挫折，但我堅持向老師請教並加強閱讀，最終在英文課上表現出色，感到自己的努力有了回報。",
                "emotion_card_1": 31,
                "emotion_card_2": 32,
                "emotion_card_3": 34,
                "before_emo_level_1": 5,
                "before_emo_level_2": 3,
                "before_emo_level_3": 4,
                "after_emo_level_1": 2,
                "after_emo_level_2": 1,
                "after_emo_level_3": 1
            }
        }


class Get_emotions(BaseModel):
    user_name: str = Field(min_length=3, max_length=20)


class Update_emotions(BaseModel):
    emo_ID: int
    story: str = Field(None)
    reaction: str = Field(None)
    results: str = Field(None)
    feelings: str = Field(None)
    expect: int = Field(None, ge=1, le=3)
    actions: str = Field(None)
    emotion_card_1: int = Field(None, ge=1, le=65)
    emotion_card_2: int = Field(None, ge=1, le=65)
    emotion_card_3: int = Field(None, ge=1, le=65)
    before_emo_level_1: int = Field(None, ge=1, le=5)
    before_emo_level_2: int = Field(None, ge=1, le=5)
    before_emo_level_3: int = Field(None, ge=1, le=5)
    after_emo_level_1: int = Field(None, ge=1, le=5)
    after_emo_level_2: int = Field(None, ge=1, le=5)
    after_emo_level_3: int = Field(None, ge=1, le=5)

    class Config:
        json_schema_extra = {
            "example": {
                "emo_ID": 1,
                "story": "我考試的分數不理想，讓我感到沮喪、失望和挫敗。",
                "reaction": "我開始更加努力地讀書，找老師請教問題，並參加補習班。我還挑燈夜戰，誓死打敗全班第一．"
            }
        }

class Forgotten(BaseModel):
    email: str 