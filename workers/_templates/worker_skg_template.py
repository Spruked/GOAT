"""
GOAT Worker SKG Template - Reference Implementation
Implements mini-SKG integration, temp vault management, and UCM/CALI communication
Version: 1.1 (Surgically Improved)
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import uuid

class WorkerSKG:
    """
    Base class for all GOAT workers.
    Each forged worker inherits from this and implements job-specific logic.
    """

    def __init__(self, worker_id: str, job_name: str, ucm_connector):
        """
        Initialize worker with SKG capabilities

        Args:
            worker_id: Unique identifier for this worker instance
            job_name: Name of the job (e.g., 'onboarding')
            ucm_connector: Interface to UCM/CALI for transfers
        """
        self.worker_id = worker_id
        self.job_name = job_name
        self.ucm_connector = ucm_connector

        # Paths - location-agnostic for portability
        base_dir = Path(__file__).resolve().parents[2]  # GOAT/
        self.worker_dir = base_dir / "workers" / f"{job_name}_worker"
        self.mini_skg_dir = self.worker_dir / "mini_skg"
        self.temp_vault_dir = self.worker_dir / "temp_vault"
        self.unanswered_path = self.temp_vault_dir / "unanswered_queries.json"
        self.logic_path = self.worker_dir / "logic.json"
        self.script_path = self.worker_dir / f"{job_name}_script.json"

        # Initialize components
        self._initialize_directories()
        self.logic_config = self._load_logic_config()
        self.script_data = self._load_script()
        self.mini_skg = MiniSKG(self.mini_skg_dir)

    def _initialize_directories(self):
        """Create worker directory structure if missing"""
        self.mini_skg_dir.mkdir(parents=True, exist_ok=True)
        (self.worker_dir / "temp_vault").mkdir(exist_ok=True)

    def _load_logic_config(self) -> Dict[str, Any]:
        """Load logic.json configuration"""
        if self.logic_path.exists():
            with open(self.logic_path, 'r') as f:
                return json.load(f)
        return self._create_default_logic()

    def _create_default_logic(self) -> Dict[str, Any]:
        """Create default logic configuration"""
        default = {
            "worker_id": self.worker_id,
            "job_name": self.job_name,
            "version": "1.0",
            "learning_mode": "restricted",  # From memory #18
            "transfer_triggers": {
                "unanswered_threshold": 3,  # Transfer to UCM after 3 unanswered
                "time_interval_minutes": 60
            },
            "approved_improvements": [],
            "pending_reviews": []
        }
        self._save_logic_config(default)
        return default

    def _save_logic_config(self, config: Dict[str, Any]):
        """Save logic.json"""
        with open(self.logic_path, 'w') as f:
            json.dump(config, f, indent=2)

    def _load_script(self) -> Dict[str, Any]:
        """Load the job script JSON"""
        if self.script_path.exists():
            with open(self.script_path, 'r') as f:
                return json.load(f)
        return {"script": [], "metadata": {"version": "1.0", "last_updated": None}}

    def _save_script(self):
        """Save updated script"""
        with open(self.script_path, 'w') as f:
            json.dump(self.script_data, f, indent=2)

    def run(self, user_input: str, user_context: Dict[str, Any]) -> str:
        """
        Main execution method for worker tasks
        (Renamed from execute_job for lifecycle clarity)

        Args:
            user_input: Raw input from user
            user_context: Context about user (session, preferences, etc.)

        Returns:
            Response to user
        """
        # 1. Query mini-SKG for relevant script sections
        relevant_sections = self.mini_skg.query(user_input, self.script_data["script"])

        # 2. Attempt to generate response
        response = self._generate_response(user_input, relevant_sections, user_context)

        # 3. If response is inadequate, save to temp vault
        if not response or self._is_inadequate(response):
            self._save_to_temp_vault(user_input, user_context, response)
            return self._get_fallback_response()

        return response

    def _generate_response(self, user_input: str, sections: List[Dict], context: Dict) -> Optional[str]:
        """Generate response from script sections"""
        # Implementation specific to job type
        # Override in subclass
        raise NotImplementedError

    def _is_inadequate(self, response: str) -> bool:
        """Check if response is inadequate (e.g., 'I don't know')"""
        inadequacy_markers = [
            "i don't know", "i'm not sure", "cannot answer",
            "not specified", "no information", "unclear"
        ]
        return any(marker in response.lower() for marker in inadequacy_markers)

    def _save_to_temp_vault(self, user_input: str, context: Dict, attempted_response: Optional[str]):
        """Save unanswered query to temp vault for UCM review"""
        vault_entry = {
            "query_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "worker_id": self.worker_id,
            "job_name": self.job_name,
            "user_input": user_input,
            "user_context": context,
            "attempted_response": attempted_response,
            "script_version": self.script_data["metadata"]["version"]
        }

        # Load existing vault
        vault = []
        if self.unanswered_path.exists():
            with open(self.unanswered_path, 'r') as f:
                vault = json.load(f)

        # Add new entry
        vault.append(vault_entry)

        # Save vault
        with open(self.unanswered_path, 'w') as f:
            json.dump(vault, f, indent=2)

        # Check if transfer threshold reached
        if len(vault) >= self.logic_config["transfer_triggers"]["unanswered_threshold"]:
            self._transfer_to_ucm()

    def _transfer_to_ucm(self):
        """Transfer temp vault contents to UCM/CALI"""
        if not self.unanswered_path.exists():
            return

        with open(self.unanswered_path, 'r') as f:
            vault_data = json.load(f)

        # Send to UCM via connector
        transfer_payload = {
            "source": "worker",
            "worker_id": self.worker_id,
            "job_name": self.job_name,
            "data_type": "unanswered_queries",
            "data": vault_data,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.ucm_connector.submit_for_review(transfer_payload)

        # Clear temp vault after successful transfer
        self.unanswered_path.write_text(json.dumps([]))

        # Update logic config
        self.logic_config["pending_reviews"].append({
            "transfer_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "query_count": len(vault_data)
        })
        self._save_logic_config(self.logic_config)

    def apply_improvement(self, improvement_data: Dict[str, Any]):
        """
        Apply approved improvement from UCM/CALI

        Args:
            improvement_data: Contains updates for script or logic
        """
        # Verify this improvement is for this worker
        if improvement_data.get("worker_id") != self.worker_id:
            return

        # Apply script updates
        if "script_updates" in improvement_data:
            self._apply_script_updates(improvement_data["script_updates"])

        # Apply logic updates
        if "logic_updates" in improvement_data:
            self._apply_logic_updates(improvement_data["logic_updates"])

        # Update approved improvements log
        self.logic_config["approved_improvements"].append({
            "improvement_id": improvement_data.get("improvement_id"),
            "applied_at": datetime.utcnow().isoformat(),
            "changes": improvement_data
        })
        self._save_logic_config(self.logic_config)

    def _apply_script_updates(self, updates: Dict[str, Any]):
        """Apply updates to script.json"""
        # Merge updates into script data
        if "new_sections" in updates:
            self.script_data["script"].extend(updates["new_sections"])

        if "modified_sections" in updates:
            for mod in updates["modified_sections"]:
                # Find and replace section
                for i, section in enumerate(self.script_data["script"]):
                    if section.get("id") == mod.get("id"):
                        self.script_data["script"][i] = mod
                        break

        # Update metadata
        self.script_data["metadata"]["last_updated"] = datetime.utcnow().isoformat()
        
        # Safe version bump logic (edge-safe)
        version = self.script_data["metadata"]["version"]
        major, minor = map(int, version.split("."))
        self.script_data["metadata"]["version"] = f"{major}.{minor + 1}"

        # Save updated script
        self._save_script()

        # Reindex mini-SKG
        self.mini_skg.reindex(self.script_data["script"])

    def _apply_logic_updates(self, updates: Dict[str, Any]):
        """Apply updates to logic.json"""
        self.logic_config.update(updates)
        self._save_logic_config(self.logic_config)

    def _get_fallback_response(self) -> str:
        """Get fallback response when question cannot be answered"""
        return self.logic_config.get(
            "fallback_response",
            "I've noted your question and will get back to you with a complete answer soon."
        )

    def get_status(self) -> Dict[str, Any]:
        """Get worker status for monitoring"""
        temp_vault_count = 0
        if self.unanswered_path.exists():
            with open(self.unanswered_path, 'r') as f:
                temp_vault_count = len(json.load(f))

        return {
            "worker_id": self.worker_id,
            "job_name": self.job_name,
            "logic_version": self.logic_config["version"],
            "script_version": self.script_data["metadata"]["version"],
            "temp_vault_pending": temp_vault_count,
            "pending_reviews": len(self.logic_config["pending_reviews"]),
            "approved_improvements": len(self.logic_config["approved_improvements"])
        }


class MiniSKG:
    """Mini-SKG for job-specific knowledge (already exists per user)"""

    def __init__(self, skg_dir: Path):
        self.skg_dir = skg_dir
        self.kg_path = skg_dir / "knowledge_graph.json"
        self.embeddings_path = skg_dir / "embeddings.db"
        self._initialize_skg()

    def _initialize_skg(self):
        """Initialize mini-SKG storage"""
        if not self.kg_path.exists():
            self.kg_path.write_text(json.dumps({"nodes": [], "edges": []}))

        # Initialize SQLite for embeddings
        conn = sqlite3.connect(self.embeddings_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                id TEXT PRIMARY KEY,
                content TEXT,
                embedding BLOB,
                metadata TEXT
            )
        """)
        conn.close()

    def query(self, user_input: str, script_sections: List[Dict]) -> List[Dict]:
        """Query mini-SKG for relevant script sections"""
        # Simplified implementation - in production you'd use embeddings
        relevant = []
        input_lower = user_input.lower()

        for section in script_sections:
            # Simple keyword matching for demo
            keywords = section.get("keywords", [])
            if any(keyword.lower() in input_lower for keyword in keywords):
                relevant.append(section)

        return relevant

    def reindex(self, script_sections: List[Dict]):
        """Reindex mini-SKG when script updates"""
        # Extract keywords and embeddings from script sections
        kg_data = {
            "nodes": [],
            "edges": [],
            "last_indexed": datetime.utcnow().isoformat()
        }

        for section in script_sections:
            node = {
                "id": section.get("id"),
                "type": "script_section",
                "keywords": section.get("keywords", []),
                "content_preview": section.get("content", "")[:100]
            }
            kg_data["nodes"].append(node)

        self.kg_path.write_text(json.dumps(kg_data, indent=2))