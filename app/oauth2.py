from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from jose import jwt #, JWTError

SECRET_KEY = "08a8e0ddac772c8c95f08bc80671bf7c137ea5d691f3e4b47f1321ca55937136"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# ALGORITHM = "HS256" # is default in jwt.encode() anyway

def create_access_token(data):
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = data.copy()
    payload.update({"expire": jsonable_encoder(expire)})
    return jwt.encode(payload, SECRET_KEY)
