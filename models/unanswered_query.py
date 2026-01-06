from sqlalchemy import Column, String, Text, Float, DateTime, JSON, Integer
from sqlalchemy.sql import func
from models import Base

class UnansweredQuery(Base):
    __tablename__ = "unanswered_query"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    session_id = Column(String(36), nullable=False)
    query_text = Column(Text, nullable=False)
    query_vec = Column(JSON)                 # optional embedding
    skg_clusters_returned = Column(Integer, default=0)
    max_cluster_conf = Column(Float, default=0.0)
    worker_name = Column(String(20))         # Regent/Nora/Mark
    vault_reason = Column(String(50))        # "no_cluster"|"low_conf"|"escalated"
    created_at = Column(DateTime, server_default=func.now())