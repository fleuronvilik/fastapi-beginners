from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

# from .. import db, models, utils, schemas, oauth2

import database
import models
import utils
import schemas
import oauth2

router = APIRouter(tags=['Authentification'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
        
    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    