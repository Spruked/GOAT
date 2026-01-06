# backend/app/security/auth.py
"""
Authentication and authorization for SKG GOAT
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

security = HTTPBearer()

def dual_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dual authentication: API key or JWT token
    """
    token = credentials.credentials

    # For now, accept any token (simplified)
    # In production, validate JWT or API key
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return tenant info
    return {
        "tenant_id": "default",
        "user_id": "user_123",
        "permissions": ["read", "write"]
    }