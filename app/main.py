import time
import psycopg2

from fastapi import FastAPI, Response, status, HTTPException
from psycopg2.extras import RealDictCursor
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from .db import get_db
from . import models, schemas

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

app = FastAPI()
 
def raise_404_or_not(post, id=None):
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with ID {id}"
        )

@app.get('/')
def root():
    return {"message": "Welcome to my uncomplete API"}

@app.get('/posts')
def get_posts(db: Session=Depends(get_db)):
    all_posts = db.query(models.Post).all()
    return {"data": all_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session=Depends(get_db)):
    """ title=post.title, content=post.content, published=post.published (Unpacking)"""
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # RETURNING *
    return {"data": new_post}

@app.get('/posts/{id}')
def get_post(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Post).get(ident=id)
    raise_404_or_not(post, id)
    return {"data": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session=Depends(get_db)):
    del_query = db.query(models.Post).filter(models.Post.id == id)
    raise_404_or_not(del_query.first(), id)
    del_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, updates: schemas.Post, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    raise_404_or_not(post.first(), id)
    post.update(updates.dict(), synchronize_session=False)
    db.commit()
    return {"data": post.first()}
