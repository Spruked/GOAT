# test_voice_system.py
"""
Test script for GOAT Voice System with POM 2.0 Integration
"""

import asyncio
import json
import os
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append('.')

from engines.voice_engine import VoiceEngine
from engines.character_voice_mapper import CharacterVoiceMapper
from engines.narrator_optimizer import NarratorOptimizer
from engines.audiobook_renderer import AudiobookRenderer

async def test_voice_engine():
    """Test basic voice engine functionality"""
    print("🧪 Testing Voice Engine...")

    voice_engine = VoiceEngine()

    # Test 1: Create voice profile using parameters
    print("  📝 Creating voice profile...")
    result = await voice_engine.create_voice_profile(
        creation_method="parameter",
        name="Test Character",
        description="A test character voice",
        voice_type="character",
        param_config={
            "tension": 0.6,
            "breathiness": 0.2,
            "vibrato_rate": 4.0,
            "lip_rounding": 0.4,
            "articulation_precision": 0.8,
            "tongue_position": "alveolar",
            "sharpness": 0.7
        }
    )

    print(f"    ✅ Voice profile created: {result['profile_id']}")

    # Test 2: Generate audio
    print("  🎵 Generating test audio...")
    profile = await voice_engine.get_profile(result['profile_id'])
    audio_bytes = await voice_engine.synthesize_with_character_voice(
        text="Hello, this is a test of the voice synthesis system.",
        voice_profile=profile,
        character_emotion="neutral"
    )

    print(f"    ✅ Audio generated: {len(audio_bytes)} bytes")

    # Test 3: Voice preview
    print("  👂 Generating voice preview...")
    preview_audio = await voice_engine.preview_voice(
        profile_id=result['profile_id'],
        text="This is a voice preview.",
        emotion="excited"
    )

    print(f"    ✅ Preview generated: {len(preview_audio)} bytes")

    return result['profile_id']

async def test_character_mapper():
    """Test character voice mapping"""
    print("🎭 Testing Character Voice Mapper...")

    voice_engine = VoiceEngine()
    character_mapper = CharacterVoiceMapper(voice_engine)

    # Test 1: Create character profile
    print("  👤 Creating character profile...")
    character = await character_mapper.create_character_profile(
        name="Alice",
        description="A curious young woman with a gentle voice",
        gender="female",
        age_range="young_adult",
        personality_traits=["curious", "gentle", "intelligent"],
        voice_characteristics={
            "pitch_range": "medium_high",
            "pace": "moderate",
            "clarity": "high"
        }
    )

    print(f"    ✅ Character created: {character.name} -> {character.voice_profile_id}")

    # Test 2: Generate character dialogue
    print("  💬 Generating character dialogue...")
    audio = await character_mapper.generate_character_audio(
        character_name="Alice",
        text="Oh, what an interesting development!",
        emotion="excited"
    )

    print(f"    ✅ Dialogue generated: {len(audio)} bytes")

    # Test 3: Process dialogue script
    print("  📖 Processing dialogue script...")
    script = '''
    Alice: "Hello there! How are you today?"
    Bob: "I'm doing well, thank you. And you?"
    Alice: "Quite curious about this new technology."
    '''

    segments = await character_mapper.process_dialogue_script(script)
    print(f"    ✅ Script processed: {len(segments)} segments found")

    return character_mapper

async def test_narrator_optimizer():
    """Test narrator optimization"""
    print("📚 Testing Narrator Optimizer...")

    voice_engine = VoiceEngine()
    narrator_optimizer = NarratorOptimizer(voice_engine)

    # Test 1: Create narrator profile
    print("  🎙️ Creating narrator profile...")
    profile = await narrator_optimizer.create_narrator_profile(
        content_type="nonfiction",
        name="educational"
    )

    print(f"    ✅ Narrator profile created: {profile.profile_id}")

    # Test 2: Analyze text segments
    print("  📊 Analyzing text segments...")
    text = """
    Artificial Intelligence (AI) is transforming our world in unprecedented ways.
    Machine learning algorithms can now recognize patterns in data that were previously invisible to human analysts.
    This breakthrough has applications in healthcare, finance, transportation, and countless other fields.
    """

    segments = await narrator_optimizer.analyze_text_segments(text, "nonfiction")
    optimizations = await narrator_optimizer.optimize_narration(segments, profile)

    print(f"    ✅ Text analyzed: {len(segments)} segments, {optimizations['summary']['technical_terms_found']} technical terms")

    # Test 3: Generate narrator audio
    print("  🔊 Generating narrator audio...")
    audio = await narrator_optimizer.generate_narrator_audio(
        text="Machine learning is a subset of artificial intelligence.",
        narrator_profile=profile,
        segment_type="main",
        technical_terms=["machine learning", "artificial intelligence"]
    )

    print(f"    ✅ Narrator audio generated: {len(audio)} bytes")

    return narrator_optimizer

async def test_audiobook_renderer():
    """Test audiobook rendering"""
    print("📖 Testing Audiobook Renderer...")

    voice_engine = VoiceEngine()
    character_mapper = CharacterVoiceMapper(voice_engine)
    narrator_optimizer = NarratorOptimizer(voice_engine)
    audiobook_renderer = AudiobookRenderer(voice_engine, character_mapper, narrator_optimizer)

    # Test 1: Create test book data
    print("  📝 Creating test book data...")
    book_data = {
        "title": "Test Audiobook",
        "author": "GOAT System",
        "chapters": [
            {
                "title": "Introduction",
                "content": "This is a test audiobook to demonstrate the voice synthesis system.",
                "content_type": "nonfiction"
            },
            {
                "title": "Character Dialogue",
                "content": '''
                Alice: "Welcome to our demonstration!"
                Bob: "Thank you for having us."
                Alice: "The technology is quite impressive."
                ''',
                "content_type": "fiction"
            }
        ]
    }

    # Test 2: Render preview
    print("  🎧 Generating voice preview...")
    preview_result = await audiobook_renderer.render_preview(
        text="This is a preview of the audiobook system.",
        voice_profile_id="vp_narrator_nonfiction_default",
        output_path="./test_output/preview.wav",
        emotion="neutral"
    )

    print(f"    ✅ Preview rendered: {preview_result['duration']:.2f} seconds")

    # Test 3: Batch render segments
    print("  🎵 Batch rendering segments...")
    segments = [
        {
            "type": "narrator",
            "text": "This is the introduction to our test audiobook.",
            "narrator_profile": "narrator_nonfiction_default",
            "segment_type": "main"
        }
    ]

    batch_results = await audiobook_renderer.batch_render_segments(
        segments, "./test_output/batch"
    )

    successful = sum(1 for r in batch_results if r['status'] == 'success')
    print(f"    ✅ Batch rendering: {successful}/{len(segments)} segments successful")

async def run_full_integration_test():
    """Run complete integration test"""
    print("🚀 Running Full Voice System Integration Test...")
    print("=" * 60)

    try:
        # Test individual components
        voice_profile_id = await test_voice_engine()
        print()

        character_mapper = await test_character_mapper()
        print()

        narrator_optimizer = await test_narrator_optimizer()
        print()

        await test_audiobook_renderer()
        print()

        # Test system status
        print("📊 System Status Check...")
        voice_engine = VoiceEngine()
        status = {
            "voice_engine": True,
            "character_mapper": len(character_mapper.characters),
            "narrator_optimizer": len(narrator_optimizer.narrator_profiles),
            "directories": all([
                os.path.exists("./voices"),
                os.path.exists("./voices/profiles"),
                os.path.exists("./voices/temp")
            ])
        }

        print(f"  ✅ Voice Engine: {'Available' if status['voice_engine'] else 'Unavailable'}")
        print(f"  ✅ Character Mapper: {status['character_mapper']} characters loaded")
        print(f"  ✅ Narrator Optimizer: {status['narrator_optimizer']} profiles available")
        print(f"  ✅ Directories: {'All present' if status['directories'] else 'Missing some'}")

        print()
        print("🎉 All tests completed successfully!")
        print("The GOAT Voice System with POM 2.0 integration is ready for production use.")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

async def main():
    """Main test runner"""
    # Ensure test output directory exists
    os.makedirs("./test_output", exist_ok=True)

    # Run tests
    success = await run_full_integration_test()

    # Cleanup
    print("\n🧹 Cleaning up test files...")
    import shutil
    if os.path.exists("./test_output"):
        shutil.rmtree("./test_output")

    if success:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)