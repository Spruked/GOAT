"""
APEX DOC Status Polling Endpoint.

Implements the GET /v1/certify/{apex_request_id}/status endpoint
for asynchronous certification status checking.
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter()

# Mock status storage - in production, this would be a database
_certification_statuses = {}

def update_certification_status(apex_request_id: str, status_data: Dict[str, Any]):
    """Update certification status (called by orchestrator)."""
    _certification_statuses[apex_request_id] = status_data

@router.get("/v1/certify/{apex_request_id}/status")
async def get_certification_status(apex_request_id: str) -> Dict[str, Any]:
    """
    Poll certification status.

    Returns current status of certification request.
    """
    if apex_request_id not in _certification_statuses:
        raise HTTPException(status_code=404, detail="Certification request not found")

    status_data = _certification_statuses[apex_request_id]

    # Build response based on current status
    response = {
        "apex_request_id": apex_request_id,
        "bundle_id": status_data.get("bundle_id", ""),
        "status": status_data["status"],
        "timestamps": {
            "submitted": status_data.get("submitted_at", ""),
            "started": status_data.get("started_at", ""),
            "completed": status_data.get("completed_at", "")
        }
    }

    # Add status-specific fields
    if status_data["status"] == "PROCESSING":
        # Add progress information
        response["progress"] = {
            "current_layer": status_data.get("current_layer", 0),
            "total_layers": 13,
            "estimated_seconds_remaining": status_data.get("estimated_seconds_remaining", 0)
        }
    elif status_data["status"] == "COMPLETED":
        response["result"] = status_data.get("result", {})
    elif status_data["status"] in ["REJECTED", "FAILED"]:
        if status_data["status"] == "REJECTED":
            response["rejection_reasons"] = status_data.get("result", {}).get("rejection_reasons", [])
        else:
            response["error"] = status_data.get("error", "Unknown error")

    return response

# Example status updates for testing
async def simulate_certification_progress(apex_request_id: str, bundle_id: str):
    """Simulate certification progress for testing."""

    # Initial status
    update_certification_status(apex_request_id, {
        "bundle_id": bundle_id,
        "status": "PENDING_VALIDATION",
        "submitted_at": datetime.utcnow().isoformat() + "Z"
    })

    await asyncio.sleep(1)

    # Start processing
    update_certification_status(apex_request_id, {
        "bundle_id": bundle_id,
        "status": "PROCESSING",
        "submitted_at": datetime.utcnow().isoformat() + "Z",
        "started_at": datetime.utcnow().isoformat() + "Z",
        "current_layer": 1,
        "estimated_seconds_remaining": 45
    })

    # Simulate layer progress
    for layer in range(2, 14):
        await asyncio.sleep(0.5)
        update_certification_status(apex_request_id, {
            "bundle_id": bundle_id,
            "status": "PROCESSING",
            "submitted_at": datetime.utcnow().isoformat() + "Z",
            "started_at": datetime.utcnow().isoformat() + "Z",
            "current_layer": layer,
            "estimated_seconds_remaining": max(0, 45 - (layer * 3))
        })

    # Complete
    update_certification_status(apex_request_id, {
        "bundle_id": bundle_id,
        "status": "COMPLETED",
        "submitted_at": datetime.utcnow().isoformat() + "Z",
        "started_at": datetime.utcnow().isoformat() + "Z",
        "completed_at": datetime.utcnow().isoformat() + "Z",
        "result": {
            "certificate_id": f"APEX-CERT-{apex_request_id.split('-')[-1]}",
            "layers_certified": 13,
            "confidence_score": 0.95
        }
    })