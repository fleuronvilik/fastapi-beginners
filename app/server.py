# This is the main file that will run the FastAPI application.
# It will import the routers and models and create the database.

from fastapi import FastAPI

from routers import users, post, auth, vote

import models
import database

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


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
app.include_router(users.router)
app.include_router(vote.router)
