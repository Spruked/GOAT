"""
GOAT Internal Certificate Generator

Interface for generating GOAT's internal 13-layer certificate chains.
Layers 1-11 are internal; 12-13 are external integrations.
"""

from typing import Dict, Any, Optional
from goat.security.certificate_generator import CertificateGenerator

class InternalCertificateGenerator:
    """
    GOAT Internal Certificate Generator.

    Generates 11-layer internal certificate chains for GOAT operations.
    Provides simplified interface for common certificate operations.
    """

    def __init__(self, cert_store_path: str = "goat/security/certificates/",
                 key_store_path: str = "goat/security/keys/"):
        """
        Initialize certificate generator.

        Args:
            cert_store_path: Path to store certificates
            key_store_path: Path to store private keys
        """
        self.generator = CertificateGenerator(cert_store_path, key_store_path)

    def generate_certificate(self, cert_id: str, subject_info: Dict[str, str],
                           validity_days: int = 365, key_type: str = "rsa") -> Dict[str, Any]:
        """
        Generate an 11-layer internal certificate chain.

        Args:
            cert_id: Unique certificate identifier
            subject_info: Subject information (CN, O, OU, etc.)
            validity_days: Certificate validity period
            key_type: Key type ('rsa' or 'ec')

        Returns:
            Certificate generation result
        """
        return self.generator.generate_certificate_chain(
            cert_id, subject_info, validity_days, key_type
        )

    def get_certificate_info(self, cert_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a certificate.

        Args:
            cert_id: Certificate identifier

        Returns:
            Certificate information or None if not found
        """
        return self.generator.get_certificate_info(cert_id)

    def list_certificates(self, status: str = None) -> list:
        """
        List certificates with optional status filter.

        Args:
            status: Filter by status ('active', 'revoked', etc.)

        Returns:
            List of certificates
        """
        return self.generator.list_certificates(status)

    def revoke_certificate(self, cert_id: str, reason: str = "manual_revoke"):
        """
        Revoke a certificate.

        Args:
            cert_id: Certificate to revoke
            reason: Revocation reason
        """
        self.generator.revoke_certificate(cert_id, reason)

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on certificate generator.

        Returns:
            Health status information
        """
        return await self.generator.health_check()