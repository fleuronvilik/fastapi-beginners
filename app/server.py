import time # sleep
import psycopg2

from fastapi import FastAPI, status, Depends, HTTPException
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

import models
import schemas
import database
import utils

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

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

@app.get('/')
def root():
    return {
        "status": "in progress",
        "releases": None,
        "packages": None,
        "documentation": "https://fastapi.tiangolo.com/",
    }

@app.get('/posts', response_model=list[schemas.Post])
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all() # cursor.execute("""SELECT * FROM posts""")
    return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(database.get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    # print(query)
    return query.first()

@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(database.get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() is None:
        # return {"data": f"Post {id} not found"}
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    return {"data": f"Post {id} has been deleted"}

@app.put('/posts/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(database.get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()


@app.post('/users', response_model=schemas.UserCreated)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model=schemas.UserCreated)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return user