#!/usr/bin/env python3
"""
GOAT Field Review CLI
Command-line interface for reviewing and approving GOAT Field improvement proposals.
"""

import argparse
import json
import sys
from datetime import datetime
from goat.admin.field_review import field_review
from goat.core.field_reflection_service import field_reflection_service

def list_pending():
    """List all pending proposals."""
    pending = field_review.list_pending()

    if not pending:
        print("No pending proposals.")
        return

    print(f"\n📋 Pending Improvement Proposals ({len(pending)})\n")

    for i, proposal in enumerate(pending, 1):
        print(f"{i}. Proposal {proposal['proposal_id'][:8]}")
        print(f"   Type: {proposal['pattern_type']}")
        print(f"   Target: {proposal['target_component']}")
        print(f"   Observation: {proposal['observation']}")
        print(f"   Confidence: {proposal['confidence']:.2f}")
        print(f"   Proposed: {proposal['proposed_at']}")
        print()

def list_approved():
    """List all approved proposals."""
    approved = field_review.list_approved()

    if not approved:
        print("No approved proposals.")
        return

    print(f"\n✅ Approved Proposals ({len(approved)})\n")

    for proposal in approved:
        print(f"• {proposal['proposal_id'][:8]} - {proposal['target_component']}")
        print(f"  Approved: {proposal['approved_at']} by {proposal['approved_by']}")
        if 'approved_config' in proposal:
            print(f"  Config: {json.dumps(proposal['approved_config'], indent=2)}")
        print()

def approve_proposal(proposal_id, config_file=None, approver="admin"):
    """Approve a proposal with optional configuration."""
    # Load config if provided
    config = {}
    if config_file:
        with open(config_file, 'r') as f:
            config = json.load(f)

    try:
        field_review.approve(proposal_id, config, approver)
        print(f"✅ Approved proposal {proposal_id}")

        if config:
            print(f"Configuration applied: {json.dumps(config, indent=2)}")

    except ValueError as e:
        print(f"❌ Error: {e}")

def reject_proposal(proposal_id, reason, rejector="admin"):
    """Reject a proposal with reason."""
    try:
        field_review.reject(proposal_id, reason, rejector)
        print(f"❌ Rejected proposal {proposal_id}: {reason}")
    except ValueError as e:
        print(f"❌ Error: {e}")

def show_proposal_details(proposal_id):
    """Show detailed information about a specific proposal."""
    proposal = field_review.get_proposal_details(proposal_id)

    if not proposal:
        print(f"Proposal {proposal_id} not found.")
        return

    print(f"\n📄 Proposal Details: {proposal_id}\n")
    print(f"Type: {proposal['pattern_type']}")
    print(f"Target: {proposal['target_component']}")
    print(f"Status: {proposal['status']}")
    print(f"Confidence: {proposal['confidence']:.2f}")
    print(f"Proposed: {proposal['proposed_at']}")
    print()
    print("Observation:")
    print(f"  {proposal['observation']}")
    print()
    print("Suggestion:")
    print(f"  {proposal['suggestion']}")
    print()

    if 'evidence' in proposal and proposal['evidence']:
        print("Evidence:")
        for evidence in proposal['evidence']:
            print(f"  • {evidence}")
        print()

    if proposal['status'] == 'approved':
        print("Approved Configuration:")
        print(json.dumps(proposal.get('approved_config', {}), indent=2))
    elif proposal['status'] == 'rejected':
        print(f"Rejection Reason: {proposal.get('rejection_reason', 'N/A')}")

def show_stats():
    """Show field statistics and review summary."""
    stats = field_reflection_service.get_field_stats()
    review_report = field_review.generate_review_report()

    print("📊 GOAT Field Statistics\n")
    print(f"Total Observations: {stats['total_observations']}")
    print(f"Graph Nodes: {stats['graph_nodes']}")
    print(f"Graph Edges: {stats['graph_edges']}")
    print(f"Pending Proposals: {stats['pending_proposals']}")
    print(f"Last Reflection: {stats['last_reflection']}")
    print(f"Reflection Active: {stats['reflection_active']}")

    # Show graph health if available
    if 'graph_health' in stats:
        health = stats['graph_health']
        print(f"\n🩺 Graph Health: {health.get('status', 'unknown')}")
        if health.get('status') != 'networkx_unavailable':
            print(f"  - Meta Patterns: {health.get('meta_patterns', 0)}")
            print(f"  - Archived Nodes: {stats.get('archived_nodes', 0)}")
            print(f"  - Last Repair: {stats.get('last_repair', 'never')}")
            print(f"  - Clutter Stats: {stats.get('clutter_stats', {})}")

    print("
📋 Review Summary\n"    summary = review_report['summary']
    print(f"Total Proposals: {summary['total_proposals']}")
    print(f"Pending: {summary['pending']}")
    print(f"Approved: {summary['approved']}")
    print(f"Rejected: {summary['rejected']}")
    print()

    if review_report['by_type']:
        print("By Type:")
        for ptype, counts in review_report['by_type'].items():
            print(f"  {ptype}: {counts['pending']} pending, {counts['approved']} approved, {counts['rejected']} rejected")

def trigger_compaction():
    """Manually trigger graph compaction and repair."""
    import asyncio

    async def run_compaction():
        print("🔧 Triggering GOAT Field compaction and repair...")
        try:
            await field_reflection_service.field._compaction_pass()
            print("✅ Compaction completed successfully")

            # Show updated stats
            stats = field_reflection_service.get_field_stats()
            if 'graph_health' in stats:
                health = stats['graph_health']
                print(f"📊 Post-compaction health: {health.get('status', 'unknown')}")
                if 'clutter_stats' in stats:
                    print(f"🧹 Clutter removed: {stats['clutter_stats']}")

        except Exception as e:
            print(f"❌ Compaction failed: {e}")

    asyncio.run(run_compaction())

def main():
    parser = argparse.ArgumentParser(description="GOAT Field Review CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List commands
    subparsers.add_parser('pending', help='List pending proposals')
    subparsers.add_parser('approved', help='List approved proposals')

    # Action commands
    approve_parser = subparsers.add_parser('approve', help='Approve a proposal')
    approve_parser.add_argument('proposal_id', help='Proposal ID to approve')
    approve_parser.add_argument('--config', help='JSON config file for approval')
    approve_parser.add_argument('--approver', default='admin', help='Approver name')

    reject_parser = subparsers.add_parser('reject', help='Reject a proposal')
    reject_parser.add_argument('proposal_id', help='Proposal ID to reject')
    reject_parser.add_argument('reason', help='Rejection reason')
    reject_parser.add_argument('--rejector', default='admin', help='Rejector name')

    # Info commands
    details_parser = subparsers.add_parser('details', help='Show proposal details')
    details_parser.add_argument('proposal_id', help='Proposal ID')

    subparsers.add_parser('stats', help='Show field statistics')

    audit_parser = subparsers.add_parser('audit', help='Show audit trail')
    audit_parser.add_argument('--limit', type=int, default=10, help='Number of entries to show')

    subparsers.add_parser('compact', help='Trigger manual graph compaction')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == 'pending':
            list_pending()
        elif args.command == 'approved':
            list_approved()
        elif args.command == 'approve':
            approve_proposal(args.proposal_id, args.config, args.approver)
        elif args.command == 'reject':
            reject_proposal(args.proposal_id, args.reason, args.rejector)
        elif args.command == 'details':
            show_proposal_details(args.proposal_id)
        elif args.command == 'stats':
            show_stats()
        elif args.command == 'audit':
            show_audit_trail(args.limit)
        elif args.command == 'compact':
            trigger_compaction()

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()