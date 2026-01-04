# backend/app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn
import structlog
from datetime import datetime
import sys
import os

# Add DALS to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'DALS'))

from app.config import settings
from app.core.database import init_database
from app.core.cache import init_cache
from app.core.tracing import setup_tracing
from app.api.v1.endpoints import triples, query, analytics, admin, video, auth
from app.security.auth import dual_auth

# Import DALS routers - commented out temporarily for auth implementation
# from api.host_routes import router as host_router
# from api.uqv_routes import router as uqv_router
# from api.tts_routes import router as tts_router
# from api.broadcast_routes import router as broadcast_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STRICT STARTUP ORDER WITH VERIFICATION
    logger = structlog.get_logger()
    logger.info("goat_startup_begin", version="2.0.0")

    try:
        # 1. Validate environment (skip for now)
        # settings.validate_environment()

        # 2. Initialize database with timeout
        await init_database(timeout=30)

        # 3. Initialize Redis cache (placeholder)
        await init_cache()

        # 4. Verify all external dependencies (skip for now)
        # await verify_external_services()

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
        "https://goat.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "X-Tenant-ID"],
    expose_headers=["X-Rate-Limit-Remaining", "X-Request-ID"],
)

# ROUTES
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(triples.router, prefix="/api/v1/triples", tags=["Triples"])
app.include_router(query.router, prefix="/api/v1/query", tags=["Query"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(video.router, prefix="/api/v1/video", tags=["Video"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])

# DALS ROUTES - All GOAT options available through DALS plugin
# Temporarily commented out for auth implementation
# app.include_router(host_router, prefix="/dals/host", tags=["DALS Host"])
# app.include_router(uqv_router, prefix="/dals/uqv", tags=["DALS UQV"])
# app.include_router(tts_router, prefix="/dals/tts", tags=["DALS TTS"])
# app.include_router(broadcast_router, prefix="/dals/broadcast", tags=["DALS Broadcast"])

# HEALTH & METRICS
@app.get("/health", tags=["System"])
async def health_check():
    from app.core.database import get_db_status
    from app.core.cache import get_cache_status

    db_ok = await get_db_status()
    cache_ok = await get_cache_status()

    if not (db_ok and cache_ok):
        raise HTTPException(status_code=503, detail="Service unavailable")

    return {
        "status": "healthy",
        "service": "SKG-GOAT",
        "version": "2.0.0",
        "database": db_ok,
        "cache": cache_ok,
        "timestamp": datetime.utcnow().isoformat()
    }

async def verify_external_services():
    """Verify Redis, FFmpeg, OpenAI are accessible"""
    from app.core.cache import redis_client
    from shutil import which

    # Check Redis
    try:
        await redis_client.ping()
    except:
        raise RuntimeError("Redis unavailable")

    # Check FFmpeg
    if not which("ffmpeg"):
        raise RuntimeError("FFmpeg not installed")

    # Check OpenAI API key
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OpenAI API key not configured")

async def shutdown_services():
    """Clean shutdown of services"""
    pass

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )