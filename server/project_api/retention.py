import os
from fastapi import APIRouter

router = APIRouter()

@router.post('/api/project/set-retention')
def set_retention(project_id: str, retention: str):
    """Set the retention policy for a project (temporary, local, server, blockchain)."""
    # In production, store this in project.gproj or DB
    # Here, just return for demo
    return { 'project_id': project_id, 'retention': retention, 'message': 'Retention policy set (demo)' }
