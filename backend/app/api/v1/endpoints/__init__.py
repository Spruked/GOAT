# backend/app/api/v1/endpoints/__init__.py

from .host_bubble import router as host_bubble_router
from .triples import router as triples
from .query import router as query
from .analytics import router as analytics
from .admin import router as admin
from .video import router as video
from .auth import router as auth