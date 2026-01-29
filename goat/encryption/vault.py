"""
GOAT Encryption Vault

Unified interface for GOAT's encryption operations.
Provides ChaCha20-Poly1305 authenticated encryption.
"""

from typing import Dict, Any, Optional
from goat.security.chacha20_vault import ChaCha20EncryptionVault

class EncryptionVault:
    """
    GOAT Encryption Vault.

    Unified interface for encryption operations.
    Wraps ChaCha20EncryptionVault for simplified usage.
    """

    def __init__(self, vault_path: str = "goat/security/vault/",
                 key_store_path: str = "goat/security/keys/"):
        """
        Initialize encryption vault.

        Args:
            vault_path: Path to store vault data
            key_store_path: Path to store encryption keys
        """
        self.vault = ChaCha20EncryptionVault(vault_path, key_store_path)

    async def encrypt(self, data: bytes, key_id: str = None,
                     context: str = "general") -> Dict[str, Any]:
        """
        Encrypt data using specified or default key.

        Args:
            data: Data to encrypt
            key_id: Encryption key ID (creates if doesn't exist)
            context: Key usage context

        Returns:
            Encryption result
        """
        if key_id is None:
            key_id = "default_general"
            if key_id not in [k['key_id'] for k in self.vault.list_keys()]:
                self.vault.create_data_key(key_id, context)

        return await self.vault.encrypt_data(key_id, data)

    async def decrypt(self, encryption_result: Dict[str, Any]) -> bytes:
        """
        Decrypt data from encryption result.

        Args:
            encryption_result: Result from encrypt operation

        Returns:
            Decrypted data
        """
        return await self.vault.decrypt_data(encryption_result)

    def create_key(self, key_id: str, context: str = "general") -> str:
        """
        Create a new encryption key.

        Args:
            key_id: Unique key identifier
            context: Key usage context

        Returns:
            Key identifier
        """
        return self.vault.create_data_key(key_id, context)

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on encryption vault.

        Returns:
            Health status information
        """
        return await self.vault.health_check()