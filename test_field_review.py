#!/usr/bin/env python3
"""
Test the GOAT Field Review System - Courtroom-grade human oversight.
"""

import sys
import os
from pathlib import Path

# Add goat to path
sys.path.insert(0, str(Path(__file__).parent))

from goat.core.field_review_system import GOATFieldReviewSystem, ImprovementProposal
import json

def test_review_system():
    """Test the complete review workflow."""
    print("🧪 Testing GOAT Field Review System...")

    # Initialize system
    review_system = GOATFieldReviewSystem()

    # Create a test proposal
    proposal = ImprovementProposal(
        proposal_id="test_123",
        pattern_type="performance_anomaly",
        target_component="visidata_distiller:csv",
        observation="CSV files averaging 78s processing time",
        suggestion="Consider chunking strategy",
        confidence=0.35,
        evidence=[
            {"seq": 112, "duration_ms": 81234},
            {"seq": 118, "duration_ms": 79012}
        ],
        proposed_at="2026-01-27T18:14:02Z"
    )

    print("📝 Submitting test proposal...")
    review_system.submit_proposal(proposal)

    # Check pending proposals
    pending = review_system.get_pending_proposals()
    print(f"📋 Found {len(pending)} pending proposals")
    assert len(pending) == 1
    assert pending[0].proposal_id == "test_123"

    # Get full proposal details
    full_proposal = review_system.get_proposal("test_123")
    print(f"🔍 Retrieved proposal: {full_proposal.proposal_id}")
    assert full_proposal is not None
    assert full_proposal.status == "pending_review"

    # Approve the proposal
    print("✅ Approving proposal...")
    review_system.approve_proposal(
        proposal_id="test_123",
        approved_config={"chunk_size": 1000, "pre_filter": "drop_empty_rows"},
        human_rationale="Chunking improves CSV without affecting accuracy; tested locally.",
        reviewed_by="test_admin"
    )

    # Check approved insights
    insights = review_system.get_approved_insights()
    print(f"🧠 Found {len(insights)} approved insights")
    assert len(insights) == 1
    assert insights[0]['target_component'] == "visidata_distiller:csv"

    # Check decision history
    history = review_system.get_decision_history()
    print(f"📚 Found {len(history)} decisions in history")
    assert len(history) == 1
    assert history[0]['status'] == 'approved'

    print("✅ All tests passed! GOAT Field Review System is working correctly.")

    # Test rejection
    print("❌ Testing rejection workflow...")

    # Create another proposal
    reject_proposal = ImprovementProposal(
        proposal_id="test_reject_456",
        pattern_type="reliability_concern",
        target_component="worker:complex_processor",
        observation="Worker failing on complex tasks",
        suggestion="Adjust complexity thresholds",
        confidence=0.28,
        evidence=[{"seq": 200, "outcome": "failure"}],
        proposed_at="2026-01-27T19:00:00Z"
    )

    review_system.submit_proposal(reject_proposal)

    # Reject it
    review_system.reject_proposal(
        proposal_id="test_reject_456",
        human_rationale="Worker failures due to upstream data quality issues, not complexity.",
        reviewed_by="test_admin"
    )

    # Check history again
    history = review_system.get_decision_history()
    assert len(history) == 2
    rejected = [h for h in history if h['status'] == 'rejected']
    assert len(rejected) == 1

    print("✅ Rejection workflow tested successfully!")

if __name__ == "__main__":
    test_review_system()