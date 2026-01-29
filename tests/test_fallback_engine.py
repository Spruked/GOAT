# test_fallback_engine.py
"""
Test Caleon Prime Fallback Engine
Validates personality-aligned fallback responses
"""

import asyncio
import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from fallback_engine import get_fallback_engine, CaleonFallbackEngine

def test_fallback_categories():
    """Test all fallback categories."""
    print("🧪 Testing Fallback Categories...")

    engine = get_fallback_engine()
    categories = engine.fallback_categories

    print(f"Available categories: {len(categories)}")
    for category, config in categories.items():
        print(f"✅ {category}: {config['description']}")

    assert len(categories) >= 8, "Should have at least 8 fallback categories"
    print("✅ All categories loaded successfully")

def test_personality_bible():
    """Test Persona Bible loading."""
    print("\n📖 Testing Persona Bible...")

    engine = get_fallback_engine()
    bible = engine.persona_bible

    # Test core identity
    assert bible["identity"]["name"] == "Caleon Prime"
    assert bible["identity"]["nickname"] == "Cali"
    print("✅ Identity loaded correctly")

    # Test personality traits
    traits = bible["traits"]
    assert traits["direct"] == True
    assert traits["confident"] == True
    assert traits["calm"] == True
    print("✅ Personality traits loaded correctly")

    # Test forbidden phrases
    forbidden = bible["forbidden_phrases"]
    assert "As an AI" in forbidden
    assert "I'm sorry" in forbidden
    print("✅ Forbidden phrases configured correctly")

    # Test allowed phrases
    allowed = bible["allowed_phrases"]
    assert "Here's the truth" in allowed
    assert "Stay sharp" in allowed
    print("✅ Allowed phrases configured correctly")

def test_phi3_fallback():
    """Test Phi-3 unavailable fallback."""
    print("\n🤖 Testing Phi-3 Fallback...")

    engine = get_fallback_engine()
    response = engine.get_fallback_response("phi3_unavailable")

    print(f"Response: {response['response'][:100]}...")
    assert response["category"] == "phi3_unavailable"
    assert response["personality_alignment"] == "confident_maintenance"
    assert response["fallback_mode"] == True
    assert "PHI-3 ARTICULATION OFFLINE" in response["response"]
    print("✅ Phi-3 fallback maintains confident personality")

def test_ucm_fallback():
    """Test UCM unavailable fallback."""
    print("\n🧠 Testing UCM Fallback...")

    engine = get_fallback_engine()
    response = engine.get_fallback_response("ucm_unavailable")

    print(f"Response: {response['response'][:100]}...")
    assert response["category"] == "ucm_unavailable"
    assert response["personality_alignment"] == "calm_resilience"
    assert "## Operational Status" in response["response"]
    print("✅ UCM fallback maintains calm resilience")

def test_security_fallback():
    """Test security protection fallback."""
    print("\n🔒 Testing Security Fallback...")

    engine = get_fallback_engine()
    response = engine.get_fallback_response("security_protection")

    print(f"Response: {response['response'][:100]}...")
    assert response["category"] == "security_protection"
    assert response["personality_alignment"] == "protective_strength"
    assert "SECURITY PROTOCOLS ENGAGED" in response["response"]
    print("✅ Security fallback maintains protective strength")

def test_consent_fallback():
    """Test consent violation fallback."""
    print("\n⚖️ Testing Consent Fallback...")

    engine = get_fallback_engine()
    response = engine.get_fallback_response("consent_violation")

    print(f"Response: {response['response'][:100]}...")
    assert response["category"] == "consent_violation"
    assert response["personality_alignment"] == "ethical_firmness"
    assert "Ethical protocols engaged" in response["response"]
    print("✅ Consent fallback maintains ethical firmness")

def test_fallback_stats():
    """Test fallback statistics tracking."""
    print("\n📊 Testing Fallback Statistics...")

    # Create a fresh engine instance for this test
    engine = CaleonFallbackEngine()
    initial_total = engine.fallback_stats["total_fallbacks"]

    # Generate some fallback responses using the same engine instance
    engine.get_fallback_response("phi3_unavailable")
    engine.get_fallback_response("ucm_unavailable")
    engine.get_fallback_response("phi3_unavailable")

    final_total = engine.fallback_stats["total_fallbacks"]
    phi3_count = engine.fallback_stats["category_usage"].get("phi3_unavailable", 0)
    ucm_count = engine.fallback_stats["category_usage"].get("ucm_unavailable", 0)

    assert final_total == initial_total + 3, f"Expected {initial_total + 3}, got {final_total}"
    assert phi3_count == 2, f"Expected 2 phi3_unavailable, got {phi3_count}"
    assert ucm_count == 1, f"Expected 1 ucm_unavailable, got {ucm_count}"
    print("✅ Statistics tracking works correctly")

def test_personality_conditioning():
    """Test that responses follow personality rules."""
    print("\n🎭 Testing Personality Conditioning...")

    engine = get_fallback_engine()

    # Test multiple responses for forbidden phrases
    responses_to_check = [
        engine.get_fallback_response("phi3_unavailable"),
        engine.get_fallback_response("ucm_unavailable"),
        engine.get_fallback_response("security_protection")
    ]

    for response in responses_to_check:
        response_text = response["response"]

        # Should not contain forbidden phrases
        forbidden_phrases = engine.persona_bible["forbidden_phrases"]
        for forbidden in forbidden_phrases:
            assert forbidden.lower() not in response_text.lower(), f"Found forbidden phrase '{forbidden}' in response"

        # Should be direct and confident (check for hedging)
        assert "probably" not in response_text.lower(), "Found hedging language"
        assert "maybe" not in response_text.lower(), "Found hedging language"

    print("✅ Personality conditioning prevents forbidden phrases and hedging")

def test_structured_responses():
    """Test structured response formatting."""
    print("\n📋 Testing Structured Responses...")

    engine = get_fallback_engine()

    # Test categories that should have structured responses
    structured_categories = ["phi3_unavailable", "ucm_unavailable", "resource_limit", "security_protection"]

    for category in structured_categories:
        response = engine.get_fallback_response(category)
        response_text = response["response"]

        # Should have markdown headers
        assert "#" in response_text, f"Category {category} should have structured formatting"

        # Should have status indicators
        assert "✅" in response_text, f"Category {category} should have status indicators"

    print("✅ Structured responses maintain clear formatting")

def test_integration_with_phi3():
    """Test integration with Phi-3 driver fallback."""
    print("\n🔗 Testing Phi-3 Driver Integration...")

    from phi3_driver import Phi3Articulator

    articulator = Phi3Articulator()

    # Force a scenario that triggers fallback
    test_plan = {"chapter_title": "Test", "section_title": "Test Section", "goals": "Test fallback"}
    response = articulator._fallback_response("test prompt")

    # Should use fallback engine
    assert "PHI-3 ARTICULATION" in response
    assert "Operating in structured mode" in response
    print("✅ Phi-3 driver properly uses fallback engine")

def main():
    """Run all fallback engine tests."""
    print("🚀 Starting Caleon Prime Fallback Engine Tests")
    print("=" * 60)

    try:
        test_fallback_categories()
        test_personality_bible()
        test_phi3_fallback()
        test_ucm_fallback()
        test_security_fallback()
        test_consent_fallback()
        test_fallback_stats()
        test_personality_conditioning()
        test_structured_responses()
        test_integration_with_phi3()

        print("\n" + "=" * 60)
        print("🎉 ALL FALLBACK ENGINE TESTS PASSED!")
        print("Caleon Prime maintains her personality even in fallback mode.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)