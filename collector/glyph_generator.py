"""
Glyph Generator - Creates cryptographically signed glyphs for NFT data
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3


class GlyphGenerator:
    """Generate unique, signed glyphs for NFT data"""
    
    def __init__(self, private_key: Optional[str] = None):
        """
        Initialize glyph generator
        
        Args:
            private_key: Optional private key for EIP-191 signing
        """
        self.account = Account.from_key(private_key) if private_key else None
    
    @staticmethod
    def hash_data(data: Dict[str, Any]) -> str:
        """
        Create SHA-256 hash of data
        
        Args:
            data: Data to hash
        
        Returns:
            Hex string of hash
        """
        data_json = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_json.encode()).hexdigest()
    
    @staticmethod
    def generate_glyph_id(data_hash: str, source: str) -> str:
        """
        Generate unique glyph ID using keccak256
        
        Args:
            data_hash: SHA-256 hash of data
            source: Data source identifier
        
        Returns:
            0x-prefixed glyph ID
        """
        combined = f"{data_hash}:{source}".encode()
        return Web3.keccak(text=combined.decode()).hex()
    
    def sign_glyph(self, data_hash: str) -> tuple[str, str]:
        """
        Sign data hash with EIP-191
        
        Args:
            data_hash: Hash to sign
        
        Returns:
            Tuple of (signature, signer_address)
        """
        if self.account:
            message = encode_defunct(text=data_hash)
            signed = self.account.sign_message(message)
            return signed.signature.hex(), self.account.address
        else:
            # Fallback server signature
            signature = hashlib.sha256(f"goat_server:{data_hash}".encode()).hexdigest()
            return f"0x{signature}", "goat_server"
    
    def create_glyph(
        self,
        data: Dict[str, Any],
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a complete glyph from NFT data
        
        Args:
            data: NFT data to create glyph for
            source: Source identifier (e.g., "ipfs://Qm...", "opensea", "contract:0x...")
            metadata: Optional additional metadata
        
        Returns:
            Complete glyph dictionary
        """
        # Hash the data
        data_hash = self.hash_data(data)
        
        # Generate unique ID
        glyph_id = self.generate_glyph_id(data_hash, source)
        
        # Sign it
        signature, signer = self.sign_glyph(data_hash)
        
        # Build glyph
        glyph = {
            "id": glyph_id,
            "data_hash": data_hash,
            "source": source,
            "timestamp": int(datetime.utcnow().timestamp()),
            "signer": signer,
            "signature": signature,
            "data": data,
            "verified": True,
            "metadata": metadata or {}
        }
        
        return glyph
    
    @staticmethod
    def verify_glyph(glyph: Dict[str, Any]) -> bool:
        """
        Verify glyph signature
        
        Args:
            glyph: Glyph to verify
        
        Returns:
            True if signature is valid
        """
        data_hash = glyph.get("data_hash")
        signature = glyph.get("signature")
        signer = glyph.get("signer")
        
        if not all([data_hash, signature, signer]):
            return False
        
        # Server signature check
        if signer == "goat_server":
            expected = hashlib.sha256(f"goat_server:{data_hash}".encode()).hexdigest()
            return signature == f"0x{expected}"
        
        # EIP-191 signature check
        try:
            message = encode_defunct(text=data_hash)
            recovered = Account.recover_message(message, signature=signature)
            return recovered.lower() == signer.lower()
        except Exception:
            return False


# Example usage
if __name__ == "__main__":
    # Create generator (no private key = server signing)
    generator = GlyphGenerator()
    
    # Create glyph from NFT data
    nft_data = {
        "title": "Solidity Storage Patterns",
        "description": "Learn about mappings, arrays, and structs",
        "skill_level": "intermediate",
        "image": "ipfs://QmImage..."
    }
    
    glyph = generator.create_glyph(
        data=nft_data,
        source="ipfs://QmExample123",
        metadata={"platform": "truemark"}
    )
    
    print(f"Created glyph: {glyph['id']}")
    print(f"Data hash: {glyph['data_hash']}")
    print(f"Signature valid: {generator.verify_glyph(glyph)}")
