# test_manual_generation.py
"""
Test Manual Generation Engine
Tests user manual, owner's manual, and training manual creation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engines.manual_engine import ManualEngine

def test_user_manual():
    """Test user manual generation"""
    print("Testing User Manual Generation...")

    engine = ManualEngine()

    request_data = {
        "product_name": "GOAT Writing Assistant",
        "features": [
            "AI-powered content generation",
            "Multi-format output support",
            "Real-time collaboration",
            "Advanced analytics"
        ],
        "instructions": {
            "getting_started": "Install the software and create your account.",
            "basic_usage": "Select a template and start writing.",
            "advanced_features": "Use AI suggestions for enhanced content.",
            "troubleshooting": "Check internet connection and restart if needed.",
            "safety": "Do not share sensitive information."
        }
    }

    try:
        manual = engine.generate_user_manual(**request_data)
        print(f"✓ User manual generated: {manual['title']}")
        print(f"  Sections: {len(manual['sections'])}")
        return True
    except Exception as e:
        print(f"✗ User manual generation failed: {str(e)}")
        return False

def test_owner_manual():
    """Test owner's manual generation"""
    print("\nTesting Owner's Manual Generation...")

    engine = ManualEngine()

    request_data = {
        "product_name": "Industrial Coffee Machine",
        "specifications": {
            "power": "220V, 50Hz",
            "capacity": "50 cups per hour",
            "dimensions": "30x40x50 cm",
            "weight": "25kg",
            "installation": "Place on stable surface, connect to power and water.",
            "operation": "Fill water tank, add coffee grounds, press start.",
            "warranty": "2 years parts and labor"
        },
        "maintenance": {
            "daily_cleaning": "Wipe exterior and empty grounds.",
            "weekly_maintenance": "Descale with vinegar solution.",
            "annual_service": "Professional inspection recommended."
        }
    }

    try:
        manual = engine.generate_owner_manual(**request_data)
        print(f"✓ Owner's manual generated: {manual['title']}")
        print(f"  Sections: {len(manual['sections'])}")
        return True
    except Exception as e:
        print(f"✗ Owner's manual generation failed: {str(e)}")
        return False

def test_training_manual():
    """Test training manual generation"""
    print("\nTesting Training Manual Generation...")

    engine = ManualEngine()

    request_data = {
        "topic": "Advanced Python Programming",
        "objectives": [
            "Master object-oriented programming concepts",
            "Implement design patterns",
            "Build scalable applications",
            "Debug complex code issues"
        ],
        "content": {
            "prerequisites": "Basic Python knowledge required",
            "module_1": "Introduction to OOP principles",
            "module_2": "Design patterns implementation",
            "module_3": "Testing and debugging",
            "exercises": "Complete coding assignments for each module",
            "assessment": "Final project and code review"
        }
    }

    try:
        manual = engine.generate_training_manual(**request_data)
        print(f"✓ Training manual generated: {manual['title']}")
        print(f"  Sections: {len(manual['sections'])}")
        return True
    except Exception as e:
        print(f"✗ Training manual generation failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Running Manual Generation Tests...\n")

    results = []
    results.append(test_user_manual())
    results.append(test_owner_manual())
    results.append(test_training_manual())

    passed = sum(results)
    total = len(results)

    print(f"\nTest Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All manual generation tests passed!")
    else:
        print("✗ Some tests failed. Check output above.")