from typing import Dict, Any, Optional, List
import asyncio
from dandy_skg_core import DandySKG

# Dummy IModulePlugin for SM-P1 compliance
class IModulePlugin:
    def initialize(self, config: Dict[str, Any]) -> bool: ...
    async def handle(self, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]: ...
    def get_status(self) -> Dict[str, Any]: ...
    def shutdown(self) -> bool: ...
    @property
    def module_id(self) -> str: ...
    @property
    def capabilities(self) -> List[str]: ...

class DandySKGModule(IModulePlugin):
    """SM-P1 adapter for Dandy SKG"""
    def __init__(self):
        self.skg: Optional[DandySKG] = None
        self.config: Dict[str, Any] = {}
    def initialize(self, config: Dict[str, Any]) -> bool:
        self.config = config
        vault_path = config.get("dandy_vault_path", "./dandy_vault")
        self.skg = DandySKG(vault_path)
        if "podcast_manifest" in config:
            asyncio.create_task(self._ingest_async(config["podcast_manifest"]))
        return True
    async def _ingest_async(self, manifest: Dict[str, Any]):
        print(f"🎙️ Ingesting Dandy podcast history...")
        stats = await self.skg.ingest_podcast_history(manifest)
        print(f"✅ Dandy personas crystallized: Phil({len(self.skg.phil.trait_vector)} traits), Jim({len(self.skg.jim.trait_vector)} traits)")
    async def handle(self, payload: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        action = payload.get("action")
        if action == "submit_build":
            review_id = await self.skg.submit_build_for_review(payload["build_data"])
            return {"status": "submitted", "review_id": review_id}
        if action == "generate_review":
            build_id = payload["build_id"]
            platforms = payload.get("platforms", ["youtube"])
            if build_id not in self.skg.build_reviews:
                return {"status": "error", "message": "Build not found"}
            build = self.skg.build_reviews[build_id]
            content = await self.skg.generate_social_content(build, platforms)
            return {
                "status": "success",
                "content": content,
                "speakers": {
                    "phil": self.skg.phil.name,
                    "jim": self.skg.jim.name
                }
            }
        if action == "get_personas":
            return {
                "status": "success",
                "phil": {
                    "name": self.skg.phil.name,
                    "traits": self.skg.phil.trait_vector,
                    "expertise": self.skg.phil.expertise_areas
                },
                "jim": {
                    "name": self.skg.jim.name,
                    "traits": self.skg.jim.trait_vector,
                    "expertise": self.skg.jim.expertise_areas
                }
            }
        return {"status": "error", "message": f"Unknown action: {action}"}
    def get_status(self) -> Dict[str, Any]:
        if not self.skg:
            return {"status": "uninitialized"}
        return {
            "status": "healthy",
            "build_reviews": len(self.skg.build_reviews),
            "podcast_history": len(self.skg.podcast_history),
            "personas_active": True
        }
    def shutdown(self) -> bool:
        return True
    @property
    def module_id(self) -> str:
        return "dandy_skg"
    @property
    def capabilities(self) -> List[str]:
        return ["build_review", "podcast_generation", "social_content", "dual_persona"]
