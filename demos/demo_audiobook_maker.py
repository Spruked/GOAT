#!/usr/bin/env python3
"""
Audiobook Maker Demo - Test the complete audiobook creation workflow
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from workers.audiobook_maker_worker.worker_body import AudiobookMakerWorker, UCMConnector

def demo_audiobook_maker():
    """Demonstrate the complete audiobook maker workflow"""

    print("🎧  GOAT Audiobook Maker Demo")
    print("=" * 50)

    # Initialize worker
    ucm = UCMConnector()
    worker = AudiobookMakerWorker(ucm_connector=ucm)

    # Simulate user context
    context = {
        "user_id": "demo_user_123",
        "current_step": 1,
        "order_id": None
    }

    print("\n📤 Step 1: Content Upload")
    print("-" * 30)

    # Simulate uploading a manuscript file (60,000 words)
    upload_input = json.dumps({
        "filename": "my_novel.docx",
        "size": 360000  # ~60KB for 60,000 words
    })

    response = worker._generate_response(upload_input, [], context)
    print(response)

    # Update context after upload
    context["current_step"] = 2

    print("\n🎯 Step 2: Pass Selection")
    print("-" * 30)

    # Show available passes
    response = worker._generate_response("show options", [], context)
    print(response)

    # Add some passes
    print("\nAdding Audio Flow Pass...")
    response = worker._generate_response("add audio_flow", [], context)
    print(response)

    print("\nAdding Voice Pass...")
    response = worker._generate_response("add voice", [], context)
    print(response)

    print("\nAdding Audio Finish Pass...")
    response = worker._generate_response("add audio_finish", [], context)
    print(response)

    print("\n💳 Step 3: Cart Review")
    print("-" * 30)

    # Review cart
    context["current_step"] = 3
    response = worker._generate_response("review", [], context)
    print(response)

    print("\n💰 Step 4: Payment Processing")
    print("-" * 30)

    # Proceed to payment
    context["current_step"] = 4
    response = worker._generate_response("pay", [], context)
    print(response)

    print("\n⚙️  Step 5: Processing")
    print("-" * 30)

    # Start processing
    context["current_step"] = 5
    response = worker._generate_response("", [], context)
    print(response)

    print("\n📊 Step 6: Status Check")
    print("-" * 30)

    # Check status
    response = worker._generate_response("status", [], context)
    print(response)

    print("\n✅ Step 7: Delivery")
    print("-" * 30)

    # Simulate completion and get download links
    import time
    print("⏳ Simulating processing time...")
    time.sleep(10)

    # Force completion for demo
    order_id = context.get("order_id")
    if order_id:
        order_manager = worker.order_manager
        order = order_manager.load_order(context["user_id"], order_id)
        order["processing_status"] = "completed"
        order["processing_completed_at"] = datetime.utcnow().isoformat()
        order["outputs"] = {
            "foundation_sample": f"{order_id}_sample.mp3",
            "full_narration": f"{order_id}_full.mp3",
            "chapter_files": f"{order_id}_chapters.zip",
            "metadata_acx": f"{order_id}_acx_metadata.json",
            "chapter_markers": f"{order_id}_markers.json",
            "production_checklist": f"{order_id}_production_checklist.txt"
        }
        order_manager.save_order(order["user_id"], order["order_id"], order)

    response = worker._generate_response("download", [], context)
    print(response)

    print("\n🎉 Demo Complete!")
    print("=" * 50)
    print("Audiobook Maker workflow successfully demonstrated!")
    print(f"Order ID: {context.get('order_id', 'N/A')}")
    print("Files would be available for download in a real implementation.")

if __name__ == "__main__":
    demo_audiobook_maker()