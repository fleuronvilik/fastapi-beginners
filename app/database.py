from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_user}:{settings.db_upwd}@{settings.db_host}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # allows sqlalchemy to conn to db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # use to "talk" to db

Base = declarative_base() # base class for all models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()