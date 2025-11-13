"""
On-Chain Anchoring - Merkle tree anchoring for vault glyphs
"""

import os
from typing import List, Dict, Any, Optional
from merkletools import MerkleTools
from web3 import Web3
from eth_account import Account
import json


class OnChainAnchor:
    """Anchor glyph batches to blockchain using Merkle roots"""
    
    def __init__(
        self,
        rpc_url: Optional[str] = None,
        contract_address: Optional[str] = None,
        private_key: Optional[str] = None
    ):
        """
        Initialize on-chain anchor
        
        Args:
            rpc_url: RPC endpoint (defaults to env POLYGON_RPC)
            contract_address: Vault anchor contract (defaults to env ANCHOR_CONTRACT)
            private_key: Private key for transactions (defaults to env PRIVATE_KEY)
        """
        self.rpc_url = rpc_url or os.getenv("POLYGON_RPC", "https://polygon-rpc.com")
        self.contract_address = contract_address or os.getenv("ANCHOR_CONTRACT")
        self.private_key = private_key or os.getenv("PRIVATE_KEY")
        
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.account = Account.from_key(self.private_key) if self.private_key else None
        
        # GOATVaultAnchor ABI
        self.abi = [
            {
                "inputs": [{"name": "root", "type": "bytes32"}],
                "name": "anchor",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "root", "type": "bytes32"}],
                "name": "isAnchored",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "", "type": "bytes32"}],
                "name": "anchors",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "root", "type": "bytes32"},
                    {"indexed": False, "name": "timestamp", "type": "uint256"}
                ],
                "name": "Anchored",
                "type": "event"
            }
        ]
        
        if self.contract_address and self.w3.is_address(self.contract_address):
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=self.abi
            )
        else:
            self.contract = None
    
    def create_merkle_tree(self, glyph_ids: List[str]) -> MerkleTools:
        """
        Create Merkle tree from glyph IDs
        
        Args:
            glyph_ids: List of glyph IDs to include
        
        Returns:
            MerkleTools instance
        """
        mt = MerkleTools(hash_type='sha256')
        
        # Add each glyph ID as a leaf
        for glyph_id in glyph_ids:
            # Convert to bytes if hex string
            if glyph_id.startswith("0x"):
                leaf = bytes.fromhex(glyph_id[2:])
            else:
                leaf = glyph_id.encode()
            
            mt.add_leaf(leaf, do_hash=True)
        
        mt.make_tree()
        return mt
    
    def get_merkle_root(self, glyph_ids: List[str]) -> str:
        """
        Get Merkle root hash for glyph batch
        
        Args:
            glyph_ids: List of glyph IDs
        
        Returns:
            Hex string of root hash
        """
        mt = self.create_merkle_tree(glyph_ids)
        root = mt.get_merkle_root()
        return "0x" + root.hex() if root else "0x"
    
    def get_proof(self, glyph_ids: List[str], glyph_id: str) -> List[str]:
        """
        Get Merkle proof for specific glyph
        
        Args:
            glyph_ids: Complete list of glyphs in tree
            glyph_id: Glyph to prove
        
        Returns:
            List of proof hashes
        """
        mt = self.create_merkle_tree(glyph_ids)
        
        # Find index
        try:
            index = glyph_ids.index(glyph_id)
        except ValueError:
            return []
        
        proof = mt.get_proof(index)
        return ["0x" + p['right'].hex() if p.get('right') else "0x" + p['left'].hex() for p in proof]
    
    def anchor_batch(self, glyph_ids: List[str], gas_price: Optional[int] = None) -> Dict[str, Any]:
        """
        Anchor glyph batch on-chain
        
        Args:
            glyph_ids: List of glyph IDs to anchor
            gas_price: Optional gas price in gwei
        
        Returns:
            Transaction result
        """
        if not self.contract or not self.account:
            return {
                "error": "Contract or account not configured",
                "mock_root": self.get_merkle_root(glyph_ids)
            }
        
        # Get Merkle root
        root_hex = self.get_merkle_root(glyph_ids)
        root_bytes = bytes.fromhex(root_hex[2:])
        
        # Check if already anchored
        if self.contract.functions.isAnchored(root_bytes).call():
            return {
                "status": "already_anchored",
                "root": root_hex,
                "glyph_count": len(glyph_ids)
            }
        
        # Build transaction
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        
        tx_params = {
            'from': self.account.address,
            'nonce': nonce,
            'gas': 200000
        }
        
        if gas_price:
            tx_params['gasPrice'] = self.w3.to_wei(gas_price, 'gwei')
        else:
            tx_params['gasPrice'] = self.w3.eth.gas_price
        
        # Build and sign transaction
        tx = self.contract.functions.anchor(root_bytes).build_transaction(tx_params)
        signed_tx = self.account.sign_transaction(tx)
        
        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "status": "success" if receipt['status'] == 1 else "failed",
            "tx_hash": tx_hash.hex(),
            "root": root_hex,
            "glyph_count": len(glyph_ids),
            "block_number": receipt['blockNumber'],
            "gas_used": receipt['gasUsed']
        }
    
    def verify_proof(self, root: str, glyph_id: str, proof: List[str]) -> bool:
        """
        Verify Merkle proof for glyph
        
        Args:
            root: Merkle root hash
            glyph_id: Glyph ID to verify
            proof: Merkle proof hashes
        
        Returns:
            True if proof is valid
        """
        # Convert glyph to leaf hash
        if glyph_id.startswith("0x"):
            leaf = bytes.fromhex(glyph_id[2:])
        else:
            leaf = glyph_id.encode()
        
        import hashlib
        current = hashlib.sha256(leaf).digest()
        
        # Verify proof
        for proof_hash in proof:
            proof_bytes = bytes.fromhex(proof_hash[2:])
            
            # Concatenate and hash
            if current < proof_bytes:
                current = hashlib.sha256(current + proof_bytes).digest()
            else:
                current = hashlib.sha256(proof_bytes + current).digest()
        
        computed_root = "0x" + current.hex()
        return computed_root == root
    
    def is_anchored(self, root: str) -> Dict[str, Any]:
        """
        Check if root is anchored on-chain
        
        Args:
            root: Merkle root to check
        
        Returns:
            Anchor status and timestamp
        """
        if not self.contract:
            return {"error": "Contract not configured", "anchored": False}
        
        root_bytes = bytes.fromhex(root[2:])
        
        is_anchored = self.contract.functions.isAnchored(root_bytes).call()
        timestamp = self.contract.functions.anchors(root_bytes).call() if is_anchored else 0
        
        return {
            "anchored": is_anchored,
            "timestamp": timestamp,
            "root": root,
            "date": None if timestamp == 0 else str(timestamp)
        }


# Example usage
if __name__ == "__main__":
    # Initialize (will use env vars)
    anchor = OnChainAnchor()
    
    # Create test glyphs
    test_glyphs = [
        "0xabc123def456",
        "0x111222333444",
        "0x555666777888"
    ]
    
    # Get Merkle root
    root = anchor.get_merkle_root(test_glyphs)
    print(f"Merkle root: {root}")
    
    # Get proof for first glyph
    proof = anchor.get_proof(test_glyphs, test_glyphs[0])
    print(f"Proof for {test_glyphs[0]}: {proof}")
    
    # Verify proof
    valid = anchor.verify_proof(root, test_glyphs[0], proof)
    print(f"Proof valid: {valid}")
    
    # Anchor on-chain (if configured)
    # result = anchor.anchor_batch(test_glyphs)
    # print(f"Anchor result: {result}")
