from fastapi import APIRouter
from .organizer_routes import router as organizer_router

api_router = APIRouter()
api_router.include_router(organizer_router, prefix="/organizer", tags=["Organizer"])
