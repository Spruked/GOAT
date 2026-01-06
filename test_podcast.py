#!/usr/bin/env python3
"""
Test script for GOAT Podcast Engine
Tests the Phil and Jim Dandy Show podcast generation
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from podcast_builder.builder import PodcastBuilder
import sys
import os

# Import podcast_engine module directly
sys.path.insert(0, os.path.dirname(__file__))
exec(open('podcast_engine.py').read())

def test_podcast_builder():
    """Test the podcast builder with Phil and Jim Dandy theme"""
    print("🎙️ Testing GOAT Podcast Builder")
    print("=" * 50)

    try:
        # Test the podcast builder
        builder = PodcastBuilder()

        # Create a podcast about fishing brothers
        topic = "The Phil and Jim Dandy Show - Brothers who fish daily"
        audience = "fishing enthusiasts, outdoor lovers, family audiences"
        tone = "casual, brotherly, enthusiastic"
        length = "short"

        print(f"Building podcast: {topic}")
        result = builder.build(
            topic=topic,
            audience=audience,
            tone=tone,
            length=length
        )

        print("✅ Podcast content generated successfully!")
        print(f"Content length: {len(result)} characters")

        # Save the result
        output_file = Path("test_podcast_output.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"✅ Podcast saved to: {output_file}")

        # Print a preview
        print("\n📄 Content Preview:")
        print("-" * 30)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("-" * 30)

        return True

    except Exception as e:
        print(f"❌ Podcast builder test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_podcast_engine():
    """Test the full podcast engine"""
    print("\n🎙️ Testing GOAT Podcast Engine")
    print("=" * 50)

    try:
        engine = PodcastEngine()

        # Create legacy input for fishing brothers podcast
        user_input = LegacyInput(
            topic="Daily Fishing Adventures of the Dandy Brothers",
            notes="Phil and Jim Dandy are brothers who fish every day. They share stories, tips, and laughs from their fishing trips.",
            source_materials=[],
            intent="entertainment",
            audience="fishing enthusiasts",
            output_format="podcast",
            tone="casual",
            length_estimate="short",
            create_audiobook=True,
            voice="male_narrator"
        )

        print("Creating legacy podcast...")
        result = engine.create_legacy(user_input)

        print("✅ Podcast engine completed!")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Audio Path: {result.get('audiobook_path', 'N/A')}")

        return True

    except Exception as e:
        print(f"❌ Podcast engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all podcast tests"""
    print("🧪 GOAT Podcast System Test Suite")
    print("=" * 60)

    tests = [
        ("Podcast Builder", test_podcast_builder),
        ("Podcast Engine", test_podcast_engine)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 60)
    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All podcast tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())