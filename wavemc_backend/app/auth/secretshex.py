import secrets
import time

secret = secrets.token_hex()
ACCESS_TOKEN_EXPIRE_SECOND = 60 * 30
print(secret)
print(time.time())
print(time.localtime())
print(ACCESS_TOKEN_EXPIRE_SECOND)

