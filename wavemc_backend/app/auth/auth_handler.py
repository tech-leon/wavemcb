# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict

import jwt
from decouple import config
from passlib.context import CryptContext


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_SECOND = 60 * 30

pwd_context =\
    CryptContext(schemes=["bcrypt"], deprecated="auto")


def token_response(token: str):
    return {"access_token": token}


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# function used for signing the JWT string


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id,
               "expires": time.time() + ACCESS_TOKEN_EXPIRE_SECOND}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
