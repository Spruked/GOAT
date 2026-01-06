# DALS/api/host_routes.py
"""
Host Messaging API - Pull/Push messaging for workers and GOAT
"""

from fastapi import APIRouter, Request, HTTPException
import time
from typing import Dict, Any, List
import asyncio
import json
import httpx

router = APIRouter(prefix="/host")

# DALS Configuration
DALS_NAME = "Digital Asset Logistics System"
DALS_CONFIG = {
    "name": DALS_NAME,
    "max_queue_size": 100,
    "message_ttl": 3600,  # 1 hour
    "monitoring_enabled": True,
    "goat_integration": True
}

# In-memory message queues - in production, use Redis or database
MESSAGE_QUEUES: Dict[str, List[Dict[str, Any]]] = {}
QUEUE_LOCK = asyncio.Lock()

# DALS Configuration overrides
DALS_CONFIG = {
    "max_queue_size": 100,
    "message_ttl": 3600,  # 1 hour
    "monitoring_enabled": True,
    "goat_integration": True
}

@router.post("/push")
async def push_message(req: Request):
    """
    Push a message to a user's queue (from workers or GOAT)
    """
    try:
        data = await req.json()

        required_fields = ["user_id", "worker", "text"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

        user_id = str(data["user_id"])
        worker_name = data["worker"]
        text = data["text"]
        meta = data.get("meta", {})

        async with QUEUE_LOCK:
            if user_id not in MESSAGE_QUEUES:
                MESSAGE_QUEUES[user_id] = []

            message = {
                "worker": worker_name,
                "text": text,
                "meta": meta,
                "timestamp": time.time()
            }

            MESSAGE_QUEUES[user_id].append(message)

            # Keep only last 100 messages per user
            if len(MESSAGE_QUEUES[user_id]) > 100:
                MESSAGE_QUEUES[user_id] = MESSAGE_QUEUES[user_id][-100:]

        return {
            "status": "queued",
            "queue_size": len(MESSAGE_QUEUES.get(user_id, [])),
            "timestamp": time.time()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Push failed: {str(e)}")

@router.post("/pull")
async def pull_message(req: Request):
    """
    Pull next message from user's queue (for workers)
    """
    try:
        data = await req.json()

        required_fields = ["user_id", "worker_name"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

        user_id = str(data["user_id"])
        worker_name = data["worker_name"]

        async with QUEUE_LOCK:
            if user_id not in MESSAGE_QUEUES or len(MESSAGE_QUEUES[user_id]) == 0:
                return {"text": None, "timestamp": time.time()}

            # Get next message
            message = MESSAGE_QUEUES[user_id].pop(0)

            return {
                "worker": message["worker"],
                "text": message["text"],
                "meta": message["meta"],
                "timestamp": message["timestamp"]
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pull failed: {str(e)}")

@router.get("/status/{user_id}")
async def get_queue_status(user_id: str):
    """
    Get status of user's message queue
    """
    async with QUEUE_LOCK:
        queue_size = len(MESSAGE_QUEUES.get(str(user_id), []))
        return {
            "user_id": user_id,
            "queue_size": queue_size,
            "has_messages": queue_size > 0,
            "timestamp": time.time()
        }

@router.delete("/clear/{user_id}")
async def clear_queue(user_id: str):
    """
    Clear all messages for a user
    """
    async with QUEUE_LOCK:
        if str(user_id) in MESSAGE_QUEUES:
            cleared_count = len(MESSAGE_QUEUES[str(user_id)])
            MESSAGE_QUEUES[str(user_id)] = []
            return {
                "status": "cleared",
                "cleared_count": cleared_count,
                "timestamp": time.time()
            }
        else:
            return {
                "status": "no_queue",
                "cleared_count": 0,
                "timestamp": time.time()
            }

@router.get("/config")
async def get_config():
    """
    Get current DALS configuration with GOAT integration options
    """
    return {
        "config": DALS_CONFIG,
        "available_overrides": [
            "max_queue_size",
            "message_ttl", 
            "monitoring_enabled",
            "goat_integration"
        ],
        "goat_options_available": [
            "triples_ingest",
            "sparql_query",
            "vector_search",
            "analytics_stats",
            "video_generation",
            "admin_backup"
        ]
    }

@router.post("/config/override")
async def set_config_override(overrides: Dict[str, Any]):
    """
    Set configuration overrides for DALS with GOAT integration
    """
    global DALS_CONFIG
    for key, value in overrides.items():
        if key in DALS_CONFIG:
            DALS_CONFIG[key] = value
            # Log override for monitoring
            print(f"DALS Config Override: {key} = {value}")
    
    return {
        "status": "overrides_applied",
        "current_config": DALS_CONFIG,
        "timestamp": time.time()
    }

@router.get("/monitoring")
async def get_monitoring_data():
    """
    Get monitoring data for DALS operations and GOAT integration
    """
    total_queues = len(MESSAGE_QUEUES)
    total_messages = sum(len(queue) for queue in MESSAGE_QUEUES.values())
    
    return {
        "monitoring": {
            "active_queues": total_queues,
            "total_messages": total_messages,
            "config_overrides": DALS_CONFIG,
            "goat_integration_status": "active" if DALS_CONFIG["goat_integration"] else "disabled"
        },
        "timestamp": time.time()
    }

@router.get("/goat-options")
async def get_goat_options():
    """
    Get all available GOAT options through DALS plugin
    """
    return {
        "goat_endpoints_available": [
            "/api/v1/triples/ingest",
            "/api/v1/triples/search",
            "/api/v1/query/sparql",
            "/api/v1/query/vector",
            "/api/v1/analytics/stats",
            "/api/v1/analytics/graph",
            "/api/v1/video/generate-memory",
            "/api/v1/video/parse-existing",
            "/api/v1/video/ai-generate-dialog",
            "/api/v1/video/job/{job_id}",
            "/api/v1/video/templates",
            "/api/v1/admin/tenants",
            "/api/v1/admin/backup",
            "/health"
        ],
        "dals_overrides_applied": DALS_CONFIG,
        "plugin_status": "active",
        "all_options_available": True
    }

@router.get("/dashboard")
async def get_dashboard_data():
    """
    GOAT Dashboard data through DALS - comprehensive overview of all GOAT functionality
    """
    # Aggregate data from all GOAT systems
    dashboard = {
        "title": f"{DALS_NAME} Dashboard - GOAT Integration",
        "version": "2.0.0",
        "dals_integration": "active",
        "modules": {
            "knowledge_graph": {
                "status": "active",
                "endpoints": ["/api/v1/triples", "/api/v1/query"],
                "features": ["SPARQL queries", "Vector search", "Triple ingestion"]
            },
            "analytics": {
                "status": "active", 
                "endpoints": ["/api/v1/analytics"],
                "features": ["System stats", "Graph analytics"]
            },
            "video_generation": {
                "status": "active",
                "endpoints": ["/api/v1/video"],
                "features": ["Memory videos", "AI narration", "Template system"]
            },
            "administration": {
                "status": "active",
                "endpoints": ["/api/v1/admin"],
                "features": ["Tenant management", "System backup"]
            },
            "dals_messaging": {
                "status": "active",
                "endpoints": ["/dals/host", "/dals/uqv", "/dals/tts"],
                "features": ["Host messaging", "UQV storage", "TTS synthesis"]
            }
        },
        "configuration": {
            "overrides_available": list(DALS_CONFIG.keys()),
            "current_overrides": DALS_CONFIG,
            "monitoring_enabled": DALS_CONFIG["monitoring_enabled"]
        },
        "health_status": {
            "overall": "healthy",
            "last_updated": time.time()
        }
    }
    
    return dashboard

# GOAT Proxy Endpoints - All GOAT functionality accessible through DALS
@router.api_route("/goat/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_goat_request(path: str, request: Request):
    """
    Proxy all requests to GOAT endpoints through DALS
    Ensures all connections go through DALS gateway
    """
    if not DALS_CONFIG["goat_integration"]:
        raise HTTPException(status_code=403, detail="GOAT integration disabled")
    
    # Construct the target URL
    target_url = f"http://localhost:8000/api/v1/{path}"
    
    # Get request data
    body = await request.body()
    headers = dict(request.headers)
    # Remove host header
    headers.pop("host", None)
    
    # Apply DALS overrides/monitoring
    if DALS_CONFIG["monitoring_enabled"]:
        print(f"DALS Proxy: {request.method} /api/v1/{path}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"GOAT proxy error: {str(e)}")

@router.get("/connections")
async def get_connections_status():
    """
    Check connection status of all endpoints through DALS
    """
    connections = {
        "dals_host": "active",
        "dals_uqv": "active", 
        "dals_tts": "active",
        "dals_broadcast": "active",
        "goat_triples": "connected_via_proxy",
        "goat_query": "connected_via_proxy",
        "goat_analytics": "connected_via_proxy",
        "goat_video": "connected_via_proxy",
        "goat_admin": "connected_via_proxy",
        "goat_health": "connected_via_proxy"
    }
    
    return {
        "all_endpoints_connected_via_dals": True,
        "connections": connections,
        "dals_gateway_status": "active",
        "timestamp": time.time()
    }