"""
GOAT Certificate Models

Data models for certificate operations and metadata.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CertificateInfo:
    """
    Information about a generated certificate.
    """
    cert_id: str
    created_at: str
    validity_days: int
    key_type: str
    status: str
    subject: Dict[str, str]
    layers: int
    chain_hash: str
    root_cert_hash: str
    ee_cert_hash: str

@dataclass
class CertificateChain:
    """
    Complete certificate chain data.
    """
    cert_id: str
    pem_chain: str
    private_key: str
    metadata: CertificateInfo

@dataclass
class CertificateRequest:
    """
    Request for certificate generation.
    """
    cert_id: str
    subject_info: Dict[str, str]
    validity_days: int = 365
    key_type: str = "rsa"
    usage: str = "general"

@dataclass
class CertificateHealth:
    """
    Health status of certificate system.
    """
    cert_status: str
    cert_store_exists: bool
    key_store_exists: bool
    total_certificates: int
    active_certificates: int
    audit_entries: int
    error: Optional[str] = None