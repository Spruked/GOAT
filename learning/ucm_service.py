#!/usr/bin/env python3
"""
UCM Service - Universal Cognitive Model Service
Deploys cognitive workers to GOAT departments via Caleon bubble
"""

import os
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from pathlib import Path

from .difficulty_engine import DifficultyEngine
from .event_logger import EventLogger

class CognitiveEngine:
    """Simple cognitive engine for UCM service"""
    def __init__(self):
        self.active_workers = []
        self.cycle_count = 0

    def get_cycle_status(self):
        return "active"

    async def process_learning_cycle(self, content):
        self.cycle_count += 1
        return {"processed": True, "cycle": self.cycle_count}

app = FastAPI(title="UCM Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
cognitive_engine = CognitiveEngine()
difficulty_engine = DifficultyEngine()
event_logger = EventLogger()

# DALS (Distributed Agent Learning System) - manages worker deployment
class DALS:
    def __init__(self):
        self.dals_endpoint = os.getenv("DALS_ENDPOINT", "http://backend:5000")
        self.api_key = os.getenv("UCM_API_KEY", "ucm_secret_key")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def deploy_worker_to_department(self, department: str, worker_config: Dict[str, Any]) -> bool:
        """Deploy a cognitive worker to a GOAT department"""
        try:
            payload = {
                "department": department,
                "worker_type": "cognitive_agent",
                "config": worker_config,
                "ucm_source": True,
                "timestamp": datetime.utcnow().isoformat()
            }

            response = self.session.post(
                f"{self.dals_endpoint}/api/ucm/deploy-worker",
                json=payload
            )

            if response.status_code == 200:
                print(f"✓ Deployed cognitive worker to {department}")
                return True
            else:
                print(f"✗ Failed to deploy worker to {department}: {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ DALS deployment error: {e}")
            return False

    def get_department_status(self, department: str) -> Dict[str, Any]:
        """Get status of a GOAT department"""
        try:
            response = self.session.get(f"{self.dals_endpoint}/api/departments/{department}/status")
            if response.status_code == 200:
                return response.json()
            return {"status": "unknown", "workers": []}
        except Exception as e:
            return {"status": "error", "error": str(e)}

dals = DALS()

# Department configurations for worker deployment
DEPARTMENTS = {
    "audiobook": {
        "description": "Audiobook generation and processing",
        "worker_types": ["ssml_converter", "audio_builder", "stitching_engine"]
    },
    "podcast": {
        "description": "Podcast creation and management",
        "worker_types": ["dialogue_detector", "segmenter", "voice_synthesizer"]
    },
    "knowledge": {
        "description": "Knowledge graph and learning systems",
        "worker_types": ["graph_builder", "embedding_engine", "reasoning_agent"]
    },
    "caleon": {
        "description": "Caleon generative bubble",
        "worker_types": ["generative_agent", "creativity_engine", "innovation_worker"]
    }
}

@app.get("/health")
async def health_check():
    """UCM service health check"""
    return {
        "status": "healthy",
        "service": "UCM",
        "timestamp": datetime.utcnow().isoformat(),
        "dals_connected": dals.get_department_status("audiobook")["status"] != "error"
    }

@app.get("/api/departments")
async def list_departments():
    """List available GOAT departments for worker deployment"""
    return {
        "departments": DEPARTMENTS,
        "dals_endpoint": dals.dals_endpoint
    }

@app.post("/api/deploy/{department}")
async def deploy_workers_to_department(department: str, background_tasks: BackgroundTasks):
    """Deploy cognitive workers to a specific GOAT department"""
    if department not in DEPARTMENTS:
        raise HTTPException(status_code=404, detail=f"Department {department} not found")

    # Deploy workers in background
    background_tasks.add_task(deploy_workers_async, department)

    return {
        "message": f"Deploying cognitive workers to {department}",
        "department": department,
        "worker_types": DEPARTMENTS[department]["worker_types"],
        "status": "initiated"
    }

async def deploy_workers_async(department: str):
    """Asynchronously deploy workers to department"""
    dept_config = DEPARTMENTS[department]

    for worker_type in dept_config["worker_types"]:
        worker_config = {
            "type": worker_type,
            "department": department,
            "cognitive_capabilities": ["learning", "reasoning", "adaptation"],
            "memory_system": "graph_based",
            "communication_protocol": "glyph_tracing",
            "deployment_time": datetime.utcnow().isoformat()
        }

        success = dals.deploy_worker_to_department(department, worker_config)

        if success:
            # Log successful deployment
            event_logger.log_event(
                event_type="worker_deployment",
                details={
                    "department": department,
                    "worker_type": worker_type,
                    "status": "success"
                }
            )
        else:
            # Log failed deployment
            event_logger.log_event(
                event_type="worker_deployment_failed",
                details={
                    "department": department,
                    "worker_type": worker_type,
                    "status": "failed"
                }
            )

@app.get("/api/cognition/cycle")
async def get_cognitive_cycle():
    """Get current cognitive cycle status"""
    return {
        "cycle_status": "active",
        "active_workers": 0,  # TODO: Implement worker tracking
        "learning_metrics": difficulty_engine.get_metrics(),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/cognition/learn")
async def trigger_learning_cycle(content: Dict[str, Any]):
    """Trigger a learning cycle in the cognitive engine"""
    try:
        # Use the cognitive engine to process content
        result = await cognitive_engine.process_learning_cycle(content)
        return {
            "result": result,
            "cycle_completed": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning cycle failed: {str(e)}")

@app.get("/api/workers/status")
async def get_worker_status():
    """Get status of all deployed workers across departments"""
    status = {}
    for dept in DEPARTMENTS.keys():
        status[dept] = dals.get_department_status(dept)

    return {
        "worker_status": status,
        "total_departments": len(DEPARTMENTS),
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting UCM Service on port {port}")
    print(f"📡 Connecting to DALS at: {dals.dals_endpoint}")

    uvicorn.run(
        "learning.ucm_service:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )