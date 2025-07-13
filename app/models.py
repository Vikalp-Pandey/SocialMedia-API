# Defining the Database Models by ORM
from .database import Base,engine
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, null, text


class Post(Base):
    __tablename__ = "posts"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Primary key
    user_id = Column(Integer,ForeignKey("users.user_id") ,nullable=True)  # Foreign key to the user who created the post
    title = Column(String, nullable=False)  # Title of the post
    content = Column(String, nullable=False)  # Content of the post
    published = Column(Boolean, server_default='True',nullable=False)  # Published status of the post
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)  # Creation timestamp
    rating = Column(Integer, nullable=True,)  # Optional rating field

class User(Base):
    __tablename__ = "users"  # Name of the table in the database

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Primary key
    email = Column(String, nullable=False, unique=True)  # Email of the user
    password = Column(String, nullable=False)  # Password of the user
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)  # Creation timestamp
    