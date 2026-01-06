"""
Customer Lead Scoring System
Evaluates prospects for marketing automation and sales prioritization
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from pathlib import Path

class LeadScorer:
    """
    Scores leads based on multiple factors:
    - Signup data quality
    - Engagement signals
    - Budget indicators
    - Timeline urgency
    - Use case alignment
    """

    def __init__(self, goat_base_dir: Path):
        self.users_dir = goat_base_dir / "users" / "active"
        self.scoring_weights = {
            "budget_range": 0.35,
            "timeline": 0.25,
            "use_case": 0.20,
            "organization": 0.10,
            "marketing_consent": 0.10
        }

    def score_new_lead(self, user_id: str) -> Dict[str, Any]:
        """
        Calculate comprehensive lead score for new user

        Returns dict with score, tier, and recommended actions
        """
        profile_path = self.users_dir / user_id / "profile.json"
        if not profile_path.exists():
            return {"score": 0, "tier": "cold", "actions": []}

        with open(profile_path, 'r') as f:
            profile = json.load(f)

        user_data = profile["profile"]

        # Calculate component scores
        scores = {
            "budget_score": self._score_budget(user_data.get("budget_range")),
            "timeline_score": self._score_timeline(user_data.get("timeline")),
            "use_case_score": self._score_use_case(user_data.get("use_case")),
            "organization_score": self._score_organization(user_data.get("organization")),
            "consent_score": self._score_consent(user_data.get("marketing_consent", {}))
        }

        # Weighted total score
        total_score = sum(
            scores[component] * self.scoring_weights[component.replace("_score", "")]
            for component in scores.keys()
        )

        # Determine lead tier
        tier = self._determine_lead_tier(total_score)

        # Recommended actions
        actions = self._get_recommended_actions(tier, user_data)

        return {
            "user_id": user_id,
            "total_score": round(total_score, 2),
            "component_scores": scores,
            "tier": tier,
            "actions": actions,
            "scored_at": datetime.utcnow().isoformat()
        }

    def _score_budget(self, budget_range: Optional[str]) -> float:
        """Score based on stated budget range"""
        budget_scores = {
            "enterprise": 100,
            "500_plus": 90,
            "100_500": 70,
            "50_100": 40,
            "under_50": 20,
            None: 10  # No budget specified
        }
        return budget_scores.get(budget_range, 10)

    def _score_timeline(self, timeline: Optional[str]) -> float:
        """Score based on purchase timeline"""
        timeline_scores = {
            "immediate": 100,
            "this_month": 80,
            "next_month": 60,
            "exploring": 30,
            None: 20
        }
        return timeline_scores.get(timeline, 20)

    def _score_use_case(self, use_case: Optional[str]) -> float:
        """Score based on use case (some correlate with higher LTV)"""
        use_case_scores = {
            "corporate_trainer": 90,
            "educator": 75,
            "author": 60,
            "content_creator": 50,
            "other": 30,
            None: 20
        }
        return use_case_scores.get(use_case, 20)

    def _score_organization(self, organization: Optional[str]) -> float:
        """Score based on organization presence"""
        if organization and len(organization.strip()) > 0:
            return 80  # B2B signals
        return 20  # Individual

    def _score_consent(self, marketing_consent: Dict) -> float:
        """Score based on marketing opt-ins"""
        score = 20  # Base score

        if marketing_consent.get("marketing_email"):
            score += 40

        if marketing_consent.get("beta_access"):
            score += 40

        return min(score, 100)

    def _determine_lead_tier(self, total_score: float) -> str:
        """Convert score to lead tier"""
        if total_score >= 80:
            return "hot"
        elif total_score >= 60:
            return "warm"
        elif total_score >= 40:
            return "lukewarm"
        else:
            return "cold"

    def _get_recommended_actions(self, tier: str, user_data: Dict) -> List[str]:
        """Get recommended marketing/sales actions"""
        actions = []

        if tier == "hot":
            actions.extend([
                "Immediate sales outreach within 1 hour",
                "Schedule discovery call within 24 hours",
                "Send enterprise welcome package",
                "Add to VIP onboarding track"
            ])
        elif tier == "warm":
            actions.extend([
                "Sales outreach within 24 hours",
                "Send personalized demo invitation",
                "Include in priority nurture sequence",
                "Accelerated onboarding path"
            ])
        elif tier == "lukewarm":
            actions.extend([
                "Add to standard nurture sequence",
                "Send educational content series",
                "Monitor for engagement signals",
                "Standard onboarding flow"
            ])
        else:  # cold
            actions.extend([
                "Add to awareness nurture sequence",
                "Send basic product information",
                "Monitor for budget/timeline updates",
                "Standard onboarding flow"
            ])

        # Add use-case specific actions
        use_case = user_data.get("use_case")
        if use_case == "corporate_trainer":
            actions.append("Send enterprise case studies")
        elif use_case == "educator":
            actions.append("Send education-focused resources")

        return actions