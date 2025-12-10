# skg_node.py
"""
SKG Node & Edge Types
Defines core data structures for the Swarm Knowledge Graph
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any

class SKGNodeType(Enum):
    """Node types in the knowledge graph."""
    CERTIFICATE = "certificate"
    IDENTITY = "identity"
    CHAIN = "chain"
    PATTERN = "pattern"
    DRIFT_EVENT = "drift_event"

@dataclass
class SKGNode:
    """Immutable node representing an entity in the graph."""
    node_id: str
    node_type: SKGNodeType
    properties: Dict[str, Any]
    created_by: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    version: int = 1
    is_active: bool = True
    
    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "properties": self.properties,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "version": self.version,
            "is_active": self.is_active
        }

@dataclass
class SKGEdge:
    """Directed edge representing a relationship."""
    edge_id: str
    source_id: str
    target_id: str
    edge_type: str
    properties: Dict[str, Any]
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    confidence: float = 1.0
    
    def to_dict(self) -> dict:
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": self.edge_type,
            "properties": self.properties,
            "created_at": self.created_at,
            "confidence": self.confidence
        }
