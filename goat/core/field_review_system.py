"""
GOAT Field Review System - Courtroom-grade human oversight for self-improvement proposals.

Design Principle: GOAT may observe and suggest. Only a human may decide. Every decision is remembered.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import os
from pathlib import Path

@dataclass
class ImprovementProposal:
    """Authoritative data model for GOAT self-improvement proposals."""
    proposal_id: str
    pattern_type: str                 # performance_anomaly | reliability_concern | etc
    target_component: str             # distiller_id or worker_id
    observation: str                  # factual statement
    suggestion: str                   # non-binding suggestion
    confidence: float                 # capped ≤ 0.4
    evidence: List[Dict[str, Any]]    # references / samples / seq_ids
    proposed_at: str

    status: str                       # pending_review | approved | rejected
    approved_config: Optional[Dict[str, Any]] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    human_rationale: Optional[str] = None  # REQUIRED on approve/reject

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ImprovementProposal':
        """Create from dictionary."""
        return cls(**data)

    def validate_decision(self) -> None:
        """Ensure human_rationale is provided for decisions."""
        if self.status in ['approved', 'rejected'] and not self.human_rationale:
            raise ValueError("human_rationale is mandatory for approve/reject decisions")

    def validate_config(self) -> None:
        """Ensure approved_config is only set on approval."""
        if self.status == 'approved' and not self.approved_config:
            raise ValueError("approved_config is required for approved proposals")
        if self.status == 'rejected' and self.approved_config:
            raise ValueError("approved_config not allowed for rejected proposals")


class GOATFieldReviewSystem:
    """Courtroom-grade review system for GOAT self-improvement proposals."""

    def __init__(self, data_dir: str = "data/field_review"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.queue_file = self.data_dir / "improvement_queue.json"
        self.audit_file = self.data_dir / "audit_log.jsonl"

        # Initialize files if they don't exist
        if not self.queue_file.exists():
            self._save_queue([])
        if not self.audit_file.exists():
            self.audit_file.touch()

    def _load_queue(self) -> List[ImprovementProposal]:
        """Load proposals from JSON file."""
        try:
            with open(self.queue_file, 'r') as f:
                data = json.load(f)
                return [ImprovementProposal.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_queue(self, proposals: List[ImprovementProposal]) -> None:
        """Save proposals to JSON file."""
        data = [p.to_dict() for p in proposals]
        with open(self.queue_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _audit_log(self, event: str, proposal_id: str, reviewed_by: str = None,
                   human_rationale: str = None, approved_config_hash: str = None) -> None:
        """Append immutable audit entry."""
        entry = {
            "event": event,
            "proposal_id": proposal_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        if reviewed_by:
            entry["reviewed_by"] = reviewed_by
        if human_rationale:
            entry["human_rationale"] = human_rationale
        if approved_config_hash:
            entry["approved_config_hash"] = approved_config_hash

        with open(self.audit_file, 'a') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def submit_proposal(self, proposal: ImprovementProposal) -> None:
        """Submit a new proposal for review."""
        if proposal.confidence > 0.4:
            raise ValueError("Proposal confidence cannot exceed 0.4")

        proposal.status = "pending_review"
        proposal.proposed_at = datetime.utcnow().isoformat() + "Z"

        queue = self._load_queue()
        queue.append(proposal)
        self._save_queue(queue)

        self._audit_log("proposal_submitted", proposal.proposal_id)

    def get_pending_proposals(self) -> List[ImprovementProposal]:
        """Get all proposals awaiting review."""
        queue = self._load_queue()
        return [p for p in queue if p.status == "pending_review"]

    def get_proposal(self, proposal_id: str) -> Optional[ImprovementProposal]:
        """Get full proposal details."""
        queue = self._load_queue()
        return next((p for p in queue if p.proposal_id == proposal_id), None)

    def approve_proposal(self, proposal_id: str, approved_config: Dict[str, Any],
                        human_rationale: str, reviewed_by: str) -> None:
        """Approve a proposal with human oversight."""
        queue = self._load_queue()
        proposal = next((p for p in queue if p.proposal_id == proposal_id), None)

        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        if proposal.status != "pending_review":
            raise ValueError(f"Proposal {proposal_id} is not pending review")

        # Update proposal
        proposal.status = "approved"
        proposal.approved_config = approved_config
        proposal.reviewed_by = reviewed_by
        proposal.reviewed_at = datetime.utcnow().isoformat() + "Z"
        proposal.human_rationale = human_rationale

        proposal.validate_decision()
        proposal.validate_config()

        self._save_queue(queue)

        # Audit log
        config_hash = str(hash(json.dumps(approved_config, sort_keys=True)))
        self._audit_log("proposal_approved", proposal_id, reviewed_by, human_rationale, config_hash)

    def reject_proposal(self, proposal_id: str, human_rationale: str, reviewed_by: str) -> None:
        """Reject a proposal with human rationale."""
        queue = self._load_queue()
        proposal = next((p for p in queue if p.proposal_id == proposal_id), None)

        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        if proposal.status != "pending_review":
            raise ValueError(f"Proposal {proposal_id} is not pending review")

        # Update proposal
        proposal.status = "rejected"
        proposal.reviewed_by = reviewed_by
        proposal.reviewed_at = datetime.utcnow().isoformat() + "Z"
        proposal.human_rationale = human_rationale

        proposal.validate_decision()
        proposal.validate_config()

        self._save_queue(queue)

        # Audit log
        self._audit_log("proposal_rejected", proposal_id, reviewed_by, human_rationale)

    def get_decision_history(self) -> List[Dict[str, Any]]:
        """Get chronological decision ledger."""
        queue = self._load_queue()
        decisions = []

        for proposal in queue:
            if proposal.status in ['approved', 'rejected']:
                decisions.append({
                    "proposal_id": proposal.proposal_id,
                    "status": proposal.status,
                    "reviewed_by": proposal.reviewed_by,
                    "reviewed_at": proposal.reviewed_at,
                    "confidence": proposal.confidence,
                    "human_rationale": proposal.human_rationale
                })

        # Sort by review time
        decisions.sort(key=lambda x: x.get('reviewed_at', ''), reverse=True)
        return decisions

    def get_approved_insights(self) -> List[Dict[str, Any]]:
        """Runtime consumption: Only approved proposals for system optimization."""
        queue = self._load_queue()
        approved = [p for p in queue if p.status == "approved"]

        insights = []
        for proposal in approved:
            insights.append({
                "target_component": proposal.target_component,
                "approved_config": proposal.approved_config,
                "confidence": proposal.confidence,
                "approved_at": proposal.reviewed_at
            })

        return insights