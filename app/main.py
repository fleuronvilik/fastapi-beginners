import time
import psycopg2

# from typing import List
from fastapi import FastAPI #, Response, status
from psycopg2.extras import RealDictCursor
# from fastapi.params import Depends
# from sqlalchemy.orm.session import Session

from .db import engine
from .routers import post, user, auth
from . import models

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# @app.get('/')
# def root():
#     return {"message": "Welcome to my uncomplete API"}
