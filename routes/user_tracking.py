# routes/user_tracking.py
"""
User tracking and analytics routes for GOAT
"""

from fastapi import APIRouter, Depends, HTTPException
from routes.auth import get_current_user_dependency
from user_tracker import user_tracker
from typing import Dict, Any, List

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/customer/{user_id}")
async def get_customer_data(user_id: str, current_user: dict = Depends(get_current_user_dependency)):
    """Get customer data for a specific user"""
    # Only allow users to see their own data or admins
    if current_user.get('email') != user_id and current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Access denied")
    
    data = user_tracker.get_customer_data(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return data

@router.get("/customers")
async def get_all_customers(current_user: dict = Depends(get_current_user_dependency)):
    """Get all customer data (admin only)"""
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user_tracker.get_customer_data()

@router.get("/platforms")
async def get_platform_stats(current_user: dict = Depends(get_current_user_dependency)):
    """Get platform visit statistics"""
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user_tracker.get_platform_stats()

@router.get("/visits/{user_id}")
async def get_user_visits(
    user_id: str,
    platform: str = None,
    limit: int = 50,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get visit history for a user"""
    if current_user.get('email') != user_id and current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Access denied")
    
    return user_tracker.get_visit_history(user_id, platform, limit)

@router.post("/track-visit")
async def track_visit(
    platform: str,
    page_url: str = None,
    referrer: str = None,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Manually track a visit (for frontend integration)"""
    user_tracker.track_visit(
        user_id=current_user.get('email', 'anonymous'),
        platform=platform,
        page_url=page_url,
        referrer=referrer
    )
    return {"status": "visit tracked"}