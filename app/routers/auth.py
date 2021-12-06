from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm.session import Session
from .. import db, models, utils, schemas, oauth2

router = APIRouter(tags=['Authentification'])

@router.post('/login')
def login(user_credentials: schemas.UserCreate, db: Session=Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
        
    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    