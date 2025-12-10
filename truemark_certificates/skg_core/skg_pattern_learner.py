# skg_pattern_learner.py
"""
Pattern Learning Engine
Detects patterns in certificate data for deduplication and anomaly detection
"""

from collections import defaultdict
from typing import List, Dict, Set
import hashlib
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from skg_node import SKGNode, SKGNodeType

class SKGPatternLearner:
    """
    Detects patterns in certificate data for deduplication and anomaly detection.
    Runs in FusionQueueEngine for swarm-wide pattern convergence.
    """
    
    def __init__(self):
        self.pattern_clusters: Dict[str, List[str]] = defaultdict(list)
        self.owner_fingerprint_cache: Dict[str, str] = {}
    
    def learn_from_certificate(self, cert_data: Dict):
        """
        Extract patterns and cluster similar certificates.
        """
        
        # Pattern 1: Wallet ownership frequency
        wallet_hash = self._hash_wallet_behavior(cert_data.get('owner_wallet', ''))
        self.pattern_clusters[f"wallet_behavior:{wallet_hash}"].append(cert_data['serial_number'])
        
        # Pattern 2: IPFS storage pattern (detects duplicate content)
        ipfs_hash = cert_data.get('ipfs_hash', '')
        if ipfs_hash and len(ipfs_hash) > 16:
            ipfs_pattern = ipfs_hash[:16]  # First 16 chars
            self.pattern_clusters[f"ipfs_prefix:{ipfs_pattern}"].append(cert_data['serial_number'])
        
        # Pattern 3: Temporal issuance pattern
        minted_at = cert_data.get('minted_at', '')
        if len(minted_at) >= 13:
            hour_bucket = minted_at[:13]  # YYYY-MM-DDTHH
            self.pattern_clusters[f"issuance_hour:{hour_bucket}"].append(cert_data['serial_number'])
        
        # Pattern 4: Chain activity pattern
        chain_name = cert_data.get('chain_name', 'Unknown')
        self.pattern_clusters[f"chain_activity:{chain_name}"].append(cert_data['serial_number'])
    
    def _hash_wallet_behavior(self, wallet_address: str) -> str:
        """
        Create behavior fingerprint from wallet address.
        """
        # Simple behavioral hash (expand with transaction history)
        behavior_string = f"{wallet_address}"
        return hashlib.md5(behavior_string.encode()).hexdigest()[:8]
    
    def detect_duplicates(self, cert_data: Dict) -> List[str]:
        """
        Check if this certificate is a duplicate of existing ones.
        """
        duplicates = []
        ipfs_hash = cert_data.get('ipfs_hash', '')
        
        if ipfs_hash and len(ipfs_hash) > 16:
            for pattern_key, cert_ids in self.pattern_clusters.items():
                if pattern_key.startswith("ipfs_prefix:") and ipfs_hash[:16] in pattern_key:
                    # Don't include current cert in duplicates
                    duplicates.extend([c for c in cert_ids if c != cert_data.get('serial_number')])
        
        return duplicates
    
    def get_cluster_statistics(self) -> dict:
        """Return pattern cluster statistics."""
        return {
            "total_clusters": len(self.pattern_clusters),
            "wallet_behavior_clusters": len([k for k in self.pattern_clusters if k.startswith("wallet_behavior:")]),
            "ipfs_clusters": len([k for k in self.pattern_clusters if k.startswith("ipfs_prefix:")]),
            "temporal_clusters": len([k for k in self.pattern_clusters if k.startswith("issuance_hour:")])
        }
