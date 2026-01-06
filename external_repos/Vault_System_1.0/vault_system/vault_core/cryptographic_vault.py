import hashlib
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import threading
from collections import defaultdict

class VaultCategory(Enum):
    FINANCIAL = "financial"
    PERSONAL = "personal" 
    INTELLECTUAL = "intellectual"
    OPERATIONAL = "operational"
    STRATEGIC = "strategic"
    SENSITIVE = "sensitive"
    ANALYTICAL = "analytical"

@dataclass
class VaultEntry:
    encrypted_data: str
    timestamp: float
    category: str
    source: str
    glyph_id: str
    metadata: Dict[str, Any]
    access_count: int = 0
    last_accessed: Optional[float] = None

class CryptographicVault:
    def __init__(self, master_key: str, salt: bytes = None):
        self.salt = salt or b"vault_system_salt_2024"
        self.master_key = self._derive_key(master_key)
        self.fernet = Fernet(self.master_key)
        self.vaults = defaultdict(dict)
        self.lock = threading.RLock()
        self.retention_policy = defaultdict(lambda: 30 * 24 * 3600)  # 30 days default
        
    def _derive_key(self, password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def set_retention_policy(self, category: VaultCategory, seconds: int):
        self.retention_policy[category] = seconds
    
    def encrypt_data(self, data: Any) -> str:
        """Encrypt data with metadata"""
        encrypted = self.fernet.encrypt(
            json.dumps({
                'data': data,
                'encryption_timestamp': time.time(),
                'version': '1.0'
            }).encode()
        )
        return encrypted.decode()
    
    def decrypt_data(self, encrypted_data: str) -> Any:
        """Decrypt data and validate"""
        decrypted = self.fernet.decrypt(encrypted_data.encode())
        data_obj = json.loads(decrypted)
        return data_obj['data']
    
    def store(self, vault_id: str, category: VaultCategory, data: Any, 
              source: str, metadata: Optional[Dict] = None) -> bool:
        with self.lock:
            try:
                encrypted_data = self.encrypt_data(data)
                timestamp = time.time()
                
                vault_entry = VaultEntry(
                    encrypted_data=encrypted_data,
                    timestamp=timestamp,
                    category=category.value,
                    source=source,
                    glyph_id=f"glyph_{int(timestamp)}_{hash(vault_id) % 10000:04d}",
                    metadata=metadata or {}
                )
                
                self.vaults[category][vault_id] = vault_entry
                return True
                
            except Exception as e:
                print(f"Storage error: {e}")
                return False
    
    def retrieve(self, vault_id: str, category: VaultCategory) -> Optional[Any]:
        with self.lock:
            try:
                if category not in self.vaults or vault_id not in self.vaults[category]:
                    return None
                
                entry = self.vaults[category][vault_id]
                entry.access_count += 1
                entry.last_accessed = time.time()
                
                return self.decrypt_data(entry.encrypted_data)
                
            except Exception as e:
                print(f"Retrieval error: {e}")
                return None
    
    def cleanup_expired(self):
        """Remove expired entries based on retention policy"""
        with self.lock:
            current_time = time.time()
            for category, vaults in self.vaults.items():
                retention = self.retention_policy[category]
                expired_keys = [
                    key for key, entry in vaults.items()
                    if current_time - entry.timestamp > retention
                ]
                for key in expired_keys:
                    del vaults[key]
    
    def get_vault_stats(self) -> Dict[str, Any]:
        with self.lock:
            stats = {}
            for category, vaults in self.vaults.items():
                stats[category.value] = {
                    'count': len(vaults),
                    'total_size': sum(len(entry.encrypted_data) for entry in vaults.values()),
                    'avg_access_count': sum(entry.access_count for entry in vaults.values()) / len(vaults) if vaults else 0
                }
            return stats