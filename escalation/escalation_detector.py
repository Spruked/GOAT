"""
Escalation Detector - Detects when user needs Orb intervention before human escalation
"""

from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json

class EscalationDetector:
    """
    Monitors user interactions and triggers Orb escalation when:
    1. Multiple worker temp vaults fill up (user blocked repeatedly)
    2. User explicitly requests "help", "support", "talk to someone"
    3. Spending tier is VIP/Enterprise (priority escalation path)
    4. Sentiment analysis detects frustration
    5. Same question asked 3+ times (user not getting answers)
    """

    def __init__(self, goat_base_dir: Path):
        self.goat_base_dir = goat_base_dir
        self.users_dir = goat_base_dir / "users" / "active"
        self.escalation_thresholds = {
            "temp_vault_fill_rate": 3,  # After 3 unanswered across workers
            "frustration_keywords": ["help", "support", "agent", "human", "someone", "stuck", "frustrated", "not working"],
            "repeat_question_limit": 3,
            "frustration_sentiment_score": -0.6
        }

    def should_escalate_to_orb(self, user_id: str, user_input: str,
                               worker_context: Dict) -> Dict[str, Any]:
        """
        Determine if user should get Orb intervention

        Returns:
            {
                "escalate": bool,
                "reason": str,
                "priority": "low|medium|high|critical",
                "user_context": {}
            }
        """
        reasons = []
        priority = "low"

        # Check 1: Load user profile for tier-based escalation
        user_profile = self._load_user_profile(user_id)
        if user_profile:
            # VIP/Enterprise auto-escalate with high priority
            tier = user_profile.get("priority", {}).get("tier")
            if tier in ["vip", "enterprise"]:
                return {
                    "escalate": True,
                    "reason": f"{tier.upper()} tier priority escalation",
                    "priority": "high",
                    "user_context": {
                        "tier": tier,
                        "spending": user_profile["spending"],
                        "name": user_profile["profile"]["full_name"]
                    }
                }

        # Check 2: Explicit escalation request
        if self._is_explicit_escalation_request(user_input):
            reasons.append("explicit_user_request")
            priority = "medium"

        # Check 3: Temp vault fill rate across workers
        temp_vault_count = self._count_user_temp_vaults(user_id)
        if temp_vault_count >= self.escalation_thresholds["temp_vault_fill_rate"]:
            reasons.append(f"temp_vaults_filled_{temp_vault_count}")
            priority = "high"

        # Check 4: Repeated questions
        repeat_count = self._count_question_repetitions(user_id, user_input)
        if repeat_count >= self.escalation_thresholds["repeat_question_limit"]:
            reasons.append(f"question_repeated_{repeat_count}_times")
            priority = "medium"

        # Check 5: Sentiment analysis (placeholder)
        if self._detect_frustration(user_input):
            reasons.append("frustration_detected")
            priority = "high"

        # Decision
        should_escalate = len(reasons) > 0

        return {
            "escalate": should_escalate,
            "reason": "|".join(reasons) if reasons else "none",
            "priority": priority if should_escalate else "low",
            "user_context": {
                "profile": user_profile,
                "temp_vault_count": temp_vault_count,
                "repeat_count": repeat_count
            }
        }

    def _load_user_profile(self, user_id: str) -> Optional[Dict]:
        """Load user profile from disk"""
        profile_path = self.users_dir / user_id / "profile.json"
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                return json.load(f)
        return None

    def _is_explicit_escalation_request(self, user_input: str) -> bool:
        """Check if user is explicitly asking for help/human"""
        input_lower = user_input.lower()
        return any(keyword in input_lower for keyword in self.escalation_thresholds["frustration_keywords"])

    def _count_user_temp_vaults(self, user_id: str) -> int:
        """Count total unanswered questions across all workers for this user"""
        workers_dir = self.goat_base_dir / "workers"
        total_unanswered = 0

        for worker_dir in workers_dir.iterdir():
            if worker_dir.is_dir() and worker_dir.name != "_templates":
                temp_vault_dir = worker_dir / "temp_vault"
                if not temp_vault_dir.exists():
                    continue  # Performance safeguard: skip workers without temp vaults
                
                vault_path = temp_vault_dir / "unanswered_queries.json"
                if vault_path.exists():
                    with open(vault_path, 'r') as f:
                        vault_data = json.load(f)
                        # Count entries for this specific user
                        user_entries = [e for e in vault_data if e["user_context"].get("user_id") == user_id]
                        total_unanswered += len(user_entries)

        return total_unanswered

    def _count_question_repetitions(self, user_id: str, user_input: str) -> int:
        """
        Count how many times this user has asked a similar question.
        Simplified - in production use embeddings similarity.
        """
        # Placeholder - track in user session
        return 0  # Would check session history

    def _detect_frustration(self, user_input: str) -> bool:
        """Placeholder for sentiment analysis"""
        # In production: integrate with NLP model
        return False