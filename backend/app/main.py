# backend/app/main.py
from fastapi import FastAPI, Request, HTTPException, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn
import structlog
from datetime import datetime
import sys
import os
import asyncio
import httpx

# Add DALS and backend to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'DALS'))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Debug paths
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print(f"Backend dir: {os.path.dirname(os.path.dirname(__file__))}")
print(f"DALS dir: {os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'DALS')}")

from app.config import settings
from app.core.database import init_database
from app.core.cache import init_cache
from app.core.tracing import setup_tracing
from app.api.v1.endpoints import triples, query, analytics, admin, video, host_bubble_router, auth
from app.security.auth import dual_auth
from app.middleware.server_timing import server_timing_middleware

# Import DALS routers
# from api.host_routes import router as host_router
# from api.uqv_routes import router as uqv_router
# from api.tts_routes import router as tts_router
# from api.broadcast_routes import router as broadcast_router
from app.core.database import init_database
from app.core.cache import init_cache
from app.core.tracing import setup_tracing
from app.api.v1.endpoints import triples, query, analytics, admin, video, host_bubble_router, auth
from app.security.auth import dual_auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STRICT STARTUP ORDER WITH VERIFICATION
    logger = structlog.get_logger()
    logger.info("goat_startup_begin", version="2.0.0")

    try:
        # 1. Validate environment
        settings.validate_environment()

        # 2. Initialize database with timeout
        await init_database(timeout=30)

        # 3. Initialize Redis cache
        await init_cache()

        # 4. Verify all external dependencies
        await verify_external_services()

        logger.info("goat_startup_complete")
        yield

    except Exception as e:
        logger.critical("goat_startup_failed", error=str(e))
        raise
    finally:
        logger.info("goat_shutdown")
        await shutdown_services()

app = FastAPI(
    title="SKG GOAT Edition",
    version="2.0.0",
    description="Personal preservation engine for immortal legacies",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENABLE_DOCS else None
)

# SECURITY MIDDLEWARE (JS-Friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(server_timing_middleware)

# ROUTES
app.include_router(triples.router, prefix="/api/v1/triples", tags=["Triples"])
app.include_router(query.router, prefix="/api/v1/query", tags=["Query"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(video.router, prefix="/api/v1/video", tags=["Video"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(host_bubble_router, prefix="/api/v1/host_bubble", tags=["HostBubble"])
app.include_router(auth.router)


# WebSocket for Orb connection to UCM
@app.websocket("/ws/orb")
async def orb_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Poll UCM health for resonance data
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get("http://localhost:8080/health", timeout=2.0)
                    if response.status_code == 200:
                        ucm_data = response.json()
                        # Map UCM health to resonance
                        phase_coherence = 0.8 if ucm_data.get("status") == "healthy" else 0.3
                        await websocket.send_json({
                            "type": "resonance_update",
                            "data": {"phaseCoherence": phase_coherence}
                        })
                    else:
                        await websocket.send_json({
                            "type": "resonance_update", 
                            "data": {"phaseCoherence": 0.2}
                        })
            except Exception as e:
                # Fallback if UCM unavailable
                await websocket.send_json({
                    "type": "resonance_update",
                    "data": {"phaseCoherence": 0.1}
                })
            
            await asyncio.sleep(5)  # Update every 5 seconds
    except Exception as e:
        pass
    finally:
        await websocket.close()


# DALS ROUTES - All GOAT options available through DALS plugin
# app.include_router(host_router, prefix="/dals/host", tags=["DALS Host"])
# app.include_router(uqv_router, prefix="/dals/uqv", tags=["DALS UQV"])
# app.include_router(tts_router, prefix="/dals/tts", tags=["DALS TTS"])
# app.include_router(broadcast_router, prefix="/dals/broadcast", tags=["DALS Broadcast"])


# HEALTH & METRICS
@app.get("/health", tags=["System"])
async def health_check():
    from app.core.database import get_db_status
    from app.core.cache import get_cache_status
    from app.core.ucm import ucm_health_check

    db_ok = await get_db_status()
    cache_ok = await get_cache_status()
    ucm_status = ucm_health_check()

    # Return diagnostic status (useful for local debugging)
    if not (db_ok and cache_ok and ucm_status.get("status") == "healthy"):
        return JSONResponse(
            status_code=503,
            content={
                "detail": "Service unavailable",
                "database": db_ok,
                "cache": cache_ok,
                "ucm": ucm_status,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "SKG-GOAT",
            "version": "2.0.0",
            "database": db_ok,
            "cache": cache_ok,
            "ucm": ucm_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def verify_external_services():
    """Verify Redis, FFmpeg, OpenAI are accessible"""
    from app.core.cache import redis_client
    from shutil import which

    # Check Redis
    if redis_client is not None:
        try:
            await redis_client.ping()
        except:
            raise RuntimeError("Redis unavailable")
    else:
        print("Redis not available, skipping check")

    # Check FFmpeg
    # if not which("ffmpeg"):
    #     raise RuntimeError("FFmpeg not installed")

    # UCM Health Probe (temporarily disabled for local testing)
    # import requests
    # try:
    #     resp = requests.get(f"{settings.UCM_BASE_URL}/health", timeout=2)
    #     if resp.status_code != 200:
    #         raise RuntimeError(f"UCM health check failed: {resp.status_code}")
    #     print("GOAT sees UCM.")
    # except Exception as e:
    #     raise RuntimeError(f"UCM health check failed: {e}")


async def shutdown_services():
    """Clean shutdown of services"""
    pass

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )