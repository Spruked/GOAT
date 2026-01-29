"""
Order Manager - Handles order state persistence and management
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from app.core.database import get_db
from app.models.order import Order
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.order import Order

class OrderManager:
    """Manages order state persistence and operations"""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir:
            self.orders_base_dir = Path(base_dir) / "users" / "active"
        else:
            # Default to project root
            self.orders_base_dir = Path(__file__).resolve().parents[1] / "users" / "active"

    async def load_order(self, user_id: str, order_id: str) -> Dict:
        """Load order from database"""
        async with get_db() as session:
            order = await session.get(Order, order_id)
            if order:
                return json.loads(order.data)
            
            # Create new order if not exists
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

    async def save_order(self, user_id: str, order_id: str, order: Dict):
        """Save order to database"""
        order["last_updated"] = datetime.utcnow().isoformat()
        order_json = json.dumps(order)
        
        async with get_db() as session:
            # Check if order exists
            existing = await session.get(Order, order_id)
            if existing:
                existing.data = order_json
                existing.updated_at = func.now()
            else:
                # Determine order type from order_id or data
                order_type = "booklet"  # Default, can be improved
                if "audiobook" in order_id.lower():
                    order_type = "audiobook"
                elif "podcast" in order_id.lower():
                    order_type = "podcast"
                
                new_order = Order(
                    id=order_id,
                    user_id=int(user_id) if user_id.isdigit() else 1,  # Demo user
                    order_type=order_type,
                    data=order_json
                )
                session.add(new_order)
            
            await session.commit()

    async def list_user_orders(self, user_id: str) -> List[Dict]:
        """List all orders for a user from database"""
        async with get_db() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(Order).where(Order.user_id == int(user_id) if user_id.isdigit() else 1)
            )
            orders = result.scalars().all()
            return [json.loads(order.data) for order in orders]

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