import time
import psycopg2

from typing import List
from fastapi import FastAPI, Response, status
from psycopg2.extras import RealDictCursor
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from .db import get_db, engine
from . import models, schemas, utils

while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='postgres',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        break
    except Exception as error:
        print(error)
        time.sleep(2)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Welcome to my uncomplete API"}

@app.get('/posts', response_model=List[schemas.ResponsePost])
def get_posts(db: Session=Depends(get_db)):
    all_posts = db.query(models.Post).all()
    return all_posts

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.Post, db: Session=Depends(get_db)):
    """ title=post.title, content=post.content, published=post.published (Unpacking)"""
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # RETURNING *
    return new_post

@app.get('/posts/{id}', response_model=schemas.ResponsePost)
def get_post(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Post).get(ident=id)
    utils.raise_404_or_not(post, id)
    return post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session=Depends(get_db)):
    del_query = db.query(models.Post).filter(models.Post.id == id)
    utils.raise_404_or_not(del_query.first(), id)
    del_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', response_model=schemas.ResponsePost)
def update_post(id: int, updates: schemas.Post, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    utils.raise_404_or_not(post.first(), id)
    post.update(updates.dict(), synchronize_session=False)
    db.commit()
    return post.first()

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreated)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    user.password = utils.hash(user.password) 
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model=schemas.UserCreated)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).get(ident=id)
    utils.raise_404_or_not(user, id, msg="No User with ID {}")
    return user
