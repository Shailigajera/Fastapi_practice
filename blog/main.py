from fastapi import FastAPI, Depends, status, Response , HTTPException
from . import schemas, models
from . database import  SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog" , status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body= request.body )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT , )
def delete(id:int, db: Session = Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Blog with id {id} not found" )
    blog.delete(synchronize_session = False)
    db.commit()
    return {'detail':'Blog is deleted successfully'}

@app.put("/blog/{id}" , status_code = status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Blog with id {id} not found" )
    blog.update(request.dict())
    db.commit()
    return {'detail':"Blog is Updated successfully"}



@app.get('/blog', status_code = status.HTTP_200_OK,response_model = List[schemas.ShowBlog] )
def get(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blogs/{id}', status_code=200, response_model = schemas.ShowBlog)
def show(id: int, response : Response,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'detail': f"Blog with the id {id} is not available"}
    return blog

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')



@app.post("/user")
def create_user(request : schemas.User, db: Session = Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user