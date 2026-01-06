"""
GOAT Guest Routes - Interview Invitations
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime, timedelta
import secrets
from server.auth import get_current_user
from models.user import User

router = APIRouter()

class GuestInvite(BaseModel):
    host_name: str
    guest_email: Optional[str] = None
    guest_name: Optional[str] = None
    session_title: str
    description: Optional[str] = None
    scheduled_time: Optional[datetime] = None

class GuestSession(BaseModel):
    invite_token: str
    host_name: str
    session_title: str
    status: str  # pending, active, completed
    created_at: datetime
    expires_at: datetime

# In-memory store (use DB in production)
guest_sessions = {}

@router.post("/invite")
async def create_guest_invite(invite: GuestInvite, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
    """
    Create a guest invite link for interviews
    """
    try:
        # Generate secure token
        invite_token = secrets.token_urlsafe(32)

        # Create session
        session = GuestSession(
            invite_token=invite_token,
            host_name=invite.host_name,
            session_title=invite.session_title,
            status="pending",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=7)  # 7 days expiry
        )

        guest_sessions[invite_token] = session

        # TODO: Send email invitation if email provided
        # TODO: Generate shareable link

        invite_url = f"/guest/join/{invite_token}"

        return {
            "status": "created",
            "invite_token": invite_token,
            "invite_url": invite_url,
            "expires_at": session.expires_at.isoformat(),
            "message": "Guest invite created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create invite: {str(e)}")

@router.get("/join/{invite_token}")
async def get_guest_session(invite_token: str):
    """
    Get guest session details for joining
    """
    session = guest_sessions.get(invite_token)
    if not session:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    if datetime.utcnow() > session.expires_at:
        raise HTTPException(status_code=410, detail="Invite has expired")

    return {
        "host_name": session.host_name,
        "session_title": session.session_title,
        "status": session.status,
        "created_at": session.created_at.isoformat(),
        "expires_at": session.expires_at.isoformat()
    }

@router.post("/join/{invite_token}/start")
async def start_guest_session(invite_token: str, background_tasks: BackgroundTasks):
    """
    Start the guest interview session
    """
    session = guest_sessions.get(invite_token)
    if not session:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    if session.status != "pending":
        raise HTTPException(status_code=400, detail="Session already started or completed")

    try:
        session.status = "active"

        # TODO: Initialize recording for guest session
        # TODO: Connect to DALS for streaming
        # TODO: Notify host

        return {
            "status": "started",
            "session_title": session.session_title,
            "message": "Interview session started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")

@router.get("/sessions")
async def list_guest_sessions():
    """
    List all guest sessions (for host dashboard)
    """
    return list(guest_sessions.values())