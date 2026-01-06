# DALS/registry/worker_registry.py
"""
Worker Registry - Tracks active DALS workers
"""

from typing import Dict, Any
import time

# In-memory worker registry - in production, use database
WORKER_REGISTRY: Dict[str, Dict[str, Any]] = {}

def register_worker(name: str, api_url: str, capabilities: list = None):
    """Register a worker in the registry"""
    WORKER_REGISTRY[name] = {
        "api_url": api_url,
        "capabilities": capabilities or [],
        "registered_at": time.time(),
        "last_heartbeat": time.time(),
        "status": "active"
    }

def unregister_worker(name: str):
    """Remove a worker from the registry"""
    if name in WORKER_REGISTRY:
        del WORKER_REGISTRY[name]

def get_worker(name: str) -> Dict[str, Any]:
    """Get worker information"""
    return WORKER_REGISTRY.get(name)

def list_workers() -> Dict[str, Dict[str, Any]]:
    """Get all registered workers"""
    return WORKER_REGISTRY.copy()

def heartbeat_worker(name: str):
    """Update worker heartbeat"""
    if name in WORKER_REGISTRY:
        WORKER_REGISTRY[name]["last_heartbeat"] = time.time()
        WORKER_REGISTRY[name]["status"] = "active"

def cleanup_dead_workers(max_age: float = 300):
    """Remove workers that haven't sent heartbeat recently"""
    current_time = time.time()
    dead_workers = []

    for name, worker in WORKER_REGISTRY.items():
        if current_time - worker["last_heartbeat"] > max_age:
            dead_workers.append(name)

    for name in dead_workers:
        unregister_worker(name)

    return len(dead_workers)