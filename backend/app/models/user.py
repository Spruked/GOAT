from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    onboarding_state = Column(String, nullable=True)
    blocked = Column(Integer, default=0)  # 0 = not blocked, 1 = blocked
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserBase(BaseModel):
    email: EmailStr
    role: str = "user"
    onboarding_state: Optional[str] = None
    blocked: bool = False

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserInDB(UserBase):
    id: int
    hashed_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String, nullable=False)
    value = Column(Text, nullable=False)  # JSON data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
