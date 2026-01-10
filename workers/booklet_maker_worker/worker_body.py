"""
Booklet Maker Worker - SKG E-commerce System
Implements cart management, price calculation, payment processing, and order modification
"""

from pathlib import Path
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

sys.path.append(str(Path(__file__).resolve().parents[2]))
from workers._templates.worker_skg_template import WorkerSKG

class BookletMakerWorker(WorkerSKG):
    """Handles booklet creation from content upload through delivery"""

    def __init__(self, ucm_connector):
        super().__init__(
            worker_id="worker_booklet_v1",
            job_name="booklet_maker",
            ucm_connector=ucm_connector
        )
        self.payment_gateway = PaymentGateway()
        self.order_manager = OrderManager()

    def _generate_response(self, user_input: str, sections: List[Dict], context: Dict) -> Optional[str]:
        """
        Main logic for booklet creation workflow:
        1. Upload content → 2. Select passes → 3. Review cart → 4. Pay → 5. Process → 6. Deliver
        """
        user_id = context.get("user_id")
        current_step = context.get("current_step", 1)

        if not user_id:
            return "Error: User not authenticated. Please sign in first."

        # Load existing order or create new one
        order_id = context.get("order_id") or f"booklet_{uuid.uuid4().hex[:12]}"
        context["order_id"] = order_id  # Store in context for future calls
        order = self.order_manager.load_order(user_id, order_id)

        # Step-based workflow
        if current_step == 1:
            return self._handle_content_upload(user_input, order, context)
        elif current_step == 2:
            return self._handle_pass_selection(user_input, order, context)
        elif current_step == 3:
            return self._handle_cart_review(user_input, order, context)
        elif current_step == 4:
            return self._handle_payment(user_input, order, context)
        elif current_step == 5:
            return self._handle_processing(user_input, order, context)
        else:
            return self._get_order_status(order, context)

    def _handle_content_upload(self, user_input: str, order: Dict, context: Dict) -> str:
        """Step 1: Accept content files (PDF, DOCX, TXT, MD)"""

        # If user_input is file metadata JSON
        try:
            file_info = json.loads(user_input) if isinstance(user_input, str) else user_input
        except:
            return self._get_upload_instructions()

        # Validate file
        if not file_info.get("filename") or not file_info.get("size"):
            return self._get_upload_instructions()

        # Check file size (max 100MB for booklets)
        if file_info["size"] > 100 * 1024 * 1024:
            return "**File too large.** Maximum size is 100MB. Please compress or split your content."

        # Check file type
        valid_types = [".pdf", ".docx", ".txt", ".md"]
        file_ext = Path(file_info["filename"]).suffix.lower()
        if file_ext not in valid_types:
            return f"**Unsupported file type.** Please upload: PDF, DOCX, TXT, or Markdown files."

        # Save file info to order
        order["content_file"] = {
            "filename": file_info["filename"],
            "size": file_info["size"],
            "uploaded_at": datetime.utcnow().isoformat(),
            "status": "uploaded"
        }

        # Calculate page estimate
        estimated_pages = self._estimate_pages(file_info["size"], file_ext)
        order["metadata"] = {
            "estimated_pages": estimated_pages,
            "estimated_sheets": estimated_pages / 4  # Booklets print 4 pages per sheet
        }

        # Initialize cart with Foundation Pass (required)
        foundation_pass = self._get_pass_definition("foundation")
        order["cart"] = {
            "items": [
                {
                    "pass_id": "foundation",
                    "name": foundation_pass["name"],
                    "description": foundation_pass["description"],
                    "price": foundation_pass["base_price"],
                    "selected": True,
                    "required": True
                }
            ],
            "subtotal": foundation_pass["base_price"],
            "tax": 0,  # Tax calculated based on location
            "total": foundation_pass["base_price"]
        }

        # Save order
        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        response = f"✓ **File uploaded successfully:** {file_info['filename']}\n\n"
        response += f"**Estimated content:** ~{estimated_pages} pages ({estimated_pages // 4} sheets)\n\n"
        response += f"**Your cart has been initialized with the required Foundation Pass ($34.88).**\n\n"
        response += "Would you like to add optional enhancement passes?\n\n"
        response += "Type 'yes' to see options or 'proceed' to review your cart."

        return response

    def _get_upload_instructions(self) -> str:
        """Return upload instructions"""
        return """
**Please upload your booklet content**

Supported formats:
- PDF (.pdf)
- Microsoft Word (.docx)
- Plain text (.txt)
- Markdown (.md)

**Maximum file size:** 100MB

**What to upload:**
- Manuscripts
- Training materials
- Course content
- Any structured text content

Type or paste your file information as JSON:
```json
{
  "filename": "my_content.pdf",
  "size": 2457600
}
```

Or simply drag and drop your file to the upload area.
"""

    def _estimate_pages(self, file_size: int, file_ext: str) -> int:
        """Estimate page count based on file size and type"""
        # Rough estimates (average pages per MB)
        pages_per_mb = {
            ".pdf": 25,
            ".docx": 30,
            ".txt": 200,
            ".md": 180
        }

        mb = file_size / (1024 * 1024)
        return int(mb * pages_per_mb.get(file_ext, 25))

    def _handle_pass_selection(self, user_input: str, order: Dict, context: Dict) -> str:
        """Step 2: Select optional enhancement passes"""
        user_response = user_input.lower().strip()

        # If user said 'yes' or 'show options'
        if user_response in ['yes', 'show', 'options', 'show options']:
            return self._display_pass_options(order)

        # If user wants to proceed
        if user_response in ['proceed', 'continue', 'next', 'review']:
            context["current_step"] = 3
            return self._handle_cart_review("", order, context)

        # Parse pass selection (e.g., "add layout", "remove typography")
        if user_response.startswith('add '):
            pass_id = user_response.replace('add ', '').strip()
            return self._add_pass_to_cart(pass_id, order)

        if user_response.startswith('remove ') or user_response.startswith('no '):
            pass_id = user_response.replace('remove ', '').replace('no ', '').strip()
            return self._remove_pass_from_cart(pass_id, order)

        # Show current cart
        return self._display_pass_options(order)

    def _display_pass_options(self, order: Dict) -> str:
        """Display all available passes with pricing"""
        all_passes = self._get_all_passes()
        cart_items = {item["pass_id"]: item for item in order["cart"]["items"]}

        response = "## Available Enhancement Passes\n\n"
        response += "**Your content:** Current cart total: **${:.2f}**\n\n".format(order["cart"]["total"] / 100)

        for pass_id, pass_def in all_passes.items():
            # Skip foundation (already in cart, required)
            if pass_id == "foundation":
                continue

            is_selected = pass_id in cart_items
            price_range = f"${pass_def['price_min']/100:.0f}-${pass_def['price_max']/100:.0f}" if pass_def["price_min"] != pass_def["price_max"] else f"${pass_def['price_min']/100:.0f}"

            response += f"### {pass_def['name']} - {price_range}\n"
            response += f"{pass_def['description']}\n\n"

            if is_selected:
                response += f"✓ **SELECTED** - Type 'remove {pass_id}' to remove\n\n"
            else:
                response += f"Type 'add {pass_id}' to include this pass\n\n"

        response += "---\n\n"
        response += "**Next steps:**\n"
        response += "- Type 'add [pass_name]' to add a pass\n"
        response += "- Type 'remove [pass_name]' to remove a pass\n"
        response += "- Type 'review' to see your cart and total\n"
        response += "- Type 'help' for pass recommendations based on your content\n"

        return response

    def _add_pass_to_cart(self, pass_id: str, order: Dict) -> str:
        """Add a pass to the cart"""
        all_passes = self._get_all_passes()

        if pass_id not in all_passes:
            return f"**Invalid pass:** '{pass_id}'. Type 'show options' to see available passes."

        # Can't re-add foundation
        if pass_id == "foundation":
            return "Foundation Pass is already included (required)."

        # Check if already in cart
        cart_items = {item["pass_id"] for item in order["cart"]["items"]}
        if pass_id in cart_items:
            return f"**{all_passes[pass_id]['name']}** is already in your cart."

        # Add to cart
        pass_def = all_passes[pass_id]
        order["cart"]["items"].append({
            "pass_id": pass_id,
            "name": pass_def["name"],
            "description": pass_def["description"],
            "price": pass_def["base_price"],  # Use base price initially
            "selected": True,
            "required": False
        })

        # Recalculate total
        self._recalculate_cart_total(order)

        # Save order
        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        return f"✓ Added **{pass_def['name']}** to cart. New total: **${order['cart']['total'] / 100:.2f}**"

    def _remove_pass_from_cart(self, pass_id: str, order: Dict) -> str:
        """Remove a pass from the cart"""
        if pass_id == "foundation":
            return "**Cannot remove Foundation Pass** - It is required for all booklet orders."

        # Find and remove
        original_count = len(order["cart"]["items"])
        order["cart"]["items"] = [item for item in order["cart"]["items"] if item["pass_id"] != pass_id]

        if len(order["cart"]["items"]) == original_count:
            return f"**{pass_id}** was not in your cart."

        # Recalculate total
        self._recalculate_cart_total(order)

        # Save order
        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        return f"✓ Removed pass from cart. New total: **${order['cart']['total'] / 100:.2f}**"

    def _recalculate_cart_total(self, order: Dict):
        """Recalculate cart subtotal, tax, and total"""
        subtotal = sum(item["price"] for item in order["cart"]["items"])

        # Simple tax calculation (would be based on user location in production)
        tax_rate = 0.0  # For simplicity, no tax

        order["cart"]["subtotal"] = subtotal
        order["cart"]["tax"] = int(subtotal * tax_rate)
        order["cart"]["total"] = subtotal + order["cart"]["tax"]

    def _handle_cart_review(self, user_input: str, order: Dict, context: Dict) -> str:
        """Step 3: Review cart and allow modifications"""
        user_response = user_input.lower().strip()

        # Handle modification commands
        if user_response.startswith('add '):
            pass_id = user_response.replace('add ', '').strip()
            return self._add_pass_to_cart(pass_id, order)

        if user_response.startswith('remove '):
            pass_id = user_response.replace('remove ', '').strip()
            return self._remove_pass_from_cart(pass_id, order)

        if user_response in ['modify', 'change', 'edit']:
            context["current_step"] = 2
            return self._display_pass_options(order)

        if user_response in ['pay', 'checkout', 'proceed', 'confirm']:
            context["current_step"] = 4
            return self._handle_payment("", order, context)

        # Display cart review
        return self._display_cart_review(order)

    def _display_cart_review(self, order: Dict) -> str:
        """Display complete cart for review"""
        response = "## Order Review\n\n"

        if order["content_file"]:
            response += f"**Content:** {order['content_file']['filename']} "
            response += f"({order['metadata']['estimated_pages']} pages)\n\n"

        response += "### Selected Passes:\n\n"

        for item in order["cart"]["items"]:
            required_str = " (Required)" if item["required"] else ""
            response += f"- **{item['name']}** - ${item['price'] / 100:.2f}{required_str}\n"

        response += "\n---\n\n"
        response += f"**Subtotal:** ${order['cart']['subtotal'] / 100:.2f}\n"

        if order["cart"]["tax"] > 0:
            response += f"**Tax:** ${order['cart']['tax'] / 100:.2f}\n"

        response += f"**Total:** **${order['cart']['total'] / 100:.2f}**\n\n"

        response += "---\n\n"
        response += "**What would you like to do?**\n"
        response += "- Type 'pay' to proceed to payment\n"
        response += "- Type 'modify' to add/remove passes\n"
        response += "- Type 'remove [pass_name]' to remove a specific pass\n"
        response += "- Type 'help' for pass recommendations\n"

        return response

    def _handle_payment(self, user_input: str, order: Dict, context: Dict) -> str:
        """Step 4: Process payment"""

        # If payment already attempted, check status
        if order["payment_status"] == "processing":
            return "⏳ **Payment is being processed.** Please wait..."

        if order["payment_status"] == "completed":
            context["current_step"] = 5
            return self._handle_processing("", order, context)

        if order["payment_status"] == "failed":
            return f"❌ **Payment failed:** {order.get('payment_error', 'Unknown error')}\n\nType 'retry' to try again or 'modify' to change your order."

        # Start new payment
        order["payment_status"] = "processing"
        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        # Create payment intent
        payment_result = self.payment_gateway.create_payment_intent(
            amount=order["cart"]["total"],
            currency="usd",
            description=f"GOAT Booklet Order {order['order_id']}",
            metadata={
                "user_id": order["user_id"],
                "order_id": order["order_id"],
                "passes": json.dumps([item["pass_id"] for item in order["cart"]["items"]])
            }
        )

        if payment_result["status"] == "requires_action":
            order["payment_status"] = "pending"
            order["payment_intent_id"] = payment_result["payment_intent_id"]
            order["payment_client_secret"] = payment_result["client_secret"]
            self.order_manager.save_order(order["user_id"], order["order_id"], order)

            response = f"### Payment Required\n\n"
            response += f"**Amount:** ${order['cart']['total'] / 100:.2f}\n\n"
            response += f"**Payment Intent ID:** {payment_result['payment_intent_id']}\n\n"
            response += "Please complete payment using the secure payment form below.\n\n"
            response += "Once payment is complete, type 'confirm payment' to verify and start processing."

            return response

        elif payment_result["status"] == "succeeded":
            order["payment_status"] = "completed"
            order["payment_intent_id"] = payment_result["payment_intent_id"]
            order["paid_at"] = datetime.utcnow().isoformat()
            self.order_manager.save_order(order["user_id"], order["order_id"], order)

            context["current_step"] = 5
            return self._handle_processing("", order, context)

        else:
            order["payment_status"] = "failed"
            order["payment_error"] = payment_result.get("error", "Payment system error")
            self.order_manager.save_order(order["user_id"], order["order_id"], order)

            return f"❌ **Payment failed:** {order['payment_error']}\n\nType 'retry' to try again."

    def _handle_processing(self, user_input: str, order: Dict, context: Dict) -> str:
        """Step 5: Process booklet after payment"""

        # Handle status check
        if user_input.lower().strip() == "status":
            return self._get_processing_status(order)

        if user_input.lower().strip() == "download":
            return self._get_download_instructions(order)

        if order["processing_status"] == "not_started":
            # Start processing
            order["processing_status"] = "in_progress"
            order["processing_started_at"] = datetime.utcnow().isoformat()
            self.order_manager.save_order(order["user_id"], order["order_id"], order)

            response = "✅ **Payment confirmed!**\n\n"
            response += "### Starting Booklet Processing\n\n"

            # Get selected passes
            passes = [item["pass_id"] for item in order["cart"]["items"]]

            response += f"**Processing with passes:** {', '.join(passes)}\n\n"
            response += "The following steps will be completed:\n\n"

            for pass_id in passes:
                pass_def = self._get_pass_definition(pass_id)
                response += f"1. **{pass_def['name']}** - {pass_def['description']}\n"

            response += "\n⏳ **Processing is now in progress.**\n\n"
            response += "You will receive a notification when your booklet is ready.\n\n"
            response += "Type 'status' to check progress or 'download' to retrieve your files when complete."

            # Actually start processing in background
            self._start_processing_workflow(order)

            return response

        elif order["processing_status"] == "in_progress":
            return self._get_processing_status(order)

        elif order["processing_status"] == "completed":
            return self._get_download_instructions(order)

        else:
            return "Unknown processing status. Please contact support."

    def _start_processing_workflow(self, order: Dict):
        """Initiate actual booklet processing (background task)"""

        # In production, this would:
        # 1. Parse content file
        # 2. Apply each pass sequentially
        # 3. Generate PDF/DOCX outputs
        # 4. Upload to storage
        # 5. Update order status

        # For demo, we'll simulate with a delay
        import threading
        import time

        def process_booklet():
            time.sleep(5)  # Simulate processing time

            # Update order to completed
            order["processing_status"] = "completed"
            order["processing_completed_at"] = datetime.utcnow().isoformat()
            order["outputs"] = {
                "foundation_pdf": f"{order['order_id']}_foundation.pdf",
                "final_pdf": f"{order['order_id']}_final.pdf",
                "production_checklist": "production_checklist.json"
            }

            self.order_manager.save_order(order["user_id"], order["order_id"], order)

        thread = threading.Thread(target=process_booklet)
        thread.daemon = True
        thread.start()

    def _get_processing_status(self, order: Dict) -> str:
        """Check processing progress"""
        # In production, query actual processing pipeline
        return "⏳ **Processing in progress...** Your booklet is being prepared. Check back in a few minutes."

    def _get_download_instructions(self, order: Dict) -> str:
        """Provide download links"""
        response = "✅ **Processing Complete!**\n\n"
        response += "### Your booklet is ready for download:\n\n"

        for output_key, filename in order.get("outputs", {}).items():
            response += f"- [{filename}](/download/{order['order_id']}/{output_key})\n"

        response += "\n---\n\n"
        response += "**Production Checklist:**\n"
        response += "Your booklet includes a production_checklist.json file with printer specifications.\n\n"

        response += "### Next Steps:\n"
        response += "1. Review your booklet files\n"
        response += "2. Upload to your preferred printer (Vistaprint, Mixam, Staples, etc.)\n"
        response += "3. Reference the production checklist for print settings\n\n"

        response += "Need help with printing? Type 'help printing' for guidance."

        return response

    def _get_pass_definition(self, pass_id: str) -> Dict:
        """Get pass definition from script data"""
        for pass_def in self.script_data["script"]:
            if pass_def["pass_id"] == pass_id:
                return pass_def
        return {}

    def _get_all_passes(self) -> Dict[str, Dict]:
        """Get all pass definitions as dictionary"""
        return {pass_def["pass_id"]: pass_def for pass_def in self.script_data["script"]}


class PaymentGateway:
    """Stub for payment processing (Stripe/PayPal)"""

    def create_payment_intent(self, amount: int, currency: str, description: str, metadata: Dict) -> Dict:
        """
        Create payment intent
        Returns: { status: "requires_action"|"succeeded", payment_intent_id: str, client_secret: str }
        """
        # In production: integrate with Stripe API

        # Simulate successful payment for demo
        return {
            "status": "succeeded",
            "payment_intent_id": f"pi_{uuid.uuid4().hex[:24]}",
            "client_secret": f"cs_{uuid.uuid4().hex[:24]}"
        }


class OrderManager:
    """Manages order state persistence"""

    def __init__(self):
        self.orders_base_dir = Path(__file__).resolve().parents[2] / "users" / "active"

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
            "cart": {
                "items": [],
                "subtotal": 0,
                "tax": 0,
                "total": 0
            },
            "payment_status": "not_started",
            "payment_intent_id": None,
            "processing_status": "not_started",
            "outputs": {}
        }

    def save_order(self, user_id: str, order_id: str, order: Dict):
        """Save order to disk"""
        order_path = self._get_order_path(user_id, order_id)
        order_path.parent.mkdir(parents=True, exist_ok=True)

        order["last_updated"] = datetime.utcnow().isoformat()

        with open(order_path, 'w') as f:
            json.dump(order, f, indent=2)

    def _get_order_path(self, user_id: str, order_id: str) -> Path:
        """Get order file path"""
        return self.orders_base_dir / user_id / "booklet_orders" / order_id / "order.json"


# Pass definitions loaded from booklet_script.json
def get_pass_definitions():
    """Load pass definitions from script file"""
    script_path = Path(__file__).parent / "booklet_script.json"
    with open(script_path, 'r') as f:
        data = json.load(f)
    return {pass_def["pass_id"]: pass_def for pass_def in data["script"]}