from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_user}:{settings.db_upwd}@{settings.db_host}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # allows sqlalchemy to conn to db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # use to "talk" to db
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

""" # Initially in main.py to run raw sql
# Here to just serve as documentation
import time
import psycopg2
from psycopg2.extras import RealDictCursor

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
        time.sleep(2) """
