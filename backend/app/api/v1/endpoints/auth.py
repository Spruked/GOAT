from fastapi import APIRouter, HTTPException, status, Depends, Form
from app.models.user import UserCreate, UserLogin
from app.core.users import create_user, get_user_by_email, verify_password
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr

SECRET_KEY = "your_jwt_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix="/auth", tags=["auth"])

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup")
def signup(user: UserCreate):
    print(f"Signup attempt for email: {user.email}")
    if user.password != user.confirm_password:
        print("Passwords do not match")
        raise HTTPException(status_code=400, detail="Passwords do not match")
    existing_user = get_user_by_email(user.email)
    print(f"Existing user check: {existing_user}")
    if existing_user:
        print("Email already registered")
        raise HTTPException(status_code=400, detail="Email already registered")
    print("Creating user...")
    user_id = create_user(user)
    print(f"User created with ID: {user_id}")
    access_token = create_access_token({"sub": user.email, "role": "user", "id": user_id})
    print("Token created")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user["email"], "role": db_user["role"], "id": db_user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}
