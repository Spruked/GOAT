"""
Customer Priority Tier Assignment
Calculates tiers based on spending and engagement
"""

from datetime import datetime
from typing import Dict, List
import json
from pathlib import Path

class PriorityTierAssigner:
    """
    Assigns priority tiers to users based on:
    - Lifetime Value (LTV)
    - Average transaction size
    - Project volume
    - Recency of activity
    """

    def __init__(self, goat_base_dir: Path):
        self.users_dir = goat_base_dir / "users" / "active"
        self.tiers = {
            "enterprise": {"min_ltv": 2000, "min_projects": 10, "support": "dedicated"},
            "vip": {"min_ltv": 500, "min_projects": 3, "support": "priority"},
            "priority": {"min_ltv": 150, "min_projects": 1, "support": "standard"},
            "standard": {"min_ltv": 0, "min_projects": 0, "support": "community"}
        }

    def update_user_priority(self, user_id: str, transaction_amount: float = 0):
        """
        Update user's priority tier after each transaction

        Args:
            user_id: User identifier
            transaction_amount: Amount spent in this transaction
        """
        profile_path = self.users_dir / user_id / "profile.json"
        if not profile_path.exists():
            return

        with open(profile_path, 'r') as f:
            profile = json.load(f)

        # Update spending
        spending = profile["spending"]
        spending["total_spent"] += transaction_amount
        spending["lifetime_value"] = spending["total_spent"]  # For now, same
        spending["transaction_count"] += 1
        spending["avg_transaction"] = spending["total_spent"] / spending["transaction_count"]

        # Determine new tier
        new_tier = self._calculate_tier(spending)

        # Update priority
        profile["priority"]["tier"] = new_tier
        profile["priority"]["score"] = self._calculate_priority_score(spending)
        profile["priority"]["last_updated"] = datetime.utcnow().isoformat()

        # Save updated profile
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=2)

        return new_tier

    def _calculate_tier(self, spending: Dict) -> str:
        """Determine tier based on spending metrics"""
        ltv = spending["lifetime_value"]
        project_count = spending["transaction_count"]  # Simplified: 1 tx = 1 project

        for tier_name, tier_def in self.tiers.items():
            if ltv >= tier_def["min_ltv"] and project_count >= tier_def["min_projects"]:
                return tier_name

        return "standard"

    def _calculate_priority_score(self, spending: Dict) -> float:
        """Calculate 0-100 priority score"""
        ltv = spending["lifetime_value"]

        # Logarithmic scaling: $5000 = 100 points
        import math
        score = min(100, (math.log10(ltv + 100) - 2) * 50)

        return max(0, score)