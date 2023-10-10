from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT
from .auth_reset import one_time_decodeJWT
from app.database import db


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = \
                                await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                        status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


class One_time_JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(One_time_JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = \
                                await super(One_time_JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials, dict(await request.json())):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(
                        status_code=403, detail="Invalid authorization code.")
    
           
    def verify_jwt(self, jwtoken: str, request: dict) -> bool:
        email = request["email"] 
        isTokenValid: bool = False
        if not db.check_user(email=email)["email"]:
            return isTokenValid
        hashed_pwd = db.get_pwd_by_email(email)

        try:
            payload = one_time_decodeJWT(email, hashed_pwd, jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
