import time # sleep
import psycopg2

from fastapi import FastAPI, status, Depends, HTTPException
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

import models
import schemas
import database

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
    return {"status": "in progress"}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(database.get_db)):
    return {"status": "success"}

@app.get('/posts')
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all() # cursor.execute("""SELECT * FROM posts""")
    return {"data": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(database.get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(database.get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    print(query)
    return {"data": query.first()}

@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(database.get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first() is None:
        # return {"data": f"Post {id} not found"}
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    return {"data": f"Post {id} has been deleted"}

@app.put('/posts/{id}')
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(database.get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": query.first()}

@app.put('/posts/{id}')
def put_post(id: int, post: schemas.Post):
    query = """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *"""
    cursor.execute(query, (post.title, post.content, post.published, id))
    conn.commit()
    return {"data": cursor.fetchone()}
