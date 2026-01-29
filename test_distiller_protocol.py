#!/usr/bin/env python3
"""
Test the new Distiller Protocol and VisiData Distiller
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.distiller_interface import distiller_registry

def test_distiller_protocol():
    print("🔍 Testing GOAT Distiller Protocol...")
    print()

    # Test registry
    print("1. Testing Distiller Registry...")
    distillers = distiller_registry.list_distillers()
    print(f"   ✅ Found {len(distillers)} registered distillers:")
    for name, info in distillers.items():
        print(f"      • {name}: {info['supported_sources']} → {info['signal_types']}")

    # Test VisiData distiller
    print("\n2. Testing VisiData Distiller...")
    visidata_distiller = distiller_registry.get_distiller("visidata_distiller")

    if visidata_distiller:
        print(f"   ✅ Got distiller: {visidata_distiller.name}")
        print(f"   ✅ Supported sources: {visidata_distiller.supported_sources}")
        print(f"   ✅ Signal types: {visidata_distiller.signal_types}")

        # Test with sample data (list of dicts)
        test_data = [
            {"name": "Alice", "age": 25, "topic": "Machine Learning"},
            {"name": "Bob", "age": 30, "topic": "Data Science"},
            {"name": "Charlie", "age": 35, "topic": "AI Ethics"}
        ]

        print("\n3. Testing Distillation with sample data...")
        result = visidata_distiller.distill([test_data])

        print(f"   ✅ Distillation completed in {result.metadata.get('processing_time', 0):.3f}s")
        print(f"   ✅ Confidence: {result.metadata.get('confidence', 0):.2f}")
        print(f"   ✅ Validated: {result.validated}")

        signals = result.signals
        print(f"   ✅ Signals extracted:")
        print(f"      • Shape: {signals.get('shape', 'unknown')}")
        print(f"      • Columns: {signals.get('columns', [])}")
        print(f"      • Themes: {signals.get('extracted_themes', [])}")

        # Test validation
        print("\n4. Testing Signal Validation...")
        is_valid = visidata_distiller.validate_signals(signals)
        print(f"   ✅ Signals validation: {is_valid}")

    else:
        print("   ❌ VisiData distiller not found!")

    print("\n🎉 Distiller Protocol test completed!")

if __name__ == "__main__":
    test_distiller_protocol()