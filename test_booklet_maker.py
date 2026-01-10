#!/usr/bin/env python3
"""
Test script for Booklet Maker Worker
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from workers.booklet_maker_worker.worker_body import BookletMakerWorker, PaymentGateway, OrderManager
        print("✓ BookletMakerWorker imported successfully")

        from payments.payment_gateway import PaymentGateway as PG2
        print("✓ PaymentGateway imported successfully")

        from payments.order_manager import OrderManager as OM2
        print("✓ OrderManager imported successfully")

        # Test instantiation
        worker = BookletMakerWorker(ucm_connector=None)
        print("✓ BookletMakerWorker instantiated successfully")

        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_script_loading():
    """Test that script data loads correctly"""
    try:
        import json
        script_path = Path(__file__).parent / "workers" / "booklet_maker" / "booklet_script.json"

        with open(script_path, 'r') as f:
            data = json.load(f)

        print(f"✓ Script loaded with {len(data['script'])} passes")

        # Check required passes
        pass_ids = [p['pass_id'] for p in data['script']]
        required_passes = ['foundation', 'layout', 'typography', 'presentation', 'production']

        for pass_id in required_passes:
            if pass_id in pass_ids:
                print(f"✓ Found pass: {pass_id}")
            else:
                print(f"❌ Missing pass: {pass_id}")

        return True

    except Exception as e:
        print(f"❌ Script loading failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Booklet Maker Worker...")
    print("=" * 50)

    success = True
    success &= test_imports()
    success &= test_script_loading()

    print("=" * 50)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)