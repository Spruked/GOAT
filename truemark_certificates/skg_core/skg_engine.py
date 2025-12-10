# skg_engine.py
"""
SKG Engine
Main orchestrator for Swarm Knowledge Graph operations
"""

from typing import Dict, List, Optional
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from skg_node import SKGNode, SKGEdge, SKGNodeType
from skg_serializer import SKGSerializer
from skg_pattern_learner import SKGPatternLearner
from skg_drift_analyzer import SKGDriftAnalyzer

class SKGEngine:
    """
    Main SKG engine that coordinates pattern learning, drift detection, and graph queries.
    """
    
    def __init__(self, vault_root: Path):
        self.serializer = SKGSerializer(vault_root)
        self.pattern_learner = SKGPatternLearner()
        self.drift_analyzer = SKGDriftAnalyzer()
        
        # In-memory graph
        self.nodes: Dict[str, SKGNode] = {}
        self.edges: Dict[str, SKGEdge] = {}
        
        # Load existing graph from vault
        self._load_from_vault()
    
    def ingest_certificate(self, cert_data: Dict) -> Dict[str, str]:
        """
        Ingest certificate and create certificate, owner, and chain nodes + edges.
        Returns dict with created node IDs.
        """
        # Create certificate node
        cert_node_id = f"cert_{cert_data['serial_number']}"
        cert_node = SKGNode(
            node_id=cert_node_id,
            node_type=SKGNodeType.CERTIFICATE,
            properties=cert_data,
            created_by="truemark_forge",
            created_at=datetime.utcnow().isoformat() + "Z"
        )
        
        self._add_node(cert_node)
        
        # Create owner identity node
        owner_wallet = cert_data.get('owner_wallet', 'unknown')
        owner_node_id = f"owner_{owner_wallet[-16:]}"  # Last 16 chars
        
        if owner_node_id not in self.nodes:
            owner_node = SKGNode(
                node_id=owner_node_id,
                node_type=SKGNodeType.IDENTITY,
                properties={
                    "wallet_address": owner_wallet,
                    "total_certificates": 0
                },
                created_by="truemark_forge",
                created_at=datetime.utcnow().isoformat() + "Z"
            )
            self._add_node(owner_node)
        
        # Create chain node
        chain_contract = cert_data.get('chain_contract', 'unknown')
        chain_node_id = f"chain_{chain_contract[-8:]}"
        
        if chain_node_id not in self.nodes:
            chain_node = SKGNode(
                node_id=chain_node_id,
                node_type=SKGNodeType.CHAIN,
                properties={
                    "contract_address": chain_contract,
                    "chain_name": cert_data.get('chain_name', 'unknown')
                },
                created_by="truemark_forge",
                created_at=datetime.utcnow().isoformat() + "Z"
            )
            self._add_node(chain_node)
        
        # Create edges
        # 1. Owner -> Certificate (OWNS)
        owns_edge = SKGEdge(
            edge_id=f"edge_owns_{cert_node_id}",
            source_id=owner_node_id,
            target_id=cert_node_id,
            edge_type="OWNS",
            properties={"acquired_at": cert_data.get('minted_at', '')}
        )
        self._add_edge(owns_edge)
        
        # 2. Certificate -> Chain (ANCHORED_TO)
        anchored_edge = SKGEdge(
            edge_id=f"edge_anchored_{cert_node_id}",
            source_id=cert_node_id,
            target_id=chain_node_id,
            edge_type="ANCHORED_TO",
            properties={"block_height": cert_data.get('block_height', 0)}
        )
        self._add_edge(anchored_edge)
        
        # Update pattern learner
        self.pattern_learner.learn_from_certificate(cert_data)
        
        # Calculate drift
        drift_score = self.drift_analyzer.analyze_certificate_drift(cert_node)
        
        return {
            "cert_node_id": cert_node_id,
            "owner_node_id": owner_node_id,
            "chain_node_id": chain_node_id,
            "drift_score": drift_score
        }
    
    def query_by_wallet(self, wallet_address: str) -> Dict:
        """
        Traverse graph to find all certificates owned by wallet.
        """
        owner_node_id = f"owner_{wallet_address[-16:]}"
        
        if owner_node_id not in self.nodes:
            return {
                "wallet": wallet_address,
                "certificates": [],
                "total": 0
            }
        
        # Find all OWNS edges from this owner
        certificates = []
        for edge_id, edge in self.edges.items():
            if edge.source_id == owner_node_id and edge.edge_type == "OWNS":
                cert_node_id = edge.target_id
                if cert_node_id in self.nodes:
                    cert_node = self.nodes[cert_node_id]
                    certificates.append({
                        "serial_number": cert_node.properties.get('serial_number', ''),
                        "asset_id": cert_node.properties.get('asset_id', ''),
                        "ipfs_hash": cert_node.properties.get('ipfs_hash', ''),
                        "minted_at": cert_node.properties.get('minted_at', ''),
                        "acquired_at": edge.properties.get('acquired_at', '')
                    })
        
        return {
            "wallet": wallet_address,
            "certificates": certificates,
            "total": len(certificates)
        }
    
    def get_swarm_knowledge_summary(self) -> Dict:
        """
        Return monitoring metrics for dashboard.
        """
        cluster_stats = self.pattern_learner.get_cluster_statistics()
        global_drift = self.drift_analyzer.get_global_drift_average()
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "certificate_nodes": sum(1 for n in self.nodes.values() if n.node_type == SKGNodeType.CERTIFICATE),
            "identity_nodes": sum(1 for n in self.nodes.values() if n.node_type == SKGNodeType.IDENTITY),
            "chain_nodes": sum(1 for n in self.nodes.values() if n.node_type == SKGNodeType.CHAIN),
            "pattern_clusters": cluster_stats,
            "global_drift_average": global_drift,
            "vault_path": str(self.serializer.vault_root)
        }
    
    def _add_node(self, node: SKGNode) -> None:
        """Add node to in-memory graph and persist to vault."""
        self.nodes[node.node_id] = node
        self.serializer.save_node(node)
    
    def _add_edge(self, edge: SKGEdge) -> None:
        """Add edge to in-memory graph and persist to vault."""
        self.edges[edge.edge_id] = edge
        self.serializer.save_edge(edge)
    
    def _load_from_vault(self) -> None:
        """Load existing graph from vault for warm-start."""
        graph_data = self.serializer.load_graph()
        
        for node in graph_data['nodes']:
            if node.is_active:
                self.nodes[node.node_id] = node
        
        for edge in graph_data['edges']:
            self.edges[edge.edge_id] = edge
        
        # Rebuild pattern clusters from certificate nodes
        for node in self.nodes.values():
            if node.node_type == SKGNodeType.CERTIFICATE:
                self.pattern_learner.learn_from_certificate(node.properties)
        
        print(f"[SKG] Loaded {len(self.nodes)} nodes, {len(self.edges)} edges from vault")
