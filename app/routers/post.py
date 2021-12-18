from typing import List
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session

from fastapi import Response, status, Depends, APIRouter

from ..db import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.ResponsePost])
def get_posts(db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    all_posts = db.query(models.Post).all()
    return all_posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.Post, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    """ title=post.title, content=post.content, published=post.published (Unpacking)"""
    new_post = models.Post(owner_id=current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # RETURNING *
    return new_post

@router.get('/{id}', response_model=schemas.ResponsePost)
def get_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).get(ident=id)
    utils.raise_404_or_not(post, id)
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    utils.raise_404_or_not(post, id)
    if not current_user.id == post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post.delete()
    db.commit()

@router.put('/{id}', response_model=schemas.ResponsePost)
def update_post(id: int, updates: schemas.Post, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    utils.raise_404_or_not(post, id)
    if not current_user.id == post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post.update(updates.dict(), synchronize_session=False)
    db.commit()
    return post.first()
