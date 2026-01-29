# goat/admin/field_review.py
"""
Administrative interface for reviewing GOAT Field proposals.
Prevents unauthorized changes (like the Copilot incident).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from goat.core.goat_field_skg import GOATSpaceField
import logging

logger = logging.getLogger(__name__)

class FieldImprovementReview:
    """
    All GOAT improvements flow through here.
    No changes without explicit approval.
    """

    def __init__(self, field_path: str = "./goat_field/"):
        self.field = GOATSpaceField(field_path)
        self.audit_log = Path(field_path) / 'audit_log.jsonl'

    def list_pending(self) -> List[Dict]:
        """List all pending improvement proposals."""
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []
        return [p for p in queue if p['status'] == 'pending_review']

    def list_approved(self) -> List[Dict]:
        """List all approved proposals."""
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []
        return [p for p in queue if p['status'] == 'approved']

    def list_rejected(self) -> List[Dict]:
        """List all rejected proposals."""
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []
        return [p for p in queue if p['status'] == 'rejected']

    def approve(self, proposal_id: str, approved_config: Dict, approver: str):
        """
        Approve a proposal with specific configuration.
        Logs approver for audit.
        """
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []

        for proposal in queue:
            if proposal['proposal_id'] == proposal_id:
                proposal['status'] = 'approved'
                proposal['approved_config'] = approved_config
                proposal['approved_by'] = approver
                proposal['approved_at'] = datetime.utcnow().isoformat()

                # Log to immutable audit trail
                self._audit_log('approve', proposal_id, approver, approved_config)
                logger.info(f"Approved proposal {proposal_id} by {approver}")
                break
        else:
            raise ValueError(f"Proposal {proposal_id} not found")

        self.field.proposal_queue.write_text(json.dumps(queue, indent=2))

    def reject(self, proposal_id: str, reason: str, rejector: str):
        """Reject proposal with reason."""
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []

        for proposal in queue:
            if proposal['proposal_id'] == proposal_id:
                proposal['status'] = 'rejected'
                proposal['rejection_reason'] = reason
                proposal['rejected_by'] = rejector
                proposal['rejected_at'] = datetime.utcnow().isoformat()

                # Log to immutable audit trail
                self._audit_log('reject', proposal_id, rejector, {'reason': reason})
                logger.info(f"Rejected proposal {proposal_id} by {rejector}: {reason}")
                break
        else:
            raise ValueError(f"Proposal {proposal_id} not found")

        self.field.proposal_queue.write_text(json.dumps(queue, indent=2))

    def modify_proposal(self, proposal_id: str, modifications: Dict, modifier: str):
        """
        Modify a pending proposal before approval/rejection.
        Useful for refining suggestions.
        """
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []

        for proposal in queue:
            if proposal['proposal_id'] == proposal_id and proposal['status'] == 'pending_review':
                # Apply modifications
                for key, value in modifications.items():
                    proposal[key] = value

                proposal['modified_by'] = modifier
                proposal['modified_at'] = datetime.utcnow().isoformat()

                # Log modification
                self._audit_log('modify', proposal_id, modifier, modifications)
                logger.info(f"Modified proposal {proposal_id} by {modifier}")
                break
        else:
            raise ValueError(f"Pending proposal {proposal_id} not found")

        self.field.proposal_queue.write_text(json.dumps(queue, indent=2))

    def get_proposal_details(self, proposal_id: str) -> Optional[Dict]:
        """Get detailed information about a specific proposal."""
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []
        for proposal in queue:
            if proposal['proposal_id'] == proposal_id:
                return proposal
        return None

    def get_proposals_by_target(self, target_component: str) -> List[Dict]:
        """Get all proposals for a specific component."""
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []
        return [p for p in queue if p['target_component'] == target_component]

    def get_proposals_by_type(self, pattern_type: str) -> List[Dict]:
        """Get all proposals of a specific type."""
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []
        return [p for p in queue if p['pattern_type'] == pattern_type]

    def get_audit_trail(self, limit: int = 100) -> List[Dict]:
        """Get recent audit log entries."""
        if not self.audit_log.exists():
            return []

        entries = []
        with open(self.audit_log, 'r') as f:
            for line in f:
                entries.append(json.loads(line))
                if len(entries) >= limit:
                    break

        return list(reversed(entries))  # Most recent first

    def _audit_log(self, action: str, proposal_id: str, user: str, details: Dict):
        """Log action to immutable audit trail."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'proposal_id': proposal_id,
            'user': user,
            'details': details
        }

        with open(self.audit_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def generate_review_report(self) -> Dict:
        """
        Generate a comprehensive review report for administrators.
        """
        queue = json.loads(self.field.proposal_queue.read_text()) if self.field.proposal_queue.exists() else []

        pending = [p for p in queue if p['status'] == 'pending_review']
        approved = [p for p in queue if p['status'] == 'approved']
        rejected = [p for p in queue if p['status'] == 'rejected']

        # Group by type
        type_stats = {}
        for proposal in queue:
            ptype = proposal['pattern_type']
            status = proposal['status']
            if ptype not in type_stats:
                type_stats[ptype] = {'pending': 0, 'approved': 0, 'rejected': 0}
            type_stats[ptype][status] += 1

        return {
            'summary': {
                'total_proposals': len(queue),
                'pending': len(pending),
                'approved': len(approved),
                'rejected': len(rejected)
            },
            'by_type': type_stats,
            'recent_pending': pending[-5:],  # Last 5 pending
            'recent_activity': self.get_audit_trail(10)
        }

# Global instance
field_review = FieldImprovementReview()