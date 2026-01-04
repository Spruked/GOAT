from fastapi import APIRouter

router = APIRouter()


@router.get("/stats")
async def get_stats():
    """Get analytics stats - placeholder"""
    return {"message": "Analytics stats endpoint"}


@router.get("/graph")
async def get_graph():
    """Get graph analytics - placeholder"""
    return {"message": "Graph analytics endpoint"}
