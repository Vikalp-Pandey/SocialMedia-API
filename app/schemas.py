'''Schema/Pydnatic Models define structure of a request and response
This ensure that a user wants to create a post, the request will only go through if it has a 'title' and 'content' in the body'''


from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr, Field

# Pydantic Models
'''Pydantic Models'''

# Defining the Post Schema for creating and updating posts
class PostBase(BaseModel):
  id:int=None
  user_id: int
  title: str
  content: str
  published: bool=True         # This is optional field with default value as True
  rating: Optional[int]=None   # A fully optional field with default =None'''
  created_at: datetime=datetime.now()       #  field for creation timestamp,
  
# Inheriting from Post parent class and all its attributes
class PostCreate(PostBase):
  pass

class PostUpdate(PostBase):
  pass


# Response Model for getting posts.Inheriting all attributes from Posts class
class PostResponse(PostBase): #Response model must be passed to the response_model parameter in the FastAPI route
  id: int
  user_id: int
  title: str
  content: str
  published: bool=True
  rating: Optional[int]=None
  created_at: datetime=datetime.now()
  class Config:
    orm_mode = True  
    # This allows Pydantic to read data from SQLAlchemy models
    # This is used to convert the SQLAlchemy model to a Pydantic model
    # It allows us to use the SQLAlchemy model directly in the response
    # without having to convert it to a dictionary first.


# Defining the User Schema for creating and updating users

class UserCreate(BaseModel):
    # user_id: int=None
    email: EmailStr
    password: str  

class UserResponse(BaseModel): #Response model must be passed to the response_model parameter in the FastAPI route
    user_id: int
    email: EmailStr
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True  # This allows Pydantic to read data from SQLAlchemy models
        # It allows us to use the SQLAlchemy model directly in the response
        # without having to convert it to a dictionary first.    