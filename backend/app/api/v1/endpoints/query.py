from fastapi import APIRouter

router = APIRouter()


@router.post("/sparql")
async def sparql_query():
    """SPARQL query - placeholder"""
    return {"message": "SPARQL query endpoint"}


@router.post("/vector")
async def vector_query():
    """Vector query - placeholder"""
    return {"message": "Vector query endpoint"}
