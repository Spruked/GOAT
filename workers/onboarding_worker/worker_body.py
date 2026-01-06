"""
Onboarding Worker - GOAT Initial User Journey
Implements WorkerSKG template for onboarding flow
Version: 1.1 (Aligned with surgical improvements)
"""

from pathlib import Path
from typing import List, Dict, Optional, Any
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from workers._templates.worker_skg_template import WorkerSKG
from lib.user_store import load_user, get_user_priority_tier
import json

class OnboardingWorker(WorkerSKG):
    """Specialized worker for user onboarding process"""

    def __init__(self, ucm_connector):
        super().__init__(
            worker_id="worker_onboarding_v1",
            job_name="onboarding",
            ucm_connector=ucm_connector
        )
        self.current_step = 0  # Start with signup step

    def _generate_response(self, user_input: str, sections: List[Dict], context: Dict) -> Optional[str]:
        """
        Generate response based on user input and current onboarding step

        This implements the actual logic for answering user questions
        during onboarding. If a question cannot be answered from the
        script, returns None to trigger temp vault saving.
        """

        # Try to determine what step user is on
        user_step = context.get("current_step", self.current_step)

        # Find relevant section for this step
        step_sections = [s for s in sections if s.get("step") == user_step]
        if not step_sections:
            step_sections = sections

        # Check if user input matches expected questions
        input_lower = user_input.lower()

        for section in step_sections:
            # Check against expected questions for this section
            for expected_q in section.get("expected_questions", []):
                if self._question_match(input_lower, expected_q.lower()):
                    return self._format_answer(section, expected_q, user_input)

            # Check keywords as fallback
            if any(keyword in input_lower for keyword in section.get("keywords", [])):
                return self._format_general_answer(section, user_input)

        # No match found - question cannot be answered by script
        return None

    def _question_match(self, user_input: str, expected_question: str) -> bool:
        """Fuzzy matching for question similarity"""
        # Simple implementation - in production use embeddings
        user_words = set(user_input.split())
        expected_words = set(expected_question.split())

        # If they share significant keywords, consider it a match
        common_words = user_words.intersection(expected_words)
        return len(common_words) >= 2 or any(
            word in user_input for word in ["what", "how", "when", "where", "why", "can", "do"]
            if word in expected_question
        )

    def _format_answer(self, section: Dict, expected_q: str, original_input: str) -> str:
        """Format a specific answer to an expected question"""
        # For onboarding, we want to be conversational but informative
        step_num = section.get("step")
        step_title = section.get("title")
        content = section.get("content")

        # Generate context-aware response
        response = f"**Step {step_num}: {step_title}**\n\n"
        response += f"{content}\n\n"
        response += f"*Is there anything else about this step you'd like to know?*"

        return response

    def _format_general_answer(self, section: Dict, original_input: str) -> str:
        """Format a general answer based on keywords"""
        step_num = section.get("step")
        step_title = section.get("title")
        content = section.get("content")

        response = f"**Step {step_num}: {step_title}**\n\n"
        response += f"{content}\n\n"

        # Add helpful prompt
        if step_num < 6:
            response += f"When you're ready, we can move to the next step. Just ask 'next' or 'continue'."
        else:
            response += f"You're all set to start creating!"

        return response

    def get_next_step(self, current_step: int) -> Dict[str, Any]:
        """Get the next onboarding step"""
        next_step_num = current_step + 1

        next_section = None
        for section in self.script_data["script"]:
            if section.get("step") == next_step_num:
                next_section = section
                break

        if not next_section:
            return {"completed": True, "message": "Onboarding complete!"}

        return {
            "step": next_step_num,
            "title": next_section["title"],
            "content": next_section["content"],
            "expected_questions": next_section.get("expected_questions", [])
        }

    def process_navigation(self, user_input: str, current_step: int) -> Dict[str, Any]:
        """
        Handle navigation commands during onboarding

        Returns dict with response and step update
        """
        input_lower = user_input.lower().strip()

        # Navigation commands
        if input_lower in ["next", "continue", "proceed", "skip"]:
            return self.get_next_step(current_step)
        elif input_lower in ["back", "previous", "go back"]:
            prev_step = max(0, current_step - 1)  # Allow going back to step 0
            return {"step": prev_step, "action": "navigate"}
        elif input_lower in ["restart", "start over"]:
            return {"step": 0, "action": "restart"}  # Restart from signup
        elif input_lower.startswith("go to step"):
            try:
                target_step = int(input_lower.split()[-1])
                if 0 <= target_step <= 7:  # Updated range
                    return {"step": target_step, "action": "navigate"}
            except ValueError:
                pass

        return None

# Enhanced priority-aware methods
    def run(self, user_input: str, user_context: Dict[str, Any]) -> str:
        """
        Main execution with priority awareness
        """
        # Load user profile if available
        user_profile = self._load_user_profile(user_context.get("user_id"))

        # Adjust behavior based on priority tier
        if user_profile and self._should_accelerate(user_profile):
            return self._generate_vip_onboarding(user_input, user_context, user_profile)

        # Standard onboarding
        return super().run(user_input, user_context)

    def _load_user_profile(self, user_id: Optional[str]) -> Optional[Dict]:
        """Load user profile created during signup"""
        if not user_id:
            return None

        return load_user(user_id)

    def _should_accelerate(self, user_profile: Dict) -> bool:
        """Check if user should get accelerated VIP onboarding"""
        tier = user_profile.get("priority", {}).get("tier", "standard")
        return tier in ["vip", "enterprise"]

    def _generate_vip_onboarding(self, user_input: str, context: Dict, profile: Dict) -> str:
        """Accelerated onboarding for high-value users"""
        # Skip basic intro, go straight to advanced features
        # Mention priority support

        response = "**Welcome to GOAT Premium Onboarding**\n\n"
        response += f"Based on your profile, you're set up for success, {profile['profile']['full_name']}.\n\n"
        response += "We'll fast-track you to advanced features. Priority support is available 24/7.\n\n"

        # Process normally but with VIP context
        standard_response = super().run(user_input, context)
        return response + standard_response

# Example UCM Connector Interface
class UCMConnector:
    """Stub for UCM/CALI connection - implement actual connection logic"""

    def submit_for_review(self, payload: Dict[str, Any]):
        """Submit temp vault data to UCM for review"""
        print(f"[UCM] Received transfer from worker {payload['worker_id']}")
        print(f"[UCM] Queries to review: {len(payload['data'])}")

        # In production, this would:
        # 1. Send to CALI's immutable matrix
        # 2. Trigger ECM review process
        # 3. Queue for SoftMax analysis
        # 4. Await approval before returning improvements

        # For now, just log
        return {"status": "submitted", "review_id": "rev_" + payload["worker_id"]}

    def receive_improvement(self, worker_id: str) -> Optional[Dict[str, Any]]:
        """Check for approved improvements from UCM"""
        # In production, poll CALI for approved improvements
        return None


# Usage example
if __name__ == "__main__":
    # Initialize connector and worker
    ucm = UCMConnector()
    worker = OnboardingWorker(ucm_connector=ucm)

    # Simulate user interactions (complete onboarding sequence)
    test_inputs = [
        "How do I sign up?",  # Step 0: Signup
        "next",  # Move to goal selection
        "What can I create?",  # Step 1: Goal selection
        "I want to create a book",  # Select book option
        "next",  # Move to welcome
        "What is GOAT?",  # Step 2: Welcome
        "next",  # Move to upload
        "What file types can I upload?",  # Step 3: Upload
        "next",  # Move to voice selection
        "How many voices are available?",  # Step 4: Voice selection
        "next",  # Move to pricing
        "How much does it cost?",  # Step 5: Pricing
        "next",  # Move to blockchain
        "Do I have to use blockchain?",  # Step 6: Blockchain
        "next",  # Move to final
        "What happens next?"  # Step 7: Final
    ]

    context = {"current_step": 0, "user_id": "user_123"}  # Start from signup

    for user_input in test_inputs:
        print(f"\n[User] {user_input}")

        # Check for navigation first
        nav_result = worker.process_navigation(user_input, context["current_step"])
        if nav_result:
            if "step" in nav_result:
                context["current_step"] = nav_result["step"]
                print(f"[System] Navigated to step {nav_result['step']}")
            continue

        # Using run() instead of execute_job() for lifecycle clarity
        response = worker.run(user_input, context)
        print(f"[Worker] {response}")

    # Check worker status
    print(f"\n[Status] {json.dumps(worker.get_status(), indent=2)}")