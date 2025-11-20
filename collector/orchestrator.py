"""
NFT Orchestrator - Auto-discovery and ingestion pipeline
"""

import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from vault.core import Vault
from vault.ipfs_gateway import IPFSGateway
from collector.glyph_generator import GlyphGenerator


class NFTOrchestrator:
    """
    Orchestrates NFT data collection, enrichment, and glyph creation
    """
    
    def __init__(
        self,
        vault: Vault,
        ipfs_gateway: Optional[IPFSGateway] = None,
        glyph_generator: Optional[GlyphGenerator] = None
    ):
        """
        Initialize orchestrator
        
        Args:
            vault: Vault instance for storage
            ipfs_gateway: Optional IPFS gateway
            glyph_generator: Optional glyph generator (creates default if None)
        """
        self.vault = vault
        self.ipfs = ipfs_gateway or IPFSGateway()
        self.glyph_gen = glyph_generator or GlyphGenerator()
    
    async def ingest_ipfs(self, cid: str, auto_pin: bool = True) -> Dict[str, Any]:
        """
        Ingest NFT data from IPFS
        
        Args:
            cid: IPFS Content Identifier
            auto_pin: Whether to pin the content
        
        Returns:
            Created glyph
        """
        # Download from IPFS
        raw_data = await self.ipfs.download(cid)
        
        # Pin if requested
        if auto_pin:
            await self.ipfs.pin(cid)
        
        # Create glyph
        glyph = self.glyph_gen.create_glyph(
            data=raw_data,
            source=f"ipfs://{cid}",
            metadata={"pinned": auto_pin}
        )
        
        # Store in vault
        stored_glyph = self.vault.create_glyph(
            data=raw_data,
            source=f"ipfs://{cid}",
            signer=glyph["signer"]
        )
        
        return stored_glyph
    
    async def ingest_opensea(self, contract: str, token_id: str) -> Dict[str, Any]:
        """
        Ingest NFT metadata from OpenSea
        
        Args:
            contract: Contract address
            token_id: Token ID
        
        Returns:
            Created glyph
        """
        # Mock OpenSea API call (implement with actual API)
        opensea_data = {
            "name": f"NFT #{token_id}",
            "contract": contract,
            "token_id": token_id,
            "image_url": "https://...",
            "attributes": []
        }
        
        source = f"opensea://{contract}/{token_id}"
        
        # Create and store glyph
        glyph = self.vault.create_glyph(
            data=opensea_data,
            source=source
        )
        
        return glyph
    
    async def ingest_onchain(
        self,
        contract: str,
        token_id: str,
        rpc_url: str = "https://eth-mainnet.g.alchemy.com/v2/demo"
    ) -> Dict[str, Any]:
        """
        Ingest NFT data directly from blockchain
        
        Args:
            contract: Contract address
            token_id: Token ID
            rpc_url: RPC endpoint
        
        Returns:
            Created glyph
        """
        from web3 import Web3
        
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Standard ERC721 tokenURI call
        erc721_abi = [{
            "inputs": [{"type": "uint256", "name": "tokenId"}],
            "name": "tokenURI",
            "outputs": [{"type": "string"}],
            "stateMutability": "view",
            "type": "function"
        }]
        
        contract_instance = w3.eth.contract(
            address=Web3.to_checksum_address(contract),
            abi=erc721_abi
        )
        
        try:
            token_uri = contract_instance.functions.tokenURI(int(token_id)).call()
            
            # If it's IPFS, download it
            if token_uri.startswith("ipfs://"):
                cid = token_uri.replace("ipfs://", "")
                metadata = await self.ipfs.download(cid)
            else:
                # HTTP metadata
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.get(token_uri)
                    metadata = response.json()
            
            onchain_data = {
                "contract": contract,
                "token_id": token_id,
                "token_uri": token_uri,
                "metadata": metadata
            }
            
            source = f"onchain://{contract}/{token_id}"
            
            glyph = self.vault.create_glyph(
                data=onchain_data,
                source=source
            )
            
            return glyph
        
        except Exception as e:
            # Fallback data
            fallback_data = {
                "contract": contract,
                "token_id": token_id,
                "error": str(e)
            }
            
            return self.vault.create_glyph(
                data=fallback_data,
                source=f"onchain://{contract}/{token_id}"
            )
    
    async def ingest_manual(self, request) -> Any:
        """
        Process manually entered knowledge and generate glyphs
        
        Args:
            request: ManualKnowledgeRequest with name, category, description, content, tags, concepts, skill_level
        
        Returns:
            Created glyph with metadata
        """
        # Parse concepts from content if not provided
        extracted_concepts = []
        if not request.concepts:
            # Simple extraction: split content by double newlines, take first sentence as concept
            paragraphs = request.content.split('\n\n')
            for para in paragraphs[:5]:  # Limit to 5 concepts
                if para.strip():
                    first_sentence = para.split('.')[0].strip()
                    if first_sentence:
                        extracted_concepts.append({
                            "name": first_sentence[:50],  # First 50 chars as name
                            "definition": para.strip()[:200],  # First 200 chars as definition
                            "example": ""
                        })
        else:
            extracted_concepts = request.concepts
        
        # Generate glyph IDs for each concept
        concept_glyphs = []
        for concept in extracted_concepts:
            concept_glyph = self.vault.create_glyph(
                data={
                    "name": concept.get("name", ""),
                    "definition": concept.get("definition", ""),
                    "example": concept.get("example", ""),
                    "type": "concept"
                },
                source=f"manual://concept/{concept.get('name', 'unnamed')}"
            )
            concept_glyphs.append(concept_glyph.id)
        
        # Prepare IPFS metadata structure
        ipfs_metadata = {
            "name": request.name,
            "description": request.description,
            "category": request.category,
            "tags": [tag.strip() for tag in request.tags.split(',') if tag.strip()],
            "skill_level": request.skill_level,
            "content": request.content,
            "concepts": extracted_concepts,
            "glyph_list": concept_glyphs,
            "creator": "manual",
            "version": "2.1.0",
            "type": "knowledge_nft"
        }
        
        # Create main knowledge glyph
        main_glyph = self.vault.create_glyph(
            data=ipfs_metadata,
            source=f"manual://knowledge/{request.name}"
        )
        
        # Store glyph list in data field for return
        if not main_glyph.data:
            main_glyph.data = {}
        main_glyph.data["glyph_list"] = concept_glyphs
        main_glyph.data.update(ipfs_metadata)
        
        return main_glyph
    
    async def enrich_with_ai(self, glyph_id: str, llm_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Enrich glyph data with AI analysis
        
        Args:
            glyph_id: Glyph to enrich
            llm_prompt: Optional custom prompt
        
        Returns:
            Enriched glyph data
        """
        # Retrieve glyph
        glyph = self.vault.retrieve(glyph_id)
        
        if not glyph:
            raise ValueError(f"Glyph {glyph_id} not found")
        
        # Mock AI enrichment (implement with actual LLM)
        enriched = {
            "skill_level": "intermediate",
            "prerequisites": ["solidity_basics"],
            "learning_objectives": [
                "Understand storage patterns",
                "Optimize gas costs",
                "Implement efficient data structures"
            ],
            "difficulty_score": 7,
            "estimated_time_minutes": 45
        }
        
        # Update glyph metadata
        glyph.data["ai_enrichment"] = enriched
        
        # Re-store
        self.vault._store_encrypted(glyph)
        
        return glyph
    
    async def batch_ingest(self, sources: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Ingest multiple NFTs in batch
        
        Args:
            sources: List of source dicts with 'type' and required fields
                     Example: [{"type": "ipfs", "cid": "Qm..."}, ...]
        
        Returns:
            List of created glyphs
        """
        tasks = []
        
        for source in sources:
            source_type = source.get("type")
            
            if source_type == "ipfs":
                tasks.append(self.ingest_ipfs(source["cid"]))
            elif source_type == "opensea":
                tasks.append(self.ingest_opensea(source["contract"], source["token_id"]))
            elif source_type == "onchain":
                tasks.append(self.ingest_onchain(source["contract"], source["token_id"]))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        glyphs = [r for r in results if not isinstance(r, Exception)]
        
        return glyphs
    
    async def auto_discover(self, wallet_address: str, chain: str = "ethereum") -> List[Dict[str, Any]]:
        """
        Auto-discover NFTs owned by wallet
        
        Args:
            wallet_address: Wallet to scan
            chain: Blockchain to scan
        
        Returns:
            List of ingested glyphs
        """
        # Mock implementation (use Alchemy/Moralis NFT API)
        discovered = [
            {"type": "onchain", "contract": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", "token_id": "1"},
            {"type": "onchain", "contract": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", "token_id": "2"}
        ]
        
        return await self.batch_ingest(discovered)
    
    async def webhook_handler(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook from TrueMark or other platform
        
        Args:
            webhook_data: Webhook payload
        
        Returns:
            Processing result
        """
        event_type = webhook_data.get("event")
        
        if event_type == "nft.minted":
            # Extract NFT data
            contract = webhook_data.get("contract")
            token_id = webhook_data.get("token_id")
            
            # Auto-ingest
            glyph = await self.ingest_onchain(contract, token_id)
            
            return {
                "status": "success",
                "glyph_id": glyph.id,
                "message": f"Auto-ingested NFT {contract}/{token_id}"
            }
        
        return {"status": "unknown_event", "event": event_type}


# Example usage
async def main():
    from pathlib import Path
    
    # Initialize vault
    vault = Vault(
        storage_path=Path("./data/vault"),
        encryption_key="supersecretkey123"
    )
    
    # Create orchestrator
    orchestrator = NFTOrchestrator(vault=vault)
    
    # Ingest from IPFS
    # glyph = await orchestrator.ingest_ipfs("QmExample123")
    # print(f"Created glyph: {glyph.id}")
    
    # Batch ingest
    sources = [
        {"type": "ipfs", "cid": "QmTest1"},
        {"type": "ipfs", "cid": "QmTest2"}
    ]
    
    # glyphs = await orchestrator.batch_ingest(sources)
    # print(f"Ingested {len(glyphs)} NFTs")


if __name__ == "__main__":
    asyncio.run(main())
