from datetime import datetime
from random import randrange
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Response,status
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pydantic import BaseModel
from passlib.context import CryptContext
from . import models
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from .database import  engine, SessionLocal
from app import database, schemas
# Importing the Sqlalchemy ORM parts in database.py file


pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")  # For hashing the passwords

# Importing the database connection and session from database.py file

models.Base.metadata.create_all(bind=database.engine)  # Creating the database tables (based on the models) in the connected database(just like migrations in Django)
# In your code where you create tables:
models.Base.metadata.create_all(bind=engine)  # recreate tables with updated schema
# This will create the tables in the database based on the models defined in app/models.py



# Importing the database connection and session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Importing the FastAPI framework
app=FastAPI()


# Checking the connection to the database

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "Success"}






# Defining Path Operation
@app.get("/")      
async def get_user():
    return {'message':"Welcome To My API"}


# 1)  Getting the Posts
@app.get("/posts" ,response_model=List[schemas.PostResponse])  # response_model is used to specify the response model that will be returned by this endpoint.
def get_posts(db: Session = Depends(get_db)):
    posts= db.query(models.Post).all()  # Using the ORM to get all the posts from the database
    return posts  # Returning the posts in the form of a dictionary


# 2) (Creating and retrieving) Any Post. 

@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.PostCreate) #Status Code is written to override the default status code that is displayed after a post is getting created.
# Logic to create and retrieve any post we want.

def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db)):
    
    new_post=models.Post(**post.model_dump())    # unpacking all the parameters of the Post model using model_dump() method to create a new post object.
    db.add(new_post)  # Adding the new post to the database session
    db.commit()  # Committing the changes to the database
    db.refresh(new_post)  # Refreshing the new post object to get the updated data
    return {"data": new_post}  # Returning the new post in the form of a dictionary

@app.get("/posts/{user_id}")

def get_post(user_id: int, db:Session=Depends(get_db)):  
    
    test_post=db.query(models.Post).filter(models.Post.user_id==user_id).first()
    print(test_post)
    
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"post with id: {id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail":f"post with id: {id} was not found "}
    return {"data": test_post}  # Returning the post in the form of a dictionary


@app.get("/all/{user_id}")
# Logic to get all the Posts of a particular id.

def get_posts_by_user(user_id: int, db:Session=Depends(get_db)):
    All_posts=db.query(models.Post).filter(models.Post.user_id==user_id).all()
    if not All_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"posts with user_id: {user_id} was not found")
    return {"user_posts": All_posts}



@app.get("/latest/")
# Logic to get the most recent post.
def latest_post( db:Session=Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return {"detail": latest_post}


@app.get("/latest/{user_id}")
# Logic to get the most recent post of a particular ID.
    
# async def latest_post(id:int,post:Post):   ---Wrong: Get requests shouldn't have a request body(like post:Post)
async def latest_post(user_id:int, db:Session=Depends(get_db)):

    latest_post_of_ID=db.query(models.Post).filter(models.Post.user_id==user_id).order_by(models.Post.created_at.desc()).first()
    
    if not latest_post_of_ID:
        return {"detail": f"Post with 'id':{id} does not exists"}
        '''Why if not posts: works:
           If no posts match the given id, find_posts() returns an empty list [].
           if not posts: checks if the list is empty, which is the correct way to detect "no matching post found.'''
    else:
        return {"detail":latest_post_of_ID}



# '''
# Note:
# 1) Any path parameter like id in URL (/posts/{id}) is always gong to be returned as a string 
# even if it is an integer or some other data type.  

# So, we have to manually convert this path parameter into our desired data type(int in this case).

# 2) Also keep in mind that while struturing your api
# If you have a path parameter for a path and have another path similar to the first one (for ex: 1) /posts/{id} and  2) /posts/latest) 

# Now if we want to hit url 2 , we will see an error because the server will try to match the given url with url 1 and latest will be mapped to {id} parameter which will show an error for wrong id.
# '''

# 3)Deleting a Post

@app.delete("/posts/id={id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db:Session=Depends(get_db)): #If this id is not provided here with validation check,we will see an error.
    deleted_post=db.query(models.Post).filter(models.Post.id==id)
    
    # If we enter ID whose posts doesnot exist,then we see an Internal Server Error.To fix this
    if deleted_post.first()==None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Post with id {id} doesnot exists.")
    else:
        deleted_post.delete(synchronize_session=False)
        db.commit() # It is important to commit the changes to the database after deleting the post.
                    # If we don't commit, the changes will not be saved to the database and we will see an error.
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        return {"detail": f"Post with id {id} has been deleted successfully."}
        # Note: We are not returning any data here because we are returning a 204 status
    # Any message that we want to return will not be seen because of 404 status.We can only return it Response.
    
    


# 4) Updating a Post:


@app.put("/posts/user_id={user_id}/id={id}")

def update_posts(id:int,user_id:int, updated_post:schemas.PostUpdate, db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.user_id==user_id, models.Post.id==id)
    
    post=post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} and user_id:{user_id} does not exist.")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return {"updated_Post":post_query.first()}


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password=pwd_context.hash(user.password)  # Hashing the password using passlib,so that it is stored securely in the database.
    user.password = hashed_password  # Setting the hashed password to the user object
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": new_user}  # Returning the new user in the form of a dictionary


@app.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.user_id.asc()).all()
    return users
