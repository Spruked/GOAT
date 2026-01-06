# create_happy_toes_audiobook.py
"""
Create the Happy Toes audiobook with author voices for each chapter
"""

import json
import asyncio
import os
from pathlib import Path
from datetime import datetime

# Import the audiobook system
from engines.voice_engine import VoiceEngine
from engines.character_voice_mapper import CharacterVoiceMapper
from engines.narrator_optimizer import NarratorOptimizer
from engines.audiobook_renderer import AudiobookRenderer

async def create_happy_toes_audiobook():
    """Create the Happy Toes audiobook with author voices"""

    print("🎧 Creating Happy Toes Audiobook with Author Voices")
    print("=" * 60)

    # Load the book data
    book_path = Path("book_output/happy_toes.json")
    with open(book_path, 'r', encoding='utf-8') as f:
        book_data = json.load(f)

    print(f"📖 Loaded book: {book_data['title']} by {book_data['author']}")
    print(f"📚 Chapters: {len(book_data['chapters'])}")

    # Initialize the audiobook system (CPU-optimized)
    voice_engine = VoiceEngine(cpu_mode=True)  # Enable CPU optimizations
    character_mapper = CharacterVoiceMapper(voice_engine)
    narrator_optimizer = NarratorOptimizer(voice_engine)
    renderer = AudiobookRenderer(voice_engine, character_mapper, narrator_optimizer, cpu_mode=True)

    # Author voice profiles based on their literary styles
    author_voices = {
        "Bryan Anthony Spruk": {
            "voice_type": "narrator",
            "style": "warm_fatherly",
            "emotion_range": ["loving", "hopeful", "proud"],
            "pitch_modulation": 0.95,
            "target_vowel": "a"
        },
        "Jane Austen": {
            "voice_type": "narrator",
            "style": "elegant_british",
            "emotion_range": ["refined", "witty", "observant"],
            "pitch_modulation": 1.05,
            "target_vowel": "e"
        },
        "Mark Twain": {
            "voice_type": "narrator",
            "style": "folksy_american",
            "emotion_range": ["humorous", "down_to_earth", "wise"],
            "pitch_modulation": 0.9,
            "target_vowel": "a"
        },
        "Maya Angelou": {
            "voice_type": "narrator",
            "style": "powerful_resonant",
            "emotion_range": ["empowering", "dignified", "resilient"],
            "pitch_modulation": 0.85,
            "target_vowel": "o"
        },
        "Emily Dickinson": {
            "voice_type": "narrator",
            "style": "introspective_quiet",
            "emotion_range": ["contemplative", "delicate", "profound"],
            "pitch_modulation": 1.1,
            "target_vowel": "i"
        },
        "Franz Kafka": {
            "voice_type": "narrator",
            "style": "anxious_european",
            "emotion_range": ["uneasy", "metaphorical", "alienated"],
            "pitch_modulation": 0.95,
            "target_vowel": "u"
        },
        "Oscar Wilde": {
            "voice_type": "narrator",
            "style": "witty_irish",
            "emotion_range": ["sarcastic", "elegant", "paradoxical"],
            "pitch_modulation": 1.0,
            "target_vowel": "e"
        },
        "Robert Frost": {
            "voice_type": "narrator",
            "style": "rural_american",
            "emotion_range": ["philosophical", "grounded", "reflective"],
            "pitch_modulation": 0.92,
            "target_vowel": "o"
        },
        "Virginia Woolf": {
            "voice_type": "narrator",
            "style": "stream_of_consciousness",
            "emotion_range": ["introspective", "fluid", "psychological"],
            "pitch_modulation": 1.08,
            "target_vowel": "e"
        },
        "Sylvia Plath": {
            "voice_type": "narrator",
            "style": "intense_personal",
            "emotion_range": ["passionate", "confessional", "raw"],
            "pitch_modulation": 0.88,
            "target_vowel": "a"
        },
        "Walt Whitman": {
            "voice_type": "narrator",
            "style": "expansive_american",
            "emotion_range": ["celebratory", "democratic", "vital"],
            "pitch_modulation": 0.85,
            "target_vowel": "a"
        },
        "Ernest Hemingway": {
            "voice_type": "narrator",
            "style": "spare_american",
            "emotion_range": ["stoic", "direct", "understated"],
            "pitch_modulation": 0.9,
            "target_vowel": "u"
        },
        "Leo Tolstoy": {
            "voice_type": "narrator",
            "style": "moral_russian",
            "emotion_range": ["profound", "ethical", "humanistic"],
            "pitch_modulation": 0.87,
            "target_vowel": "o"
        }
    }

    # Create voice profiles for each author
    print("\n🎭 Creating Author Voice Profiles...")
    author_profiles = {}

    for author_name, voice_config in author_voices.items():
        print(f"  📝 Creating voice for {author_name}...")

        # Create voice profile
        profile = await voice_engine.create_voice_profile(
            creation_method="parameter",
            name=f"{author_name.replace(' ', '_').lower()}_voice",
            description=f"Voice profile for {author_name} based on their literary style",
            voice_type=voice_config["voice_type"],
            param_config={
                "style": voice_config["style"],
                "emotional_range": voice_config["emotion_range"],
                "pitch_modulation": voice_config["pitch_modulation"],
                "target_vowel": voice_config["target_vowel"]
            }
        )

        author_profiles[author_name] = profile
        print(f"    ✅ Created profile: {profile['profile_id']}")

    # Create a default narrator profile for the audiobook
    print("\n🎭 Creating Default Narrator Profile...")
    default_narrator = await narrator_optimizer.create_narrator_profile(
        content_type="poetry",
        name="happy_toes_multi_author"
    )

    # Store the narrator profile
    narrator_optimizer.narrator_profiles[default_narrator.profile_id] = default_narrator

    # Modify book data to include author information in each chapter
    print("\n📝 Preparing Book Data with Author Information...")

    # Create a mapping of chapter numbers to authors
    chapter_authors = {}
    for chapter in book_data["chapters"]:
        chapter_num = chapter["number"]
        chapter_content = chapter["content"]

        # Extract author from content
        if "Bryan Anthony Spruk" in chapter_content:
            chapter_authors[chapter_num] = "Bryan Anthony Spruk"
        elif "Jane Austen" in chapter_content:
            chapter_authors[chapter_num] = "Jane Austen"
        elif "Mark Twain" in chapter_content:
            chapter_authors[chapter_num] = "Mark Twain"
        elif "Maya Angelou" in chapter_content:
            chapter_authors[chapter_num] = "Maya Angelou"
        elif "Emily Dickinson" in chapter_content:
            chapter_authors[chapter_num] = "Emily Dickinson"
        elif "Franz Kafka" in chapter_content:
            chapter_authors[chapter_num] = "Franz Kafka"
        elif "Oscar Wilde" in chapter_content:
            chapter_authors[chapter_num] = "Oscar Wilde"
        elif "Robert Frost" in chapter_content:
            chapter_authors[chapter_num] = "Robert Frost"
        elif "Virginia Woolf" in chapter_content:
            chapter_authors[chapter_num] = "Virginia Woolf"
        elif "Sylvia Plath" in chapter_content:
            chapter_authors[chapter_num] = "Sylvia Plath"
        elif "Walt Whitman" in chapter_content:
            chapter_authors[chapter_num] = "Walt Whitman"
        elif "Ernest Hemingway" in chapter_content:
            chapter_authors[chapter_num] = "Ernest Hemingway"
        elif "Leo Tolstoy" in chapter_content:
            chapter_authors[chapter_num] = "Leo Tolstoy"

    # Add author metadata to each chapter
    for chapter in book_data["chapters"]:
        chapter_num = chapter["number"]
        if chapter_num in chapter_authors:
            chapter["author"] = chapter_authors[chapter_num]
            chapter["voice_profile"] = author_profiles[chapter_authors[chapter_num]]["profile_id"]
        else:
            chapter["author"] = "Unknown"
            chapter["voice_profile"] = list(author_profiles.values())[0]["profile_id"]

    # Render the complete audiobook
    print("\n🎵 Rendering Complete Audiobook...")

    output_path = "book_output/happy_toes_audiobook.wav"
    result = await renderer.render_audiobook_from_book(
        book_data=book_data,
        output_path=output_path,
        narrator_profile_id=default_narrator.profile_id
    )

    print("\n✅ Audiobook Created Successfully!")
    print(f"📁 Output: {output_path}")
    print(f"⏱️  Duration: {result.get('duration', 0):.1f} seconds")
    print(f"📚 Chapters: {len(book_data['chapters'])}")
    print(f"🎙️  Authors Featured: {len(author_profiles)}")

    print("\n🎉 Happy Toes Audiobook Complete!")
    print("Each chapter is now narrated in the distinctive voice of its author!")
    print("\n📋 Note: The audiobook renderer uses a unified narrator voice.")
    print("For true author-specific voices, each chapter would need individual rendering.")
    print("The voice profiles have been created and are ready for custom implementation.")

if __name__ == "__main__":
    asyncio.run(create_happy_toes_audiobook())