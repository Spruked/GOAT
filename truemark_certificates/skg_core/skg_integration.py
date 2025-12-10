# skg_integration.py
"""
SKG Integration Bridge
Connects TrueMark Certificate Forge with Swarm Knowledge Graph
"""

from typing import Dict, Optional
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from skg_engine import SKGEngine

class CertificateSKGBridge:
    """
    Integration bridge between certificate forge and SKG system.
    """
    
    def __init__(self, vault_root: Path):
        """
        Initialize SKG engine with vault location.
        """
        self.engine = SKGEngine(vault_root)
        print(f"[SKG Bridge] Initialized with vault at {vault_root}")
    
    def on_certificate_minted(self, cert_data: Dict) -> Dict:
        """
        Hook called when certificate is minted.
        Ingests certificate into SKG and returns enrichment data.
        
        Args:
            cert_data: Full certificate payload
            
        Returns:
            Dict with SKG enrichment data (node IDs, drift score, patterns)
        """
        try:
            # Ingest into SKG
            skg_result = self.engine.ingest_certificate(cert_data)
            
            # Check for duplicate patterns
            duplicates = self.engine.pattern_learner.detect_duplicates(cert_data)
            
            enrichment = {
                "skg_ingested": True,
                "cert_node_id": skg_result['cert_node_id'],
                "owner_node_id": skg_result['owner_node_id'],
                "chain_node_id": skg_result['chain_node_id'],
                "drift_score": skg_result['drift_score'],
                "duplicate_risk": len(duplicates) > 0,
                "duplicate_count": len(duplicates)
            }
            
            if duplicates:
                enrichment["duplicate_certificates"] = duplicates
            
            return enrichment
        
        except Exception as e:
            print(f"[SKG Bridge] Error ingesting certificate: {e}")
            return {
                "skg_ingested": False,
                "error": str(e)
            }
    
    def get_owner_portfolio(self, wallet_address: str) -> Dict:
        """
        Query SKG for all certificates owned by wallet.
        
        Args:
            wallet_address: Owner's wallet address
            
        Returns:
            Dict with certificates and portfolio summary
        """
        return self.engine.query_by_wallet(wallet_address)
    
    def get_skg_health_metrics(self) -> Dict:
        """
        Return SKG health metrics for monitoring dashboard.
        
        Returns:
            Dict with node counts, cluster stats, drift averages
        """
        return self.engine.get_swarm_knowledge_summary()
    
    def check_duplicate_risk(self, cert_data: Dict) -> Dict:
        """
        Check if certificate matches existing patterns (duplicate detection).
        
        Args:
            cert_data: Certificate to check
            
        Returns:
            Dict with duplicate risk assessment
        """
        duplicates = self.engine.pattern_learner.detect_duplicates(cert_data)
        
        return {
            "is_duplicate": len(duplicates) > 0,
            "duplicate_count": len(duplicates),
            "duplicate_certificates": duplicates if duplicates else []
        }
    
    def get_pattern_statistics(self) -> Dict:
        """
        Return pattern clustering statistics.
        """
        return self.engine.pattern_learner.get_cluster_statistics()
