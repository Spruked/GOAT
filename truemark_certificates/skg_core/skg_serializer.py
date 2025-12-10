# skg_serializer.py
"""
SKG Serializer
Vault-compatible JSONL serialization for SKG nodes and edges
"""

import json
from typing import Dict, List
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from skg_node import SKGNode, SKGEdge, SKGNodeType

class SKGSerializer:
    """
    Handles serialization/deserialization of SKG data to vault-compatible JSONL.
    """
    
    def __init__(self, vault_root: Path):
        self.vault_root = Path(vault_root)
        self.nodes_path = self.vault_root / "skg" / "nodes.jsonl"
        self.edges_path = self.vault_root / "skg" / "edges.jsonl"
        self.transactions_path = self.vault_root / "skg" / "transactions.jsonl"
        
        # Create directories if needed
        self.nodes_path.parent.mkdir(parents=True, exist_ok=True)
    
    def save_node(self, node: SKGNode) -> None:
        """
        Append node to JSONL vault.
        """
        node_data = node.to_dict()
        
        with open(self.nodes_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(node_data) + "\n")
        
        self._log_transaction("node_created", {"node_id": node.node_id})
    
    def save_edge(self, edge: SKGEdge) -> None:
        """
        Append edge to JSONL vault.
        """
        edge_data = edge.to_dict()
        
        with open(self.edges_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(edge_data) + "\n")
        
        self._log_transaction("edge_created", {"edge_id": edge.edge_id})
    
    def load_graph(self) -> Dict[str, List]:
        """
        Load all nodes and edges from vault for warm-start.
        Returns dict with 'nodes' and 'edges' lists.
        """
        nodes = []
        edges = []
        
        # Load nodes
        if self.nodes_path.exists():
            with open(self.nodes_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        node_data = json.loads(line)
                        nodes.append(SKGNode(
                            node_id=node_data['node_id'],
                            node_type=SKGNodeType(node_data['node_type']),  # Convert string to Enum
                            properties=node_data['properties'],
                            created_by=node_data.get('created_by', 'system'),
                            created_at=node_data['created_at'],
                            version=node_data.get('version', 1),
                            is_active=node_data.get('is_active', True)
                        ))
        
        # Load edges
        if self.edges_path.exists():
            with open(self.edges_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        edge_data = json.loads(line)
                        edges.append(SKGEdge(
                            edge_id=edge_data['edge_id'],
                            source_id=edge_data['source_id'],
                            target_id=edge_data['target_id'],
                            edge_type=edge_data['edge_type'],
                            properties=edge_data['properties'],
                            confidence=edge_data.get('confidence', 1.0)
                        ))
        
        return {"nodes": nodes, "edges": edges}
    
    def _log_transaction(self, event_type: str, payload: Dict) -> None:
        """
        Record SKG transaction for monitoring.
        """
        transaction = {
            "event_type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        with open(self.transactions_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(transaction) + "\n")
    
    def get_transaction_log(self, limit: int = 100) -> List[Dict]:
        """
        Retrieve recent SKG transactions for monitoring.
        """
        transactions = []
        
        if self.transactions_path.exists():
            with open(self.transactions_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        transactions.append(json.loads(line))
        
        return transactions[-limit:]
