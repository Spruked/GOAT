# event_logger.py
"""
GOAT Event Logger - Logs learning events to DALS
"""

import requests
import json
from typing import Dict, Any
from datetime import datetime
import os

class EventLogger:
    """Logs learning events to DALS (Data Analytics & Learning System)"""

    def __init__(self, dals_endpoint: str = None, iss_endpoint: str = None):
        self.dals_endpoint = dals_endpoint or os.getenv("DALS_ENDPOINT", "http://localhost:8001")
        self.iss_endpoint = iss_endpoint or os.getenv("ISS_ENDPOINT", "http://localhost:8002")
        self.api_key = os.getenv("DALS_API_KEY")

    def log_quiz_completion(self, user_id: str, skill_id: str, quiz_result: Dict[str, Any]):
        """Log quiz completion event"""
        event = {
            "event_type": "quiz_completion",
            "user_id": user_id,
            "skill_id": skill_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {
                "score": quiz_result.get("score", 0),
                "passed": quiz_result.get("passed", False),
                "correct_count": quiz_result.get("correct_count", 0),
                "total_questions": quiz_result.get("total_questions", 0),
                "time_taken": quiz_result.get("time_taken_seconds"),
                "difficulty": quiz_result.get("difficulty", "medium")
            }
        }

        self._send_to_dals(event)
        self._send_to_iss(event)

    def log_lesson_view(self, user_id: str, skill_id: str, lesson_data: Dict[str, Any]):
        """Log lesson view event"""
        event = {
            "event_type": "lesson_view",
            "user_id": user_id,
            "skill_id": skill_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {
                "lesson_type": lesson_data.get("type", "explanation"),
                "time_spent": lesson_data.get("time_spent_seconds"),
                "completion_rate": lesson_data.get("completion_rate", 0),
                "user_level": lesson_data.get("user_level", "beginner")
            }
        }

        self._send_to_dals(event)

    def log_achievement_unlocked(self, user_id: str, achievement: Dict[str, str]):
        """Log achievement unlock event"""
        event = {
            "event_type": "achievement_unlocked",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {
                "achievement_title": achievement.get("title"),
                "achievement_description": achievement.get("description"),
                "rarity": "common"  # Could be calculated
            }
        }

        self._send_to_dals(event)
        self._send_to_iss(event)

    def log_skill_mastery_update(self, user_id: str, skill_id: str, old_mastery: float, new_mastery: float):
        """Log skill mastery update"""
        event = {
            "event_type": "skill_mastery_update",
            "user_id": user_id,
            "skill_id": skill_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {
                "old_mastery": old_mastery,
                "new_mastery": new_mastery,
                "improvement": new_mastery - old_mastery,
                "mastery_level": self._classify_mastery(new_mastery)
            }
        }

        self._send_to_dals(event)

    def log_nft_mint(self, user_id: str, glyph_id: str, nft_data: Dict[str, Any]):
        """Log NFT minting event"""
        event = {
            "event_type": "nft_mint",
            "user_id": user_id,
            "glyph_id": glyph_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {
                "nft_type": nft_data.get("type", "teaching"),
                "skill_id": nft_data.get("skill_id"),
                "traits": nft_data.get("traits", []),
                "cert_sig_ready": nft_data.get("cert_sig_ready", False)
            }
        }

        self._send_to_dals(event)
        self._send_to_iss(event)

    def _classify_mastery(self, mastery: float) -> str:
        """Classify mastery level"""
        if mastery >= 0.9:
            return "expert"
        elif mastery >= 0.7:
            return "proficient"
        elif mastery >= 0.5:
            return "competent"
        else:
            return "beginner"

    def _send_to_dals(self, event: Dict[str, Any]):
        """Send event to DALS"""
        try:
            response = requests.post(
                f"{self.dals_endpoint}/api/events",
                json=event,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                } if self.api_key else {"Content-Type": "application/json"}
            )
            if response.status_code not in [200, 201]:
                print(f"DALS logging failed: {response.status_code}")
        except Exception as e:
            print(f"DALS logging error: {e}")

    def _send_to_iss(self, event: Dict[str, Any]):
        """Send event to ISS (if applicable)"""
        try:
            response = requests.post(
                f"{self.iss_endpoint}/api/events",
                json=event,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                } if self.api_key else {"Content-Type": "application/json"}
            )
            # ISS might not always respond, so don't log failures
        except:
            pass