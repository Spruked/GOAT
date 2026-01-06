from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    role: str = "user"
    onboarding_state: Optional[str] = None

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserInDB(UserBase):
    hashed_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
