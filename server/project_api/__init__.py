from fastapi import APIRouter
from .export import router as export_router
from .resume import router as resume_router
from .purge import router as purge_router
from .retention import router as retention_router
from .create import router as create_router

router = APIRouter()
router.include_router(export_router)
router.include_router(resume_router)
router.include_router(purge_router)
router.include_router(retention_router)
router.include_router(create_router)
