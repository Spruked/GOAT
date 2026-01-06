# auth.py
"""
Authentication and user management for GOAT
"""

from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from user_tracker import user_tracker

# Password hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-256-bit-key-here-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class User(BaseModel):
    id: Optional[int] = None
    user_id: str
    email: str
    name: str
    signup_date: Optional[datetime] = None
    is_active: bool = True
    marketing_opt_in: bool = True

class UserCreate(BaseModel):
    email: str
    full_name: str  # Frontend sends full_name
    password: str
    marketing_opt_in: bool = True
    
    @property
    def name(self):
        """Alias for backward compatibility"""
        return self.full_name

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str):
    """Authenticate user using user_tracker"""
    return user_tracker.authenticate_user(email, password)

def create_user(user: UserCreate):
    """Create user using user_tracker"""
    hashed_password = get_password_hash(user.password)
    return user_tracker.create_user(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        marketing_opt_in=user.marketing_opt_in
    )

def get_user(email: str):
    """Get user by email using user_tracker"""
    return user_tracker.get_user_by_email(email)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token and return user data"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        token_data = TokenData(email=email)
        user = get_user(email)
        if user is None:
            return None
        return user
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get current user from token with proper SQLAlchemy model"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Import here to avoid circular imports
    from models import SessionLocal
    db = SessionLocal()
    try:
        from models.user import User
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close()