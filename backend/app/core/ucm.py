# backend/app/core/ucm.py
"""
Minimal UCM health check utility for GOAT backend
"""

import os
import requests

UCM_BASE_URL = os.getenv("UCM_BASE_URL", "http://localhost:8000")


def ucm_health_check():
    """Ping the UCM health endpoint and return status dict"""
    try:
        resp = requests.get(f"{UCM_BASE_URL}/health", timeout=2)
        if resp.status_code == 200:
            return {"status": "healthy", **resp.json()}
        return {"status": "unhealthy", "code": resp.status_code}
    except Exception as e:
        return {"status": "error", "error": str(e)}
