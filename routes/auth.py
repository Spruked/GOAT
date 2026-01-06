# routes/auth.py
"""
Authentication routes for GOAT
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from server.auth import (
    User, UserCreate, UserLogin, Token,
    authenticate_user, create_user, create_access_token,
    get_user, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user_dependency(token: str = Depends(oauth2_scheme)):
    """Dependency to get current user from token"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = verify_token(token)
    if user is None:
        raise credentials_exception
    return user

@router.post("/auth/signup", response_model=User)
async def signup(user: UserCreate):
    """Create a new user account"""
    db_user = create_user(user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user

@router.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    # Admin bypass
    if form_data.username == "admin@goat.local" and form_data.password == "goat2024admin":
        access_token = create_access_token(
            data={"sub": "admin@goat.local", "is_admin": True}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/me", response_model=User)
async def get_current_user(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@router.put("/auth/profile")
async def update_profile(updates: dict, current_user: User = Depends(get_current_user)):
    """Update user profile"""
    # This route is deprecated - use /user/profile instead
    from models import SessionLocal
    db = SessionLocal()
    try:
        # Allowed fields for update
        allowed_fields = ['display_name', 'username', 'bio', 'profile_image', 'cover_image']

        for field in allowed_fields:
            if field in updates:
                setattr(current_user, field, updates[field])

        db.commit()
        return {"message": "Profile updated successfully"}
    finally:
        db.close()

@router.get("/auth/projects")
async def get_user_projects(current_user: User = Depends(get_current_user)):
    """Get user's projects"""
    # TODO: Implement project listing from database
    # For now, return empty list
    return {"projects": []}

@router.get("/user/files")
async def get_user_files(current_user: dict = Depends(get_current_user_dependency)):
    """Get user's uploaded files and processing status"""
    from user_tracker import user_tracker

    # Get user's files from database
    files_data = user_tracker.get_user_files(current_user['user_id'])

    # Separate processed and unprocessed files
    processed = []
    unprocessed = []

    for file_info in files_data.get('files', []):
        if file_info.get('status') == 'processed':
            processed.append(file_info)
        else:
            unprocessed.append(file_info)

    return {
        "processed": processed,
        "unprocessed": unprocessed,
        "total_files": len(processed) + len(unprocessed)
    }

@router.post("/auth/projects/{project_id}/export")
async def export_project_data(project_id: str, current_user: User = Depends(get_current_user)):
    """Export project data"""
    # TODO: Implement data export functionality
    raise HTTPException(status_code=501, detail="Export functionality not yet implemented")