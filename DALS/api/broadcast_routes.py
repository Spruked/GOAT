# DALS/api/broadcast_routes.py
"""
Broadcast Routes - Distribute predicates and clusters to all registered workers
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import asyncio
import httpx
from DALS.registry.worker_registry import list_workers, cleanup_dead_workers

router = APIRouter()

async def broadcast_to_worker(worker_name: str, worker_url: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Broadcast data to a specific worker"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{worker_url}{endpoint}", json=data)
            return {
                "worker": worker_name,
                "status": response.status_code,
                "response": response.json() if response.status_code < 400 else response.text
            }
    except Exception as e:
        return {
            "worker": worker_name,
            "status": "error",
            "error": str(e)
        }

@router.post("/broadcast/predicate")
async def broadcast_predicate(predicate: Dict[str, Any], background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Broadcast a predicate to all registered workers
    """
    # Clean up dead workers first
    cleanup_dead_workers()

    workers = list_workers()
    if not workers:
        raise HTTPException(status_code=400, detail="No workers registered")

    # Broadcast to all workers asynchronously
    broadcast_tasks = []
    for worker_name, worker_info in workers.items():
        if worker_info["status"] == "active":
            task = broadcast_to_worker(
                worker_name,
                worker_info["api_url"],
                "/receive/predicate",
                predicate
            )
            broadcast_tasks.append(task)

    # Execute all broadcasts concurrently
    results = await asyncio.gather(*broadcast_tasks, return_exceptions=True)

    # Process results
    successful = []
    failed = []

    for result in results:
        if isinstance(result, Exception):
            failed.append({"error": str(result)})
        elif result["status"] == "error":
            failed.append(result)
        else:
            successful.append(result)

    return {
        "total_workers": len(workers),
        "successful": len(successful),
        "failed": len(failed),
        "results": successful + failed
    }

@router.post("/broadcast/cluster")
async def broadcast_cluster(cluster: Dict[str, Any], background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Broadcast a cluster to all registered workers
    """
    # Clean up dead workers first
    cleanup_dead_workers()

    workers = list_workers()
    if not workers:
        raise HTTPException(status_code=400, detail="No workers registered")

    # Broadcast to all workers asynchronously
    broadcast_tasks = []
    for worker_name, worker_info in workers.items():
        if worker_info["status"] == "active":
            task = broadcast_to_worker(
                worker_name,
                worker_info["api_url"],
                "/receive/cluster",
                cluster
            )
            broadcast_tasks.append(task)

    # Execute all broadcasts concurrently
    results = await asyncio.gather(*broadcast_tasks, return_exceptions=True)

    # Process results
    successful = []
    failed = []

    for result in results:
        if isinstance(result, Exception):
            failed.append({"error": str(result)})
        elif result["status"] == "error":
            failed.append(result)
        else:
            successful.append(result)

    return {
        "total_workers": len(workers),
        "successful": len(successful),
        "failed": len(failed),
        "results": successful + failed
    }

@router.post("/broadcast/message")
async def broadcast_message(message: Dict[str, Any], background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Broadcast a general message to all registered workers
    """
    # Clean up dead workers first
    cleanup_dead_workers()

    workers = list_workers()
    if not workers:
        raise HTTPException(status_code=400, detail="No workers registered")

    # Broadcast to all workers asynchronously
    broadcast_tasks = []
    for worker_name, worker_info in workers.items():
        if worker_info["status"] == "active":
            task = broadcast_to_worker(
                worker_name,
                worker_info["api_url"],
                "/receive/message",
                message
            )
            broadcast_tasks.append(task)

    # Execute all broadcasts concurrently
    results = await asyncio.gather(*broadcast_tasks, return_exceptions=True)

    # Process results
    successful = []
    failed = []

    for result in results:
        if isinstance(result, Exception):
            failed.append({"error": str(result)})
        elif result["status"] == "error":
            failed.append(result)
        else:
            successful.append(result)

    return {
        "total_workers": len(workers),
        "successful": len(successful),
        "failed": len(failed),
        "results": successful + failed
    }

@router.get("/workers")
async def get_registered_workers() -> Dict[str, Any]:
    """
    Get list of all registered workers
    """
    cleanup_dead_workers()
    workers = list_workers()

    return {
        "total_workers": len(workers),
        "workers": workers
    }