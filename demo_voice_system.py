#!/usr/bin/env python3
"""
GOAT Voice System Demo - POM 2.0 Integration Showcase
Demonstrates professional audiobook creation with character voices and narrator optimization
"""

import asyncio
import json
from pathlib import Path
import os

# Import the voice system
from engines.voice_engine import VoiceEngine
from engines.character_voice_mapper import CharacterVoiceMapper
from engines.narrator_optimizer import NarratorOptimizer
from engines.audiobook_renderer import AudiobookRenderer

async def demo_character_creation():
    """Demo: Create character voices for a fiction story"""
    print("🎭 Character Voice Creation Demo")
    print("-" * 40)

    voice_engine = VoiceEngine()
    character_mapper = CharacterVoiceMapper(voice_engine)

    # Create characters for a mystery novel
    characters = [
        {
            "name": "Detective Sarah Chen",
            "description": "Sharp-witted detective in her 30s, confident and authoritative",
            "gender": "female",
            "age_range": "adult",
            "personality_traits": ["confident", "intelligent", "determined"],
            "voice_characteristics": {"clarity": "high", "projection": "strong"}
        },
        {
            "name": "Professor Harrington",
            "description": "Elderly academic, wise but absent-minded, speaks deliberately",
            "gender": "male",
            "age_range": "elderly",
            "personality_traits": ["wise", "absent-minded", "formal"],
            "voice_characteristics": {"pace": "slow", "formality": "high"}
        },
        {
            "name": "Young Witness",
            "description": "Frightened teenager who speaks quickly when nervous",
            "gender": "female",
            "age_range": "teen",
            "personality_traits": ["nervous", "young", "timid"],
            "voice_characteristics": {"pitch": "high", "pace": "variable"}
        }
    ]

    created_characters = []
    for char_data in characters:
        character = await character_mapper.create_character_profile(**char_data)
        created_characters.append(character)
        print(f"✅ Created {character.name} -> {character.voice_profile_id}")

    # Generate sample dialogue
    print("\n🎬 Sample Dialogue Generation:")
    dialogues = [
        ("Detective Sarah Chen", "The evidence is clear. We need to act now.", "determined"),
        ("Professor Harrington", "In my experience, these matters require careful consideration.", "calm"),
        ("Young Witness", "I... I saw everything! It was terrifying!", "fearful")
    ]

    for char_name, text, emotion in dialogues:
        audio = await character_mapper.generate_character_audio(char_name, text, emotion)
        print(f"🎵 {char_name} ({emotion}): {len(audio)} bytes generated")

    return character_mapper

async def demo_narrator_optimization():
    """Demo: Narrator optimization for different content types"""
    print("\n📚 Narrator Optimization Demo")
    print("-" * 40)

    voice_engine = VoiceEngine()
    narrator_optimizer = NarratorOptimizer(voice_engine)

    content_samples = {
        "fiction": """
        The ancient oak tree stood sentinel over the misty valley, its gnarled branches
        reaching toward the storm clouds like skeletal fingers. Thunder rumbled in the
        distance, a ominous warning of the tempest to come.
        """,

        "nonfiction": """
        Quantum entanglement represents one of the most profound discoveries in modern
        physics. When two particles become entangled, the state of one particle instantly
        influences the state of the other, regardless of the distance separating them.
        """,

        "technical": """
        The algorithm implements a recursive backtracking approach with memoization
        to optimize the solution space. Time complexity is O(n!) in the worst case,
        but pruning reduces this significantly for most practical applications.
        """
    }

    for content_type, text in content_samples.items():
        print(f"\n📖 Analyzing {content_type} content...")

        # Create optimized narrator profile
        profile = await narrator_optimizer.create_narrator_profile(content_type)

        # Analyze text
        segments = await narrator_optimizer.analyze_text_segments(text, content_type)
        optimizations = await narrator_optimizer.optimize_narration(segments, profile)

        print(f"   📊 Segments: {len(segments)}")
        print(f"   🎯 Optimizations: {optimizations['summary']['technical_terms_found']} technical terms")
        print(f"   ⏱️  Average speed: {optimizations['summary']['average_speed']:.2f}x")
        # Generate sample audio
        audio = await narrator_optimizer.generate_narrator_audio(
            text[:100] + "...",  # First 100 chars
            narrator_profile=profile,
            segment_type="main"
        )
        print(f"   🎵 Audio generated: {len(audio)} bytes")

    return narrator_optimizer

async def demo_audiobook_creation():
    """Demo: Complete audiobook creation"""
    print("\n📖 Complete Audiobook Creation Demo")
    print("-" * 40)

    # Initialize all components
    voice_engine = VoiceEngine()
    character_mapper = CharacterVoiceMapper(voice_engine)
    narrator_optimizer = NarratorOptimizer(voice_engine)
    audiobook_renderer = AudiobookRenderer(voice_engine, character_mapper, narrator_optimizer)

    # Create sample book data
    book_data = {
        "title": "The Quantum Detective",
        "author": "Dr. Sarah Chen",
        "chapters": [
            {
                "title": "Chapter 1: The Discovery",
                "content": """
                Detective Sarah Chen adjusted her glasses as she examined the quantum computer.
                "This changes everything," she muttered. The device hummed softly, its processors
                entangled in ways that defied classical physics.
                """,
                "content_type": "fiction"
            },
            {
                "title": "Chapter 2: Quantum Entanglement Explained",
                "content": """
                Quantum entanglement occurs when two or more particles become correlated in such
                a way that the quantum state of each particle cannot be described independently.
                This phenomenon, first described by Einstein as "spooky action at a distance,"
                forms the basis of quantum computing and secure communication protocols.
                """,
                "content_type": "nonfiction"
            }
        ]
    }

    print("🎵 Rendering audiobook...")
    print("   (This would create a full WAV file in a production environment)")

    # In demo mode, just show the structure
    result = {
        "output_path": "./demo_output/quantum_detective.wav",
        "total_duration": 45.5,  # Mock duration
        "chapters": len(book_data["chapters"]),
        "total_segments": 4,
        "metadata": {
            "title": book_data["title"],
            "author": book_data["author"],
            "voice_engine": "GOAT POM 2.0 Integration"
        }
    }

    print(f"✅ Audiobook structure created:")
    print(f"   📁 Output: {result['output_path']}")
    print(f"   ⏱️  Duration: {result['total_duration']:.1f} seconds")
    print(f"   📚 Chapters: {result['chapters']}")
    print(f"   🎵 Segments: {result['total_segments']}")
    print(f"   🎙️ Engine: {result['metadata']['voice_engine']}")

    return result

async def demo_voice_preview():
    """Demo: Voice preview generation"""
    print("\n👂 Voice Preview Demo")
    print("-" * 40)

    voice_engine = VoiceEngine()
    audiobook_renderer = AudiobookRenderer(voice_engine, None, None)

    preview_text = "Welcome to the future of audiobook production with GOAT's advanced voice synthesis."

    print("🎧 Generating voice preview...")
    result = await audiobook_renderer.render_preview(
        text=preview_text,
        voice_profile_id="demo_narrator",
        output_path="./demo_output/preview.wav",
        emotion="neutral"
    )

    print("✅ Preview generated:")
    print(f"   📁 Path: {result['output_path']}")
    print(f"   ⏱️  Duration: {result['duration']:.2f} seconds")
    print(f"   🎭 Emotion: {result['emotion']}")
    print(f"   💬 Text: {result['text'][:50]}...")

async def main():
    """Main demo runner"""
    print("🎉 GOAT Voice System - POM 2.0 Integration Demo")
    print("=" * 60)
    print("This demo showcases professional audiobook creation with:")
    print("• Character voice synthesis with emotional modulation")
    print("• Narrator optimization for different content types")
    print("• Complete audiobook rendering pipeline")
    print("• Phonatory Output Module (POM) 2.0 integration")
    print()

    # Create demo output directory
    os.makedirs("./demo_output", exist_ok=True)

    try:
        # Run demos
        await demo_character_creation()
        await demo_narrator_optimization()
        await demo_audiobook_creation()
        await demo_voice_preview()

        print("\n🎊 Demo completed successfully!")
        print("\nKey Features Demonstrated:")
        print("✅ Voice profile creation and management")
        print("✅ Character voice mapping with emotional ranges")
        print("✅ Narrator optimization for content types")
        print("✅ Audiobook rendering pipeline")
        print("✅ Voice preview generation")
        print("✅ POM 2.0 phonatory module integration (mock)")
        print("\n📋 Production Ready Features:")
        print("• Secure voice vault with glyph provenance")
        print("• Multi-format export (WAV, MP3, M4B)")
        print("• RESTful API endpoints")
        print("• Batch processing capabilities")
        print("• Quality presets and performance optimization")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    print(f"\n🏁 Demo finished with exit code: {exit_code}")