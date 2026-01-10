"""
Podcast Maker Worker - SKG E-commerce System for Audio Content
Same architecture as Booklet Maker, adapted for podcast creation
"""

from pathlib import Path
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

sys.path.append(str(Path(__file__).resolve().parents[2]))
from workers._templates.worker_skg_template import WorkerSKG

class PodcastMakerWorker(WorkerSKG):
    """Handles podcast creation from script upload through audio delivery"""

    def __init__(self, ucm_connector):
        super().__init__(
            worker_id="worker_podcast_v1",
            job_name="podcast_maker",
            ucm_connector=ucm_connector
        )
        self.payment_gateway = PaymentGateway()
        self.order_manager = PodcastOrderManager()

    def _generate_response(self, user_input: str, sections: List[Dict], context: Dict) -> Optional[str]:
        """
        Workflow: Upload content → Select passes → Review → Pay → Process → Deliver
        """
        user_id = context.get("user_id")
        current_step = context.get("current_step", 1)

        if not user_id:
            return "Error: User not authenticated. Please sign in first."

        order_id = context.get("order_id") or f"podcast_{uuid.uuid4().hex[:12]}"
        context["order_id"] = order_id  # Store in context for future calls
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
        """Step 1: Accept content (script or audio)"""

        try:
            content_info = json.loads(user_input) if isinstance(user_input, str) else user_input
        except:
            return self._get_upload_instructions()

        if not content_info.get("filename") or not content_info.get("size"):
            return self._get_upload_instructions()

        # Validate file size (max 500MB for audio)
        if content_info["size"] > 500 * 1024 * 1024:
            return "**File too large.** Maximum size is 500MB. Please compress your file."

        # Validate file type
        valid_types = [".pdf", ".docx", ".txt", ".md", ".mp3", ".wav", ".m4a"]
        file_ext = Path(content_info["filename"]).suffix.lower()
        if file_ext not in valid_types:
            return f"**Unsupported file type.** Please upload: PDF, DOCX, TXT, Markdown, MP3, WAV, or M4A files."

        # Determine content type
        is_audio = file_ext in [".mp3", ".wav", ".m4a"]
        content_type = "audio" if is_audio else "script"

        order["content_file"] = {
            "filename": content_info["filename"],
            "size": content_info["size"],
            "content_type": content_type,
            "uploaded_at": datetime.utcnow().isoformat(),
            "status": "uploaded"
        }

        # Estimate duration or word count
        if is_audio:
            estimated_duration = self._estimate_audio_duration(content_info["size"], file_ext)
            order["metadata"] = {"estimated_duration_minutes": estimated_duration}
        else:
            estimated_words = self._estimate_word_count(content_info["size"], file_ext)
            order["metadata"] = {"estimated_words": estimated_words, "estimated_duration_minutes": estimated_words / 150}  # 150 wpm speaking rate

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

        response = f"✓ **{content_type.title()} uploaded:** {content_info['filename']}\n\n"

        if is_audio:
            response += f"**Estimated duration:** ~{order['metadata']['estimated_duration_minutes']:.1f} minutes\n\n"
        else:
            response += f"**Estimated script length:** ~{order['metadata']['estimated_words']} words "
            response += f"(~{order['metadata']['estimated_duration_minutes']:.1f} minutes spoken)\n\n"

        response += "**Your cart has been initialized with Foundation Pass ($54.88).**\n\n"
        response += "Would you like to add enhancement passes? Type 'yes' to see options or 'proceed' to review cart."

        return response

    def _estimate_audio_duration(self, file_size: int, file_ext: str) -> float:
        """Estimate audio duration in minutes based on file size"""
        # Bitrate estimates: MP3 128kbps ~ 1MB/min, WAV ~ 10MB/min
        mb_per_minute = 10.0 if file_ext == ".wav" else 1.0

        mb = file_size / (1024 * 1024)
        return mb / mb_per_minute

    def _estimate_word_count(self, file_size: int, file_ext: str) -> int:
        """Estimate word count from text file size"""
        # Average: 1 word ≈ 6 bytes + space
        bytes_per_word = 6

        return int(file_size / bytes_per_word)

    def _get_upload_instructions(self) -> str:
        return """
**Upload your podcast content**

Supported formats:
- **Script:** PDF, DOCX, TXT, Markdown
- **Audio:** MP3, WAV, M4A

**Maximum size:** 500MB

**What to upload:**
- Podcast script or transcript
- Existing audio to enhance
- Show notes or outline
- Interview recordings

Provide file information as JSON:
```json
{
  "filename": "episode_script.docx",
  "size": 15360
}
```

Or use the file upload button.
"""

    def _handle_pass_selection(self, user_input: str, order: Dict, context: Dict) -> str:
        """Step 2: Select enhancement passes"""
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

        response = "## Available Enhancement Passes\n\n"
        response += f"**Current total:** ${order['cart']['total'] / 100:.2f}\n\n"

        for pass_id, pass_def in all_passes.items():
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
        response += "**Commands:**\n"
        response += "- 'add [pass_name]' - Add pass to cart\n"
        response += "- 'remove [pass_name]' - Remove from cart\n"
        response += "- 'review' - See cart and total\n"
        response += "- 'help' - Get pass recommendations\n"

        return response

    def _add_pass_to_cart(self, pass_id: str, order: Dict) -> str:
        all_passes = self._get_all_passes()

        if pass_id not in all_passes:
            return f"**Invalid pass:** '{pass_id}'. Type 'show options' to see available passes."

        if pass_id == "foundation":
            return "Foundation Pass is already included (required)."

        cart_items = {item["pass_id"] for item in order["cart"]["items"]}
        if pass_id in cart_items:
            return f"**{all_passes[pass_id]['name']}** is already in your cart."

        # Calculate dynamic price based on content
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
        if pass_id == "foundation":
            return "**Cannot remove Foundation Pass** - Required for all podcast orders."

        original_count = len(order["cart"]["items"])
        order["cart"]["items"] = [item for item in order["cart"]["items"] if item["pass_id"] != pass_id]

        if len(order["cart"]["items"]) == original_count:
            return f"**{pass_id}** was not in your cart."

        self._recalculate_cart_total(order)
        self.order_manager.save_order(order["user_id"], order["order_id"], order)

        return f"✓ Removed pass. New total: **${order['cart']['total'] / 100:.2f}**"

    def _calculate_dynamic_price(self, pass_def: Dict, metadata: Dict) -> int:
        """Calculate price based on content size/duration"""
        base_price = pass_def["price_min"]

        # Factor 1: Duration/episodes
        duration = metadata.get("estimated_duration_minutes", 30)
        episode_factor = max(1, duration / 30)  # 30-minute baseline

        # Factor 2: Pass-specific adjustments
        if pass_def["pass_id"] == "structure":
            if duration > 60:
                return int(pass_def["price_max"])
            elif duration > 30:
                return int((pass_def["price_min"] + pass_def["price_max"]) / 2)
            return base_price

        elif pass_def["pass_id"] == "voice":
            # Voice Pass scales directly with duration
            price_range = pass_def["price_max"] - pass_def["price_min"]
            return int(pass_def["price_min"] + (price_range * (min(episode_factor, 3) / 3)))

        elif pass_def["pass_id"] == "audio_finish":
            # Audio Finish scales with complexity
            if metadata.get("content_type") == "audio":
                # Already has audio, just needs finishing
                return base_price
            else:
                # Needs full audio production from script
                return int(pass_def["price_max"])

        elif pass_def["pass_id"] == "production":
            # Production Pass is relatively fixed
            return base_price

        return base_price

    def _recalculate_cart_total(self, order: Dict):
        subtotal = sum(item["price"] for item in order["cart"]["items"])

        # No tax for simplicity
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

        if user_response in ['modify', 'change', 'edit']:
            context["current_step"] = 2
            return self._display_pass_options(order)

        if user_response in ['pay', 'checkout', 'proceed']:
            context["current_step"] = 4
            return self._handle_payment("", order, context)

        return self._display_cart_review(order)

    def _display_cart_review(self, order: Dict) -> str:
        response = "## Podcast Order Review\n\n"

        if order["content_file"]:
            content_type = order["content_file"]["content_type"]
            response += f"**Content Type:** {content_type.title()}\n"

            if content_type == "audio":
                response += f"**Duration:** ~{order['metadata']['estimated_duration_minutes']:.1f} minutes\n\n"
            else:
                response += f"**Script Length:** ~{order['metadata']['estimated_words']} words "
                response += f"(~{order['metadata']['estimated_duration_minutes']:.1f} min spoken)\n\n"

        response += "### Selected Passes:\n\n"

        for item in order["cart"]["items"]:
            required_str = " (Required)" if item["required"] else ""
            response += f"- **{item['name']}** - ${item['price'] / 100:.2f}{required_str}\n"

        response += "\n---\n\n"
        response += f"**Subtotal:** ${order['cart']['subtotal'] / 100:.2f}\n"
        response += f"**Total:** **${order['cart']['total'] / 100:.2f}**\n\n"

        response += "---\n\n"
        response += "**Next Steps:**\n"
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
            description=f"GOAT Podcast Order {order['order_id']}",
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
            response += f"**Payment ID:** {payment_result['payment_intent_id']}\n\n"
            response += "Complete payment via secure form. Type 'confirm payment' when done."

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

            return f"❌ **Payment failed:** {order['payment_error']}"

    def _handle_processing(self, user_input: str, order: Dict, context: Dict) -> str:
        if user_input.lower().strip() == "status":
            return self._get_processing_status(order)

        if user_input.lower().strip() == "download":
            return self._get_download_instructions(order)

        if order["processing_status"] == "not_started":
            order["processing_status"] = "in_progress"
            order["processing_started_at"] = datetime.utcnow().isoformat()
            self.order_manager.save_order(order["user_id"], order["order_id"], order)

            response = "✅ **Payment confirmed!**\n\n"
            response += "### Starting Podcast Production\n\n"

            passes = [item["pass_id"] for item in order["cart"]["items"]]
            response += f"**Selected passes:** {', '.join(passes)}\n\n"
            response += "Processing steps:\n\n"

            for pass_id in passes:
                pass_def = self._get_pass_definition(pass_id)
                response += f"1. **{pass_def['name']}** - {pass_def['description']}\n"

            response += "\n⏳ **Processing in progress...**\n\n"
            response += "You'll receive a notification when episodes are ready.\n\n"
            response += "Type 'status' to check progress."

            self._start_processing_workflow(order)

            return response

        elif order["processing_status"] == "in_progress":
            return self._get_processing_status(order)

        elif order["processing_status"] == "completed":
            return self._get_download_instructions(order)

        return "Unknown status. Contact support."

    def _start_processing_workflow(self, order: Dict):
        """Background processing of podcast episodes"""
        import threading
        import time

        def process_podcast():
            time.sleep(8)  # Simulate longer audio processing

            order["processing_status"] = "completed"
            order["processing_completed_at"] = datetime.utcnow().isoformat()
            order["outputs"] = {
                "foundation_outline": f"{order['order_id']}_outline.json",
                "episode_audio": f"{order['order_id']}_episode.mp3",
                "show_notes": f"{order['order_id']}_shownotes.md",
                "metadata_json": f"{order['order_id']}_metadata.json",
                "rss_feed": f"{order['order_id']}_rss.xml"
            }

            self.order_manager.save_order(order["user_id"], order["order_id"], order)

        thread = threading.Thread(target=process_podcast)
        thread.daemon = True
        thread.start()

    def _get_processing_status(self, order: Dict) -> str:
        return "⏳ **Processing your podcast...** Audio generation and post-production in progress."

    def _get_download_instructions(self, order: Dict) -> str:
        response = "✅ **Processing Complete!**\n\n"
        response += "### Your podcast is ready:\n\n"

        for output_key, filename in order.get("outputs", {}).items():
            response += f"- [{filename}](/download/{order['order_id']}/{output_key})\n"

        response += "\n---\n\n"
        response += "### Deliverables Include:\n"
        response += "- **Episode audio** (MP3, ready to upload)\n"
        response += "- **Show notes** (Markdown format)\n"
        response += "- **Metadata** (Episode title, description, tags)\n"
        response += "- **RSS feed XML** (For your podcast platform)\n"
        response += "- **Foundation outline** (Content structure)\n\n"

        response += "### Next Steps:\n"
        response += "1. Review your episode audio\n"
        response += "2. Upload to your podcast hosting platform\n"
        response += "3. GOAT does not publish - you maintain full control\n\n"

        response += "Need help choosing a host? Type 'help hosting' for recommendations."

        return response

    def _get_pass_definition(self, pass_id: str) -> Dict:
        for pass_def in self.script_data["script"]:
            if pass_def["pass_id"] == pass_id:
                return pass_def
        return {}

    def _get_all_passes(self) -> Dict[str, Dict]:
        """Get all pass definitions as dictionary"""
        return {pass_def["pass_id"]: pass_def for pass_def in self.script_data["script"]}


class PodcastOrderManager:
    """Manages podcast order persistence"""

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
        return self.orders_base_dir / user_id / "podcast_orders" / order_id / "order.json"


# Reuse payment gateway from booklet maker
class PaymentGateway:
    def create_payment_intent(self, amount: int, currency: str, description: str, metadata: Dict) -> Dict:
        return {
            "status": "succeeded",
            "payment_intent_id": f"pi_{uuid.uuid4().hex[:24]}",
            "client_secret": f"cs_{uuid.uuid4().hex[:24]}"
        }


# UCM Connector stub
class UCMConnector:
    def submit_for_review(self, payload: Dict[str, Any]):
        print(f"[UCM] {payload['data_type']} from {payload['worker_id']}")
        return {"status": "submitted"}