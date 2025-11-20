# vault_bridge.py
"""
GOAT Vault Bridge - Connects Teacher Engine to Vault Forge
"""

from pathlib import Path
from typing import Dict, Any
import shutil
import os

class VaultBridge:
    """Bridge between Teacher Engine and Vault Forge system"""

    def __init__(self, vault_forge_path: str = "./vault_forge"):
        self.vault_forge = __import__(vault_forge_path.replace("/", ".").replace("\\", "."), fromlist=["create_vault"])

    def prepare_teaching_vault(self, skill_id: str, package_path: Path) -> Dict[str, Any]:
        """Prepare teaching package for vault creation"""

        # Create deliverables directory for this skill
        deliverables_dir = Path("./deliverables") / skill_id
        deliverables_dir.mkdir(parents=True, exist_ok=True)

        # Copy teaching package files
        if package_path.exists():
            shutil.copytree(package_path, deliverables_dir / "teaching", dirs_exist_ok=True)

        # Create vault metadata
        vault_config = {
            "project_name": f"GOAT Teaching: {skill_id}",
            "tier": "basic",  # Could be dynamic based on package complexity
            "deliverables_path": str(deliverables_dir),
            "auto_upload": False  # Manual for now
        }

        return vault_config

    def create_teaching_vault(self, skill_id: str, package_path: Path) -> str:
        """Create vault package for teaching content"""
        vault_config = self.prepare_teaching_vault(skill_id, package_path)

        # Call vault forge
        zip_path = self.vault_forge.create_vault(
            vault_config["project_name"],
            vault_config["tier"],
            vault_config["deliverables_path"],
            {"auto_upload": vault_config["auto_upload"]}
        )

        return zip_path

    def export_to_vault_forge(self, skill_id: str, teaching_package: Dict[str, Any]) -> Dict[str, Any]:
        """Export complete teaching package to vault forge format"""

        # Create export structure
        export_data = {
            "skill_id": skill_id,
            "vault_ready": True,
            "package_type": "teaching_nft",
            "contents": {
                "lesson_plan": teaching_package.get("lesson_plan", []),
                "explanation": teaching_package.get("explanation", {}),
                "quiz": teaching_package.get("quiz", {}),
                "nft_metadata": teaching_package.get("nft_metadata", {})
            },
            "metadata": {
                "generated_by": "GOAT Teacher Engine",
                "version": "1.0",
                "cert_sig_ready": True,
                "truemark_ready": False  # Could be true for premium
            }
        }

        return export_data