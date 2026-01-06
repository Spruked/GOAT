#!/usr/bin/env python3
"""
UCM Routes - FastAPI endpoints for UCM integration
"""

import os
import requests
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from datetime import datetime

router = APIRouter(prefix="/api/ucm", tags=["UCM Integration"])

# UCM service connection
UCM_ENDPOINT = os.getenv("UCM_ENDPOINT", "http://ucm:8080")
UCM_API_KEY = os.getenv("UCM_API_KEY", "ucm_secret_key")

class UCMClient:
    def __init__(self):
        self.endpoint = UCM_ENDPOINT
        self.api_key = UCM_API_KEY
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def get_health(self) -> Dict[str, Any]:
        """Check UCM service health"""
        try:
            response = self.session.get(f"{self.endpoint}/health")
            return response.json() if response.status_code == 200 else {"status": "unhealthy"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def deploy_workers(self, department: str) -> Dict[str, Any]:
        """Deploy cognitive workers to a department"""
        try:
            response = self.session.post(f"{self.endpoint}/api/deploy/{department}")
            return response.json() if response.status_code == 200 else {"error": "deployment_failed"}
        except Exception as e:
            return {"error": str(e)}

    def get_cognitive_cycle(self) -> Dict[str, Any]:
        """Get current cognitive cycle status"""
        try:
            response = self.session.get(f"{self.endpoint}/api/cognition/cycle")
            return response.json() if response.status_code == 200 else {"error": "cycle_unavailable"}
        except Exception as e:
            return {"error": str(e)}

    def trigger_learning(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger a learning cycle"""
        try:
            response = self.session.post(f"{self.endpoint}/api/cognition/learn", json=content)
            return response.json() if response.status_code == 200 else {"error": "learning_failed"}
        except Exception as e:
            return {"error": str(e)}

    def get_worker_status(self) -> Dict[str, Any]:
        """Get status of all deployed workers"""
        try:
            response = self.session.get(f"{self.endpoint}/api/workers/status")
            return response.json() if response.status_code == 200 else {"error": "status_unavailable"}
        except Exception as e:
            return {"error": str(e)}

ucm_client = UCMClient()

@router.get("/health")
async def ucm_health():
    """UCM service health check"""
    health = ucm_client.get_health()
    return {
        "service": "UCM Integration",
        "ucm_status": health,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/deploy/{department}")
async def deploy_to_department(department: str):
    """Deploy cognitive workers to a GOAT department"""
    result = ucm_client.deploy_workers(department)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return {
        "message": f"Cognitive workers deployed to {department}",
        "result": result,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/cognition/cycle")
async def get_cognitive_cycle():
    """Get current cognitive cycle status"""
    cycle = ucm_client.get_cognitive_cycle()
    return cycle

@router.post("/cognition/learn")
async def trigger_learning(content: Dict[str, Any]):
    """Trigger a learning cycle with provided content"""
    result = ucm_client.trigger_learning(content)
    return result

@router.get("/workers/status")
async def get_workers_status():
    """Get status of all deployed cognitive workers"""
    status = ucm_client.get_worker_status()
    return status

@router.post("/deploy-worker")
async def deploy_worker(worker_data: Dict[str, Any]):
    """Handle worker deployment from UCM service"""
    department = worker_data.get("department")
    worker_type = worker_data.get("worker_type")
    config = worker_data.get("config", {})

    if not department or not worker_type:
        raise HTTPException(status_code=400, detail="Missing department or worker_type")

    # Here we would integrate with the actual department systems
    # For now, just log the deployment
    print(f"🚀 Deploying {worker_type} worker to {department} department")
    print(f"📋 Worker config: {config}")

    # In a full implementation, this would:
    # 1. Register the worker with the department's worker manager
    # 2. Initialize worker state and capabilities
    # 3. Connect worker to department's communication channels
    # 4. Start worker processes/services

    return {
        "status": "deployed",
        "department": department,
        "worker_type": worker_type,
        "worker_id": f"{department}_{worker_type}_{int(datetime.utcnow().timestamp())}",
        "timestamp": datetime.utcnow().isoformat()
    }