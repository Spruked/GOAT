"""
GOAT Licenser - Verification and badge minting system
"""

from typing import Dict, Any, Optional
from pathlib import Path
import sys
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from vault.core import Vault


class Verifier:
    """Verify learning and mint badges"""
    
    def __init__(self, vault: Vault):
        self.vault = vault
    
    def verify_quiz_completion(
        self,
        user_id: str,
        skill_id: str,
        quiz_score: float,
        glyph_ids: list[str]
    ) -> Dict[str, Any]:
        """
        Verify quiz completion and eligibility for badge
        
        Args:
            user_id: User identifier
            skill_id: Skill completed
            quiz_score: Quiz score (0.0 to 1.0)
            glyph_ids: Glyphs used in learning
        
        Returns:
            Verification result
        """
        # Check passing threshold
        passing_score = 0.7
        passed = quiz_score >= passing_score
        
        # Verify glyph provenance
        glyph_proofs = []
        all_verified = True
        
        for gid in glyph_ids:
            proof = self.vault.get_proof(gid)
            glyph_proofs.append(proof)
            
            if not proof.get("signature_valid", False):
                all_verified = False
        
        return {
            "verified": passed and all_verified,
            "user_id": user_id,
            "skill_id": skill_id,
            "quiz_score": quiz_score,
            "passed": passed,
            "glyph_proofs_valid": all_verified,
            "timestamp": int(datetime.utcnow().timestamp())
        }
    
    def mint_badge(
        self,
        user_id: str,
        skill_id: str,
        verification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Mint learner badge NFT
        (In production, this would mint actual NFT)
        
        Args:
            user_id: User receiving badge
            skill_id: Skill mastered
            verification: Verification data
        
        Returns:
            Badge data
        """
        if not verification.get("verified", False):
            return {"error": "Verification required to mint badge"}
        
        # Create badge data
        badge_data = {
            "type": "goat_learner_badge",
            "user_id": user_id,
            "skill_id": skill_id,
            "quiz_score": verification["quiz_score"],
            "verified_at": verification["timestamp"],
            "issuer": "goat_platform",
            "metadata": {
                "standard": "ERC-721",
                "provenance": verification.get("glyph_proofs_valid", False)
            }
        }
        
        # Store badge in vault
        badge_glyph = self.vault.create_glyph(
            data=badge_data,
            source=f"badge://{user_id}/{skill_id}"
        )
        
        return {
            "badge_id": badge_glyph.id,
            "badge_data": badge_data,
            "nft_metadata": {
                "name": f"GOAT Learner Badge - {skill_id}",
                "description": f"Verified completion of {skill_id} with {verification['quiz_score']:.0%} score",
                "image": f"/glyph/svg/{badge_glyph.id}",
                "attributes": [
                    {"trait_type": "Skill", "value": skill_id},
                    {"trait_type": "Score", "value": int(verification['quiz_score'] * 100)},
                    {"trait_type": "Platform", "value": "GOAT"}
                ]
            }
        }
    
    def feedback_loop(
        self,
        skill_id: str,
        user_feedback: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process user feedback to improve content
        
        Args:
            skill_id: Skill being reviewed
            user_feedback: User's feedback data
        
        Returns:
            Feedback acknowledgment
        """
        # Store feedback
        feedback_data = {
            "skill_id": skill_id,
            "rating": user_feedback.get("rating", 0),
            "comments": user_feedback.get("comments", ""),
            "difficulty_rating": user_feedback.get("difficulty", "medium"),
            "timestamp": int(datetime.utcnow().timestamp())
        }
        
        # Create feedback glyph
        feedback_glyph = self.vault.create_glyph(
            data=feedback_data,
            source=f"feedback://{skill_id}"
        )
        
        return {
            "feedback_id": feedback_glyph.id,
            "message": "Thank you for your feedback!",
            "impact": "This will help improve future lessons"
        }


# Example usage
if __name__ == "__main__":
    from pathlib import Path
    
    # Initialize vault
    vault = Vault(
        storage_path=Path("./data/vault"),
        encryption_key="supersecretkey123"
    )
    
    # Create verifier
    verifier = Verifier(vault)
    
    # Verify completion
    verification = verifier.verify_quiz_completion(
        user_id="user_123",
        skill_id="solidity_storage",
        quiz_score=0.85,
        glyph_ids=["0xabc123"]
    )
    
    print(f"Verified: {verification['verified']}")
    
    # Mint badge
    if verification["verified"]:
        badge = verifier.mint_badge("user_123", "solidity_storage", verification)
        print(f"Badge minted: {badge['badge_id']}")
