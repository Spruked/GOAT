# audiobook_engine/routers/__init__.py
"""
Audiobook Engine API Routers
"""

from .audiobook_router import router as audiobook_router

__all__ = [
    "audiobook_router"
]