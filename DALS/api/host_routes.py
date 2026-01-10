# DALS/api/host_routes.py
"""
GOAT Gateway - Intelligent proxy with health checks, policy enforcement, and feedback loops

ALIGNMENT DOCTRINE:
"DALS records truth. UCM learns from truth. GOAT produces behavior."

DALS does not learn. DALS does not adapt, decide, improve, or infer.
DALS only records, classifies, timestamps, and exposes truth about GOAT behavior.

Any appearance of "learning" in DALS refers strictly to:
- pattern recording
- trend exposure
- event emission

All cognition, interpretation, and improvement occur only in UCM.
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import Response
import time
from typing import Dict, Any, List, Optional
import asyncio
import json
import httpx
from datetime import datetime, timedelta
import hashlib
from contextlib import asynccontextmanager

# Background health check task
async def background_health_check():
    """Continuously monitor GOAT health in background"""
    while True:
        try:
            await check_goat_health()
        except Exception as e:
            print(f"Background health check error: {e}")
        await asyncio.sleep(DALS_CONFIG["health_check_interval"])

# FastAPI lifespan for background tasks
@asynccontextmanager
async def lifespan(app):
    """FastAPI lifespan event for background tasks"""
    # Start background health check
    health_task = asyncio.create_task(background_health_check())

    yield

    # Cleanup
    health_task.cancel()
    try:
        await health_task
    except asyncio.CancelledError:
        pass

router = APIRouter(prefix="/host", lifespan=lifespan)

# DALS Configuration
DALS_NAME = "Digital Asset Logistics System"
DALS_CONFIG = {
    "name": DALS_NAME,
    "max_queue_size": 100,
    "message_ttl": 3600,  # 1 hour
    "monitoring_enabled": True,
    "goat_integration": True,
    "goat_base_url": "http://localhost:5000",
    "health_check_interval": 30,  # seconds
    "health_cache_ttl": 60,  # seconds
    "rate_limit_requests": 100,  # per minute per user
    "rate_limit_window": 60,  # seconds
}

# GOAT Health and Configuration Cache
GOAT_HEALTH_CACHE: Dict[str, Any] = {
    "last_check": 0,
    "overall_status": "unknown",
    "modules": {},
    "version": None,
    "endpoints": [],
    "config": {}
}

# Rate limiting storage
RATE_LIMITS: Dict[str, List[float]] = {}

# Request metrics for feedback loop
REQUEST_METRICS: Dict[str, Any] = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "response_times": [],
    "errors_by_endpoint": {},
    "errors_by_type": {}
}

# GOAT Behavior Observation Store - for UCM consumption
GOAT_OBSERVATION_STORE: Dict[str, Any] = {
    "endpoint_performance": {},  # Historical performance per endpoint
    "behavior_patterns": {},     # Recorded patterns of GOAT behavior
    "capability_declarations": {}, # What GOAT declares it can do
    "observation_events": []        # Events for UCM to consume
}

# UCM Event Emission
UCM_TRIGGERS = {
    "goat_failure": True,        # Trigger UCM on GOAT failures
    "goat_hesitation": True,     # Trigger on slow/weak responses
    "goat_contradiction": True,  # Trigger on conflicting answers
    "latency_threshold": 5.0,    # Trigger UCM if GOAT takes > 5 seconds
    "low_confidence_threshold": 0.7  # Trigger if confidence < 70%
}

# In-memory message queues - in production, use Redis or database
MESSAGE_QUEUES: Dict[str, List[Dict[str, Any]]] = {}
QUEUE_LOCK = asyncio.Lock()

async def check_goat_health() -> Dict[str, Any]:
    """Real GOAT health check - validates actual endpoints"""
    current_time = time.time()

    # Return cached result if recent
    if current_time - GOAT_HEALTH_CACHE["last_check"] < DALS_CONFIG["health_cache_ttl"]:
        return GOAT_HEALTH_CACHE

    health_status = {
        "last_check": current_time,
        "overall_status": "down",
        "modules": {},
        "version": None,
        "endpoints": [],
        "response_time": None
    }

    try:
        start_time = time.time()

        # Check main GOAT health endpoint
        async with httpx.AsyncClient(timeout=10.0) as client:
            health_response = await client.get(f"{DALS_CONFIG['goat_base_url']}/api/health")
            health_status["response_time"] = time.time() - start_time

            if health_response.status_code == 200:
                health_data = health_response.json()
                health_status["overall_status"] = health_data.get("status", "unknown")
                health_status["version"] = health_data.get("version")

                # Check individual modules
                modules_to_check = [
                    ("triples", "/api/v1/triples/search"),
                    ("analytics", "/api/v1/analytics/stats"),
                    ("video", "/api/v1/video/templates"),
                    ("vault", "/api/vault/stats"),
                    ("knowledge", "/api/v1/query/sparql")
                ]

                for module_name, endpoint in modules_to_check:
                    try:
                        module_response = await client.get(f"{DALS_CONFIG['goat_base_url']}{endpoint}", timeout=5.0)
                        health_status["modules"][module_name] = {
                            "status": "healthy" if module_response.status_code < 400 else "unhealthy",
                            "response_time": time.time() - start_time,
                            "http_status": module_response.status_code
                        }
                        health_status["endpoints"].append({
                            "name": module_name,
                            "endpoint": endpoint,
                            "status": "available" if module_response.status_code < 400 else "unavailable"
                        })
                    except Exception as e:
                        health_status["modules"][module_name] = {
                            "status": "unhealthy",
                            "error": str(e)
                        }

                # Get GOAT configuration if available
                try:
                    config_response = await client.get(f"{DALS_CONFIG['goat_base_url']}/api/v1/admin/config")
                    if config_response.status_code == 200:
                        health_status["config"] = config_response.json()
                except:
                    pass  # Config endpoint might not exist or be protected

            else:
                health_status["overall_status"] = "unhealthy"

    except Exception as e:
        health_status["overall_status"] = "down"
        health_status["error"] = str(e)

    # Update cache
    GOAT_HEALTH_CACHE.update(health_status)
    return health_status

async def enforce_rate_limit(user_id: str) -> bool:
    """Enforce rate limiting per user"""
    current_time = time.time()
    window_start = current_time - DALS_CONFIG["rate_limit_window"]

    if user_id not in RATE_LIMITS:
        RATE_LIMITS[user_id] = []

    # Remove old requests outside the window
    RATE_LIMITS[user_id] = [t for t in RATE_LIMITS[user_id] if t > window_start]

    # Check if under limit
    if len(RATE_LIMITS[user_id]) >= DALS_CONFIG["rate_limit_requests"]:
        return False

    # Add current request
    RATE_LIMITS[user_id].append(current_time)
    return True

def classify_goat_response(response: httpx.Response, response_time: float, path: str) -> Dict[str, Any]:
    """Classify GOAT response for observability and UCM event emission"""
    classification = {
        "endpoint": path,
        "http_status": response.status_code,
        "response_time": response_time,
        "success": response.status_code < 400,
        "classification": "unknown",
        "confidence": 1.0,
        "triggers_ucm": False,
        "observation_event": None,
        "metadata": {}
    }

    try:
        response_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}

        # Classify response type
        if response.status_code >= 500:
            classification["classification"] = "server_error"
            classification["triggers_ucm"] = UCM_TRIGGERS["goat_failure"]
            classification["observation_event"] = "goat_server_failure"
        elif response.status_code >= 400:
            classification["classification"] = "client_error"
            classification["triggers_ucm"] = UCM_TRIGGERS["goat_failure"]
            classification["observation_event"] = "goat_client_error"
        elif response_time > UCM_TRIGGERS["latency_threshold"]:
            classification["classification"] = "slow_response"
            classification["triggers_ucm"] = UCM_TRIGGERS["goat_hesitation"]
            classification["observation_event"] = "goat_slow_response"
        elif isinstance(response_data, dict):
            # Check for confidence indicators
            confidence = response_data.get("confidence", response_data.get("score", 1.0))
            if isinstance(confidence, (int, float)) and confidence < UCM_TRIGGERS["low_confidence_threshold"]:
                classification["classification"] = "low_confidence"
                classification["confidence"] = confidence
                classification["triggers_ucm"] = UCM_TRIGGERS["goat_hesitation"]
                classification["observation_event"] = "goat_low_confidence"
            else:
                classification["classification"] = "successful"
        else:
            classification["classification"] = "successful"

        # Store metadata for observation
        classification["metadata"] = {
            "response_size": len(response.content),
            "has_data": bool(response_data),
            "content_type": response.headers.get("content-type"),
            "timestamp": time.time()
        }

    except Exception as e:
        classification["classification"] = "parse_error"
        classification["error"] = str(e)
        classification["triggers_ucm"] = UCM_TRIGGERS["goat_failure"]
        classification["observation_event"] = "goat_response_parse_error"

    return classification

def store_goat_behavior(endpoint: str, classification: Dict[str, Any], request_data: Dict[str, Any] = None):
    """Store GOAT behavior for UCM consumption"""
    # Update endpoint performance history
    if endpoint not in GOAT_OBSERVATION_STORE["endpoint_performance"]:
        GOAT_OBSERVATION_STORE["endpoint_performance"][endpoint] = []

    GOAT_OBSERVATION_STORE["endpoint_performance"][endpoint].append({
        "timestamp": time.time(),
        "classification": classification,
        "request_data": request_data
    })

    # Keep only last 100 events per endpoint
    if len(GOAT_OBSERVATION_STORE["endpoint_performance"][endpoint]) > 100:
        GOAT_OBSERVATION_STORE["endpoint_performance"][endpoint] = GOAT_OBSERVATION_STORE["endpoint_performance"][endpoint][-100:]

    # Create observation event for UCM
    if classification["observation_event"]:
        observation_event = {
            "event_type": classification["observation_event"],
            "endpoint": endpoint,
            "classification": classification,
            "timestamp": time.time(),
            "request_context": request_data
        }

        GOAT_OBSERVATION_STORE["observation_events"].append(observation_event)

        # Keep only last 500 observation events
        if len(GOAT_OBSERVATION_STORE["observation_events"]) > 500:
            GOAT_OBSERVATION_STORE["observation_events"] = GOAT_OBSERVATION_STORE["observation_events"][-500:]

async def emit_ucm_event(classification: Dict[str, Any], request_data: Dict[str, Any] = None):
    """Emit GOAT behavior observation event to UCM"""
    if not classification["triggers_ucm"]:
        return

    # Prepare UCM observation payload
    ucm_payload = {
        "event_type": "goat_behavior_observation",
        "classification": classification,
        "request_context": request_data or {},
        "timestamp": time.time(),
        "source": "dals_gateway"
    }

    # Send to UCM (DALS emits events, UCM learns)
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            ucm_response = await client.post(
                f"{DALS_CONFIG['goat_base_url']}/api/v1/ucm/learn",
                json=ucm_payload,
                headers={"Authorization": "Bearer dals_gateway"}
            )

            if ucm_response.status_code == 200:
                print(f"UCM event emitted for: {classification['observation_event']}")
            else:
                print(f"UCM event emission failed: {ucm_response.status_code}")

    except Exception as e:
        print(f"UCM event emission error: {e}")
        # Store for later retry
        GOAT_OBSERVATION_STORE["observation_events"].append({
            "event_type": "ucm_event_failed",
            "original_event": classification["observation_event"],
            "error": str(e),
            "timestamp": time.time()
        })

async def validate_goat_request(path: str, method: str) -> bool:
    """Validate if GOAT endpoint exists and is healthy"""
    health = await check_goat_health()

    if health["overall_status"] not in ["healthy", "ok"]:
        return False

    # Check if specific endpoint is available
    endpoint_name = path.split('/')[1] if len(path.split('/')) > 1 else "unknown"

    for endpoint in health["endpoints"]:
        if endpoint["name"] == endpoint_name and endpoint["status"] == "available":
            return True

    # Allow unknown endpoints if GOAT is generally healthy
    return health["overall_status"] in ["healthy", "ok"]

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
    Get DALS configuration merged with GOAT's authoritative config
    """
    health = await check_goat_health()

    # GOAT's available options come from actual health checks
    goat_options_available = []
    for endpoint in health["endpoints"]:
        if endpoint["status"] == "available":
            goat_options_available.append(endpoint["name"])

    # GOAT config overrides DALS assumptions
    goat_config = health.get("config", {})

    return {
        "dals_config": DALS_CONFIG,
        "goat_config": goat_config,
        "available_overrides": [
            "max_queue_size",
            "message_ttl",
            "monitoring_enabled",
            "goat_integration",
            "goat_base_url",
            "health_check_interval",
            "rate_limit_requests",
            "rate_limit_window"
        ],
        "goat_options_available": goat_options_available,
        "goat_options_verified": health["overall_status"] in ["healthy", "ok"],
        "config_source": "goat_authoritative" if goat_config else "dals_default"
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
    Real monitoring data with GOAT health and request metrics
    """
    total_queues = len(MESSAGE_QUEUES)
    total_messages = sum(len(queue) for queue in MESSAGE_QUEUES.values())

    # Get current GOAT health
    goat_health = await check_goat_health()

    # Calculate response time stats
    response_times = REQUEST_METRICS["response_times"]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    max_response_time = max(response_times) if response_times else 0

    return {
        "monitoring": {
            "active_queues": total_queues,
            "total_messages": total_messages,
            "config_overrides": DALS_CONFIG,
            "goat_integration_status": "active" if DALS_CONFIG["goat_integration"] else "disabled",
            "goat_health": goat_health,
            "request_metrics": {
                "total_requests": REQUEST_METRICS["total_requests"],
                "successful_requests": REQUEST_METRICS["successful_requests"],
                "failed_requests": REQUEST_METRICS["failed_requests"],
                "success_rate": REQUEST_METRICS["successful_requests"] / REQUEST_METRICS["total_requests"] if REQUEST_METRICS["total_requests"] > 0 else 0,
                "avg_response_time": avg_response_time,
                "max_response_time": max_response_time,
                "errors_by_endpoint": REQUEST_METRICS["errors_by_endpoint"],
                "errors_by_type": REQUEST_METRICS["errors_by_type"]
            },
            "goat_observation": {
                "total_observation_events": len(GOAT_OBSERVATION_STORE["observation_events"]),
                "endpoint_performance_tracked": len(GOAT_OBSERVATION_STORE["endpoint_performance"]),
                "behavior_patterns_recorded": len(GOAT_OBSERVATION_STORE["behavior_patterns"]),
                "recent_observation_events": GOAT_OBSERVATION_STORE["observation_events"][-5:] if GOAT_OBSERVATION_STORE["observation_events"] else []
            },
            "rate_limits": {
                "active_users": len(RATE_LIMITS),
                "config": {
                    "requests_per_minute": DALS_CONFIG["rate_limit_requests"],
                    "window_seconds": DALS_CONFIG["rate_limit_window"]
                }
            }
        },
        "timestamp": time.time()
    }

@router.get("/goat-options")
async def get_goat_options():
    """
    Get verified GOAT options based on actual health checks
    """
    health = await check_goat_health()

    available_endpoints = []
    for endpoint in health["endpoints"]:
        if endpoint["status"] == "available":
            available_endpoints.append(f"/api/v1/{endpoint['name']}")

    # Add known working endpoints that might not be in health check
    standard_endpoints = ["/health"]
    if health["overall_status"] in ["healthy", "ok"]:
        standard_endpoints.extend([
            "/api/v1/admin/config",
            "/api/v1/admin/health"
        ])

    return {
        "goat_endpoints_available": available_endpoints + standard_endpoints,
        "goat_endpoints_verified": [e for e in health["endpoints"] if e["status"] == "available"],
        "goat_endpoints_unavailable": [e for e in health["endpoints"] if e["status"] != "available"],
        "goat_version": health["version"],
        "goat_overall_status": health["overall_status"],
        "dals_overrides_applied": DALS_CONFIG,
        "plugin_status": "active" if DALS_CONFIG["goat_integration"] else "disabled",
        "all_options_available": health["overall_status"] in ["healthy", "ok"],
        "last_health_check": health["last_check"]
    }

@router.get("/dashboard")
async def get_dashboard_data():
    """
    Real-time GOAT Dashboard based on actual health checks and metrics
    """
    health = await check_goat_health()

    # Build modules based on actual health
    modules = {
        "dals_messaging": {
            "status": "active",
            "endpoints": ["/dals/host", "/dals/uqv", "/dals/tts"],
            "features": ["Host messaging", "UQV storage", "TTS synthesis"]
        }
    }

    # Add GOAT modules based on real health
    for endpoint in health["endpoints"]:
        module_name = endpoint["name"]
        modules[module_name] = {
            "status": "active" if endpoint["status"] == "available" else "unhealthy",
            "endpoints": [f"/api/v1/{module_name}"],
            "features": [f"{module_name.title()} operations"],
            "health": health["modules"].get(module_name, {})
        }

    # Calculate success rate
    total_requests = REQUEST_METRICS["total_requests"]
    success_rate = REQUEST_METRICS["successful_requests"] / total_requests if total_requests > 0 else 0

    dashboard = {
        "title": f"{DALS_NAME} Dashboard - GOAT Integration",
        "version": health["version"] or "2.0.0",
        "dals_integration": "active" if DALS_CONFIG["goat_integration"] else "disabled",
        "goat_overall_status": health["overall_status"],
        "modules": modules,
        "configuration": {
            "overrides_available": list(DALS_CONFIG.keys()),
            "current_overrides": DALS_CONFIG,
            "monitoring_enabled": DALS_CONFIG["monitoring_enabled"]
        },
        "health_status": {
            "overall": health["overall_status"],
            "last_updated": health["last_check"],
            "response_time": health["response_time"]
        },
        "performance": {
            "total_requests": total_requests,
            "success_rate": success_rate,
            "active_rate_limits": len(RATE_LIMITS),
            "goat_modules_healthy": len([m for m in health["modules"].values() if m.get("status") == "healthy"])
        }
    }

    return dashboard

# GOAT Gateway - Intelligent routing with validation and policy enforcement
@router.api_route("/goat/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway_goat_request(path: str, request: Request):
    """
    GOAT Gateway - Validates requests, enforces policies, and provides feedback
    """
    start_time = time.time()

    # 1. Check if GOAT integration is enabled
    if not DALS_CONFIG["goat_integration"]:
        update_request_metrics(path, False, time.time() - start_time, "integration_disabled")
        raise HTTPException(status_code=403, detail="GOAT integration disabled")

    # 2. Validate GOAT health and endpoint availability
    if not await validate_goat_request(path, request.method):
        update_request_metrics(path, False, time.time() - start_time, "goat_unhealthy")
        raise HTTPException(status_code=503, detail="GOAT service unavailable")

    # 3. Extract user identity for rate limiting and auth
    user_id = None
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        # Extract user from JWT (simplified - in production use proper JWT decoding)
        token = auth_header[7:]
        # For now, assume user_id is passed in a custom header or query param
        user_id = request.headers.get("x-user-id") or request.query_params.get("user_id")

    # 4. Enforce rate limiting if user identified
    if user_id and not await enforce_rate_limit(user_id):
        update_request_metrics(path, False, time.time() - start_time, "rate_limited")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # 5. Construct target URL dynamically
    target_url = f"{DALS_CONFIG['goat_base_url']}/api/v1/{path}"

    # 6. Prepare request
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)  # Remove host header

    # 7. Add DALS tracking headers
    headers["x-dals-gateway"] = "true"
    headers["x-dals-request-id"] = hashlib.md5(f"{time.time()}_{path}".encode()).hexdigest()[:8]

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params
            )

            response_time = time.time() - start_time

            # CLASSIFY AND LEARN FROM GOAT RESPONSE
            classification = classify_goat_response(response, response_time, path)

            # Extract request context for observation
            request_context = {
                "method": request.method,
                "query_params": dict(request.query_params),
                "user_id": user_id,
                "headers": {k: v for k, v in request.headers.items() if k.lower() not in ['authorization', 'cookie']}
            }

            # Store behavior for UCM consumption
            store_goat_behavior(path, classification, request_context)

            # Emit UCM event if needed
            await emit_ucm_event(classification, request_context)

            # Update metrics based on classification
            success = classification["success"]
            error_type = classification["classification"] if not success else None

            update_request_metrics(path, success, response_time, error_type)

            # Return response with DALS metadata
            response_headers = dict(response.headers)
            response_headers["x-dals-processed"] = "true"
            response_headers["x-dals-response-time"] = str(response_time)
            response_headers["x-dals-classification"] = classification["classification"]
            response_headers["x-dals-confidence"] = str(classification["confidence"])

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=response_headers
            )

    except httpx.TimeoutException:
        update_request_metrics(path, False, time.time() - start_time, "timeout")
        raise HTTPException(status_code=504, detail="GOAT request timeout")
    except httpx.ConnectError:
        update_request_metrics(path, False, time.time() - start_time, "connection_error")
        raise HTTPException(status_code=503, detail="Cannot connect to GOAT")
    except Exception as e:
        update_request_metrics(path, False, time.time() - start_time, "gateway_error")
        raise HTTPException(status_code=500, detail=f"Gateway error: {str(e)}")

@router.get("/connections")
async def get_connections_status():
    """
    Real connection status based on actual health checks
    """
    health = await check_goat_health()

    connections = {
        "dals_host": "active",
        "dals_uqv": "active",
        "dals_tts": "active",
        "dals_broadcast": "active"
    }

    # Add GOAT connections based on real health
    for endpoint in health["endpoints"]:
        connections[f"goat_{endpoint['name']}"] = endpoint["status"]

    # Add overall GOAT health
    connections["goat_overall"] = health["overall_status"]

    return {
        "all_endpoints_connected_via_dals": health["overall_status"] in ["healthy", "ok"],
        "connections": connections,
        "dals_gateway_status": "active",
        "goat_health": health,
        "timestamp": time.time()
    }

@router.get("/goat-capabilities")
async def get_goat_capabilities():
    """
    Get GOAT's declared capabilities for UCM reasoning
    """
    health = await check_goat_health()

    capabilities = {
        "declared_endpoints": [],
        "verified_endpoints": [],
        "unavailable_endpoints": [],
        "performance_profile": {},
        "observation_insights": {},
        "last_updated": health["last_check"]
    }

    # Build capability declarations from health checks
    for endpoint in health["endpoints"]:
        cap_entry = {
            "name": endpoint["name"],
            "endpoint": f"/api/v1/{endpoint['name']}",
            "status": endpoint["status"],
            "module_health": health["modules"].get(endpoint["name"], {})
        }

        if endpoint["status"] == "available":
            capabilities["verified_endpoints"].append(cap_entry)
        else:
            capabilities["unavailable_endpoints"].append(cap_entry)

        capabilities["declared_endpoints"].append(cap_entry)

    # Add performance profile
    capabilities["performance_profile"] = {
        "overall_health": health["overall_status"],
        "response_time": health["response_time"],
        "modules_healthy": len([m for m in health["modules"].values() if m.get("status") == "healthy"]),
        "modules_total": len(health["modules"])
    }

    # Add observation insights
    capabilities["observation_insights"] = {
        "total_observation_events": len(GOAT_OBSERVATION_STORE["observation_events"]),
        "recent_events": GOAT_OBSERVATION_STORE["observation_events"][-10:] if GOAT_OBSERVATION_STORE["observation_events"] else [],
        "endpoint_performance_summary": {
            endpoint: {
                "total_calls": len(events),
                "success_rate": len([e for e in events if e["classification"]["success"]]) / len(events) if events else 0,
                "avg_response_time": sum(e["classification"]["response_time"] for e in events) / len(events) if events else 0
            }
            for endpoint, events in GOAT_OBSERVATION_STORE["endpoint_performance"].items()
        }
    }

    return capabilities

@router.get("/goat-observation-events")
async def get_goat_observation_events(limit: int = 50, event_type: str = None):
    """
    Get GOAT behavior observation events for UCM consumption
    """
    events = GOAT_OBSERVATION_STORE["observation_events"]

    if event_type:
        events = [e for e in events if e.get("event_type") == event_type]

    # Return most recent events
    recent_events = events[-limit:] if events else []

    return {
        "total_events": len(GOAT_OBSERVATION_STORE["observation_events"]),
        "returned_events": len(recent_events),
        "events": recent_events,
        "event_types_available": list(set(e.get("event_type") for e in GOAT_OBSERVATION_STORE["observation_events"]))
    }

@router.post("/ucm/observe")
async def receive_ucm_observation(request: Request):
    """
    Receive observation feedback from UCM about GOAT behavior
    """
    try:
        observation_data = await request.json()

        # Store UCM feedback in observation store
        feedback_event = {
            "event_type": "ucm_feedback",
            "feedback": observation_data,
            "timestamp": time.time(),
            "source": "ucm_to_dals"
        }

        GOAT_OBSERVATION_STORE["observation_events"].append(feedback_event)

        # Update behavior patterns based on UCM feedback
        if "behavior_pattern" in observation_data:
            pattern_key = observation_data["behavior_pattern"]
            if pattern_key not in GOAT_OBSERVATION_STORE["behavior_patterns"]:
                GOAT_OBSERVATION_STORE["behavior_patterns"][pattern_key] = []

            GOAT_OBSERVATION_STORE["behavior_patterns"][pattern_key].append({
                "feedback": observation_data,
                "timestamp": time.time()
            })

        return {"status": "observation_stored", "events_processed": 1}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"UCM observation storage failed: {str(e)}")

@router.get("/goat-behavior-analysis")
async def get_goat_behavior_analysis():
    """
    Provide UCM with analysis of GOAT behavior patterns
    """
    analysis = {
        "endpoint_performance": {},
        "behavior_patterns": GOAT_OBSERVATION_STORE["behavior_patterns"],
        "observation_summary": {
            "total_events": len(GOAT_OBSERVATION_STORE["observation_events"]),
            "event_types": {},
            "time_range": {}
        },
        "recommendations": []
    }

    # Analyze endpoint performance
    for endpoint, events in GOAT_OBSERVATION_STORE["endpoint_performance"].items():
        if events:
            success_rate = len([e for e in events if e["classification"]["success"]]) / len(events)
            avg_response_time = sum(e["classification"]["response_time"] for e in events) / len(events)

            analysis["endpoint_performance"][endpoint] = {
                "calls": len(events),
                "success_rate": success_rate,
                "avg_response_time": avg_response_time,
                "needs_attention": success_rate < 0.8 or avg_response_time > 5.0
            }

            if success_rate < 0.8:
                analysis["recommendations"].append(f"Endpoint {endpoint} has low success rate ({success_rate:.2%})")
            if avg_response_time > 5.0:
                analysis["recommendations"].append(f"Endpoint {endpoint} is slow (avg {avg_response_time:.2f}s)")

    # Summarize observation events
    if GOAT_OBSERVATION_STORE["observation_events"]:
        event_types = {}
        timestamps = []

        for event in GOAT_OBSERVATION_STORE["observation_events"]:
            event_type = event.get("event_type", "unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1
            timestamps.append(event.get("timestamp", 0))

        analysis["observation_summary"]["event_types"] = event_types
        analysis["observation_summary"]["time_range"] = {
            "earliest": min(timestamps) if timestamps else None,
            "latest": max(timestamps) if timestamps else None
        }

    return analysis