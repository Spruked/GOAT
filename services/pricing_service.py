# services/pricing_service.py
"""
GOAT Premium Pricing Service
Pro-Sumer Content Foundry pricing: $299-$1,499 tiers with APEX DOC certification
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path

class GOATPremiumPricingService:
    """
    Premium pricing calculator for GOAT's Pro-Sumer Content Foundry.
    Implements tiered pricing with APEX DOC certification trust anchor.
    """

    # Premium Tier Definitions
    TIERS = {
        "scholar": {
            "name": "Scholar Tier",
            "price": 299,
            "data_limit_gb": 5,
            "features": [
                "5GB data parsing",
                "APEX DOC certification",
                "Basic content archaeology",
                "Single output format",
                "30-day support"
            ],
            "description": "Perfect for individual creators and researchers"
        },
        "professional": {
            "name": "Professional Tier",
            "price": 799,
            "data_limit_gb": 20,
            "features": [
                "20GB data parsing",
                "APEX DOC certification",
                "Multi-format outputs",
                "Advanced content archaeology",
                "Structure assistant",
                "90-day support",
                "Priority processing"
            ],
            "description": "For consultants, coaches, and professional creators"
        },
        "legacy": {
            "name": "Legacy Tier",
            "price": 1499,
            "data_limit_gb": 50,
            "features": [
                "50GB data parsing",
                "APEX DOC certification",
                "All output formats",
                "Full content archaeology suite",
                "Multi-file intelligence",
                "Collaboration tools",
                "1-year support",
                "White-glove onboarding",
                "Custom integrations"
            ],
            "description": "For organizations and legacy content creators"
        }
    }

    # Add-on Services
    ADD_ONS = {
        "perpetual_storage": {
            "name": "Perpetual Storage",
            "price": 199,
            "features": [
                "ChaCha20-Poly1305 encryption",
                "IPFS + Arweave redundancy",
                "APEX DOC storage certification",
                "Permanent link generation"
            ]
        },
        "apex_certification_upgrade": {
            "name": "13-Layer APEX DOC Certification",
            "price": 349,
            "features": [
                "Complete 13-layer attestation stack",
                "Cryptographic provenance proof",
                "Multi-sig node validation",
                "Blockchain timestamp anchoring",
                "Legal IP assignment framework"
            ]
        }
    }

    # Output Format Pricing (Professional+ tiers)
    OUTPUT_FORMATS = {
        "book_manuscript": {"name": "Book Manuscript", "included_in": ["legacy"], "price": 0},
        "executive_summary": {"name": "Executive Summary", "included_in": ["professional", "legacy"], "price": 0},
        "course_curriculum": {"name": "Course Curriculum", "included_in": ["professional", "legacy"], "price": 0},
        "knowledge_base": {"name": "Knowledge Base Articles", "included_in": ["legacy"], "price": 49},
        "training_materials": {"name": "Training Materials", "included_in": ["legacy"], "price": 49},
        "social_content": {"name": "Social Media Content", "included_in": ["professional", "legacy"], "price": 29},
        "presentation_deck": {"name": "Presentation Deck", "included_in": ["professional", "legacy"], "price": 39}
    }

    def __init__(self, pricing_db_path: str = "./data/premium_pricing.db"):
        """
        Initialize premium pricing service

        Args:
            pricing_db_path: Path to pricing database
        """
        self.pricing_db_path = Path(pricing_db_path)
        self.pricing_db_path.parent.mkdir(parents=True, exist_ok=True)

        # Load or create pricing database
        self._load_pricing_db()

    def _load_pricing_db(self):
        """Load pricing database"""
        if self.pricing_db_path.exists():
            with open(self.pricing_db_path, 'r') as f:
                self.pricing_db = json.load(f)
        else:
            self.pricing_db = {
                "users": {},
                "transactions": [],
                "tier_subscriptions": {},
                "last_updated": datetime.utcnow().isoformat()
            }
            self._save_pricing_db()

    def _save_pricing_db(self):
        """Save pricing database"""
        with open(self.pricing_db_path, 'w') as f:
            json.dump(self.pricing_db, f, indent=2, default=str)

    def calculate_premium_cost(self,
                              tier: str,
                              data_size_gb: float,
                              output_formats: List[str] = None,
                              add_ons: List[str] = None,
                              perpetual_storage: bool = False,
                              apex_certification: bool = False) -> Dict[str, Any]:
        """
        Calculate total premium cost for a legacy creation project

        Args:
            tier: Pricing tier (scholar, professional, legacy)
            data_size_gb: Size of data in GB
            output_formats: List of additional output formats
            add_ons: List of add-on services
            perpetual_storage: Include perpetual storage
            apex_certification: Include APEX DOC certification upgrade

        Returns:
            Complete cost breakdown
        """
        if tier not in self.TIERS:
            raise ValueError(f"Invalid tier: {tier}")

        tier_info = self.TIERS[tier]
        base_cost = tier_info["price"]

        # Check data size limits
        if data_size_gb > tier_info["data_limit_gb"]:
            raise ValueError(f"Data size {data_size_gb}GB exceeds {tier} tier limit of {tier_info['data_limit_gb']}GB")

        cost_breakdown = {
            "tier": {
                "name": tier_info["name"],
                "base_price": base_cost,
                "data_limit_gb": tier_info["data_limit_gb"]
            },
            "add_ons": [],
            "total_cost": base_cost,
            "features_included": tier_info["features"].copy()
        }

        # Add perpetual storage
        if perpetual_storage:
            storage_cost = self.ADD_ONS["perpetual_storage"]["price"]
            cost_breakdown["add_ons"].append({
                "name": "Perpetual Storage",
                "price": storage_cost,
                "features": self.ADD_ONS["perpetual_storage"]["features"]
            })
            cost_breakdown["total_cost"] += storage_cost

        # Add APEX certification upgrade
        if apex_certification:
            cert_cost = self.ADD_ONS["apex_certification_upgrade"]["price"]
            cost_breakdown["add_ons"].append({
                "name": "13-Layer APEX DOC Certification",
                "price": cert_cost,
                "features": self.ADD_ONS["apex_certification_upgrade"]["features"]
            })
            cost_breakdown["total_cost"] += cert_cost

        # Add output formats (for Professional+ tiers)
        format_costs = 0
        if output_formats and tier in ["professional", "legacy"]:
            for fmt in output_formats:
                if fmt in self.OUTPUT_FORMATS:
                    format_info = self.OUTPUT_FORMATS[fmt]
                    if tier not in format_info["included_in"]:
                        format_costs += format_info["price"]
                        cost_breakdown["add_ons"].append({
                            "name": format_info["name"],
                            "price": format_info["price"],
                            "type": "output_format"
                        })

        cost_breakdown["total_cost"] += format_costs

        # Add premium justification
        cost_breakdown["premium_justification"] = self._generate_premium_justification(tier, cost_breakdown["total_cost"])

        return cost_breakdown

    def _generate_premium_justification(self, tier: str, total_cost: float) -> Dict[str, Any]:
        """Generate premium value justification"""
        justifications = {
            "scholar": {
                "value_comparison": "Professional ghostwriter: $5,000-15,000 for similar manuscript",
                "goat_value": "70% of professional quality at 2% of the cost",
                "trust_anchor": "APEX DOC certification provides cryptographic provenance",
                "differentiation": "AI-powered content archaeology finds hidden gems in your data"
            },
            "professional": {
                "value_comparison": "Content agency package: $10,000-25,000 for multi-format content suite",
                "goat_value": "Complete content transformation pipeline with permanent certification",
                "trust_anchor": "13-layer APEX DOC attestation stack for enterprise-grade trust",
                "differentiation": "Multi-file intelligence cross-references your entire knowledge base"
            },
            "legacy": {
                "value_comparison": "Legacy content firm: $50,000+ for organizational knowledge distillation",
                "goat_value": "Enterprise-scale content transformation with collaboration tools",
                "trust_anchor": "Full APEX DOC ecosystem integration with custom legal frameworks",
                "differentiation": "Transforms organizational data into monetizable intellectual property"
            }
        }

        return justifications.get(tier, {})

    def get_tier_comparison(self) -> Dict[str, Any]:
        """Get comparison of all pricing tiers"""
        return {
            "tiers": self.TIERS,
            "comparison_matrix": {
                "data_parsing": {
                    "scholar": "5GB",
                    "professional": "20GB",
                    "legacy": "50GB"
                },
                "apex_certification": {
                    "scholar": "Basic (included)",
                    "professional": "Basic (included)",
                    "legacy": "Basic (included)"
                },
                "output_formats": {
                    "scholar": "1 format",
                    "professional": "3 formats + add-ons",
                    "legacy": "All formats included"
                },
                "support": {
                    "scholar": "30 days",
                    "professional": "90 days",
                    "legacy": "1 year"
                },
                "processing_priority": {
                    "scholar": "Standard",
                    "professional": "Priority",
                    "legacy": "White-glove"
                }
            },
            "add_ons": self.ADD_ONS,
            "output_formats": self.OUTPUT_FORMATS
        }

    def estimate_project_cost(self,
                            data_size_gb: float,
                            desired_formats: List[str] = None,
                            needs_certification: bool = True,
                            needs_storage: bool = True) -> Dict[str, Any]:
        """
        Recommend optimal tier and estimate cost for a project

        Args:
            data_size_gb: Size of data in GB
            desired_formats: Desired output formats
            needs_certification: Needs APEX DOC certification
            needs_storage: Needs perpetual storage

        Returns:
            Tier recommendation and cost estimate
        """
        # Determine appropriate tier based on data size
        if data_size_gb <= 5:
            recommended_tier = "scholar"
        elif data_size_gb <= 20:
            recommended_tier = "professional"
        else:
            recommended_tier = "legacy"

        # Calculate cost for recommended tier
        try:
            cost_estimate = self.calculate_premium_cost(
                tier=recommended_tier,
                data_size_gb=data_size_gb,
                output_formats=desired_formats,
                perpetual_storage=needs_storage,
                apex_certification=needs_certification
            )
        except ValueError as e:
            # If data size exceeds tier limit, recommend upgrade
            if "exceeds" in str(e):
                if recommended_tier == "scholar":
                    recommended_tier = "professional"
                elif recommended_tier == "professional":
                    recommended_tier = "legacy"
                else:
                    raise ValueError("Data size exceeds maximum supported limit")

                cost_estimate = self.calculate_premium_cost(
                    tier=recommended_tier,
                    data_size_gb=data_size_gb,
                    output_formats=desired_formats,
                    perpetual_storage=needs_storage,
                    apex_certification=needs_certification
                )

        return {
            "recommended_tier": recommended_tier,
            "cost_estimate": cost_estimate,
            "data_size_gb": data_size_gb,
            "alternative_tiers": self._get_alternative_tiers(recommended_tier, data_size_gb)
        }

    def _get_alternative_tiers(self, recommended_tier: str, data_size_gb: float) -> List[Dict[str, Any]]:
        """Get alternative tier options"""
        alternatives = []

        for tier_name, tier_info in self.TIERS.items():
            if tier_name != recommended_tier and data_size_gb <= tier_info["data_limit_gb"]:
                try:
                    alt_cost = self.calculate_premium_cost(tier_name, data_size_gb, perpetual_storage=True, apex_certification=True)
                    alternatives.append({
                        "tier": tier_name,
                        "name": tier_info["name"],
                        "price": alt_cost["total_cost"],
                        "savings_vs_recommended": self.TIERS[recommended_tier]["price"] - alt_cost["total_cost"]
                    })
                except:
                    continue

        return sorted(alternatives, key=lambda x: x["price"])

    def record_subscription(self, user_id: str, tier: str, transaction_id: str) -> str:
        """
        Record a tier subscription

        Args:
            user_id: User identifier
            tier: Subscribed tier
            transaction_id: Payment transaction ID

        Returns:
            Subscription ID
        """
        subscription_id = f"sub_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{user_id}"

        subscription = {
            "subscription_id": subscription_id,
            "user_id": user_id,
            "tier": tier,
            "transaction_id": transaction_id,
            "started_at": datetime.utcnow().isoformat(),
            "status": "active",
            "data_used_gb": 0,
            "data_limit_gb": self.TIERS[tier]["data_limit_gb"]
        }

        self.pricing_db["tier_subscriptions"][subscription_id] = subscription

        # Update user subscriptions
        if user_id not in self.pricing_db["users"]:
            self.pricing_db["users"][user_id] = {"subscriptions": []}

        self.pricing_db["users"][user_id]["subscriptions"].append(subscription_id)
        self._save_pricing_db()

        return subscription_id

    def check_user_limits(self, user_id: str, requested_gb: float) -> Dict[str, Any]:
        """
        Check if user has sufficient tier limits for requested data size

        Args:
            user_id: User identifier
            requested_gb: Requested data size in GB

        Returns:
            Limit check results
        """
        user_subs = self.pricing_db["users"].get(user_id, {}).get("subscriptions", [])

        if not user_subs:
            return {
                "has_subscription": False,
                "can_process": False,
                "message": "No active subscription found",
                "upgrade_required": True
            }

        # Get active subscription (most recent)
        active_sub = None
        for sub_id in reversed(user_subs):
            sub = self.pricing_db["tier_subscriptions"].get(sub_id)
            if sub and sub["status"] == "active":
                active_sub = sub
                break

        if not active_sub:
            return {
                "has_subscription": False,
                "can_process": False,
                "message": "No active subscription found",
                "upgrade_required": True
            }

        tier_info = self.TIERS[active_sub["tier"]]
        remaining_gb = tier_info["data_limit_gb"] - active_sub["data_used_gb"]

        return {
            "has_subscription": True,
            "tier": active_sub["tier"],
            "tier_name": tier_info["name"],
            "data_limit_gb": tier_info["data_limit_gb"],
            "data_used_gb": active_sub["data_used_gb"],
            "remaining_gb": remaining_gb,
            "can_process": remaining_gb >= requested_gb,
            "upgrade_required": remaining_gb < requested_gb,
            "message": f"Remaining capacity: {remaining_gb:.1f}GB of {tier_info['data_limit_gb']}GB"
        }

# Global instance
premium_pricing_service = GOATPremiumPricingService()
    """
    GOAT pricing calculator and billing service.
    Handles all pricing logic for the pay-per-GB model.
    """

    # GOAT Pricing Constants
    BASE_PRICE = 19.99  # First GB processing
    PER_GB_PRICE = 5.00  # Additional GB cost
    PERMANENT_STORAGE_PRICE = 9.99  # Flat rate for IPFS/Arweave
    OUTPUT_FORMAT_PRICE = 4.99  # Per additional output format

    def __init__(self, pricing_db_path: str = "./data/pricing.db"):
        """
        Initialize pricing service

        Args:
            pricing_db_path: Path to pricing database (JSON for simplicity)
        """
        self.pricing_db_path = Path(pricing_db_path)
        self.pricing_db_path.parent.mkdir(parents=True, exist_ok=True)

        # Load or create pricing database
        self._load_pricing_db()

    def _load_pricing_db(self):
        """Load pricing database or create if doesn't exist"""
        if self.pricing_db_path.exists():
            with open(self.pricing_db_path, 'r') as f:
                self.pricing_db = json.load(f)
        else:
            self.pricing_db = {
                "users": {},
                "transactions": [],
                "last_updated": datetime.utcnow().isoformat()
            }
            self._save_pricing_db()

    def _save_pricing_db(self):
        """Save pricing database"""
        with open(self.pricing_db_path, 'w') as f:
            json.dump(self.pricing_db, f, indent=2, default=str)

    def calculate_processing_cost(self, data_size_gb: float, output_formats: int = 1) -> Dict[str, Any]:
        """
        Calculate processing cost for legacy building

        Args:
            data_size_gb: Size of data in GB
            output_formats: Number of output formats (1 = base, additional = $4.99 each)

        Returns:
            Dict with cost breakdown
        """
        # Base processing cost
        if data_size_gb <= 1.0:
            processing_cost = self.BASE_PRICE
            data_cost_breakdown = f"1GB base: ${self.BASE_PRICE}"
        else:
            base_cost = self.BASE_PRICE
            additional_gb = data_size_gb - 1.0
            additional_cost = additional_gb * self.PER_GB_PRICE
            processing_cost = base_cost + additional_cost
            data_cost_breakdown = f"1GB base: ${self.BASE_PRICE} + {additional_gb:.1f}GB × ${self.PER_GB_PRICE}: ${additional_cost:.2f}"

        # Output format costs
        format_cost = 0
        if output_formats > 1:
            format_cost = (output_formats - 1) * self.OUTPUT_FORMAT_PRICE
            format_breakdown = f"{output_formats - 1} additional formats: ${format_cost:.2f}"
        else:
            format_breakdown = "1 format included"

        total_cost = processing_cost + format_cost

        return {
            "data_size_gb": data_size_gb,
            "processing_cost": processing_cost,
            "format_cost": format_cost,
            "total_cost": total_cost,
            "breakdown": {
                "data_processing": data_cost_breakdown,
                "output_formats": format_breakdown
            },
            "pricing_model": "goat_pay_per_gb",
            "timestamp": datetime.utcnow().isoformat()
        }

    def calculate_storage_cost(self, permanent_storage: bool = False) -> Dict[str, Any]:
        """
        Calculate permanent storage cost

        Args:
            permanent_storage: Whether to include permanent storage

        Returns:
            Storage cost breakdown
        """
        if permanent_storage:
            return {
                "storage_cost": self.PERMANENT_STORAGE_PRICE,
                "storage_type": "permanent_ipfs_arweave",
                "includes_gas_fees": True,
                "description": "Permanent storage on IPFS + Arweave (gas fees included)"
            }
        else:
            return {
                "storage_cost": 0,
                "storage_type": "temporary",
                "description": "Temporary storage (download only)"
            }

    def calculate_total_cost(self,
                           data_size_gb: float,
                           output_formats: int = 1,
                           permanent_storage: bool = False) -> Dict[str, Any]:
        """
        Calculate total cost for complete legacy creation

        Args:
            data_size_gb: Data size in GB
            output_formats: Number of output formats
            permanent_storage: Include permanent storage

        Returns:
            Complete cost breakdown
        """
        processing = self.calculate_processing_cost(data_size_gb, output_formats)
        storage = self.calculate_storage_cost(permanent_storage)

        total_cost = processing["total_cost"] + storage["storage_cost"]

        return {
            "processing": processing,
            "storage": storage,
            "total_cost": total_cost,
            "cost_summary": {
                "data_processing": f"${processing['processing_cost']:.2f}",
                "output_formats": f"${processing['format_cost']:.2f}",
                "permanent_storage": f"${storage['storage_cost']:.2f}",
                "total": f"${total_cost:.2f}"
            },
            "user_facing_message": self._generate_user_message(processing, storage, total_cost)
        }

    def _generate_user_message(self, processing: Dict, storage: Dict, total: float) -> str:
        """Generate user-friendly cost message"""
        msg = f"Total cost: ${total:.2f}"

        if processing["data_size_gb"] > 1:
            msg += f" (includes ${processing['processing_cost']:.2f} for {processing['data_size_gb']:.1f}GB processing)"
        else:
            msg += f" (includes ${processing['processing_cost']:.2f} for up to 1GB)"

        if processing["format_cost"] > 0:
            msg += f" + ${processing['format_cost']:.2f} for additional formats"

        if storage["storage_cost"] > 0:
            msg += f" + ${storage['storage_cost']:.2f} for permanent storage"

        return msg

    def record_transaction(self,
                          user_id: str,
                          cost_details: Dict[str, Any],
                          transaction_type: str = "legacy_creation") -> str:
        """
        Record a pricing transaction

        Args:
            user_id: User identifier
            cost_details: Cost breakdown from calculate_total_cost
            transaction_type: Type of transaction

        Returns:
            Transaction ID
        """
        transaction_id = f"txn_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{user_id}"

        transaction = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "type": transaction_type,
            "cost_details": cost_details,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending"  # Could be 'completed', 'failed', etc.
        }

        self.pricing_db["transactions"].append(transaction)

        # Update user transaction history
        if user_id not in self.pricing_db["users"]:
            self.pricing_db["users"][user_id] = {"transactions": []}

        self.pricing_db["users"][user_id]["transactions"].append(transaction_id)
        self._save_pricing_db()

        return transaction_id

    def get_user_cost_history(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get user's cost history

        Args:
            user_id: User identifier
            days: Number of days to look back

        Returns:
            Cost history summary
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        user_transactions = []
        total_spent = 0

        for txn in self.pricing_db["transactions"]:
            if txn["user_id"] == user_id:
                txn_date = datetime.fromisoformat(txn["timestamp"])
                if txn_date >= cutoff_date:
                    user_transactions.append(txn)
                    total_spent += txn["cost_details"]["total_cost"]

        return {
            "user_id": user_id,
            "period_days": days,
            "total_spent": total_spent,
            "transaction_count": len(user_transactions),
            "transactions": user_transactions[-10:],  # Last 10 transactions
            "average_cost": total_spent / len(user_transactions) if user_transactions else 0
        }

    def estimate_cost_realtime(self, current_bytes: int, estimated_total_bytes: int) -> Dict[str, Any]:
        """
        Provide real-time cost estimation during upload/processing

        Args:
            current_bytes: Bytes processed so far
            estimated_total_bytes: Estimated total bytes

        Returns:
            Real-time cost estimate
        """
        current_gb = current_bytes / (1024 ** 3)
        estimated_gb = estimated_total_bytes / (1024 ** 3)

        current_cost = self.calculate_processing_cost(current_gb)["processing_cost"]
        estimated_cost = self.calculate_processing_cost(estimated_gb)["processing_cost"]

        progress_percent = (current_bytes / estimated_total_bytes) * 100 if estimated_total_bytes > 0 else 0

        return {
            "current_size_gb": current_gb,
            "estimated_total_gb": estimated_gb,
            "progress_percent": progress_percent,
            "current_cost": current_cost,
            "estimated_final_cost": estimated_cost,
            "cost_so_far": f"${current_cost:.2f}",
            "estimated_total": f"${estimated_cost:.2f}",
            "message": f"Processing {current_gb:.1f}GB of ~{estimated_gb:.1f}GB - Cost so far: ${current_cost:.2f}"
        }

# Global instance
pricing_service = GOATPricingService()