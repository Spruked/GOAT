"""
IPFS Gateway - Handles IPFS pinning and retrieval for vault storage
"""

import httpx
import json
from typing import Optional, Dict, Any, List
from pathlib import Path
import asyncio


class IPFSGateway:
    """Interface for IPFS operations"""
    
    def __init__(
        self,
        api_url: str = "http://127.0.0.1:5001",
        gateway_url: str = "https://ipfs.io",
        pinata_jwt: Optional[str] = None
    ):
        self.api_url = api_url.rstrip("/")
        self.gateway_url = gateway_url.rstrip("/")
        self.pinata_jwt = pinata_jwt
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def download(self, cid: str) -> Dict[str, Any]:
        """
        Download content from IPFS by CID
        
        Args:
            cid: IPFS Content Identifier (Qm... or baf...)
        
        Returns:
            Parsed JSON content or raw text
        """
        # Try local node first
        try:
            response = await self.client.post(
                f"{self.api_url}/api/v0/cat",
                params={"arg": cid}
            )
            response.raise_for_status()
            
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"raw": response.text}
        
        except (httpx.HTTPError, httpx.ConnectError):
            # Fallback to public gateway
            response = await self.client.get(f"{self.gateway_url}/ipfs/{cid}")
            response.raise_for_status()
            
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"raw": response.text}
    
    async def pin(self, cid: str) -> bool:
        """
        Pin content to local IPFS node
        
        Args:
            cid: Content to pin
        
        Returns:
            Success status
        """
        try:
            response = await self.client.post(
                f"{self.api_url}/api/v0/pin/add",
                params={"arg": cid}
            )
            response.raise_for_status()
            return True
        
        except (httpx.HTTPError, httpx.ConnectError):
            # Try Pinata if configured
            if self.pinata_jwt:
                return await self._pin_to_pinata(cid)
            return False
    
    async def _pin_to_pinata(self, cid: str) -> bool:
        """Pin via Pinata service"""
        try:
            response = await self.client.post(
                "https://api.pinata.cloud/pinning/pinByHash",
                json={"hashToPin": cid},
                headers={"Authorization": f"Bearer {self.pinata_jwt}"}
            )
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
    
    async def upload(self, data: Dict[str, Any], pin: bool = True) -> str:
        """
        Upload JSON data to IPFS
        
        Args:
            data: JSON serializable data
            pin: Whether to pin after upload
        
        Returns:
            CID of uploaded content
        """
        try:
            # Upload to local node
            json_str = json.dumps(data)
            
            response = await self.client.post(
                f"{self.api_url}/api/v0/add",
                files={"file": ("data.json", json_str.encode(), "application/json")}
            )
            response.raise_for_status()
            
            result = response.json()
            cid = result["Hash"]
            
            if pin:
                await self.pin(cid)
            
            return cid
        
        except (httpx.HTTPError, httpx.ConnectError):
            # Fallback to Pinata
            if self.pinata_jwt:
                return await self._upload_to_pinata(data)
            raise
    
    async def _upload_to_pinata(self, data: Dict[str, Any]) -> str:
        """Upload via Pinata service"""
        response = await self.client.post(
            "https://api.pinata.cloud/pinning/pinJSONToIPFS",
            json={"pinataContent": data},
            headers={"Authorization": f"Bearer {self.pinata_jwt}"}
        )
        response.raise_for_status()
        
        result = response.json()
        return result["IpfsHash"]
    
    async def unpin(self, cid: str) -> bool:
        """Remove pin from content"""
        try:
            response = await self.client.post(
                f"{self.api_url}/api/v0/pin/rm",
                params={"arg": cid}
            )
            response.raise_for_status()
            return True
        except (httpx.HTTPError, httpx.ConnectError):
            return False
    
    async def list_pins(self) -> List[str]:
        """List all pinned content"""
        try:
            response = await self.client.post(
                f"{self.api_url}/api/v0/pin/ls"
            )
            response.raise_for_status()
            
            result = response.json()
            return list(result.get("Keys", {}).keys())
        except (httpx.HTTPError, httpx.ConnectError):
            return []
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get IPFS node statistics"""
        try:
            response = await self.client.post(
                f"{self.api_url}/api/v0/stats/repo"
            )
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.ConnectError):
            return {"error": "Cannot connect to IPFS node"}
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Synchronous wrapper for convenience
class IPFSGatewaySync:
    """Synchronous wrapper for IPFSGateway"""
    
    def __init__(self, *args, **kwargs):
        self.gateway = IPFSGateway(*args, **kwargs)
    
    def download(self, cid: str) -> Dict[str, Any]:
        return asyncio.run(self.gateway.download(cid))
    
    def pin(self, cid: str) -> bool:
        return asyncio.run(self.gateway.pin(cid))
    
    def upload(self, data: Dict[str, Any], pin: bool = True) -> str:
        return asyncio.run(self.gateway.upload(data, pin))
    
    def unpin(self, cid: str) -> bool:
        return asyncio.run(self.gateway.unpin(cid))
    
    def list_pins(self) -> List[str]:
        return asyncio.run(self.gateway.list_pins())
    
    def get_stats(self) -> Dict[str, Any]:
        return asyncio.run(self.gateway.get_stats())


# Example usage
if __name__ == "__main__":
    async def main():
        # Initialize gateway
        ipfs = IPFSGateway(
            api_url="http://127.0.0.1:5001",
            gateway_url="https://ipfs.io"
        )
        
        # Upload data
        test_data = {
            "title": "GOAT NFT Knowledge",
            "content": "Learn Solidity storage patterns",
            "skill_level": "intermediate"
        }
        
        try:
            cid = await ipfs.upload(test_data, pin=True)
            print(f"Uploaded to IPFS: {cid}")
            
            # Download it back
            retrieved = await ipfs.download(cid)
            print(f"Retrieved: {retrieved}")
            
            # List pins
            pins = await ipfs.list_pins()
            print(f"Total pins: {len(pins)}")
            
            # Stats
            stats = await ipfs.get_stats()
            print(f"IPFS stats: {stats}")
        
        finally:
            await ipfs.close()
    
    # Run async main
    asyncio.run(main())
