"""
Audiobook Maker Worker - SKG E-commerce System for Audiobook Production
Follows identical pattern to Booklet & Podcast Makers
"""

from pathlib import Path
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

sys.path.append(str(Path(__file__).resolve().parents[2]))
from workers._templates.worker_skg_template import WorkerSKG

class AudiobookMakerWorker(WorkerSKG):
    """Handles audiobook creation from manuscript upload through narration delivery"""

    def __init__(self, ucm_connector):
        super().__init__(
            worker_id="worker_audiobook_v1",
            job_name="audiobook_maker",
            ucm_connector=ucm_connector
        )
        self.payment_gateway = PaymentGateway()
        self.order_manager = AudiobookOrderManager()

    def _generate_response(self, user_input: str, sections: List[Dict], context: Dict) -> Optional[str]:
        user_id = context.get("user_id")
        current_step = context.get("current_step", 1)

        if not user_id:
            return "Error: User not authenticated. Please sign in first."

        order_id = context.get("order_id") or f"audiobook_{uuid.uuid4().hex[:12]}"
        context["order_id"] = order_id  # Ensure order_id is persisted in context
        order = self.order_manager.load_order(user_id, order_id)

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
        try:
            content_info = json.loads(user_input) if isinstance(user_input, str) else user_input
        except:
            return self._get_upload_instructions()

        if not content_info.get("filename") or not content_info.get("size"):
            return self._get_upload_instructions()

        # Validate file size (max 200MB for manuscripts)
        if content_info["size"] > 200 * 1024 * 1024:
            return "**File too large.** Maximum size is 200MB. Please compress or split your manuscript."

        # Validate file type
        valid_types = [".pdf", ".docx", ".txt", ".md"]
        file_ext = Path(content_info["filename"]).suffix.lower()
        if file_ext not in valid_types:
            return f"**Unsupported file type.** Please upload: PDF, DOCX, TXT, or Markdown files."

        order["content_file"] = {
            "filename": content_info["filename"],
            "size": content_info["size"],
            "uploaded_at": datetime.utcnow().isoformat(),
            "status": "uploaded"
        }

        # Estimate content metrics
        estimated_words = self._estimate_word_count(content_info["size"], file_ext)
        estimated_chapters = max(1, estimated_words // 5000)  # Assume 5000 words/chapter
        estimated_duration_hours = estimated_words / 9000  # ~9,000 words/hour spoken

        order["metadata"] = {
            "estimated_words": estimated_words,
            "estimated_chapters": estimated_chapters,
            "estimated_duration_hours": estimated_duration_hours,
            "estimated_duration_minutes": estimated_duration_hours * 60
        }

        # Initialize cart with Foundation Pass
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
            "tax": 0,
            "total": foundation_pass["base_price"]
        }

        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        response = f"✓ **Manuscript uploaded:** {content_info['filename']}\n\n"
        response += f"**Estimated length:** {estimated_words:,} words, {estimated_chapters} chapters "
        response += f"(~{estimated_duration_hours:.1f} hours narration)\n\n"
        response += "**Your cart has been initialized with Foundation Pass ($59.88).**\n\n"
        response += "Includes: watermarked narration sample, chapter segmentation, pacing guidance.\n\n"
        response += "Would you like to add optional enhancement passes? Type 'yes' to see options or 'proceed' to review."

        return response

    def _estimate_word_count(self, file_size: int, file_ext: str) -> int:
        """Estimate word count from manuscript file size"""
        if file_ext == ".pdf":
            bytes_per_word = 8  # PDFs have overhead
        elif file_ext == ".docx":
            bytes_per_word = 7
        else:  # txt, md
            bytes_per_word = 6

        return int(file_size / bytes_per_word)

    def _get_upload_instructions(self) -> str:
        return """
**Upload your audiobook manuscript**

Supported formats:
- PDF (.pdf)
- Microsoft Word (.docx)
- Plain text (.txt)
- Markdown (.md)

**Maximum size:** 200MB

**What to upload:**
- Complete book manuscript
- Chaptered content
- Any written work ready for narration

Provide file information as JSON:
```json
{
  "filename": "my_book.docx",
  "size": 1048576
}
```

Or drag and drop your manuscript file.
"""

    def _handle_pass_selection(self, user_input: str, order: Dict, context: Dict) -> str:
        user_response = user_input.lower().strip()

        if user_response in ['yes', 'show', 'options']:
            return self._display_pass_options(order)

        if user_response in ['proceed', 'continue', 'next', 'review']:
            context["current_step"] = 3
            return self._handle_cart_review("", order, context)

        if user_response.startswith('add '):
            pass_id = user_response.replace('add ', '').strip()
            return self._add_pass_to_cart(pass_id, order)

        if user_response.startswith('remove ') or user_response.startswith('no '):
            pass_id = user_response.replace('remove ', '').replace('no ', '').strip()
            return self._remove_pass_from_cart(pass_id, order)

        return self._display_pass_options(order)

    def _display_pass_options(self, order: Dict) -> str:
        all_passes = self._get_all_passes()
        cart_items = {item["pass_id"]: item for item in order["cart"]["items"]}

        response = "## Audiobook Enhancement Passes\n\n"
        response += f"**Manuscript:** ~{order['metadata']['estimated_words']:,} words, "
        response += f"{order['metadata']['estimated_chapters']} chapters\n\n"
        response += f"**Current total:** ${order['cart']['total'] / 100:.2f}\n\n"

        for pass_id, pass_def in all_passes.items():
            if pass_id == "foundation":
                continue

            is_selected = pass_id in cart_items
            price_range = f"${pass_def['price_min']}-{pass_def['price_max']}" if pass_def["price_min"] != pass_def["price_max"] else f"${pass_def['price_min']}"

            response += f"### {pass_def['name']} - {price_range}\n"
            response += f"{pass_def['description']}\n\n"

            if is_selected:
                response += f"✓ **SELECTED** - Type 'remove {pass_id}' to remove\n\n"
            else:
                response += f"Type 'add {pass_id}' to include this pass\n\n"

        response += "---\n\n"
        response += "**Commands:**\n"
        response += "- 'add [pass_name]' - Add pass to cart\n"
        response += "- 'remove [pass_name]' - Remove from cart\n"
        response += "- 'review' - See cart and total\n"
        response += "- 'recommend' - Get pass recommendations for your manuscript\n"

        return response

    def _add_pass_to_cart(self, pass_id: str, order: Dict) -> str:
        # Prevent modification after payment
        if order.get("payment_status") == "completed":
            return "This order is locked after payment. Create a new order to make changes."

        all_passes = self._get_all_passes()

        if pass_id not in all_passes:
            return f"**Invalid pass:** '{pass_id}'. Type 'show options' to see available passes."

        if pass_id == "foundation":
            return "Foundation Pass is already included (required)."

        cart_items = {item["pass_id"] for item in order["cart"]["items"]}
        if pass_id in cart_items:
            return f"**{all_passes[pass_id]['name']}** is already in your cart."

        # Calculate dynamic price based on manuscript size
        pass_def = all_passes[pass_id]
        dynamic_price = self._calculate_dynamic_price(pass_def, order["metadata"])

        order["cart"]["items"].append({
            "pass_id": pass_id,
            "name": pass_def["name"],
            "description": pass_def["description"],
            "price": dynamic_price,
            "selected": True,
            "required": False
        })

        self._recalculate_cart_total(order)
        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        return f"✓ Added **{pass_def['name']}** (${dynamic_price / 100:.2f}). New total: **${order['cart']['total'] / 100:.2f}**"

    def _remove_pass_from_cart(self, pass_id: str, order: Dict) -> str:
        # Prevent modification after payment
        if order.get("payment_status") == "completed":
            return "This order is locked after payment. Create a new order to make changes."

        if pass_id == "foundation":
            return "**Cannot remove Foundation Pass** - Required for all audiobook orders."

        original_count = len(order["cart"]["items"])
        order["cart"]["items"] = [item for item in order["cart"]["items"] if item["pass_id"] != pass_id]

        if len(order["cart"]["items"]) == original_count:
            return f"**{pass_id}** was not in your cart."

        self._recalculate_cart_total(order)
        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        return f"✓ Removed pass. New total: **${order['cart']['total'] / 100:.2f}**"

    def _calculate_dynamic_price(self, pass_def: Dict, metadata: Dict) -> int:
        """Calculate price based on manuscript size and complexity"""
        base_price = pass_def["price_min"]
        chapters = metadata["estimated_chapters"]
        duration_hours = metadata["estimated_duration_hours"]

        if pass_def["pass_id"] == "audio_flow":
            # Scales with chapters
            if chapters > 20:
                return int(pass_def["price_max"])
            elif chapters > 10:
                return int((pass_def["price_min"] + pass_def["price_max"]) / 2)
            return base_price

        elif pass_def["pass_id"] == "voice":
            # Scales heavily with duration
            # $70-130 per voice, but we simplify to single narrator for now
            duration_factor = min(duration_hours / 5, 3)  # 5-hour baseline
            price_range = pass_def["price_max"] - pass_def["price_min"]
            return int(pass_def["price_min"] + (price_range * duration_factor / 3))

        elif pass_def["pass_id"] == "audio_finish":
            # Scales with duration
            duration_factor = min(duration_hours / 8, 2)  # 8-hour baseline
            price_range = pass_def["price_max"] - pass_def["price_min"]
            return int(pass_def["price_min"] + (price_range * duration_factor / 2))

        elif pass_def["pass_id"] == "production":
            # ACX compliance - relatively fixed
            return base_price

        return base_price

    def _recalculate_cart_total(self, order: Dict):
        subtotal = sum(item["price"] for item in order["cart"]["items"])
        order["cart"]["subtotal"] = subtotal
        order["cart"]["tax"] = 0
        order["cart"]["total"] = subtotal

    def _handle_cart_review(self, user_input: str, order: Dict, context: Dict) -> str:
        user_response = user_input.lower().strip()

        if user_response.startswith('add '):
            pass_id = user_response.replace('add ', '').strip()
            return self._add_pass_to_cart(pass_id, order)

        if user_response.startswith('remove '):
            pass_id = user_response.replace('remove ', '').strip()
            return self._remove_pass_from_cart(pass_id, order)

        if user_response in ['modify', 'change']:
            context["current_step"] = 2
            return self._display_pass_options(order)

        if user_response in ['pay', 'checkout', 'proceed']:
            context["current_step"] = 4
            return self._handle_payment("", order, context)

        return self._display_cart_review(order)

    def _display_cart_review(self, order: Dict) -> str:
        response = "## Audiobook Order Review\n\n"

        if order["content_file"]:
            response += f"**Manuscript:** {order['content_file']['filename']}\n"
            response += f"**Length:** {order['metadata']['estimated_words']:,} words, {order['metadata']['estimated_chapters']} chapters "
            response += f"(~{order['metadata']['estimated_duration_hours']:.1f} hours)\n\n"

        response += "### Selected Passes:\n\n"

        for item in order["cart"]["items"]:
            required_str = " (Required)" if item["required"] else ""
            response += f"- **{item['name']}** - ${item['price'] / 100:.2f}{required_str}\n"
            if item["pass_id"] == "foundation":
                response += "  Includes: watermarked sample, chapter segmentation, pacing guidance\n"

        response += "\n---\n\n"
        response += f"**Subtotal:** ${order['cart']['subtotal'] / 100:.2f}\n"
        response += f"**Total:** **${order['cart']['total'] / 100:.2f}**\n\n"

        response += "---\n\n"
        response += "**Actions:**\n"
        response += "- Type 'pay' to proceed to payment\n"
        response += "- Type 'modify' to change passes\n"
        response += "- Type 'remove [pass_name]' to remove specific pass\n"

        return response

    def _handle_payment(self, user_input: str, order: Dict, context: Dict) -> str:
        if order["payment_status"] == "processing":
            return "⏳ **Payment processing...** Please wait."

        if order["payment_status"] == "completed":
            context["current_step"] = 5
            return self._handle_processing("", order, context)

        if order["payment_status"] == "failed":
            return f"❌ **Payment failed:** {order.get('payment_error', 'Unknown error')}\n\nType 'retry' or 'modify' to adjust order."

        order["payment_status"] = "processing"
        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        payment_result = self.payment_gateway.create_payment_intent(
            amount=order["cart"]["total"],
            currency="usd",
            description=f"GOAT Audiobook Order {order['order_id']}",
            metadata={
                "user_id": order["user_id"],
                "order_id": order["order_id"],
                "passes": json.dumps([item["pass_id"] for item in order["cart"]["items"]])
            }
        )

        if payment_result["status"] == "succeeded":
            order["payment_status"] = "completed"
            order["payment_intent_id"] = payment_result["payment_intent_id"]
            order["paid_at"] = datetime.utcnow().isoformat()
            self.order_manager.save_order(order["user_id"], order["order_id"], order)

            context["current_step"] = 5
            return self._handle_processing("", order, context)

        order["payment_status"] = "failed"
        order["payment_error"] = payment_result.get("error", "Payment system error")
        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        return f"❌ **Payment failed:** {order['payment_error']}"

    def _handle_processing(self, user_input: str, order: Dict, context: Dict) -> str:
        if order["processing_status"] == "not_started":
            order["processing_status"] = "in_progress"
            order["processing_started_at"] = datetime.utcnow().isoformat()
            self.order_manager.save_order(order["user_id"], order["order_id"], order)

            response = "✅ **Payment confirmed!**\n\n"
            response += "### Starting Audiobook Production\n\n"

            passes = [item["pass_id"] for item in order["cart"]["items"]]
            has_voice_pass = "voice" in passes

            response += f"**Selected passes:** {', '.join(passes)}\n\n"
            response += "Processing steps:\n\n"

            for pass_id in passes:
                pass_def = self._get_pass_definition(pass_id)
                response += f"1. **{pass_def['name']}** - {pass_def['description']}\n"

            if has_voice_pass:
                response += f"\n🎧 **Narration will be generated in ~{order['metadata']['estimated_duration_hours']:.1f} hours of audio**\n\n"

            response += "\n⏳ **Processing in progress...**\n\n"
            response += "This may take 10-30 minutes depending on length. Type 'status' to check progress."

            self._start_processing_workflow(order)

            return response

        elif order["processing_status"] == "in_progress":
            return self._get_processing_status(order)

        elif order["processing_status"] == "completed":
            return self._get_download_instructions(order)

        return "Unknown status. Contact support."

    def _start_processing_workflow(self, order: Dict):
        """Background processing of audiobook narration"""
        import threading
        import time

        def process_audiobook():
            # Simulate longer processing for audiobooks
            processing_time = min(30, max(10, order["metadata"]["estimated_duration_hours"] * 2))
            time.sleep(processing_time)

            order["processing_status"] = "completed"
            order["processing_completed_at"] = datetime.utcnow().isoformat()
            order["outputs"] = {
                "foundation_sample": f"{order['order_id']}_sample.mp3",
                "full_narration": f"{order['order_id']}_full.mp3",
                "chapter_files": f"{order['order_id']}_chapters.zip",
                "metadata_acx": f"{order['order_id']}_acx_metadata.json",
                "chapter_markers": f"{order['order_id']}_markers.json",
                "production_checklist": f"{order['order_id']}_production_checklist.txt"
            }

            self.order_manager.save_order(order["user_id"], order["order_id"], order)

        thread = threading.Thread(target=process_audiobook)
        thread.daemon = True
        thread.start()

    def _get_processing_status(self, order: Dict) -> str:
        duration = order["metadata"]["estimated_duration_hours"]
        estimated_minutes = max(10, min(30, duration * 3))

        return f"⏳ **Processing audiobook...** Narration and mastering in progress (est. {estimated_minutes} minutes). Type 'status' to check again."

    def _get_download_instructions(self, order: Dict) -> str:
        response = "✅ **Audiobook Production Complete!**\n\n"
        response += "### Your Files Are Ready:\n\n"

        for output_key, filename in order.get("outputs", {}).items():
            response += f"- [{filename}](/download/{order['order_id']}/{output_key})\n"

        response += "\n---\n\n"
        response += "### Deliverables Include:\n"
        response += "- **Watermarked sample** (Foundation Pass)\n"
        response += "- **Full narration audio** (MP3, chaptered & unchaptered)\n"
        response += "- **ACX metadata** (Ready for Audible/Spotify)\n"
        response += "- **Chapter markers** (JSON format)\n"
        response += "- **Production checklist** (Upload guide)\n\n"

        response += "---\n\n"
        response += "### Next Steps:\n"
        response += "1. Review the watermarked sample first\n"
        response += "2. Submit full audio to ACX (Audible), Spotify, or your platform\n"
        response += "3. Use provided metadata for accurate listing\n"
        response += "4. GOAT does not publish - you retain full control\n\n"
        response += "Need platform recommendations? Type 'help platforms'"

        return response

    def _get_pass_definition(self, pass_id: str) -> Dict:
        for pass_def in self.script_data["script"]:
            if pass_def["pass_id"] == pass_id:
                return pass_def
        return {}

    def _get_all_passes(self) -> Dict[str, Dict]:
        """Get all pass definitions as dictionary"""
        return {pass_def["pass_id"]: pass_def for pass_def in self.script_data["script"]}


class AudiobookOrderManager:
    """Manages audiobook order persistence"""

    def __init__(self):
        self.orders_base_dir = Path(__file__).resolve().parents[2] / "users" / "active"

    def load_order(self, user_id: str, order_id: str) -> Dict:
        order_path = self._get_order_path(user_id, order_id)

        if order_path.exists():
            with open(order_path, 'r') as f:
                return json.load(f)

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
            "processing_status": "not_started",
            "outputs": {}
        }

    def save_order(self, user_id: str, order_id: str, order: Dict):
        order_path = self._get_order_path(user_id, order_id)
        order_path.parent.mkdir(parents=True, exist_ok=True)

        order["last_updated"] = datetime.utcnow().isoformat()

        with open(order_path, 'w') as f:
            json.dump(order, f, indent=2)

    def _get_order_path(self, user_id: str, order_id: str) -> Path:
        return self.orders_base_dir / user_id / "audiobook_orders" / order_id / "order.json"


# Reuse payment gateway and UCM connector from previous workers
class PaymentGateway:
    def create_payment_intent(self, amount: int, currency: str, description: str, metadata: Dict) -> Dict:
        return {
            "status": "succeeded",
            "payment_intent_id": f"pi_{uuid.uuid4().hex[:24]}"
        }

class UCMConnector:
    def submit_for_review(self, payload: Dict[str, Any]):
        print(f"[UCM] {payload['data_type']} from {payload['worker_id']}")
        return {"status": "submitted"}