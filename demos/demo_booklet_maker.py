#!/usr/bin/env python3
"""
Demo script showing Booklet Maker Worker in action
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workers.booklet_maker_worker.worker_body import BookletMakerWorker

def demo_booklet_maker():
    """Demonstrate the booklet maker workflow"""

    print("🎯 GOAT Booklet Maker Demo")
    print("=" * 50)

    # Create worker (without UCM for demo)
    worker = BookletMakerWorker(ucm_connector=None)

    # Simulate user interactions
    user_id = "demo_user_123"
    context = {"user_id": user_id, "current_step": 1}

    interactions = [
        # Step 1: Upload content
        ('{"filename": "training_manual.pdf", "size": 5242880}', "Upload training manual"),

        # Step 2: Add passes
        ("yes", "Show available passes"),
        ("add layout", "Add Layout Pass"),
        ("add typography", "Add Typography Pass"),

        # Step 3: Review cart
        ("review", "Review order"),

        # Step 4: Proceed to payment
        ("pay", "Initiate payment"),

        # Step 5: Check status (simulated completion)
        ("status", "Check processing status"),
    ]

    for user_input, description in interactions:
        print(f"\n👤 {description}: '{user_input}'")
        print("-" * 30)

        try:
            response = worker._generate_response(user_input, [], context)
            print(f"🤖 {response}")

            # Simulate step progression based on response content
            if response and "File uploaded successfully" in response:
                context["current_step"] = 2
            elif response and "Available Enhancement Passes" in response:
                pass  # Stay on step 2
            elif response and "Order Review" in response:
                context["current_step"] = 3
            elif response and ("Payment Required" in response or "Payment confirmed" in response):
                context["current_step"] = 4
            elif response and "Processing is now in progress" in response:
                context["current_step"] = 5
                # Simulate completion for demo
                import time
                print("⏳ Simulating processing...")
                time.sleep(2)
                # Mark as completed
                order_id = context.get("order_id")
                if not order_id:
                    raise ValueError("Order ID not set")
                order = worker.order_manager.load_order(user_id, order_id)
                order["processing_status"] = "completed"
                order["outputs"] = {
                    "foundation_pdf": f"{order['order_id']}_foundation.pdf",
                    "final_pdf": f"{order['order_id']}_final.pdf",
                    "production_checklist": "production_checklist.json"
                }
                worker.order_manager.save_order(user_id, order["order_id"], order)

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("\nKey features demonstrated:")
    print("• Content upload with validation")
    print("• Dynamic cart management")
    print("• Pass selection and pricing")
    print("• Payment processing simulation")
    print("• Order state persistence")
    print("• Background processing workflow")

if __name__ == "__main__":
    demo_booklet_maker()