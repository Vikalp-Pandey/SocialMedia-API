from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import models,schemas

# Database URL
# This is the database URL for connecting to a PostgreSQL database using SQLAlchemy.
# It specifies the database type, username, password, host, and database name.
# # The format is: "database://username:password@host:port/<database name>"

# fastapSQLALCHEMY_DATABASE_URL = "postgresql://username:Password@ip-address/hostname/database_name"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Vikalp2004@@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Vikalp2004%40@localhost/fastapi"
# Note: The password contains a special character '@', which is URL-encoded as '%40'.

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

