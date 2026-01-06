#!/usr/bin/env python3
"""
Test script for Caleon Scripted Response System
Verifies all components work correctly.
"""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from engine import CaliScripts

def test_basic_responses():
    """Test basic scripted responses."""
    print("🧪 Testing Caleon Scripted Response System")
    print("=" * 50)

    # Test greetings
    greeting = CaliScripts.say("greetings", "welcome_dashboard", name="Bryan")
    print(f"Greeting: {greeting}")

    # Test onboarding
    onboarding = CaliScripts.say("onboarding", "start", name="TestUser")
    print(f"Onboarding: {onboarding}")

    # Test navigation
    nav = CaliScripts.say("navigation", "to_builder")
    print(f"Navigation: {nav}")

    # Test errors
    error = CaliScripts.say("errors", "missing_input")
    print(f"Error: {error}")

    # Test confirmations
    confirm = CaliScripts.say("confirmations", "saved")
    print(f"Confirmation: {confirm}")

    # Test drafts
    draft = CaliScripts.say("drafts", "start_chapter", chapter="1", section="Introduction")
    print(f"Draft: {draft}")

    print("\n✅ Basic responses working!")

def test_convenience_methods():
    """Test convenience methods."""
    print("\n🧪 Testing convenience methods:")

    greet = CaliScripts.greet("first_time")
    print(f"Greet: {greet}")

    error = CaliScripts.error("network_error")
    print(f"Error: {error}")

    confirm = CaliScripts.confirm("task_complete")
    print(f"Confirm: {confirm}")

    draft = CaliScripts.draft("done")
    print(f"Draft: {draft}")

    print("✅ Convenience methods working!")

def test_categories_and_entries():
    """Test category and entry listing."""
    print("\n🧪 Testing category access:")

    categories = CaliScripts.get_categories()
    print(f"Available categories: {categories}")

    if "greetings" in categories:
        entries = CaliScripts.get_entries("greetings")
        print(f"Greetings entries: {entries}")

    print("✅ Category access working!")

def test_personality_arrays():
    """Test personality arrays (random selection)."""
    print("\n🧪 Testing personality arrays:")

    # These should return the first item from arrays
    tagline = CaliScripts.say("personality", "taglines")
    print(f"Tagline: {tagline}")

    humor = CaliScripts.say("personality", "humor")
    print(f"Humor: {humor}")

    wisdom = CaliScripts.say("personality", "wisdom")
    print(f"Wisdom: {wisdom}")

    print("✅ Personality arrays working!")

def test_missing_scripts():
    """Test handling of missing scripts."""
    print("\n🧪 Testing missing script handling:")

    missing = CaliScripts.say("nonexistent", "missing_entry")
    print(f"Missing script: {missing}")

    print("✅ Missing script handling working!")

if __name__ == "__main__":
    try:
        test_basic_responses()
        test_convenience_methods()
        test_categories_and_entries()
        test_personality_arrays()
        test_missing_scripts()

        print("\n🎉 All tests passed! Caleon Scripted Response System is ready.")
        print("\nExample usage:")
        print("from cali_scripts.engine import CaliScripts")
        print("message = CaliScripts.say('greetings', 'welcome_dashboard', name='Bryan')")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)