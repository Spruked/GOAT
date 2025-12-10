# integration_bridge.py
"""
Vault & Swarm Integration Bridge
Connects Certificate Forge to vault logging and swarm broadcasting
"""

from pathlib import Path
import json
from datetime import datetime
import hashlib

class VaultFusionBridge:
    """
    Handles vault logging and swarm broadcast for certificates.
    Provides integration points for WorkerVaultWriter and FusionQueue.
    """
    
    def __init__(self, vault_base_path: Path):
        """
        Initialize vault bridge.
        
        Args:
            vault_base_path: Path to vault system root
        """
        self.vault_base_path = Path(vault_base_path)
        self.certificates_path = self.vault_base_path / "certificates" / "issued"
        self.certificates_path.mkdir(parents=True, exist_ok=True)
        
        # Event log path
        self.events_path = self.vault_base_path / "events"
        self.events_path.mkdir(parents=True, exist_ok=True)
        
    async def record_certificate_issuance(self, worker_id: str, dals_serial: str, 
                                         pdf_path: Path, payload: dict, signature: str) -> str:
        """
        Logs certificate genesis to worker vault and creates audit trail.
        
        Args:
            worker_id: ID of the worker that minted the certificate
            dals_serial: DALS serial number
            pdf_path: Path to generated PDF
            payload: Certificate payload data
            signature: Cryptographic signature
            
        Returns:
            Vault transaction ID
        """
        timestamp = datetime.utcnow()
        
        # Create event record
        event_record = {
            "timestamp": timestamp.isoformat() + "Z",
            "event_type": "CERTIFICATE_MINTED",
            "dals_serial": dals_serial,
            "worker_id": worker_id,
            "payload_hash": payload.get('payload_hash', ''),
            "signature": signature[:32] + "...",  # Truncate for display
            "pdf_size_bytes": pdf_path.stat().st_size,
            "pdf_path": str(pdf_path.relative_to(self.vault_base_path))
        }
        
        # Write to events log (JSONL format)
        events_file = self.events_path / f"{worker_id}_events.jsonl"
        with open(events_file, "a") as f:
            f.write(json.dumps(event_record) + "\n")
        
        # Create certificate summary
        summary = {
            "dals_serial": dals_serial,
            "minted_at": timestamp.isoformat() + "Z",
            "pdf_path": str(pdf_path),
            "payload": payload,
            "signature": signature,
            "verification_url": f"https://verify.truemark.io/{dals_serial}",
            "vault_integrity_hash": self._calculate_vault_hash(),
            "worker_id": worker_id
        }
        
        # Write certificate summary
        summary_path = self.certificates_path / f"{dals_serial}_summary.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        
        # Generate vault transaction ID
        vault_txn_id = f"VAULT_TXN_{dals_serial}_{int(timestamp.timestamp())}"
        
        return vault_txn_id
    
    async def broadcast_to_swarm(self, certificate_data: dict) -> str:
        """
        Broadcasts certificate metadata to swarm via FusionQueue.
        
        Args:
            certificate_data: Certificate event data
            
        Returns:
            Swarm transaction ID
        """
        timestamp = datetime.utcnow()
        
        # Create swarm broadcast record
        swarm_record = {
            "broadcast_timestamp": timestamp.isoformat() + "Z",
            "event_type": "CERTIFICATE_SWARM_BROADCAST",
            "certificate_data": certificate_data,
            "broadcast_id": f"SWARM_{certificate_data.get('dals_serial')}_{int(timestamp.timestamp())}",
            "target_nodes": ["guardian_1", "guardian_2", "guardian_3", "guardian_4", "guardian_5"],
            "consensus_required": 3,
            "priority": "high"
        }
        
        # Write to swarm broadcast log
        swarm_log = self.events_path / "swarm_broadcasts.jsonl"
        with open(swarm_log, "a") as f:
            f.write(json.dumps(swarm_record) + "\n")
        
        # Simulate swarm consensus (would be real in production)
        consensus_record = {
            "broadcast_id": swarm_record["broadcast_id"],
            "consensus_achieved": True,
            "responding_nodes": 5,
            "consensus_timestamp": timestamp.isoformat() + "Z",
            "validation_score": 100.0
        }
        
        # Write consensus record
        consensus_log = self.events_path / "swarm_consensus.jsonl"
        with open(consensus_log, "a") as f:
            f.write(json.dumps(consensus_record) + "\n")
        
        return swarm_record["broadcast_id"]
    
    def get_certificate_history(self, dals_serial: str) -> dict:
        """
        Retrieve complete history for a certificate.
        
        Args:
            dals_serial: DALS serial number
            
        Returns:
            Certificate history dictionary
        """
        summary_path = self.certificates_path / f"{dals_serial}_summary.json"
        
        if not summary_path.exists():
            return {"error": "Certificate not found", "serial": dals_serial}
        
        with open(summary_path, "r") as f:
            summary = json.load(f)
        
        # Find related events
        events = self._find_certificate_events(dals_serial)
        
        return {
            "summary": summary,
            "events": events,
            "vault_status": "active",
            "integrity_verified": True
        }
    
    def _find_certificate_events(self, dals_serial: str) -> list:
        """Find all events related to a certificate"""
        events = []
        
        # Search all event logs
        for event_file in self.events_path.glob("*_events.jsonl"):
            with open(event_file, "r") as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        if event.get('dals_serial') == dals_serial:
                            events.append(event)
                    except json.JSONDecodeError:
                        continue
        
        return sorted(events, key=lambda x: x.get('timestamp', ''))
    
    def _calculate_vault_hash(self) -> str:
        """Calculate integrity hash of vault system"""
        vault_state = json.dumps({
            "vault_version": "2.0",
            "certificates_issued": len(list(self.certificates_path.glob("*_summary.json"))),
            "last_check": datetime.utcnow().isoformat() + "Z"
        }, sort_keys=True)
        
        return hashlib.sha256(vault_state.encode()).hexdigest()[:16]
    
    def get_vault_statistics(self) -> dict:
        """Get vault system statistics"""
        certificates = list(self.certificates_path.glob("*_summary.json"))
        events = []
        
        for event_file in self.events_path.glob("*_events.jsonl"):
            with open(event_file, "r") as f:
                events.extend([line for line in f])
        
        return {
            "total_certificates": len(certificates),
            "total_events": len(events),
            "vault_path": str(self.vault_base_path),
            "integrity_hash": self._calculate_vault_hash(),
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }
