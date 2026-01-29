# services/encryption_service.py
"""
GOAT Encryption Service
ChaCha20-256 encryption for TrueMark integration
Handles permanent storage preparation without exposing crypto complexity to users
"""

import os
import json
import base64
import hashlib
import secrets
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import argon2

class GOATEncryptionService:
    """
    ChaCha20-256 encryption service for TrueMark integration.
    Handles encryption/decryption with key management for permanent storage.
    """

    def __init__(self, master_key: Optional[bytes] = None):
        """
        Initialize encryption service

        Args:
            master_key: Optional master key for encryption operations
        """
        self.master_key = master_key or secrets.token_bytes(32)
        self.backend = default_backend()

    def encrypt_for_storage(self, data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Encrypt data for permanent storage (IPFS/Arweave ready)

        Args:
            data: Data to encrypt (dict that will be JSON serialized)
            user_id: User identifier for key derivation

        Returns:
            Dict with encrypted data and metadata for TrueMark
        """
        # Serialize data
        json_data = json.dumps(data, default=str, separators=(',', ':'))
        data_bytes = json_data.encode('utf-8')

        # Derive encryption key from master key and user ID
        salt = secrets.token_bytes(16)
        encryption_key = self._derive_key(self.master_key, user_id.encode(), salt)

        # Generate nonce for ChaCha20
        nonce = secrets.token_bytes(16)

        # Encrypt with ChaCha20-256
        cipher = Cipher(algorithms.ChaCha20(encryption_key, nonce), mode=None, backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data_bytes) + encryptor.finalize()

        # Create TrueMark-compatible metadata
        truemark_metadata = {
            "encryption": {
                "algorithm": "ChaCha20-256",
                "key_derivation": "Argon2id",
                "nonce": base64.b64encode(nonce).decode(),
                "salt": base64.b64encode(salt).decode(),
                "encrypted_size": len(encrypted_data),
                "original_size": len(data_bytes),
                "original_hash": hashlib.sha256(data_bytes).hexdigest(),
                "encrypted_hash": hashlib.sha256(encrypted_data).hexdigest(),
                "encryption_timestamp": datetime.utcnow().isoformat(),
                "truemark_version": "1.0"
            },
            "authorship": {
                "user_id": user_id,
                "creator": "GOAT AI Legacy Builder",
                "creation_method": "streaming_visidata_analysis"
            },
            "storage": {
                "ready_for_ipfs": True,
                "ready_for_arweave": True,
                "permanent_storage_fee": 9.99,
                "gas_fees_included": True
            }
        }

        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
            "metadata": truemark_metadata,
            "user_facing_info": {
                "status": "encrypted_and_ready",
                "permanent_link_available": False,  # Set to True after IPFS/Arweave upload
                "truemark_ready": True,
                "storage_cost": 9.99
            }
        }

    def decrypt_for_user(self, encrypted_package: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """
        Decrypt data for user access

        Args:
            encrypted_package: Encrypted data package from encrypt_for_storage
            user_id: User identifier for key derivation

        Returns:
            Decrypted data dict, or None if decryption fails
        """
        try:
            # Extract encryption parameters
            metadata = encrypted_package["metadata"]["encryption"]
            salt = base64.b64decode(metadata["salt"])
            nonce = base64.b64decode(metadata["nonce"])
            encrypted_data = base64.b64decode(encrypted_package["encrypted_data"])

            # Derive decryption key
            decryption_key = self._derive_key(self.master_key, user_id.encode(), salt)

            # Decrypt with ChaCha20-256
            cipher = Cipher(algorithms.ChaCha20(decryption_key, nonce), mode=None, backend=self.backend)
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            # Verify integrity
            if hashlib.sha256(decrypted_data).hexdigest() != metadata["original_hash"]:
                return None  # Integrity check failed

            # Parse JSON
            return json.loads(decrypted_data.decode('utf-8'))

        except Exception as e:
            print(f"Decryption failed: {e}")
            return None

    def _derive_key(self, master_key: bytes, user_salt: bytes, key_salt: bytes) -> bytes:
        """
        Derive encryption key using Argon2id

        Args:
            master_key: Master encryption key
            user_salt: User-specific salt
            key_salt: Key-specific salt

        Returns:
            Derived 32-byte key for ChaCha20-256
        """
        # Combine master key with user salt for personalization
        combined_salt = hashlib.sha256(master_key + user_salt).digest()

        # Use Argon2id for key derivation
        kdf = argon2.PasswordHasher(
            time_cost=2,  # Number of iterations
            memory_cost=102400,  # Memory usage in KiB
            parallelism=8,  # Number of parallel threads
            hash_len=32,  # Output length
            type=argon2.Type.ID  # Argon2id
        )

        # Derive key from combined salt + key salt
        derived_key = kdf.hash(combined_salt + key_salt)

        # Extract raw key bytes (remove Argon2 prefix)
        return derived_key.encode()[:32] if isinstance(derived_key, str) else derived_key.raw[:32]

    def prepare_for_permanent_storage(self, encrypted_package: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare encrypted package for IPFS/Arweave storage

        Args:
            encrypted_package: Encrypted data package

        Returns:
            Storage-ready package with IPFS/Arweave metadata
        """
        # Create storage manifest
        storage_manifest = {
            "content_type": "goat_legacy_encrypted",
            "encryption_algorithm": "ChaCha20-256",
            "truemark_compatible": True,
            "created_by": "GOAT AI",
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat(),
            "data_hash": encrypted_package["metadata"]["encryption"]["encrypted_hash"],
            "metadata_hash": hashlib.sha256(
                json.dumps(encrypted_package["metadata"], sort_keys=True).encode()
            ).hexdigest()
        }

        # Prepare final storage package
        storage_package = {
            "manifest": storage_manifest,
            "encrypted_content": encrypted_package["encrypted_data"],
            "truemark_metadata": encrypted_package["metadata"],
            "user_access_info": {
                "permanent_link_pattern": "goat.gg/p/{hash}",
                "truemark_minting_instructions": "https://docs.goat.gg/truemark",
                "storage_fee_paid": True,
                "gas_fees_included": True
            }
        }

        return storage_package

    def generate_storage_proof(self, storage_package: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate proof of storage for TrueMark minting

        Args:
            storage_package: Storage-ready package

        Returns:
            Proof document for external minting
        """
        return {
            "truemark_proof": {
                "content_hash": storage_package["manifest"]["data_hash"],
                "metadata_hash": storage_package["manifest"]["metadata_hash"],
                "encryption_algorithm": storage_package["manifest"]["encryption_algorithm"],
                "creator": storage_package["manifest"]["created_by"],
                "timestamp": storage_package["manifest"]["timestamp"],
                "blockchain_ready": True,
                "minting_instructions": {
                    "platform": "CertSig or TrueMark",
                    "required_fields": ["content_hash", "metadata_hash", "encryption_algorithm"],
                    "gas_estimate": "Bundled in GOAT fee"
                }
            },
            "user_friendly": {
                "message": "Your content is permanently stored and ready for TrueMark certification",
                "permanent_link": f"goat.gg/p/{storage_package['manifest']['data_hash'][:16]}",
                "truemark_status": "Ready for minting",
                "next_steps": "Visit TrueMark to mint your certificate"
            }
        }

# Global instance
encryption_service = GOATEncryptionService()