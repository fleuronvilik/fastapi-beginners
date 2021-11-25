from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # allows sqlalchemy to conn to db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # use to "talk" to db
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()