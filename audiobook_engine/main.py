#!/usr/bin/env python3
"""
Audiobook Engine Main Application

FastAPI application for the GOAT Audiobook Engine.
Provides REST API for audiobook generation and management.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from .config import API_CONFIG
from .routers.audiobook_router import router as audiobook_router
from .workers.tasks import initialize_workers, shutdown_workers

# Configure logging
logging.basicConfig(
    level=getattr(logging, API_CONFIG.get('log_level', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Audiobook Engine...")
    initialize_workers()
    logger.info("Audiobook Engine started successfully")

    yield

    # Shutdown
    logger.info("Shutting down Audiobook Engine...")
    shutdown_workers()
    logger.info("Audiobook Engine shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="GOAT Audiobook Engine",
    description="Complete SSML → audio → stitching → M4B export pipeline",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG.get('cors_origins', ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(audiobook_router)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )

    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "GOAT Audiobook Engine"
    }


# API info endpoint
@app.get("/api/v1/info")
async def api_info():
    """API information endpoint."""
    return {
        "name": "GOAT Audiobook Engine",
        "version": "1.0.0",
        "description": "Complete audiobook generation pipeline",
        "endpoints": {
            "projects": "/api/v1/audiobooks/",
            "chapters": "/api/v1/audiobooks/{project_id}/chapters",
            "voices": "/api/v1/audiobooks/voices",
            "processing": "/api/v1/audiobooks/{project_id}/process",
            "export": "/api/v1/audiobooks/{project_id}/export"
        }
    }


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "audiobook_engine.main:app",
        host=API_CONFIG.get('host', '0.0.0.0'),
        port=API_CONFIG.get('port', 8000),
        reload=API_CONFIG.get('debug', False),
        log_level=API_CONFIG.get('log_level', 'info').lower()
    )