# routes/user.py
"""
Enhanced user routes for GOAT dashboard
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
import shutil
from pathlib import Path

from models import get_db, User, UserFile
from server.auth import get_current_user

router = APIRouter()

# File upload directory
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.get("/user/profile")
async def get_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get full user profile with stats"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "display_name": current_user.display_name,
        "username": current_user.username,
        "bio": current_user.bio,
        "profile_image": current_user.profile_image,
        "cover_image": current_user.cover_image,
        "theme": current_user.theme,
        "accent_color": current_user.accent_color,
        "ui_mode": current_user.ui_mode,
        "preferences": current_user.preferences,
        "stats": current_user.stats,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "last_active_at": current_user.last_active_at.isoformat() if current_user.last_active_at else None
    }

@router.patch("/user/profile")
async def update_user_profile(
    updates: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    # Allowed fields for update
    allowed_fields = [
        'display_name', 'username', 'bio', 'profile_image', 'cover_image',
        'theme', 'accent_color', 'ui_mode', 'preferences'
    ]

    for field in allowed_fields:
        if field in updates:
            setattr(current_user, field, updates[field])

    current_user.updated_at = datetime.utcnow()
    db.commit()

    return {"message": "Profile updated successfully"}

@router.post("/user/preferences")
async def update_user_preferences(
    preferences: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    # Merge with existing preferences
    current_prefs = current_user.preferences or {}
    current_prefs.update(preferences)
    current_user.preferences = current_prefs

    current_user.updated_at = datetime.utcnow()
    db.commit()

    return {"message": "Preferences updated successfully"}

@router.get("/user/files")
async def get_user_files(
    status: Optional[str] = Query(None, description="Filter by status: uploaded, processing, processed, failed"),
    file_type: Optional[str] = Query(None, description="Filter by file type"),
    favorite: Optional[bool] = Query(None, description="Filter favorites only"),
    search: Optional[str] = Query(None, description="Search in filename and tags"),
    limit: int = Query(50, description="Limit results"),
    offset: Optional[int] = Query(None, description="Offset for pagination (legacy)"),
    page: Optional[int] = Query(None, description="Page number for pagination (0-based)"),
    sort_by: Optional[str] = Query("created_at", description="Sort field"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's files with filtering, search, and pagination"""
    query = db.query(UserFile).filter(UserFile.user_id == current_user.id)

    # Apply filters
    if status:
        query = query.filter(UserFile.status == status)
    if file_type:
        query = query.filter(UserFile.file_type == file_type)
    if favorite is not None:
        query = query.filter(UserFile.is_favorite == favorite)

    # Search functionality
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (UserFile.original_filename.ilike(search_term)) |
            (UserFile.clean_filename.ilike(search_term)) |
            (UserFile.tags.any(search_term))
        )

    # Get total count for pagination
    total = query.count()

    # Apply sorting
    sort_column = getattr(UserFile, sort_by, UserFile.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    if page is not None:
        # Page-based pagination (for infinite scroll)
        offset = page * limit
    elif offset is None:
        offset = 0

    files = query.offset(offset).limit(limit).all()

    # Get user stats
    user = db.query(User).filter(User.id == current_user.id).first()
    stats = user.stats if user else {}

    return {
        "stats": stats,
        "files": [
            {
                "id": f.id,
                "original_filename": f.original_filename,
                "clean_filename": f.clean_filename,
                "display_name": f.display_name,
                "file_type": f.file_type,
                "file_size": f.file_size,
                "file_size_display": f.file_size_display,
                "status": f.status,
                "status_color": f.status_color,
                "storage_path": f.storage_path,
                "thumbnail_path": f.thumbnail_path,
                "preview_available": f.preview_available,
                "tags": f.tags,
                "is_favorite": f.is_favorite,
                "is_image": f.is_image,
                "is_document": f.is_document,
                "mime_type": f.mime_type,
                "created_at": f.created_at.isoformat() if f.created_at else None,
                "updated_at": f.updated_at.isoformat() if f.updated_at else None,
                "processed_at": f.processed_at.isoformat() if f.processed_at else None,
                "downloaded_at": f.downloaded_at.isoformat() if f.downloaded_at else None
            }
            for f in files
        ],
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "page": page if page is not None else (offset // limit),
            "has_more": offset + limit < total
        }
    }

@router.post("/user/files/{file_id}/favorite")
async def toggle_file_favorite(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle favorite status of a file"""
    file = db.query(UserFile).filter(
        UserFile.id == file_id,
        UserFile.user_id == current_user.id
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.is_favorite = not file.is_favorite
    db.commit()

    return {"is_favorite": file.is_favorite}

@router.delete("/user/files/{file_id}")
async def delete_user_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a user file"""
    file = db.query(UserFile).filter(
        UserFile.id == file_id,
        UserFile.user_id == current_user.id
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Delete physical file if it exists
    if file.storage_path and os.path.exists(file.storage_path):
        os.remove(file.storage_path)
    if file.processed_path and os.path.exists(file.processed_path):
        os.remove(file.processed_path)
    if file.thumbnail_path and os.path.exists(file.thumbnail_path):
        os.remove(file.thumbnail_path)

    # Delete from database
    db.delete(file)

    # Update user file count
    current_user.file_count = max(0, current_user.file_count - 1)
    if file.status == 'processed':
        current_user.processed_count = max(0, current_user.processed_count - 1)

    db.commit()

    return {"message": "File deleted successfully"}

@router.post("/user/files/{file_id}/rename")
async def rename_user_file(
    file_id: int,
    new_name: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rename a user file"""
    file = db.query(UserFile).filter(
        UserFile.id == file_id,
        UserFile.user_id == current_user.id
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.clean_filename = new_name
    db.commit()

    return {"message": "File renamed successfully"}

@router.get("/files/{file_id}/preview")
async def get_file_preview(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Stream file preview (PDF/image)"""
    file = db.query(UserFile).filter(
        UserFile.id == file_id,
        UserFile.user_id == current_user.id
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if not file.preview_available or not file.processed_path:
        raise HTTPException(status_code=404, detail="Preview not available")

    if not os.path.exists(file.processed_path):
        raise HTTPException(status_code=404, detail="Preview file not found")

    def file_generator():
        with open(file.processed_path, "rb") as f:
            while chunk := f.read(8192):
                yield chunk

    # Determine content type
    content_type = "application/pdf" if file.file_type == "pdf" else f"image/{file.file_type}"

    return StreamingResponse(
        file_generator(),
        media_type=content_type,
        headers={"Content-Disposition": f"inline; filename={file.display_name}"}
    )