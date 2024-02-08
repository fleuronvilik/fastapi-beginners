import time # sleep
import psycopg2

from fastapi import FastAPI, status # Response, HTTPException
from psycopg2.extras import RealDictCursor

from schemas import Post

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

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    query = """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"""
    cursor.execute(query, (post.title, post.content, post.published))
    conn.commit()
    return {"data": cursor.fetchone()}

@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    post = cursor.fetchone()
    # raise_404_or_not(post, id)
    return {"data": post}
