# routes/uqv.py
"""
Unanswered Query Vault (UQV) API Routes
Stores queries that return no/low-confidence results for later learning
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from models.unanswered_query import UnansweredQuery
from models import get_db
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/uqv", tags=["UQV"])

# Pydantic models
class VaultQueryRequest(BaseModel):
    user_id: str
    session_id: str
    query_text: str
    skg_clusters_returned: int = 0
    max_cluster_conf: float = 0.0
    worker_name: str = "unknown"
    vault_reason: str = "no_cluster"

class VaultQueryResponse(BaseModel):
    query_id: int
    status: str
    vaulted: bool

class UQVStats(BaseModel):
    total_queries: int
    no_cluster_queries: int
    low_confidence_queries: int
    escalated_queries: int
    recent_queries: int

@router.post("/store", response_model=VaultQueryResponse)
async def store_unanswered_query(
    request: VaultQueryRequest,
    db: Session = Depends(get_db)
):
    """
    Store an unanswered query in the vault for later learning
    """
    try:
        logger.info(f"Vaulting query from user {request.user_id}, worker {request.worker_name}")

        # Create vault entry
        vault_entry = UnansweredQuery(
            user_id=request.user_id,
            session_id=request.session_id,
            query_text=request.query_text,
            skg_clusters_returned=request.skg_clusters_returned,
            max_cluster_conf=request.max_cluster_conf,
            worker_name=request.worker_name,
            vault_reason=request.vault_reason
        )

        db.add(vault_entry)
        db.commit()
        db.refresh(vault_entry)

        return VaultQueryResponse(
            query_id=vault_entry.id,
            status="vaulted",
            vaulted=True
        )

    except Exception as e:
        logger.error(f"Error vaulting query: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to vault query: {str(e)}")

@router.get("/stats", response_model=UQVStats)
async def get_uqv_stats(db: Session = Depends(get_db)):
    """
    Get statistics about vaulted queries
    """
    try:
        from sqlalchemy import func
        from datetime import timedelta

        # Get counts by reason
        no_cluster = db.query(func.count(UnansweredQuery.id)).filter(
            UnansweredQuery.vault_reason == "no_cluster"
        ).scalar()

        low_conf = db.query(func.count(UnansweredQuery.id)).filter(
            UnansweredQuery.vault_reason == "low_conf"
        ).scalar()

        escalated = db.query(func.count(UnansweredQuery.id)).filter(
            UnansweredQuery.vault_reason == "escalated"
        ).scalar()

        total = db.query(func.count(UnansweredQuery.id)).scalar()

        # Recent queries (last 24 hours)
        recent_cutoff = datetime.utcnow() - timedelta(hours=24)
        recent = db.query(func.count(UnansweredQuery.id)).filter(
            UnansweredQuery.created_at >= recent_cutoff
        ).scalar()

        return UQVStats(
            total_queries=total,
            no_cluster_queries=no_cluster,
            low_confidence_queries=low_conf,
            escalated_queries=escalated,
            recent_queries=recent
        )

    except Exception as e:
        logger.error(f"Error getting UQV stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@router.get("/queries")
async def get_vaulted_queries(
    limit: int = 50,
    reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get vaulted queries for review/learning
    """
    try:
        query = db.query(UnansweredQuery).order_by(UnansweredQuery.created_at.desc())

        if reason:
            query = query.filter(UnansweredQuery.vault_reason == reason)

        queries = query.limit(limit).all()

        return {
            "queries": [
                {
                    "id": q.id,
                    "user_id": q.user_id,
                    "query_text": q.query_text,
                    "clusters_returned": q.skg_clusters_returned,
                    "max_confidence": q.max_cluster_conf,
                    "worker": q.worker_name,
                    "reason": q.vault_reason,
                    "created_at": q.created_at.isoformat()
                }
                for q in queries
            ],
            "count": len(queries)
        }

    except Exception as e:
        logger.error(f"Error getting vaulted queries: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get queries: {str(e)}")

@router.delete("/query/{query_id}")
async def delete_vaulted_query(
    query_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a vaulted query (after processing/learning)
    """
    try:
        query = db.query(UnansweredQuery).filter(UnansweredQuery.id == query_id).first()

        if not query:
            raise HTTPException(status_code=404, detail="Query not found")

        db.delete(query)
        db.commit()

        return {"status": "deleted", "query_id": query_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting query: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete query: {str(e)}")