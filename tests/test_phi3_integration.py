# test_phi3_integration.py
"""
Test Phi-3 Mini integration with Caleon Bridge
Validates the articulation pipeline works correctly
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from phi3_driver import get_articulator, Phi3Articulator

async def test_phi3_articulator():
    """Test Phi-3 articulator directly."""
    print("🧪 Testing Phi-3 Articulator...")

    articulator = get_articulator()
    status = articulator.get_status()
    print(f"Articulator status: {status}")

    # Test plan
    test_plan = {
        "chapter_title": "Test Chapter",
        "section_title": "Introduction to Phi-3 Integration",
        "goals": "Demonstrate Phi-3 Mini as Caleon's articulation engine",
        "tone": "technical_explanation",
        "continuity_context": "This is the first section of a technical guide",
        "target_length": "400-600 words"
    }

    print("\n📝 Generating articulated content...")
    try:
        content = await articulator.articulate(test_plan)
        print("✅ Articulation successful!")
        print(f"Content length: {len(content)} characters")
        print("\n--- SAMPLE OUTPUT ---")
        print(content[:500] + "..." if len(content) > 500 else content)
    except Exception as e:
        print(f"❌ Articulation failed: {e}")

    print("\n🌊 Testing streaming...")
    try:
        chunk_count = 0
        async for chunk in articulator.articulate_stream(test_plan):
            chunk_count += 1
            if chunk_count <= 5:  # Show first 5 chunks
                print(f"Chunk {chunk_count}: '{chunk[:50]}...'")
        print(f"✅ Streaming successful! Total chunks: {chunk_count}")
    except Exception as e:
        print(f"❌ Streaming failed: {e}")

def test_personality_conditioning():
    """Test Caleon's personality conditioning."""
    print("\n🎭 Testing Personality Conditioning...")

    articulator = Phi3Articulator()

    # Check personality prompt
    personality = articulator.personality_prompt
    print(f"Personality prompt loaded: {len(personality)} characters")

    # Test key personality traits
    traits = [
        "Caleon Prime",
        "sovereign AI UCM-Core-CALI",
        "direct and confident",
        "warm but not soft",
        "active voice",
        "short paragraphs"
    ]

    for trait in traits:
        if trait.lower() in personality.lower():
            print(f"✅ Found trait: {trait}")
        else:
            print(f"❌ Missing trait: {trait}")

async def main():
    """Run all tests."""
    print("🚀 Starting Phi-3 Integration Tests")
    print("=" * 50)

    await test_phi3_articulator()
    test_personality_conditioning()

    print("\n" + "=" * 50)
    print("🏁 Phi-3 Integration Tests Complete")

if __name__ == "__main__":
    asyncio.run(main())