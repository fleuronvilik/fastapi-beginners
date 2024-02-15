from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import models
import database
import utils

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', response_model=schemas.UserCreated)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserCreated)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return user
