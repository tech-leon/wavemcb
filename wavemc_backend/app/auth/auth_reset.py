import time
from typing import Dict

import jwt
from decouple import config

JWT_ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_SECOND = 60 * 60 * 6


def one_time_signJWT(email: str, hashed_pwd: str) -> Dict[str, str]:
    payload = {"email": email,
               "expires": time.time() + ACCESS_TOKEN_EXPIRE_SECOND}
    token = jwt.encode(payload, hashed_pwd, algorithm=JWT_ALGORITHM)

    return token


def one_time_decodeJWT(email:str, hashed_pwd: str, token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, hashed_pwd, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() \
                            and decoded_token["email"] == email else None
    except:
        return {}
