# backend/app/api/v1/endpoints/admin.py
"""
Admin endpoints for SKG
"""

from fastapi import APIRouter, Depends
from app.security.auth import dual_auth

router = APIRouter()

@router.get("/tenants")
async def list_tenants(token: dict = Depends(dual_auth)):
    """List all tenants"""
    return {"tenants": ["default"]}

@router.post("/backup")
async def create_backup(token: dict = Depends(dual_auth)):
    """Create system backup"""
    return {"status": "backup_created", "timestamp": "2025-12-08T00:00:00Z"}