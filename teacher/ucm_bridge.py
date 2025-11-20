# ucm_bridge.py
"""
GOAT UCM Bridge - Connects Teacher Engine to UCM cognition
"""

import requests
from typing import Dict, Any, Optional
import os

class UCMBridge:
    """Bridge between GOAT Teacher Engine and UCM cognition system"""

    def __init__(self, ucm_endpoint: str = None):
        self.ucm_endpoint = ucm_endpoint or os.getenv("UCM_ENDPOINT", "http://localhost:8000")
        self.api_key = os.getenv("UCM_API_KEY")

    def get_skill_inference(self, user_id: str) -> Dict[str, Any]:
        """Get skill inferences from UCM for user"""
        try:
            response = requests.get(
                f"{self.ucm_endpoint}/api/cognition/skills/{user_id}",
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            )
            return response.json() if response.status_code == 200 else {}
        except:
            return {}

    def request_explanation(self, skill_id: str, user_level: str = "beginner") -> str:
        """Request explanation from UCM LLM"""
        try:
            payload = {
                "skill_id": skill_id,
                "user_level": user_level,
                "context": "teaching_explanation"
            }
            response = requests.post(
                f"{self.ucm_endpoint}/api/llm/explain",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            )
            if response.status_code == 200:
                return response.json().get("explanation", "")
        except:
            pass

        # Fallback explanation
        return f"This skill covers {skill_id} concepts with practical applications."

    def get_user_cognition_history(self, user_id: str) -> Dict[str, Any]:
        """Get user's cognition history for difficulty scaling"""
        try:
            response = requests.get(
                f"{self.ucm_endpoint}/api/cognition/history/{user_id}",
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            )
            return response.json() if response.status_code == 200 else {}
        except:
            return {}

    def submit_learning_event(self, user_id: str, event: Dict[str, Any]):
        """Submit learning event to UCM"""
        try:
            payload = {
                "user_id": user_id,
                "event": event,
                "timestamp": event.get("timestamp")
            }
            requests.post(
                f"{self.ucm_endpoint}/api/events/learning",
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            )
        except:
            pass  # Silent failure for now

    def get_vault_seeds(self, user_id: str) -> List[str]:
        """Get vault seeds from UCM for teaching recommendations"""
        try:
            response = requests.get(
                f"{self.ucm_endpoint}/api/vault/seeds/{user_id}",
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            )
            if response.status_code == 200:
                return response.json().get("seeds", [])
        except:
            pass
        return []