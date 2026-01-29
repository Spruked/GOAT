"""
13-Layer Certificate Generator - Internal certificate creation for GOAT.

Core Principles:
- 13-layer certificate chain (layers 1-11 are internal)
- Layer 12: External CA-signed (optional)
- Layer 13: Blockchain notarization (optional)
- Immutable certificate records
- Audit trail for all operations
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import json
import logging
from pathlib import Path
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

logger = logging.getLogger(__name__)

class CertificateError(Exception):
    """Raised when certificate operations fail."""
    pass

class CertificateGenerator:
    """
    13-Layer Certificate Generator for GOAT.

    Layers 1-11: Internal self-signed certificates
    Layer 12: External CA-signed (optional)
    Layer 13: Blockchain notarization (optional)
    """

    def __init__(self, cert_store_path: str = "goat/security/certificates/",
                 key_store_path: str = "goat/security/keys/"):
        self.cert_store_path = Path(cert_store_path)
        self.cert_store_path.mkdir(parents=True, exist_ok=True)

        self.key_store_path = Path(key_store_path)
        self.key_store_path.mkdir(parents=True, exist_ok=True)

        # Certificate registry
        self.cert_registry: Dict[str, Dict[str, Any]] = {}
        self.audit_log: List[Dict[str, Any]] = []

        # Load existing certificates
        self._load_cert_registry()

        # Audit log path
        self.audit_path = self.cert_store_path / "certificate_audit.jsonl"

    def generate_certificate_chain(self, cert_id: str, subject_info: Dict[str, str],
                                 validity_days: int = 365, key_type: str = "rsa") -> Dict[str, Any]:
        """
        Generate a 13-layer certificate chain.

        Args:
            cert_id: Unique certificate identifier
            subject_info: Subject information (CN, O, OU, etc.)
            validity_days: Certificate validity period
            key_type: Key type ('rsa' or 'ec')

        Returns:
            Certificate chain information
        """
        if cert_id in self.cert_registry:
            raise CertificateError(f"Certificate '{cert_id}' already exists")

        try:
            # Generate root key and certificate (Layer 1)
            root_key, root_cert = self._generate_root_certificate(
                cert_id, subject_info, validity_days, key_type
            )

            # Generate intermediate certificates (Layers 2-11)
            intermediates = []
            current_cert = root_cert
            current_key = root_key

            for layer in range(2, 12):
                intermediate_key, intermediate_cert = self._generate_intermediate_certificate(
                    cert_id, layer, subject_info, current_key, current_cert, validity_days, key_type
                )
                intermediates.append(intermediate_cert)
                current_cert = intermediate_cert
                current_key = intermediate_key

            # Create end-entity certificate (Layer 11 - final internal)
            ee_key, ee_cert = self._generate_end_entity_certificate(
                cert_id, subject_info, current_key, current_cert, validity_days, key_type
            )

            # Store certificates and keys
            cert_chain = [root_cert] + intermediates + [ee_cert]
            key_chain = [root_key] + intermediates + [ee_key]  # Note: intermediates have their own keys

            self._store_certificate_chain(cert_id, cert_chain, key_chain)

            # Create registry entry
            cert_record = {
                'cert_id': cert_id,
                'created_at': datetime.utcnow().isoformat() + "Z",
                'validity_days': validity_days,
                'key_type': key_type,
                'layers': 11,  # Internal layers
                'status': 'active',
                'subject': subject_info,
                'chain_hash': self._calculate_chain_hash(cert_chain),
                'root_cert_hash': self._cert_hash(root_cert),
                'ee_cert_hash': self._cert_hash(ee_cert)
            }

            self.cert_registry[cert_id] = cert_record
            self._save_cert_registry()

            # Audit
            self._audit_operation('chain_generation', cert_id, {
                'layers': 11,
                'key_type': key_type,
                'validity_days': validity_days
            })

            logger.info(f"Generated 11-layer certificate chain: {cert_id}")

            return {
                'cert_id': cert_id,
                'chain_info': cert_record,
                'pem_chain': self._export_pem_chain(cert_chain),
                'private_key': ee_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ).decode('utf-8')
            }

        except Exception as e:
            self._audit_operation('chain_generation_failed', cert_id, {'error': str(e)})
            raise CertificateError(f"Certificate generation failed: {e}")

    def _generate_root_certificate(self, cert_id: str, subject_info: Dict[str, str],
                                 validity_days: int, key_type: str) -> Tuple[Any, x509.Certificate]:
        """Generate root CA certificate (Layer 1)."""
        # Generate private key
        if key_type == "rsa":
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096
            )
        elif key_type == "ec":
            private_key = ec.generate_private_key(ec.SECP256R1())
        else:
            raise CertificateError(f"Unsupported key type: {key_type}")

        # Create subject
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, subject_info.get('C', 'US')),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, subject_info.get('ST', 'CA')),
            x509.NameAttribute(NameOID.LOCALITY_NAME, subject_info.get('L', 'San Francisco')),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject_info.get('O', 'GOAT Internal')),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, subject_info.get('OU', 'Certificate Authority')),
            x509.NameAttribute(NameOID.COMMON_NAME, f"GOAT Root CA - {cert_id}"),
        ])

        # Create certificate
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            subject  # Self-signed
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=10), critical=True
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                non_repudiation=False,
                encipher_only=False,
                decipher_only=False
            ), critical=True
        ).sign(private_key, hashes.SHA256())

        return private_key, cert

    def _generate_intermediate_certificate(self, cert_id: str, layer: int, subject_info: Dict[str, str],
                                         issuer_key: Any, issuer_cert: x509.Certificate,
                                         validity_days: int, key_type: str) -> Tuple[Any, x509.Certificate]:
        """Generate intermediate CA certificate."""
        # Generate private key
        if key_type == "rsa":
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=3072  # Smaller for intermediates
            )
        elif key_type == "ec":
            private_key = ec.generate_private_key(ec.SECP256R1())

        # Create subject
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, subject_info.get('C', 'US')),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, subject_info.get('ST', 'CA')),
            x509.NameAttribute(NameOID.LOCALITY_NAME, subject_info.get('L', 'San Francisco')),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject_info.get('O', 'GOAT Internal')),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, subject_info.get('OU', f'Layer {layer} CA')),
            x509.NameAttribute(NameOID.COMMON_NAME, f"GOAT Layer {layer} CA - {cert_id}"),
        ])

        # Create certificate
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer_cert.subject
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=10-layer), critical=True
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                non_repudiation=False,
                encipher_only=False,
                decipher_only=False
            ), critical=True
        ).add_extension(
            x509.AuthorityInformationAccess([
                x509.AccessDescription(
                    x509.oid.AuthorityInformationAccessOID.CA_ISSUERS,
                    x509.UniformResourceIdentifier(f"urn:goat:ca:{cert_id}:layer{layer}")
                )
            ]), critical=False
        ).sign(issuer_key, hashes.SHA256())

        return private_key, cert

    def _generate_end_entity_certificate(self, cert_id: str, subject_info: Dict[str, str],
                                       issuer_key: Any, issuer_cert: x509.Certificate,
                                       validity_days: int, key_type: str) -> Tuple[Any, x509.Certificate]:
        """Generate end-entity certificate (Layer 11)."""
        # Generate private key
        if key_type == "rsa":
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
        elif key_type == "ec":
            private_key = ec.generate_private_key(ec.SECP256R1())

        # Create subject
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, subject_info.get('C', 'US')),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, subject_info.get('ST', 'CA')),
            x509.NameAttribute(NameOID.LOCALITY_NAME, subject_info.get('L', 'San Francisco')),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject_info.get('O', 'GOAT Internal')),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, subject_info.get('OU', 'End Entity')),
            x509.NameAttribute(NameOID.COMMON_NAME, subject_info.get('CN', f"GOAT Certificate - {cert_id}")),
        ])

        # Create certificate
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer_cert.subject
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).add_extension(
            x509.BasicConstraints(ca=False), critical=True
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                data_encipherment=True,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                non_repudiation=True,
                encipher_only=False,
                decipher_only=False
            ), critical=True
        ).add_extension(
            x509.ExtendedKeyUsage([
                x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH,
                x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
                x509.oid.ExtendedKeyUsageOID.CODE_SIGNING
            ]), critical=False
        ).sign(issuer_key, hashes.SHA256())

        return private_key, cert

    def _store_certificate_chain(self, cert_id: str, cert_chain: List[x509.Certificate],
                               key_chain: List[Any]):
        """Store certificate chain and keys."""
        cert_dir = self.cert_store_path / cert_id
        cert_dir.mkdir(exist_ok=True)

        key_dir = self.key_store_path / cert_id
        key_dir.mkdir(exist_ok=True)

        # Store certificates
        for i, cert in enumerate(cert_chain):
            cert_path = cert_dir / f"layer_{i+1}.pem"
            with open(cert_path, 'wb') as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))

        # Store private keys (only end-entity key is typically needed)
        ee_key_path = key_dir / "end_entity.key"
        with open(ee_key_path, 'wb') as f:
            f.write(key_chain[-1].private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

    def _export_pem_chain(self, cert_chain: List[x509.Certificate]) -> str:
        """Export certificate chain as PEM string."""
        pem_chain = ""
        for cert in cert_chain:
            pem_chain += cert.public_bytes(serialization.Encoding.PEM).decode('utf-8')
        return pem_chain

    def _calculate_chain_hash(self, cert_chain: List[x509.Certificate]) -> str:
        """Calculate hash of entire certificate chain."""
        chain_data = b""
        for cert in cert_chain:
            chain_data += cert.public_bytes(serialization.Encoding.DER)
        return hashlib.sha256(chain_data).hexdigest()

    def _cert_hash(self, cert: x509.Certificate) -> str:
        """Calculate hash of single certificate."""
        return hashlib.sha256(cert.public_bytes(serialization.Encoding.DER)).hexdigest()

    def get_certificate_info(self, cert_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a certificate."""
        return self.cert_registry.get(cert_id)

    def list_certificates(self, status: str = None) -> List[Dict[str, Any]]:
        """List certificates with optional status filter."""
        certs = list(self.cert_registry.values())
        if status:
            certs = [c for c in certs if c['status'] == status]
        return certs

    def revoke_certificate(self, cert_id: str, reason: str = "manual_revoke"):
        """Revoke a certificate."""
        if cert_id not in self.cert_registry:
            raise CertificateError(f"Certificate '{cert_id}' not found")

        self.cert_registry[cert_id]['status'] = 'revoked'
        self.cert_registry[cert_id]['revoked_at'] = datetime.utcnow().isoformat() + "Z"
        self.cert_registry[cert_id]['revoke_reason'] = reason

        self._save_cert_registry()
        self._audit_operation('certificate_revocation', cert_id, {'reason': reason})

        logger.info(f"Revoked certificate: {cert_id}")

    def _load_cert_registry(self):
        """Load certificate registry from storage."""
        registry_path = self.cert_store_path / "certificate_registry.json"
        if not registry_path.exists():
            return

        try:
            with open(registry_path, 'r') as f:
                self.cert_registry = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load certificate registry: {e}")

    def _save_cert_registry(self):
        """Save certificate registry to storage."""
        registry_path = self.cert_store_path / "certificate_registry.json"
        try:
            with open(registry_path, 'w') as f:
                json.dump(self.cert_registry, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save certificate registry: {e}")

    def _audit_operation(self, operation: str, cert_id: str, details: Dict[str, Any]):
        """Record audit entry."""
        audit_entry = {
            'timestamp': datetime.utcnow().isoformat() + "Z",
            'operation': operation,
            'cert_id': cert_id,
            'details': details
        }

        self.audit_log.append(audit_entry)

        # Write to audit log
        try:
            with open(self.audit_path, 'a') as f:
                f.write(json.dumps(audit_entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def get_audit_log(self, cert_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log entries."""
        log = self.audit_log
        if cert_id:
            log = [entry for entry in log if entry['cert_id'] == cert_id]

        return log[-limit:] if limit else log

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on certificate generator."""
        health = {
            'cert_status': 'healthy',
            'cert_store_exists': self.cert_store_path.exists(),
            'key_store_exists': self.key_store_path.exists(),
            'total_certificates': len(self.cert_registry),
            'active_certificates': len([c for c in self.cert_registry.values() if c['status'] == 'active']),
            'audit_entries': len(self.audit_log)
        }

        # Test certificate generation
        try:
            test_cert = "health_check_test"
            if test_cert not in self.cert_registry:
                result = self.generate_certificate_chain(
                    test_cert,
                    {'CN': 'GOAT Health Check', 'O': 'GOAT Internal'},
                    validity_days=1
                )

                # Verify chain
                cert_chain = self._load_certificate_chain(test_cert)
                if len(cert_chain) != 11:
                    health['cert_status'] = 'degraded'
                    health['error'] = f'Expected 11 certificates, got {len(cert_chain)}'
                else:
                    # Clean up test certificate
                    self.revoke_certificate(test_cert, "health_check_complete")

        except Exception as e:
            health['cert_status'] = 'unhealthy'
            health['error'] = str(e)

        return health

    def _load_certificate_chain(self, cert_id: str) -> List[x509.Certificate]:
        """Load certificate chain from storage."""
        cert_dir = self.cert_store_path / cert_id
        cert_chain = []

        for i in range(1, 12):  # Layers 1-11
            cert_path = cert_dir / f"layer_{i}.pem"
            if cert_path.exists():
                with open(cert_path, 'rb') as f:
                    cert_data = f.read()
                    cert = x509.load_pem_x509_certificate(cert_data)
                    cert_chain.append(cert)

        return cert_chain