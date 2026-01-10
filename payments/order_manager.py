"""
Order Manager - Handles order state persistence and management
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

class OrderManager:
    """Manages order state persistence and operations"""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir:
            self.orders_base_dir = Path(base_dir) / "users" / "active"
        else:
            # Default to project root
            self.orders_base_dir = Path(__file__).resolve().parents[1] / "users" / "active"

    def load_order(self, user_id: str, order_id: str) -> Dict:
        """Load order from disk or create new one"""
        order_path = self._get_order_path(user_id, order_id)

        if order_path.exists():
            with open(order_path, 'r') as f:
                return json.load(f)

        # Create new order
        return {
            "order_id": order_id,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "status": "draft",
            "content_file": None,
            "metadata": {},
            "cart": {
                "items": [],
                "subtotal": 0,
                "tax": 0,
                "total": 0
            },
            "payment_status": "not_started",
            "payment_intent_id": None,
            "payment_client_secret": None,
            "paid_at": None,
            "processing_status": "not_started",
            "processing_started_at": None,
            "processing_completed_at": None,
            "outputs": {},
            "last_updated": datetime.utcnow().isoformat()
        }

    def save_order(self, user_id: str, order_id: str, order: Dict):
        """Save order to disk"""
        order_path = self._get_order_path(user_id, order_id)
        order_path.parent.mkdir(parents=True, exist_ok=True)

        order["last_updated"] = datetime.utcnow().isoformat()

        with open(order_path, 'w') as f:
            json.dump(order, f, indent=2)

    def list_user_orders(self, user_id: str) -> List[Dict]:
        """List all orders for a user"""
        user_dir = self.orders_base_dir / user_id / "booklet_orders"
        if not user_dir.exists():
            return []

        orders = []
        for order_dir in user_dir.iterdir():
            if order_dir.is_dir():
                order_path = order_dir / "order.json"
                if order_path.exists():
                    with open(order_path, 'r') as f:
                        orders.append(json.load(f))

        return sorted(orders, key=lambda x: x.get("created_at", ""), reverse=True)

    def update_order_status(self, user_id: str, order_id: str, status: str,
                          additional_data: Dict = None):
        """Update order status with optional additional data"""
        order = self.load_order(user_id, order_id)
        order["status"] = status

        if additional_data:
            order.update(additional_data)

        self.save_order(user_id, order_id, order)

    def add_order_note(self, user_id: str, order_id: str, note: str, note_type: str = "info"):
        """Add a note to the order"""
        order = self.load_order(user_id, order_id)

        if "notes" not in order:
            order["notes"] = []

        order["notes"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "type": note_type,
            "note": note
        })

        self.save_order(user_id, order_id, order)

    def calculate_order_total(self, order: Dict) -> Dict:
        """Recalculate order totals"""
        subtotal = sum(item["price"] for item in order["cart"]["items"])

        # Tax calculation (simplified - would be based on user location)
        tax_rate = 0.0  # No tax for demo
        tax = int(subtotal * tax_rate)

        total = subtotal + tax

        order["cart"]["subtotal"] = subtotal
        order["cart"]["tax"] = tax
        order["cart"]["total"] = total

        return order["cart"]

    def validate_order_for_payment(self, order: Dict) -> Dict:
        """Validate order is ready for payment"""
        errors = []

        if not order.get("content_file"):
            errors.append("No content file uploaded")

        if not order["cart"]["items"]:
            errors.append("No items in cart")

        if order["cart"]["total"] <= 0:
            errors.append("Invalid order total")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def get_order_summary(self, order: Dict) -> str:
        """Generate human-readable order summary"""
        summary = f"Order {order['order_id']}\n"
        summary += f"Status: {order['status']}\n"
        summary += f"Created: {order['created_at']}\n"

        if order.get("content_file"):
            summary += f"Content: {order['content_file']['filename']}\n"

        summary += f"Items: {len(order['cart']['items'])}\n"
        summary += f"Total: ${order['cart']['total'] / 100:.2f}\n"

        summary += f"Payment: {order['payment_status']}\n"
        summary += f"Processing: {order['processing_status']}\n"

        return summary

    def archive_order(self, user_id: str, order_id: str):
        """Move order to archive (for cleanup)"""
        order_path = self._get_order_path(user_id, order_id)
        archive_path = self.orders_base_dir / user_id / "archived_orders" / order_id

        if order_path.exists():
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.move(str(order_path.parent), str(archive_path))

    def _get_order_path(self, user_id: str, order_id: str) -> Path:
        """Get order file path"""
        return self.orders_base_dir / user_id / "booklet_orders" / order_id / "order.json"

    def cleanup_old_drafts(self, days_old: int = 30):
        """Clean up old draft orders"""
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days_old)

        # This would iterate through all users and orders
        # For now, just return success
        return {"cleaned": 0, "message": "Cleanup not implemented in demo"}