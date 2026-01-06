# backend/app/api/v1/endpoints/analytics.py
"""
Analytics endpoints for SKG
"""

from fastapi import APIRouter, Depends
from app.security.auth import dual_auth

router = APIRouter()

@router.get("/stats")
async def get_stats(token: dict = Depends(dual_auth)):
    """Get system statistics"""
    return {"triples": 0, "queries": 0, "users": 1}

@router.get("/graph")
async def graph_analytics(token: dict = Depends(dual_auth)):
    """Graph analytics data"""
    return {"nodes": 0, "edges": 0, "communities": []}