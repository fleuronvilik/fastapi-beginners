from time import time
# from datetime import datetime, timedelta
# from fastapi.encoders import jsonable_encoder
from jose import jwt, JWTError

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app import schemas

SECRET_KEY = "08a8e0ddac772c8c95f08bc80671bf7c137ea5d691f3e4b47f1321ca55937136"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256" # is default in jwt.encode() anyway

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def create_access_token(data: dict):
    expire = time() + ACCESS_TOKEN_EXPIRE_MINUTES*60
    # expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = data.copy()
    # payload.update({"exp": jsonable_encoder(expire)})
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY)

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload["user_id"]
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return verify_access_token(token, credentials_exception)
