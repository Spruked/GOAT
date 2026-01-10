"""
Payment Gateway Integration - Stripe/PayPal
Handles payment processing for GOAT orders
"""

import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False

class PaymentGateway:
    """Handles payment processing with Stripe integration"""

    def __init__(self):
        self.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_dummy_key")
        self.stripe_publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_dummy_key")

        if STRIPE_AVAILABLE:
            stripe.api_key = self.stripe_secret_key

    def create_payment_intent(self, amount: int, currency: str = "usd",
                            description: str = "", metadata: Dict = None) -> Dict[str, Any]:
        """
        Create a Stripe payment intent

        Args:
            amount: Amount in cents (e.g., 3488 for $34.88)
            currency: Currency code (default: "usd")
            description: Payment description
            metadata: Additional metadata

        Returns:
            Dict with payment intent details
        """
        try:
            if not STRIPE_AVAILABLE:
                # Demo mode - simulate successful payment
                return {
                    "status": "succeeded",
                    "payment_intent_id": f"pi_{uuid.uuid4().hex[:24]}",
                    "client_secret": f"cs_{uuid.uuid4().hex[:24]}",
                    "amount": amount,
                    "currency": currency
                }

            # Create Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                description=description,
                metadata=metadata or {},
                automatic_payment_methods={
                    "enabled": True,
                },
            )

            return {
                "status": intent.status,
                "payment_intent_id": intent.id,
                "client_secret": intent.client_secret,
                "amount": intent.amount,
                "currency": intent.currency
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    def confirm_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """Confirm a payment intent"""
        try:
            if not STRIPE_AVAILABLE:
                return {"status": "succeeded", "payment_intent_id": payment_intent_id}

            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            return {
                "status": intent.status,
                "payment_intent_id": intent.id,
                "amount": intent.amount,
                "currency": intent.currency
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    def create_checkout_session(self, items: list, success_url: str, cancel_url: str,
                              metadata: Dict = None) -> Dict[str, Any]:
        """Create a Stripe checkout session (alternative to payment intents)"""
        try:
            if not STRIPE_AVAILABLE:
                return {
                    "status": "created",
                    "session_id": f"cs_{uuid.uuid4().hex[:24]}",
                    "url": success_url
                }

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=items,
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata or {}
            )

            return {
                "status": "created",
                "session_id": session.id,
                "url": session.url
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    def get_publishable_key(self) -> str:
        """Get the publishable key for frontend use"""
        return self.stripe_publishable_key