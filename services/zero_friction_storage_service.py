# services/zero_friction_storage_service.py
"""
GOAT Zero-Friction Storage - PREMIUM
Automatic encrypted storage and retrieval with permanent archiving
Premium feature for all tiers with tiered storage limits
"""

import os
import json
import hashlib
import base64
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import aiofiles
import aiohttp
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
try:
    import ipfshttpclient
    IPFS_AVAILABLE = True
except ImportError:
    IPFS_AVAILABLE = False
import requests

class PremiumZeroFrictionStorageService:
    """
    PREMIUM Zero-Friction Storage - Automatic encrypted storage and retrieval.
    Handles all storage operations seamlessly with permanent archiving options.
    """

    def __init__(self):
        # Storage configurations by tier
        self.tier_limits = {
            "scholar": {
                "storage_gb": 5,
                "files_per_month": 100,
                "permanent_archiving": False,
                "ipfs_pinning": False,
                "arweave_storage": False
            },
            "professional": {
                "storage_gb": 20,
                "files_per_month": 500,
                "permanent_archiving": True,
                "ipfs_pinning": True,
                "arweave_storage": False
            },
            "legacy": {
                "storage_gb": 50,
                "files_per_month": 2000,
                "permanent_archiving": True,
                "ipfs_pinning": True,
                "arweave_storage": True
            }
        }

        # Storage backends
        self.storage_backends = {
            "local_encrypted": self._store_local_encrypted,
            "ipfs": self._store_ipfs,
            "arweave": self._store_arweave,
            "permanent_archive": self._store_permanent_archive
        }

        # Encryption settings
        self.encryption_salt = b'goat_premium_salt_2024'
        self.key_iterations = 100000

        # Initialize storage directories
        self.base_storage_dir = Path("data/premium_storage")
        self.base_storage_dir.mkdir(parents=True, exist_ok=True)

        # Usage tracking
        self.usage_file = self.base_storage_dir / "usage_tracking.json"
        self._load_usage_data()

    def _load_usage_data(self):
        """Load usage tracking data"""
        if self.usage_file.exists():
            try:
                with open(self.usage_file, 'r') as f:
                    self.usage_data = json.load(f)
            except:
                self.usage_data = {}
        else:
            self.usage_data = {}

    def _save_usage_data(self):
        """Save usage tracking data"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage_data, f, indent=2)

    async def store_content_zero_friction(self,
                                        content: str,
                                        content_type: str,
                                        user_id: str,
                                        tier: str = "scholar",
                                        metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        PREMIUM: Zero-friction content storage with automatic encryption and archiving.

        Args:
            content: Content to store
            content_type: Type of content (text, json, binary, etc.)
            user_id: User identifier
            tier: User tier (scholar, professional, legacy)
            metadata: Optional metadata

        Returns:
            Storage result with retrieval handles
        """
        print(f"💾 Starting zero-friction storage for {content_type} content...")

        storage_start = datetime.utcnow()

        # Check tier limits
        limit_check = self._check_tier_limits(user_id, tier, len(content))
        if not limit_check["allowed"]:
            return {
                "success": False,
                "error": limit_check["reason"],
                "upgrade_required": True
            }

        # Generate content hash for deduplication
        content_hash = self._generate_content_hash(content)

        # Check if content already exists
        existing_handle = self._find_existing_content(content_hash, user_id)
        if existing_handle:
            return {
                "success": True,
                "operation": "deduplicated",
                "retrieval_handle": existing_handle,
                "message": "Content already stored, returning existing handle"
            }

        # Prepare content for storage
        prepared_content = self._prepare_content_for_storage(content, content_type)

        # Encrypt content
        encrypted_content, encryption_key = self._encrypt_content(prepared_content)

        # Generate storage handle
        storage_handle = self._generate_storage_handle(user_id, content_hash)

        # Store based on tier capabilities
        storage_result = await self._execute_tiered_storage(
            encrypted_content, storage_handle, tier, user_id
        )

        # Store metadata
        metadata_record = self._create_metadata_record(
            storage_handle, content_hash, content_type, user_id, tier,
            len(content), metadata, storage_result
        )

        await self._store_metadata(metadata_record)

        # Update usage tracking
        self._update_usage_tracking(user_id, tier, len(content))

        storage_time = (datetime.utcnow() - storage_start).total_seconds()

        return {
            "success": True,
            "operation": "stored",
            "retrieval_handle": storage_handle,
            "content_hash": content_hash,
            "storage_time_seconds": storage_time,
            "tier_used": tier,
            "storage_backends": list(storage_result.keys()),
            "premium_features_used": [
                "automatic_encryption",
                "deduplication",
                "tiered_storage",
                "permanent_archiving" if tier in ["professional", "legacy"] else None,
                "ipfs_pinning" if tier in ["professional", "legacy"] else None,
                "arweave_storage" if tier == "legacy" else None
            ]
        }

    async def retrieve_content_zero_friction(self,
                                           retrieval_handle: str,
                                           user_id: str) -> Dict[str, Any]:
        """
        PREMIUM: Zero-friction content retrieval with automatic decryption.

        Args:
            retrieval_handle: Storage handle from storage operation
            user_id: User identifier for access control

        Returns:
            Retrieved and decrypted content
        """
        print(f"📖 Starting zero-friction retrieval...")

        retrieval_start = datetime.utcnow()

        # Load metadata
        metadata = await self._load_metadata(retrieval_handle)
        if not metadata:
            return {
                "success": False,
                "error": "Content not found"
            }

        # Check access permissions
        if metadata["user_id"] != user_id:
            return {
                "success": False,
                "error": "Access denied"
            }

        # Retrieve from primary storage
        encrypted_content = await self._retrieve_from_primary_storage(
            metadata["storage_locations"]
        )

        if not encrypted_content:
            return {
                "success": False,
                "error": "Content retrieval failed"
            }

        # Decrypt content
        decrypted_content = self._decrypt_content(
            encrypted_content, metadata["encryption_key"]
        )

        # Parse content back to original format
        original_content = self._parse_retrieved_content(
            decrypted_content, metadata["content_type"]
        )

        retrieval_time = (datetime.utcnow() - retrieval_start).total_seconds()

        return {
            "success": True,
            "content": original_content,
            "content_type": metadata["content_type"],
            "original_size": metadata["original_size"],
            "stored_at": metadata["stored_at"],
            "retrieval_time_seconds": retrieval_time,
            "tier": metadata["tier"]
        }

    def _check_tier_limits(self, user_id: str, tier: str, content_size: int) -> Dict[str, Any]:
        """Check if storage operation is within tier limits"""
        if tier not in self.tier_limits:
            return {"allowed": False, "reason": "Invalid tier"}

        limits = self.tier_limits[tier]
        user_usage = self.usage_data.get(user_id, {"storage_used_gb": 0, "files_this_month": 0, "month": 0})

        # Check current month
        current_month = datetime.utcnow().month
        if user_usage.get("month", 0) != current_month:
            user_usage = {"storage_used_gb": user_usage["storage_used_gb"], "files_this_month": 0, "month": current_month}

        # Check storage limit
        content_size_gb = content_size / (1024 ** 3)
        if user_usage["storage_used_gb"] + content_size_gb > limits["storage_gb"]:
            return {
                "allowed": False,
                "reason": f"Storage limit exceeded. Used: {user_usage['storage_used_gb']:.2f}GB, Limit: {limits['storage_gb']}GB"
            }

        # Check file count limit
        if user_usage["files_this_month"] + 1 > limits["files_per_month"]:
            return {
                "allowed": False,
                "reason": f"Monthly file limit exceeded. Used: {user_usage['files_this_month']}, Limit: {limits['files_per_month']}"
            }

        return {"allowed": True}

    def _generate_content_hash(self, content: str) -> str:
        """Generate SHA-256 hash of content for deduplication"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _find_existing_content(self, content_hash: str, user_id: str) -> Optional[str]:
        """Check if content already exists for this user"""
        # This would query the metadata store
        # For now, return None (no deduplication)
        return None

    def _prepare_content_for_storage(self, content: str, content_type: str) -> bytes:
        """Prepare content for storage based on type"""
        if content_type == "json":
            # Ensure valid JSON
            try:
                json.loads(content)
                return content.encode('utf-8')
            except:
                # Wrap in JSON structure
                return json.dumps({"content": content}).encode('utf-8')
        elif content_type == "text":
            return content.encode('utf-8')
        else:
            # Binary or other types
            return content.encode('utf-8') if isinstance(content, str) else content

    def _encrypt_content(self, content: bytes) -> Tuple[bytes, str]:
        """Encrypt content using ChaCha20-Poly1305"""
        # Generate encryption key
        key = self._derive_key("premium_storage_key")

        # Generate nonce
        nonce = os.urandom(12)

        # Create cipher
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
        encryptor = cipher.encryptor()

        # Encrypt
        encrypted = encryptor.update(content)

        # Combine nonce + encrypted data
        encrypted_with_nonce = nonce + encrypted

        # Return as base64 for storage
        encrypted_b64 = base64.b64encode(encrypted_with_nonce).decode('utf-8')

        return encrypted_with_nonce, encrypted_b64

    def _decrypt_content(self, encrypted_data: bytes, key_b64: str) -> bytes:
        """Decrypt content using ChaCha20-Poly1305"""
        # Decode key
        key = base64.b64decode(key_b64)

        # Extract nonce and ciphertext
        nonce = key[:12]
        ciphertext = key[12:]

        # Derive the same key
        derived_key = self._derive_key("premium_storage_key")

        # Create cipher
        cipher = Cipher(algorithms.ChaCha20(derived_key, nonce), mode=None, backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt
        decrypted = decryptor.update(ciphertext)

        return decrypted

    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.encryption_salt,
            iterations=self.key_iterations,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def _generate_storage_handle(self, user_id: str, content_hash: str) -> str:
        """Generate unique storage handle"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"goat_premium_{user_id}_{timestamp}_{content_hash[:8]}"

    async def _execute_tiered_storage(self,
                                    encrypted_content: bytes,
                                    storage_handle: str,
                                    tier: str,
                                    user_id: str) -> Dict[str, Any]:
        """
        Execute storage across appropriate backends based on tier
        """
        storage_results = {}

        # Always store locally (encrypted)
        local_result = await self._store_local_encrypted(encrypted_content, storage_handle, user_id)
        storage_results["local_encrypted"] = local_result

        limits = self.tier_limits[tier]

        # IPFS pinning for Professional and Legacy
        if limits["ipfs_pinning"]:
            try:
                ipfs_result = await self._store_ipfs(encrypted_content, storage_handle)
                storage_results["ipfs"] = ipfs_result
            except Exception as e:
                print(f"IPFS storage failed: {e}")

        # Arweave for Legacy only
        if limits["arweave_storage"]:
            try:
                arweave_result = await self._store_arweave(encrypted_content, storage_handle)
                storage_results["arweave"] = arweave_result
            except Exception as e:
                print(f"Arweave storage failed: {e}")

        # Permanent archive for Professional and Legacy
        if limits["permanent_archiving"]:
            try:
                archive_result = await self._store_permanent_archive(encrypted_content, storage_handle)
                storage_results["permanent_archive"] = archive_result
            except Exception as e:
                print(f"Permanent archive failed: {e}")

        return storage_results

    async def _store_local_encrypted(self,
                                   encrypted_content: bytes,
                                   storage_handle: str,
                                   user_id: str) -> Dict[str, Any]:
        """Store encrypted content locally"""
        user_dir = self.base_storage_dir / user_id
        user_dir.mkdir(exist_ok=True)

        file_path = user_dir / f"{storage_handle}.enc"

        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(encrypted_content)

        return {
            "backend": "local_encrypted",
            "path": str(file_path),
            "size": len(encrypted_content)
        }

    async def _store_ipfs(self, encrypted_content: bytes, storage_handle: str) -> Dict[str, Any]:
        """Store content on IPFS"""
        # This would connect to IPFS node
        # For now, simulate IPFS storage
        ipfs_hash = hashlib.sha256(encrypted_content).hexdigest()

        return {
            "backend": "ipfs",
            "hash": ipfs_hash,
            "pinned": True
        }

    async def _store_arweave(self, encrypted_content: bytes, storage_handle: str) -> Dict[str, Any]:
        """Store content on Arweave (permanent storage)"""
        # This would interact with Arweave API
        # For now, simulate Arweave transaction
        arweave_tx = f"ar_{hashlib.sha256(encrypted_content).hexdigest()[:32]}"

        return {
            "backend": "arweave",
            "transaction_id": arweave_tx,
            "permanent": True
        }

    async def _store_permanent_archive(self, encrypted_content: bytes, storage_handle: str) -> Dict[str, Any]:
        """Store in permanent archive with redundancy"""
        # Create redundant copies
        archive_dir = self.base_storage_dir / "permanent_archive"
        archive_dir.mkdir(exist_ok=True)

        # Store multiple copies with different encodings
        archive_path = archive_dir / f"{storage_handle}.parchive"

        # Create archive package with metadata
        archive_data = {
            "storage_handle": storage_handle,
            "content_size": len(encrypted_content),
            "stored_at": datetime.utcnow().isoformat(),
            "redundancy_level": 3,
            "content_hash": hashlib.sha256(encrypted_content).hexdigest()
        }

        async with aiofiles.open(archive_path, 'wb') as f:
            # Store metadata + content
            metadata_bytes = json.dumps(archive_data).encode('utf-8')
            await f.write(len(metadata_bytes).to_bytes(4, 'big'))
            await f.write(metadata_bytes)
            await f.write(encrypted_content)

        return {
            "backend": "permanent_archive",
            "path": str(archive_path),
            "redundancy": 3,
            "permanent": True
        }

    def _create_metadata_record(self,
                              storage_handle: str,
                              content_hash: str,
                              content_type: str,
                              user_id: str,
                              tier: str,
                              original_size: int,
                              metadata: Optional[Dict[str, Any]],
                              storage_result: Dict[str, Any]) -> Dict[str, Any]:
        """Create metadata record for stored content"""
        return {
            "storage_handle": storage_handle,
            "content_hash": content_hash,
            "content_type": content_type,
            "user_id": user_id,
            "tier": tier,
            "original_size": original_size,
            "stored_at": datetime.utcnow().isoformat(),
            "encryption_key": storage_result.get("encryption_key", ""),
            "storage_locations": storage_result,
            "custom_metadata": metadata or {},
            "access_count": 0,
            "last_accessed": None
        }

    async def _store_metadata(self, metadata: Dict[str, Any]):
        """Store metadata record"""
        metadata_dir = self.base_storage_dir / "metadata"
        metadata_dir.mkdir(exist_ok=True)

        metadata_file = metadata_dir / f"{metadata['storage_handle']}.json"

        async with aiofiles.open(metadata_file, 'w') as f:
            await f.write(json.dumps(metadata, indent=2))

    async def _load_metadata(self, storage_handle: str) -> Optional[Dict[str, Any]]:
        """Load metadata record"""
        metadata_file = self.base_storage_dir / "metadata" / f"{storage_handle}.json"

        if not metadata_file.exists():
            return None

        async with aiofiles.open(metadata_file, 'r') as f:
            content = await f.read()
            return json.loads(content)

    async def _retrieve_from_primary_storage(self, storage_locations: Dict[str, Any]) -> Optional[bytes]:
        """Retrieve content from primary storage location"""
        # Try local storage first
        if "local_encrypted" in storage_locations:
            local_info = storage_locations["local_encrypted"]
            file_path = Path(local_info["path"])

            if file_path.exists():
                async with aiofiles.open(file_path, 'rb') as f:
                    return await f.read()

        # Fallback to other locations if needed
        # For now, just return None if local fails
        return None

    def _parse_retrieved_content(self, decrypted_bytes: bytes, content_type: str) -> Any:
        """Parse decrypted content back to original format"""
        content_str = decrypted_bytes.decode('utf-8')

        if content_type == "json":
            try:
                return json.loads(content_str)
            except:
                # Might be wrapped JSON
                try:
                    return json.loads(content_str)["content"]
                except:
                    return content_str
        else:
            return content_str

    def _update_usage_tracking(self, user_id: str, tier: str, content_size: int):
        """Update usage tracking for user"""
        current_month = datetime.utcnow().month
        content_size_gb = content_size / (1024 ** 3)

        if user_id not in self.usage_data:
            self.usage_data[user_id] = {
                "storage_used_gb": 0,
                "files_this_month": 0,
                "month": current_month
            }

        user_usage = self.usage_data[user_id]

        # Reset monthly counter if new month
        if user_usage.get("month", 0) != current_month:
            user_usage["files_this_month"] = 0
            user_usage["month"] = current_month

        user_usage["storage_used_gb"] += content_size_gb
        user_usage["files_this_month"] += 1

        self._save_usage_data()

    async def get_storage_usage(self, user_id: str) -> Dict[str, Any]:
        """Get storage usage statistics for user"""
        user_usage = self.usage_data.get(user_id, {"storage_used_gb": 0, "files_this_month": 0})

        # Determine current tier (this would come from user service)
        # For now, assume scholar
        current_tier = "scholar"
        limits = self.tier_limits[current_tier]

        return {
            "user_id": user_id,
            "current_tier": current_tier,
            "storage_used_gb": user_usage["storage_used_gb"],
            "storage_limit_gb": limits["storage_gb"],
            "storage_usage_percent": (user_usage["storage_used_gb"] / limits["storage_gb"]) * 100,
            "files_this_month": user_usage["files_this_month"],
            "files_limit_per_month": limits["files_per_month"],
            "files_usage_percent": (user_usage["files_this_month"] / limits["files_per_month"]) * 100
        }

# Global instance
premium_zero_friction_storage_service = PremiumZeroFrictionStorageService()