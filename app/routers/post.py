from typing import List
from sqlalchemy.orm.session import Session

from fastapi import Response, status, Depends, APIRouter

from ..db import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.ResponsePost])
def get_posts(db: Session=Depends(get_db)):
    all_posts = db.query(models.Post).all()
    return all_posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.Post, db: Session=Depends(get_db)):
    """ title=post.title, content=post.content, published=post.published (Unpacking)"""
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # RETURNING *
    return new_post

@router.get('/{id}', response_model=schemas.ResponsePost)
def get_post(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Post).get(ident=id)
    utils.raise_404_or_not(post, id)
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session=Depends(get_db)):
    del_query = db.query(models.Post).filter(models.Post.id == id)
    utils.raise_404_or_not(del_query.first(), id)
    del_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.ResponsePost)
def update_post(id: int, updates: schemas.Post, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    utils.raise_404_or_not(post.first(), id)
    post.update(updates.dict(), synchronize_session=False)
    db.commit()
    return post.first()
