#!/usr/bin/env python3
"""
Test the new Distiller Interface and VisiData Distiller
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.distiller_interface import distiller_registry

def test_distiller_interface():
    print("🔍 Testing GOAT Distiller Interface...")
    print()

    # Test registry
    print("1. Testing Distiller Registry...")
    distillers = distiller_registry.list_distillers()
    print(f"   ✅ Found {len(distillers)} registered distillers:")
    for name, info in distillers.items():
        print(f"      • {name}: {info}")

    # Test VisiData distiller
    print("\n2. Testing VisiData Distiller...")
    visidata_distiller = distiller_registry.get_distiller("visidata_distiller")

    if visidata_distiller:
        print(f"   ✅ Got distiller: {visidata_distiller.name}")
        print(f"   ✅ Input types: {visidata_distiller.input_types}")
        print(f"   ✅ Output signals: {visidata_distiller.output_signals}")

        # Test with a simple data structure
        test_data = [
            {"name": "Alice", "age": 25, "topic": "Machine Learning"},
            {"name": "Bob", "age": 30, "topic": "Data Science"},
            {"name": "Charlie", "age": 35, "topic": "AI Ethics"}
        ]

        print("\n3. Testing Distillation...")
        result = visidata_distiller.distill(test_data)

        print(f"   ✅ Distillation completed in {result.metadata.get('processing_time', 0):.3f}s")
        print(f"   ✅ Confidence: {result.metadata.get('confidence', 0):.2f}")

        signals = result.signals
        print(f"   ✅ Signals extracted:")
        print(f"      • Shape: {signals.get('shape', 'unknown')}")
        print(f"      • Columns: {signals.get('columns', [])}")
        print(f"      • Themes: {signals.get('extracted_themes', [])}")

    else:
        print("   ❌ VisiData distiller not found!")

    print("\n🎉 Distiller Interface test completed!")

if __name__ == "__main__":
    test_distiller_interface()