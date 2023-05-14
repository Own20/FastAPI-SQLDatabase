#Import the SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Create a database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

#Create the SQLAlchemy engine
#connect_args={"check_same_thread": False} only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#Create a SessionLocal class
#Each instance of the SessionLocal class will be a database session. This instance will be the actual database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create a Base class
#function /declarative_base()/ that returns a class.
#Later inherit from this class to create each of the database models or classes (the ORM models)
Base = declarative_base()