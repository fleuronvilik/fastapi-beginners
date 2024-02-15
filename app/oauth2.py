from time import time
from datetime import datetime, timedelta
# from fastapi.encoders import jsonable_encoder
from jose import jwt, JWTError

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

# from app import schemas, models, db
# from .config import settings

import schemas
import models
import database as db

SECRET_KEY = "69e45d3d041511b44e3b6a6dc2ca42c6b6dc7cf4476afb8ce1bf14038b33f437" #settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # settings.access_token_expire_minutes
ALGORITHM = "HS256" # settings.algorithm # is default in jwt.encode() anyway

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def create_access_token(data: dict):
    expire = time() + ACCESS_TOKEN_EXPIRE_MINUTES*60
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = data.copy()
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY)

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload["user_id"]
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str=Depends(oauth2_scheme), db: Session=Depends(db.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).get(token.id)
    return user