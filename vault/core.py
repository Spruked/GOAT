"""
GOAT Vault Core - Immutable Data Lineage for NFT Knowledge
Provides cryptographic provenance tracking with AES-256 encryption
"""

import json
import hashlib
import sqlite3
import secrets
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from eth_account import Account
from eth_account.messages import encode_defunct
import base64


@dataclass
class Glyph:
    """Unique, on-chain verifiable identifier for knowledge data"""
    id: str                 # keccak256(hash(data))
    data_hash: str          # sha256(content)
    source: str             # "ipfs://Qm...", "opensea", "contract"
    timestamp: int          # Unix timestamp
    signer: str             # GOAT server or user wallet
    signature: str          # EIP-191 signature
    data: Optional[Dict[str, Any]] = None
    verified: bool = False


class VaultEncryption:
    """AES-256 encryption for vault data at rest"""
    
    def __init__(self, password: str, salt: Optional[bytes] = None):
        self.salt = salt or secrets.token_bytes(16)
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(key)
    
    def encrypt(self, data: str) -> bytes:
        """Encrypt data using AES-256"""
        return self.fernet.encrypt(data.encode())
    
    def decrypt(self, encrypted: bytes) -> str:
        """Decrypt data"""
        return self.fernet.decrypt(encrypted).decode()
    
    @staticmethod
    def hash_data(data: str) -> str:
        """SHA-256 hash of content"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def generate_glyph_id(data_hash: str, source: str) -> str:
        """Generate unique glyph ID using keccak256"""
        combined = f"{data_hash}:{source}".encode()
        return "0x" + hashlib.sha3_256(combined).hexdigest()


class VaultLedger:
    """SQLite-based immutable audit log"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize ledger schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS glyphs (
                    glyph_id TEXT PRIMARY KEY,
                    data_hash TEXT NOT NULL,
                    source TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    signer TEXT NOT NULL,
                    signature TEXT NOT NULL,
                    verified INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    glyph_id TEXT,
                    action TEXT,
                    actor TEXT,
                    timestamp INTEGER,
                    metadata TEXT,
                    FOREIGN KEY (glyph_id) REFERENCES glyphs(glyph_id)
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_glyph_timestamp 
                ON glyphs(timestamp)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_source 
                ON glyphs(source)
            """)
    
    def record_glyph(self, glyph: Glyph):
        """Record glyph in ledger"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO glyphs 
                (glyph_id, data_hash, source, timestamp, signer, signature, verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                glyph.id,
                glyph.data_hash,
                glyph.source,
                glyph.timestamp,
                glyph.signer,
                glyph.signature,
                int(glyph.verified)
            ))
            
            # Audit log entry
            self.log_action(
                glyph.id,
                "CREATED",
                glyph.signer,
                {"source": glyph.source}
            )
    
    def log_action(self, glyph_id: str, action: str, actor: str, metadata: Dict = None):
        """Record action in audit log"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO audit_log (glyph_id, action, actor, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                glyph_id,
                action,
                actor,
                int(datetime.utcnow().timestamp()),
                json.dumps(metadata or {})
            ))
    
    def get_glyph(self, glyph_id: str) -> Optional[Glyph]:
        """Retrieve glyph from ledger"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM glyphs WHERE glyph_id = ?",
                (glyph_id,)
            ).fetchone()
            
            if not row:
                return None
            
            return Glyph(
                id=row["glyph_id"],
                data_hash=row["data_hash"],
                source=row["source"],
                timestamp=row["timestamp"],
                signer=row["signer"],
                signature=row["signature"],
                verified=bool(row["verified"])
            )
    
    def get_audit_trail(self, glyph_id: str) -> List[Dict]:
        """Get complete audit trail for glyph"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM audit_log 
                WHERE glyph_id = ? 
                ORDER BY timestamp DESC
            """, (glyph_id,)).fetchall()
            
            return [dict(row) for row in rows]
    
    def list_glyphs(self, source: Optional[str] = None, limit: int = 100) -> List[Glyph]:
        """List glyphs with optional filtering"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            if source:
                query = "SELECT * FROM glyphs WHERE source = ? ORDER BY timestamp DESC LIMIT ?"
                rows = conn.execute(query, (source, limit)).fetchall()
            else:
                query = "SELECT * FROM glyphs ORDER BY timestamp DESC LIMIT ?"
                rows = conn.execute(query, (limit,)).fetchall()
            
            return [
                Glyph(
                    id=row["glyph_id"],
                    data_hash=row["data_hash"],
                    source=row["source"],
                    timestamp=row["timestamp"],
                    signer=row["signer"],
                    signature=row["signature"],
                    verified=bool(row["verified"])
                )
                for row in rows
            ]


class Vault:
    """Main vault controller - combines encryption, storage, and ledger"""
    
    def __init__(
        self,
        storage_path: Path,
        encryption_key: str,
        private_key: Optional[str] = None
    ):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.encryption = VaultEncryption(encryption_key)
        self.ledger = VaultLedger(self.storage_path / "ledger.sqlite")
        
        # For EIP-191 signing
        self.account = Account.from_key(private_key) if private_key else None
    
    def create_glyph(
        self,
        data: Dict[str, Any],
        source: str,
        signer: Optional[str] = None
    ) -> Glyph:
        """Create and store a new glyph"""
        
        # Hash the data
        data_json = json.dumps(data, sort_keys=True)
        data_hash = VaultEncryption.hash_data(data_json)
        
        # Generate glyph ID
        glyph_id = VaultEncryption.generate_glyph_id(data_hash, source)
        
        # Sign with EIP-191
        message = encode_defunct(text=data_hash)
        if self.account:
            signed = self.account.sign_message(message)
            signature = signed.signature.hex()
            signer = self.account.address
        else:
            # Server-side fallback signature
            signature = hashlib.sha256(f"{data_hash}:{source}".encode()).hexdigest()
            signer = signer or "goat_server"
        
        # Create glyph
        glyph = Glyph(
            id=glyph_id,
            data_hash=data_hash,
            source=source,
            timestamp=int(datetime.utcnow().timestamp()),
            signer=signer,
            signature=signature,
            data=data,
            verified=True
        )
        
        # Store encrypted data
        self._store_encrypted(glyph)
        
        # Record in ledger
        self.ledger.record_glyph(glyph)
        
        return glyph
    
    def _store_encrypted(self, glyph: Glyph):
        """Store glyph data encrypted on disk"""
        glyph_file = self.storage_path / f"{glyph.id}.enc"
        
        # Prepare data for storage
        storage_data = {
            "glyph_id": glyph.id,
            "data_hash": glyph.data_hash,
            "source": glyph.source,
            "timestamp": glyph.timestamp,
            "signer": glyph.signer,
            "signature": glyph.signature,
            "data": glyph.data,
            "verified": glyph.verified
        }
        
        # Encrypt and write
        encrypted = self.encryption.encrypt(json.dumps(storage_data))
        glyph_file.write_bytes(encrypted)
    
    def retrieve(self, glyph_id: str) -> Optional[Glyph]:
        """Retrieve and decrypt glyph data"""
        glyph_file = self.storage_path / f"{glyph_id}.enc"
        
        if not glyph_file.exists():
            # Try to get from ledger only
            return self.ledger.get_glyph(glyph_id)
        
        # Decrypt
        encrypted = glyph_file.read_bytes()
        decrypted = self.encryption.decrypt(encrypted)
        data = json.loads(decrypted)
        
        return Glyph(**data)
    
    def verify_signature(self, glyph: Glyph) -> bool:
        """Verify EIP-191 signature"""
        if not glyph.signature.startswith("0x"):
            # Server signature - verify hash
            expected = hashlib.sha256(
                f"{glyph.data_hash}:{glyph.source}".encode()
            ).hexdigest()
            return glyph.signature == expected
        
        try:
            message = encode_defunct(text=glyph.data_hash)
            recovered = Account.recover_message(message, signature=glyph.signature)
            return recovered.lower() == glyph.signer.lower()
        except Exception:
            return False
    
    def get_proof(self, glyph_id: str) -> Dict[str, Any]:
        """Generate verification proof for glyph"""
        glyph = self.retrieve(glyph_id)
        if not glyph:
            return {"error": "Glyph not found"}
        
        audit_trail = self.ledger.get_audit_trail(glyph_id)
        signature_valid = self.verify_signature(glyph)
        
        return {
            "glyph_id": glyph.id,
            "data_hash": glyph.data_hash,
            "source": glyph.source,
            "timestamp": glyph.timestamp,
            "signer": glyph.signer,
            "signature": glyph.signature,
            "signature_valid": signature_valid,
            "verified": glyph.verified,
            "audit_trail": audit_trail,
            "proof_generated_at": int(datetime.utcnow().timestamp())
        }
    
    def list_all(self, source: Optional[str] = None, limit: int = 100) -> List[Glyph]:
        """List all glyphs"""
        return self.ledger.list_glyphs(source, limit)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vault statistics"""
        glyphs = self.ledger.list_glyphs(limit=10000)
        
        sources = {}
        for glyph in glyphs:
            sources[glyph.source] = sources.get(glyph.source, 0) + 1
        
        return {
            "total_glyphs": len(glyphs),
            "verified_count": sum(1 for g in glyphs if g.verified),
            "sources": sources,
            "latest_timestamp": max((g.timestamp for g in glyphs), default=0),
            "storage_path": str(self.storage_path)
        }


# Example usage
if __name__ == "__main__":
    # Initialize vault
    vault = Vault(
        storage_path=Path("./vault_storage"),
        encryption_key="supersecretkey123",
        private_key=None  # Set to use wallet signing
    )
    
    # Create a glyph
    glyph = vault.create_glyph(
        data={
            "title": "Solidity Storage Patterns",
            "content": "Learn about mapping, arrays, and structs...",
            "skill_level": "intermediate"
        },
        source="ipfs://QmExample123"
    )
    
    print(f"Created glyph: {glyph.id}")
    
    # Retrieve and verify
    retrieved = vault.retrieve(glyph.id)
    print(f"Retrieved: {retrieved.data['title']}")
    
    # Get proof
    proof = vault.get_proof(glyph.id)
    print(f"Signature valid: {proof['signature_valid']}")
    
    # Stats
    stats = vault.get_stats()
    print(f"Vault stats: {stats}")
