from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def admin_status():
    """Admin status - placeholder"""
    return {"message": "Admin status endpoint"}
