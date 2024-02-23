from typing import List
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func

from fastapi import status, Depends, APIRouter #, Response

from app import models, schemas, utils, oauth2, database as db

# import database as db
# import models
# import schemas
# import oauth2
# import utils

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# current_user: int=Depends(oauth2.get_current_user)
@router.get('/', response_model=List[schemas.PostWithVotesCount])
def get_posts(db: Session=Depends(db.get_db), limit: int=10, skip: int=0, search: str=""):
    # all_posts = db.query(models.Post).limit(limit).offset(skip).all()
    results = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Post.id==models.Vote.post_id,
        isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).offset(skip).limit(limit).all()

    return results

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.PostCreate, db: Session=Depends(db.get_db), current_user: int=Depends(oauth2.get_current_user)):
    """ title=post.title, content=post.content, published=post.published (Unpacking)"""
    new_post = models.Post(owner_id=current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # RETURNING *
    return new_post

# current_user: int=Depends(oauth2.get_current_user)
@router.get('/{id}', response_model=schemas.PostWithVotesCount)
def get_post(id: int, db: Session=Depends(db.get_db)):
    post = db.query(models.Post).get(ident=id)
    utils.raise_404_or_not(post, id)
    result = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Post.id==models.Vote.post_id,
        isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.id==id
    ).first()
    return result

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session=Depends(db.get_db), current_user: int=Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    utils.raise_404_or_not(post, id)
    if not current_user.id == post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    query.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', response_model=schemas.ResponsePost)
def update_post(id: int, updates: schemas.PostCreate, db: Session=Depends(db.get_db), current_user: int=Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    utils.raise_404_or_not(post, id)
    if not current_user.id == post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    query.update(updates.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()
