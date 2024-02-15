import time # sleep
import psycopg2

from fastapi import FastAPI # , status, Depends, HTTPException
from psycopg2.extras import RealDictCursor
# from sqlalchemy.orm import Session

from routers import users, posts, auth

import models
# import schemas
import database
# import utils

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

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
