# DALS/api/uqv_routes.py
"""
UQV Routes - Unanswered Query Vault API for storing and retrieving unanswered queries
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from models.unanswered_query import UnansweredQuery
from models import get_db

router = APIRouter()

@router.post("/uqv/store")
async def store_unanswered_query(
    query: str,
    context: Optional[str] = None,
    worker_id: Optional[str] = None,
    db: Session = Depends(get_db)
) -> dict:
    """
    Store an unanswered query in the UQV
    """
    try:
        uqv_entry = UnansweredQuery(
            id=str(uuid.uuid4()),
            query=query,
            context=context,
            worker_id=worker_id,
            created_at=datetime.utcnow(),
            status="unanswered"
        )

        db.add(uqv_entry)
        db.commit()
        db.refresh(uqv_entry)

        return {
            "success": True,
            "uqv_id": uqv_entry.id,
            "message": "Query stored in UQV"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to store query: {str(e)}")

@router.get("/uqv/retrieve")
async def retrieve_unanswered_queries(
    limit: int = 10,
    offset: int = 0,
    status: Optional[str] = None,
    worker_id: Optional[str] = None,
    db: Session = Depends(get_db)
) -> dict:
    """
    Retrieve unanswered queries from the UQV
    """
    try:
        query = db.query(UnansweredQuery)

        if status:
            query = query.filter(UnansweredQuery.status == status)

        if worker_id:
            query = query.filter(UnansweredQuery.worker_id == worker_id)

        total = query.count()
        queries = query.order_by(UnansweredQuery.created_at.desc()).offset(offset).limit(limit).all()

        return {
            "total": total,
            "queries": [
                {
                    "id": q.id,
                    "query": q.query,
                    "context": q.context,
                    "worker_id": q.worker_id,
                    "created_at": q.created_at.isoformat(),
                    "status": q.status
                }
                for q in queries
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve queries: {str(e)}")

@router.put("/uqv/{uqv_id}/status")
async def update_query_status(
    uqv_id: str,
    status: str,
    db: Session = Depends(get_db)
) -> dict:
    """
    Update the status of an unanswered query
    """
    try:
        query = db.query(UnansweredQuery).filter(UnansweredQuery.id == uqv_id).first()

        if not query:
            raise HTTPException(status_code=404, detail="Query not found")

        query.status = status
        db.commit()

        return {
            "success": True,
            "message": f"Query status updated to {status}"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update status: {str(e)}")

@router.delete("/uqv/{uqv_id}")
async def delete_unanswered_query(
    uqv_id: str,
    db: Session = Depends(get_db)
) -> dict:
    """
    Delete an unanswered query from the UQV
    """
    try:
        query = db.query(UnansweredQuery).filter(UnansweredQuery.id == uqv_id).first()

        if not query:
            raise HTTPException(status_code=404, detail="Query not found")

        db.delete(query)
        db.commit()

        return {
            "success": True,
            "message": "Query deleted from UQV"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete query: {str(e)}")

@router.get("/uqv/stats")
async def get_uqv_stats(db: Session = Depends(get_db)) -> dict:
    """
    Get statistics about the UQV
    """
    try:
        total_queries = db.query(UnansweredQuery).count()
        unanswered = db.query(UnansweredQuery).filter(UnansweredQuery.status == "unanswered").count()
        answered = db.query(UnansweredQuery).filter(UnansweredQuery.status == "answered").count()
        learning = db.query(UnansweredQuery).filter(UnansweredQuery.status == "learning").count()

        return {
            "total_queries": total_queries,
            "unanswered": unanswered,
            "answered": answered,
            "learning": learning
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")