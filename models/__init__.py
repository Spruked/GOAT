# models/__init__.py
"""
GOAT Database Models
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - using SQLite for now, can be changed to PostgreSQL later
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/goat.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Import models
from .user import User
from .user_file import UserFile
from .unanswered_query import UnansweredQuery

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()