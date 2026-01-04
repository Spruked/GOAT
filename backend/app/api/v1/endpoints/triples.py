from fastapi import APIRouter

router = APIRouter()


@router.get("/search")
async def search_triples():
    """Search triples - placeholder"""
    return {"message": "Triples search endpoint"}


@router.post("/ingest")
async def ingest_triples():
    """Ingest triples - placeholder"""
    return {"message": "Triples ingest endpoint"}
