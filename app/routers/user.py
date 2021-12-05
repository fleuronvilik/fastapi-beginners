from sqlalchemy.orm.session import Session

from fastapi import status, Depends, APIRouter
from ..db import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreated)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    user.password = utils.hash(user.password) 
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserCreated)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).get(ident=id)
    utils.raise_404_or_not(user, id, msg="No User with ID {}")
    return user
