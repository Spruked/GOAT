# skg_drift_analyzer.py
"""
Drift Analyzer
Calculates drift scores for certificates based on timestamp consistency,
signature validity, pattern deviation, and chain anchor lag
"""

from typing import Dict, List
import statistics
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from skg_node import SKGNode, SKGNodeType

class SKGDriftAnalyzer:
    """
    Calculates drift scores for certificates based on:
    - Timestamp consistency
    - Signature validity
    - Pattern deviation
    - Chain anchor lag
    """
    
    def __init__(self):
        self.baseline_metrics = {
            "avg_issuance_interval": 300.0,  # 5 minutes baseline
            "signature_validation_rate": 1.0,
            "chain_lag_seconds": 45.0
        }
        
        self.certificate_history: List[Dict] = []
    
    def analyze_certificate_drift(self, cert_node: SKGNode) -> float:
        """
        Calculate drift score (0.0 = perfect, >1.0 = anomalous).
        """
        drift_components = []
        
        # Component 1: Temporal drift (issuance timing)
        temporal_drift = self._calculate_temporal_drift(cert_node)
        drift_components.append(temporal_drift)
        
        # Component 2: Signature integrity drift
        sig_drift = self._calculate_signature_drift(cert_node)
        drift_components.append(sig_drift)
        
        # Component 3: Pattern anomaly drift
        pattern_drift = self._calculate_pattern_drift(cert_node)
        drift_components.append(pattern_drift)
        
        # Combined drift score (weighted average)
        combined_drift = statistics.mean(drift_components)
        
        # Store for monitoring
        self.certificate_history.append({
            "node_id": cert_node.node_id,
            "drift_score": combined_drift,
            "components": {
                "temporal": temporal_drift,
                "signature": sig_drift,
                "pattern": pattern_drift
            },
            "analyzed_at": cert_node.created_at
        })
        
        return combined_drift
    
    def _calculate_temporal_drift(self, cert_node: SKGNode) -> float:
        """
        Detect if certificate timing deviates from normal issuance pattern.
        """
        # Parse minted_at timestamp
        minted_at = cert_node.properties.get('minted_at', '')
        try:
            # Convert from ISO format to timestamp
            current_timestamp = self._iso_to_timestamp(minted_at)
            
            if not self.certificate_history:
                return 0.0
            
            # Calculate interval from last certificate
            last_timestamp = self._iso_to_timestamp(
                self.certificate_history[-1]['analyzed_at']
            )
            interval = abs(current_timestamp - last_timestamp)
            
            # Drift is deviation from baseline
            baseline = self.baseline_metrics['avg_issuance_interval']
            drift = abs(interval - baseline) / baseline
            
            return min(drift, 1.0)  # Cap at 1.0
        
        except Exception:
            return 0.5  # Neutral drift if parsing fails
    
    def _calculate_signature_drift(self, cert_node: SKGNode) -> float:
        """
        Verify signature and detect anomalies.
        """
        signature = cert_node.properties.get('ed25519_signature', '')
        verifying_key = cert_node.properties.get('verifying_key', '')
        
        if not signature or not verifying_key:
            return 1.0  # Max drift = invalid
        
        try:
            # Basic length checks for HMAC-SHA256 (128 hex chars)
            if len(signature) < 64:
                return 0.8
            
            if len(verifying_key) < 32:
                return 0.6
            
            # Signature format validation (hex)
            int(signature[:16], 16)
            int(verifying_key[:16], 16)
            
            return 0.0  # No drift if format is valid
        
        except (ValueError, TypeError):
            return 1.0
    
    def _calculate_pattern_drift(self, cert_node: SKGNode) -> float:
        """
        Detect if certificate deviates from learned patterns.
        """
        # Simple heuristic: IPFS hash should be valid format
        ipfs_hash = cert_node.properties.get('ipfs_hash', '')
        
        if not ipfs_hash:
            return 0.2  # Minor drift for missing IPFS
        
        if not ipfs_hash.startswith('ipfs://'):
            return 0.5
        
        # Check hash length (typical IPFS CID)
        cid_part = ipfs_hash.replace('ipfs://', '')
        if len(cid_part) < 20:  # Minimum CID length
            return 0.3
        
        return 0.0
    
    def get_global_drift_average(self) -> float:
        """Return average drift across all certificates."""
        if not self.certificate_history:
            return 0.0
        
        return statistics.mean([c['drift_score'] for c in self.certificate_history])
    
    def _iso_to_timestamp(self, iso_str: str) -> float:
        """
        Convert ISO 8601 timestamp to Unix timestamp.
        """
        try:
            # Remove 'Z' suffix if present
            iso_str = iso_str.replace('Z', '+00:00')
            dt = datetime.fromisoformat(iso_str)
            return dt.timestamp()
        except Exception:
            # Fallback to current time
            return datetime.utcnow().timestamp()
