from passlib.context import CryptContext
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # For hashing the passwords

def hash(password: str):
    return pwd_context.hash(password)