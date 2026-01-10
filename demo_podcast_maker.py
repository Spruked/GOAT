#!/usr/bin/env python3
"""
Podcast Maker Demo - Test the complete podcast creation workflow
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from workers.podcast_maker_worker.worker_body import PodcastMakerWorker, UCMConnector

def demo_podcast_maker():
    """Demonstrate the complete podcast maker workflow"""

    print("🎙️  GOAT Podcast Maker Demo")
    print("=" * 50)

    # Initialize worker
    ucm = UCMConnector()
    worker = PodcastMakerWorker(ucm)

    # Simulate user context
    context = {
        "user_id": "demo_user_123",
        "current_step": 1,
        "order_id": None
    }

    print("\n📤 Step 1: Content Upload")
    print("-" * 30)

    # Simulate uploading a script file
    upload_input = json.dumps({
        "filename": "episode_script.docx",
        "size": 25600  # 25KB
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
    print("\nAdding Structure Pass...")
    response = worker._generate_response("add structure", [], context)
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
            "foundation_outline": f"{order_id}_outline.json",
            "episode_audio": f"{order_id}_episode.mp3",
            "show_notes": f"{order_id}_shownotes.md",
            "metadata_json": f"{order_id}_metadata.json",
            "rss_feed": f"{order_id}_rss.xml"
        }
        order_manager.save_order(order["user_id"], order["order_id"], order)

    response = worker._generate_response("download", [], context)
    print(response)

    print("\n🎉 Demo Complete!")
    print("=" * 50)
    print("Podcast Maker workflow successfully demonstrated!")
    print(f"Order ID: {context.get('order_id', 'N/A')}")
    print("Files would be available for download in a real implementation.")

if __name__ == "__main__":
    demo_podcast_maker()