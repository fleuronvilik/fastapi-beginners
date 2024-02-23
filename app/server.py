# This is the main file that will run the FastAPI application.
# It will import the routers and models and create the database.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, post, posts, auth, vote

#import models
#import database
#models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# origins = ["http://localhost:8000"] # ["http://localhost", "http://localhost:8080", "http://localhost:3000", "http://localhost:8000", "http://localhost:5000", "http://localhost:80", "http://localhost:443
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # True if you want to allow the credentials (cookies, authorization headers, etc)
    allow_methods=["*"], # ["GET", "POST", "PUT", "DELETE", "PATCH"]
    allow_headers=["*"], # ["Authorization", "Content-Type"]
)


@app.get("/")
def root():
    return {
        "status": "in progress",
        "releases": None,
        "packages": None,
        "documentation": "https://fastapi.tiangolo.com/",
    }


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(vote.router)
