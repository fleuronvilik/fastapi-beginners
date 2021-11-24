import time
import psycopg2

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    sql_insert = """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"""
    cursor.execute(sql_insert, (post.title, post.content, post.published))
    conn.commit()
    return {"data": cursor.fetchone()}

@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    post = cursor.fetchone()
    raise_404_or_not(post, id)
    return {"data": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    raise_404_or_not(cursor.fetchone(), id)
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    sql_update = """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *"""
    cursor.execute(sql_update, (post.title, post.content, post.published, id))
    post_up = cursor.fetchone()
    raise_404_or_not(post_up, id)
    conn.commit()
    return {"data": post_up}
