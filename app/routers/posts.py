# from server import app, database, schemas, models
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
import models
import schemas
import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=list[schemas.Post])
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all() # cursor.execute("""SELECT * FROM posts""")
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}')
def get_post(id: int, db: Session = Depends(database.get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    # print(query)
    return query.first()

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post is None:
        # return {"data": f"Post {id} not found"}
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this post")
    query.delete(synchronize_session=False)
    db.commit()
    return {"data": f"Post {id} has been deleted"}

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to edit this post")
    query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()