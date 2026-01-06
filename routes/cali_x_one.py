# routes/cali_x_one.py
"""
CALI X One Routes - Host Bubble API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from server.auth import get_current_user
from models.user import User
from cali_scripts.host_bubble import host_bubble

router = APIRouter(prefix="/api/cali-x-one", tags=["CALI X One"])

@router.post("/session/start")
async def start_cognitive_session(
    context: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """
    Start a new CALI X One cognitive session
    """
    try:
        session_id = await host_bubble.initialize_session(str(current_user.id), context)
        return {
            "session_id": session_id,
            "status": "started",
            "message": "Cognitive session initialized"
        }
    except Exception as e:
        raise HTTPException(500, f"Failed to start session: {str(e)}")

@router.post("/session/{session_id}/cluster")
async def process_skg_cluster(
    session_id: str,
    cluster_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """
    Process SKG cluster data through Host Bubble
    """
    try:
        result = await host_bubble.process_skg_cluster(session_id, cluster_data)
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, f"Failed to process cluster: {str(e)}")

@router.post("/session/{session_id}/end")
async def end_cognitive_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    End cognitive session and get summary
    """
    try:
        summary = await host_bubble.end_session(session_id)
        return {
            "summary": summary,
            "message": "Session ended successfully"
        }
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, f"Failed to end session: {str(e)}")

@router.get("/status")
async def get_host_bubble_status(current_user: User = Depends(get_current_user)):
    """
    Get Host Bubble status and active sessions
    """
    return {
        "active_sessions": len(host_bubble.active_sessions),
        "cognitive_cycles": len(host_bubble.cognitive_cycles),
        "status": "operational"
    }