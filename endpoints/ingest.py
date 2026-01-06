# endpoints/ingest.py
"""
Ingest endpoint for GOAT
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class IngestRequest(BaseModel):
    data: Dict[str, Any]
    source: str = "api"

@router.post("/ingest")
async def ingest_data(request: IngestRequest):
    """Ingest data into GOAT system"""
    try:
        # Simple ingest - just return success for now
        return {
            "status": "success",
            "message": f"Data ingested from {request.source}",
            "data": request.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingest failed: {str(e)}")