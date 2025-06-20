from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn 

app = FastAPI() # instance 


@app.get('/blog')
def index(limit = 10 ,published :bool= True , sort: Optional[str] = None):
    #only get 10 published blog
    if published:
        return {'data': f'{limit} published blog list from db'}
    else:
        return {'data': f'{limit} blog list from db'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blog'}


@app.get('/blog/{id}')
def show(id: int):
    #fetch blog with id = id
    return {'data': id}

@app.get("/blog/{id}/comments")
def comments(id : int , limit=10):
    #fetch comments where id = id
    return {'data': {'1', '2', '3','4','5','6','7','8','9','10','11','12'}}


class Blog(BaseModel):
    title :str
    body : str
    published: Optional[bool]
@app.post("/blog")
def create_blog(blog: Blog):
    
    return {"data" :f"Blog is created with title {blog.title}"}



# if __name__ == "__main__":
#     uvicorn.run(app, host='127.0.0.1', port=9000)