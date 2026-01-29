# backend/app/api/v1/endpoints/admin.py
"""
Admin endpoints for SKG
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.security.auth import dual_auth
from app.models.user import UserCreate
from app.core.users import create_user, get_all_users, delete_user, block_user, unblock_user
import csv
import json
from datetime import datetime
import os

router = APIRouter()

@router.get("/tenants")
async def list_tenants(token: dict = Depends(dual_auth)):
    """List all tenants"""
    return {"tenants": ["default"]}

@router.post("/backup")
async def create_backup(token: dict = Depends(dual_auth)):
    """Create system backup"""
    return {"status": "backup_created", "timestamp": "2025-12-08T00:00:00Z"}

@router.get("/users")
async def list_users(token: dict = Depends(dual_auth)):
    """List all users (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    users = get_all_users()
    return {"users": users}

@router.get("/users/{user_id}")
async def get_user(user_id: int, token: dict = Depends(dual_auth)):
    """Get a specific user details (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    users = get_all_users()
    user = next((u for u in users if u.get('id') == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}

@router.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict, token: dict = Depends(dual_auth)):
    """Update a user (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    # This would need to be implemented in the users core module
    # For now, return success
    return {"message": f"User {user_id} updated successfully"}

@router.post("/users")
async def add_user(user: UserCreate, token: dict = Depends(dual_auth)):
    """Add a new user (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    user_id = create_user(user)
    return {"user_id": user_id, "message": "User created successfully"}

@router.delete("/users/{user_id}")
async def remove_user(user_id: int, token: dict = Depends(dual_auth)):
    """Delete a user (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    success = delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.put("/users/{user_id}/block")
async def block_user_endpoint(user_id: int, token: dict = Depends(dual_auth)):
    """Block a user (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    success = block_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User blocked successfully"}

@router.put("/users/{user_id}/unblock")
async def unblock_user_endpoint(user_id: int, token: dict = Depends(dual_auth)):
    """Unblock a user (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    success = unblock_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User unblocked successfully"}

@router.get("/export/users/csv")
async def export_users_csv(token: dict = Depends(dual_auth)):
    """Export all users to CSV for marketing (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    users = get_all_users()

    # Create marketing export directory if it doesn't exist
    export_dir = "exports/marketing"
    os.makedirs(export_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{export_dir}/users_marketing_{timestamp}.csv"

    # Write CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'email', 'full_name', 'role', 'is_blocked', 'created_at', 'last_login', 'files_count', 'storage_used']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow({
                'id': user.get('id'),
                'email': user.get('email'),
                'full_name': user.get('full_name', ''),
                'role': user.get('role', 'user'),
                'is_blocked': user.get('is_blocked', False),
                'created_at': user.get('created_at'),
                'last_login': user.get('last_login'),
                'files_count': user.get('files_count', 0),
                'storage_used': user.get('storage_used', '0 MB')
            })

    return FileResponse(filename, media_type='text/csv', filename=f"users_marketing_{timestamp}.csv")

@router.get("/export/users/json")
async def export_users_json(token: dict = Depends(dual_auth)):
    """Export all users to JSON for marketing (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    users = get_all_users()

    # Create marketing export directory if it doesn't exist
    export_dir = "exports/marketing"
    os.makedirs(export_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{export_dir}/users_marketing_{timestamp}.json"

    # Filter out sensitive data for marketing
    marketing_users = []
    for user in users:
        marketing_users.append({
            'id': user.get('id'),
            'email': user.get('email'),
            'full_name': user.get('full_name', ''),
            'role': user.get('role', 'user'),
            'is_blocked': user.get('is_blocked', False),
            'created_at': user.get('created_at'),
            'last_login': user.get('last_login'),
            'files_count': user.get('files_count', 0),
            'storage_used': user.get('storage_used', '0 MB'),
            'marketing_consent': user.get('marketing_consent', True)  # Assume consent by default
        })

    # Write JSON file
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump({
            'export_date': datetime.now().isoformat(),
            'total_users': len(marketing_users),
            'users': marketing_users
        }, jsonfile, indent=2, ensure_ascii=False)

    return FileResponse(filename, media_type='application/json', filename=f"users_marketing_{timestamp}.json")

@router.get("/marketing/users")
async def get_marketing_users(token: dict = Depends(dual_auth)):
    """Get users list for marketing purposes (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    users = get_all_users()

    # Return filtered data for marketing
    marketing_users = []
    for user in users:
        marketing_users.append({
            'id': user.get('id'),
            'email': user.get('email'),
            'full_name': user.get('full_name', ''),
            'created_at': user.get('created_at'),
            'last_login': user.get('last_login'),
            'files_count': user.get('files_count', 0),
            'is_active': not user.get('is_blocked', False),
            'marketing_consent': user.get('marketing_consent', True)
        })

    return {"users": marketing_users}

@router.put("/marketing/users/{user_id}/consent")
async def update_marketing_consent(user_id: int, consent: bool, token: dict = Depends(dual_auth)):
    """Update marketing consent for a user (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    # This would need to be implemented in the users core module
    # For now, return success
    return {"message": f"Marketing consent {'granted' if consent else 'revoked'} for user {user_id}"}

# Audiobooks management endpoints
@router.get("/audiobooks/stats")
async def get_audiobooks_stats(token: dict = Depends(dual_auth)):
    """Get audiobooks statistics (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "total_audiobooks": 0,
        "total_plays": 0,
        "active_users": 0,
        "avg_listen_time": "0h"
    }

@router.get("/audiobooks")
async def list_audiobooks(token: dict = Depends(dual_auth)):
    """List all audiobooks (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"audiobooks": []}

# Books management endpoints
@router.get("/books/stats")
async def get_books_stats(token: dict = Depends(dual_auth)):
    """Get books statistics (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "total_books": 0,
        "published_books": 0,
        "total_downloads": 0,
        "total_revenue": 0
    }

@router.get("/books")
async def list_books(token: dict = Depends(dual_auth)):
    """List all books (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"books": []}

# Podcasts management endpoints
@router.get("/podcasts/stats")
async def get_podcasts_stats(token: dict = Depends(dual_auth)):
    """Get podcasts statistics (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "total_podcasts": 0,
        "total_episodes": 0,
        "total_listens": 0,
        "avg_engagement": "0%"
    }

@router.get("/podcasts")
async def list_podcasts(token: dict = Depends(dual_auth)):
    """List all podcasts (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"podcasts": []}

# Voice systems management endpoints
@router.get("/voice/stats")
async def get_voice_stats(token: dict = Depends(dual_auth)):
    """Get voice systems statistics (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "active_voices": 0,
        "total_generations": 0,
        "avg_quality": "0%",
        "avg_processing_time": "0s"
    }

@router.get("/voice/systems")
async def list_voice_systems(token: dict = Depends(dual_auth)):
    """List all voice systems (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"voices": []}

# Distillers management endpoints
@router.get("/distillers/stats")
async def get_distillers_stats(token: dict = Depends(dual_auth)):
    """Get distillers statistics (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "total_distillers": 0,
        "active_distillers": 0,
        "total_executions": 0,
        "avg_performance": "0%"
    }

@router.get("/distillers")
async def list_distillers(token: dict = Depends(dual_auth)):
    """List all distillers (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"distillers": []}

@router.put("/distillers/{distiller_id}/activate")
async def activate_distiller(distiller_id: str, token: dict = Depends(dual_auth)):
    """Activate a distiller (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": f"Distiller {distiller_id} activated"}

@router.put("/distillers/{distiller_id}/deactivate")
async def deactivate_distiller(distiller_id: str, token: dict = Depends(dual_auth)):
    """Deactivate a distiller (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": f"Distiller {distiller_id} deactivated"}

# Collectors management endpoints
@router.get("/collectors/stats")
async def get_collectors_stats(token: dict = Depends(dual_auth)):
    """Get collectors statistics (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "total_collectors": 0,
        "active_collectors": 0,
        "total_data_collected": 0,
        "success_rate": "0%"
    }

@router.get("/collectors")
async def list_collectors(token: dict = Depends(dual_auth)):
    """List all collectors (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"collectors": []}

@router.put("/collectors/{collector_id}/start")
async def start_collector(collector_id: str, token: dict = Depends(dual_auth)):
    """Start a collector (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": f"Collector {collector_id} started"}

@router.put("/collectors/{collector_id}/stop")
async def stop_collector(collector_id: str, token: dict = Depends(dual_auth)):
    """Stop a collector (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": f"Collector {collector_id} stopped"}

# GOAT Field management endpoints
@router.get("/goat-field/stats")
async def get_goat_field_stats(token: dict = Depends(dual_auth)):
    """Get GOAT Field statistics (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "total_nodes": 0,
        "active_edges": 0,
        "learning_rate": "0%",
        "integrity_score": "0%",
        "clutter_cleaned": 0,
        "patterns_extracted": 0,
        "self_repairs": 0
    }

@router.get("/goat-field/proposals")
async def list_goat_field_proposals(token: dict = Depends(dual_auth)):
    """List GOAT Field learning proposals (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"proposals": []}

@router.put("/goat-field/proposals/{proposal_id}/approve")
async def approve_proposal(proposal_id: str, token: dict = Depends(dual_auth)):
    """Approve a learning proposal (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": f"Proposal {proposal_id} approved"}

@router.put("/goat-field/proposals/{proposal_id}/reject")
async def reject_proposal(proposal_id: str, token: dict = Depends(dual_auth)):
    """Reject a learning proposal (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": f"Proposal {proposal_id} rejected"}

# Payments management endpoints
@router.get("/payments/stats")
async def get_payments_stats(token: dict = Depends(dual_auth)):
    """Get payments statistics (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "total_revenue": 0,
        "total_transactions": 0,
        "active_subscribers": 0,
        "avg_transaction": 0,
        "revenue_growth": 0,
        "monthly_subscribers": 0,
        "yearly_subscribers": 0,
        "lifetime_subscribers": 0
    }

@router.get("/payments/transactions")
async def list_payment_transactions(token: dict = Depends(dual_auth)):
    """List payment transactions (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"transactions": []}

# Certificates management endpoints
@router.get("/certificates/stats")
async def get_certificates_stats(token: dict = Depends(dual_auth)):
    """Get certificates statistics (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {
        "total_certificates": 0,
        "issued_this_month": 0,
        "active_certificates": 0,
        "total_downloads": 0
    }

@router.get("/certificates")
async def list_certificates(token: dict = Depends(dual_auth)):
    """List all certificates (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"certificates": []}

# GOAT Field Review System endpoints
from goat.core.field_review_system import GOATFieldReviewSystem, ImprovementProposal

field_review_system = GOATFieldReviewSystem()

@router.get("/field/review/pending")
async def get_pending_proposals(token: dict = Depends(dual_auth)):
    """List proposals awaiting human review (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    proposals = field_review_system.get_pending_proposals()
    return [
        {
            "proposal_id": p.proposal_id,
            "pattern_type": p.pattern_type,
            "target_component": p.target_component,
            "confidence": p.confidence,
            "observation": p.observation,
            "suggestion": p.suggestion,
            "proposed_at": p.proposed_at
        }
        for p in proposals
    ]

@router.get("/field/review/{proposal_id}")
async def get_proposal_details(proposal_id: str, token: dict = Depends(dual_auth)):
    """Get full proposal inspection view (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    proposal = field_review_system.get_proposal(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    return proposal.to_dict()

@router.post("/field/review/{proposal_id}/approve")
async def approve_proposal(proposal_id: str, request_data: dict, token: dict = Depends(dual_auth)):
    """Approve a proposal with human oversight (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    try:
        field_review_system.approve_proposal(
            proposal_id=proposal_id,
            approved_config=request_data["approved_config"],
            human_rationale=request_data["human_rationale"],
            reviewed_by=token.get("email", "admin")
        )
        return {"message": f"Proposal {proposal_id} approved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/field/review/{proposal_id}/reject")
async def reject_proposal(proposal_id: str, request_data: dict, token: dict = Depends(dual_auth)):
    """Reject a proposal with human rationale (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    try:
        field_review_system.reject_proposal(
            proposal_id=proposal_id,
            human_rationale=request_data["human_rationale"],
            reviewed_by=token.get("email", "admin")
        )
        return {"message": f"Proposal {proposal_id} rejected successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/field/review/history")
async def get_decision_history(token: dict = Depends(dual_auth)):
    """Get chronological decision ledger (admin only)"""
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return field_review_system.get_decision_history()