from fastapi import APIRouter, HTTPException, status, Depends, Form, Request
from app.models.user import UserCreate, UserLogin
from app.core.users import create_user, get_user_by_email, verify_password
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr

SECRET_KEY = "your_jwt_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup")
async def signup(request: Request):
    """Create a new user account"""
    print("Signup endpoint called")
    user = await request.json()
    print(f"Received data: {user}")
    print(f"Signup attempt for email: {user.get('email')}")
    
    # Extract fields
    email = user.get('email')
    full_name = user.get('full_name', '')
    master_password = user.get('master_password')
    agreements_accepted = user.get('agreements_accepted', False)
    
    if not email or not master_password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    if not agreements_accepted:
        raise HTTPException(status_code=400, detail="Must accept terms")
    
    # Check if user exists
    existing_user = get_user_by_email(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user with master_password as password
    user_create = UserCreate(
        email=email,
        password=master_password,
        confirm_password=master_password,  # Set to same
        full_name=full_name
    )
    
    print("Creating user...")
    user_id = create_user(user_create)
    print(f"User created with ID: {user_id}")
    
    # For signup, don't auto-login, just confirm creation
    return {"message": "Account created successfully", "user_id": user_id}

@router.post("/login")
async def login(request: Request):
    """Login and get access token"""
    user = await request.json()
    print(f"Login attempt for email: {user.get('email')}")
    
    # Admin bypass
    if user.get('email') == "admin@goat.com" and user.get('password') == "Acs222fiat":
        access_token = create_access_token({"sub": "admin@goat.com", "role": "admin", "id": 0})
        return {"access_token": access_token, "token_type": "bearer"}
    
    db_user = get_user_by_email(user.get('email'))
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if db_user.get("blocked"):
        raise HTTPException(status_code=403, detail="Account is blocked")
    if not verify_password(user.get('password'), db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user["email"], "role": db_user["role"], "id": db_user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}
