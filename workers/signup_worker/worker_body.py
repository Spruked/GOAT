"""
Signup Worker - User Profile Creation & Initial Data Collection
Collects signup data, creates customer profile, and calculates initial priority
"""

from pathlib import Path
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _templates.worker_skg_template import WorkerSKG
from lib.user_store import save_user
from analytics.priority_tier_assignment import PriorityTierAssigner

class SignupWorker(WorkerSKG):
    """Handles user signup and initial profile creation"""

    def __init__(self, ucm_connector):
        super().__init__(
            worker_id="worker_signup_v1",
            job_name="signup",
            ucm_connector=ucm_connector
        )
    
    def run(self, user_input, user_context: Dict[str, Any]) -> str:
        """
        Override run method to handle structured form data instead of text queries
        """
        # user_input here is form data dict, not text
        form_data = user_input
        context = user_context
        
        # Load signup script sections
        sections = self.script_data["script"]
        
        # Validate required fields
        current_step = context.get("current_step", 1)
        step_section = next((s for s in sections if s.get("step") == current_step), None)

        if not step_section:
            return json.dumps({"error": "Invalid step"})

        # Validate fields
        validation_errors = self._validate_fields(form_data, step_section.get("fields", []))
        if validation_errors:
            return json.dumps({"error": f"Please correct these fields: {', '.join(validation_errors)}"})

        # Store in context (will be saved when complete)
        if "collected_data" not in context:
            context["collected_data"] = {}

        context["collected_data"].update(form_data)

        # Check if signup is complete
        if current_step >= len(sections):
            return self._complete_signup(context)

        return json.dumps({"status": f"step_{current_step}_completed", "next_step": current_step + 1})

    def _validate_fields(self, form_data: Dict, fields: List[Dict]) -> List[str]:
        """Validate form field data"""
        errors = []

        for field in fields:
            field_name = field["field"]
            if field["required"] and not form_data.get(field_name):
                errors.append(field_name)

            # Validate format if provided and field has value
            if form_data.get(field_name) and "validation" in field:
                import re
                if not re.match(field["validation"], str(form_data[field_name])):
                    errors.append(f"{field_name}_format")

        return errors

    def _complete_signup(self, context: Dict) -> str:
        """Create user profile and calculate initial priority"""
        collected_data = context.get("collected_data", {})
        user_id = f"user_{uuid.uuid4().hex[:12]}"

        # Calculate initial priority score
        initial_score = self._calculate_initial_priority(collected_data)
        
        # Use priority tier assigner to determine initial tier
        tier_assigner = PriorityTierAssigner(Path(__file__).resolve().parents[2])
        initial_tier = self._determine_initial_tier(initial_score)

        # Create user profile
        profile = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "profile": {
                "email": collected_data.get("email"),
                "full_name": collected_data.get("full_name"),
                "organization": collected_data.get("organization"),
                "use_case": collected_data.get("use_case"),
                "marketing_consent": {
                    "marketing_email": collected_data.get("marketing_email", False),
                    "beta_access": collected_data.get("beta_access", False)
                }
            },
            "spending": {
                "total_spent": 0,
                "lifetime_value": 0,
                "avg_transaction": 0,
                "transaction_count": 0,
                "products_purchased": []
            },
            "priority": {
                "tier": initial_tier,
                "score": initial_score,
                "last_updated": datetime.utcnow().isoformat()
            },
            "activity": {
                "first_login": datetime.utcnow().isoformat(),
                "last_login": None,
                "projects_created": 0,
                "projects_completed": 0
            }
        }

        # Save profile to disk
        self._save_user_profile(user_id, profile)

        # Transfer to UCM for customer analytics
        self._transfer_profile_to_ucm(user_id, profile)

        return json.dumps({
            "status": "signup_complete",
            "user_id": user_id,
            "next_action": "start_onboarding",
            "message": f"Welcome, {collected_data.get('full_name')}! Your account is ready. Let's set up your first project."
        })

    def _calculate_initial_priority(self, data: Dict) -> float:
        """
        Calculate initial priority score based on signup data
        Score: 0-100 (higher = more valuable/prospect)
        """
        score = 0.0

        # Budget range scoring
        budget = data.get("budget_range")
        budget_scores = {
            "under_50": 5,
            "50_100": 15,
            "100_500": 40,
            "500_plus": 75,
            "enterprise": 90
        }
        score += budget_scores.get(budget, 10)

        # Timeline scoring
        timeline = data.get("timeline")
        timeline_scores = {
            "immediate": 30,
            "this_month": 20,
            "next_month": 10,
            "exploring": 5
        }
        score += timeline_scores.get(timeline, 5)

        # Use case scoring (some use cases correlate with higher LTV)
        use_case = data.get("use_case")
        if use_case == "corporate_trainer":
            score += 25
        elif use_case == "educator":
            score += 15
        elif use_case == "author":
            score += 10

        # Organization presence
        if data.get("organization"):
            score += 10

        # Cap at 100
        return min(score, 100)

    def _determine_initial_tier(self, score: float) -> str:
        """Determine initial tier based on signup priority score"""
        if score >= 90:
            return "vip"
        elif score >= 70:
            return "priority"
        elif score >= 50:
            return "standard"
        else:
            return "standard"

    def _save_user_profile(self, user_id: str, profile: Dict):
        """Save user profile to disk"""
        save_user(user_id, profile)

    def _transfer_profile_to_ucm(self, user_id: str, profile: Dict):
        """Transfer new user profile to UCM for analytics"""
        transfer_payload = {
            "source": "signup_worker",
            "worker_id": self.worker_id,
            "job_name": "signup",
            "data_type": "new_user_profile",
            "data": {
                "user_id": user_id,
                "profile": profile["profile"],
                "priority_score": profile["priority"]["score"],
                "tier": profile["priority"]["tier"]
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        self.ucm_connector.submit_for_review(transfer_payload)