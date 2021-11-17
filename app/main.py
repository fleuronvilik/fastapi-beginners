from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = [
    {
        "id": 1,
        "title": "Quod Ducimus Omnis",
        "content": "Quod Ducimus Omnis"
    },
    {
        "id": 2,
        "title": "Python API Development",
        "content": "Watch the full length course on our YT channel"
    }
]

app = FastAPI()

def get_post_by_id(id):
    for post_at, post in enumerate(my_posts):
        if post["id"] == id:
            return post, post_at
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, # res.status_code = status.HTTP_404_NOT_FOUND
        detail=f"No post with ID {id}" # return {"message": "No post with this ID"}
    )

def get_last_id():
    if not my_posts:
        return 0
    return my_posts[-1]["id"]

@app.get('/')
def root():
    return {"message": "Welcome to my uncomplete API"}

@app.get('/posts')
def get_posts():
    return {"data": my_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = get_last_id() + 1
    my_posts.append(post_dict)
    return {
        # "message": "Successfully created post",
        "data": post_dict
    }

@app.get('/posts/{id}')
def get_post(id: int, res: Response):
    data, _ = get_post_by_id(id) 
    return {"data": data}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    _, post_at = get_post_by_id(id)
    my_posts.pop(post_at)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    _, post_at = get_post_by_id(id)
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[post_at] = post_dict
    return {"data": post_dict}
