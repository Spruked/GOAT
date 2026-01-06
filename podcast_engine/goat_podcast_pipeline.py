#!/usr/bin/env python3
"""
GOAT Podcast Pipeline - Integrates SKG with GOAT content system
"""
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import argparse

# Add paths for imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

from skg.skg_manager import SpeakerKnowledgeGraph
from skg.dandy_show_generator import DandyShowGenerator

def generate_weekly_podcast(topics: List[Dict] = None, test_mode: bool = False):
    """Main pipeline for GOAT system"""

    print("🎙️  Initializing Phil & Jim Dandy Show SKG...")

    # 1. Initialize SKG
    skg = SpeakerKnowledgeGraph()

    # 2. Get topics (from GOAT system or test data)
    if topics is None:
        if test_mode:
            topics = get_test_topics()
        else:
            # Try to import GOAT content ingestor
            try:
                from content_manager import GOATContentIngestor
                ingestor = GOATContentIngestor()
                topics = ingestor.get_submissions(limit=5)
            except ImportError:
                print("⚠️  GOAT content manager not found, using test topics")
                topics = get_test_topics()

    print(f"📥 Found {len(topics)} topics for this episode")

    # 3. Generate segments for each topic
    generator = DandyShowGenerator(skg)
    all_segments = []

    for i, topic in enumerate(topics, 1):
        print(f"🎙️  Generating segment {i}/{len(topics)}: {topic['title']}")
        segments = generator.generate_episode_segment(topic)
        all_segments.extend(segments)

    # 4. Concatenate with transitions
    print("🎵 Concatenating segments with transitions...")
    final_audio = concatenate_with_transitions(all_segments)

    # 5. Add intro/outro
    print("📦 Adding production packaging...")
    final_audio = add_production_packaging(final_audio)

    # 6. Export and upload
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "podcast_episode_001.mp3"
    final_audio.export(str(output_file), format="mp3")

    print(f"✅ Episode complete: {output_file}")
    print(f"📊 Total duration: {len(final_audio)/1000:.1f} seconds")

    return str(output_file)

def get_test_topics() -> List[Dict]:
    """Generate test topics for development"""
    return [
        {
            "title": "The GOAT System",
            "description": "A modular, multi-persona AI orchestrator for content and teams. GOAT features a host assistant bubble, SM-P1 plugin architecture, and seamless integration with social platforms. It enables autonomous teams and next-gen content creation.",
            "submitter": "@goat_team",
            "category": "AI/Orchestration",
            "key_points": ["GOAT", "autonomous teams", "content creation", "SM-P1"]
        }
    ]

def concatenate_with_transitions(segments: List[Dict]):
    """Combine audio segments with music beds and transitions"""
    try:
        from pydub import AudioSegment
    except ImportError:
        print("❌ pydub required for audio processing")
        raise

    full_episode = AudioSegment.silent(duration=1000)  # 1s silence

    for i, segment in enumerate(segments):
        if segment["audio_path"] and os.path.exists(segment["audio_path"]):
            audio = AudioSegment.from_wav(segment["audio_path"])
            full_episode += audio

            # Add short transition between topics
            if segment["type"] == "closing" and i < len(segments) - 1:
                # Try to add transition music if available
                transition_path = Path(__file__).parent / "assets" / "transition_sting.mp3"
                if transition_path.exists():
                    transition = AudioSegment.from_mp3(str(transition_path))
                    full_episode += transition
                else:
                    # Short silence instead
                    full_episode += AudioSegment.silent(duration=500)
        else:
            print(f"⚠️  Skipping segment with missing audio: {segment['speaker']}")

    return full_episode

def add_production_packaging(audio):
    """Add intro/outro music and metadata"""
    try:
        from pydub import AudioSegment
    except ImportError:
        print("❌ pydub required for audio processing")
        return audio

    # Try to add intro music
    intro_path = Path(__file__).parent / "assets" / "intro_music.mp3"
    if intro_path.exists():
        intro = AudioSegment.from_mp3(str(intro_path))
        audio = intro + audio

    # Try to add outro music
    outro_path = Path(__file__).parent / "assets" / "outro_music.mp3"
    if outro_path.exists():
        outro = AudioSegment.from_mp3(str(outro_path))
        audio = audio + outro

    return audio

def setup_skg_environment():
    """Setup the SKG environment with required directories"""
    print("Setting up Phil & Jim Dandy Show SKG environment...")

    # Create directory structure
    dirs = [
        "coqui/reference_audio",
        "output/segments",
        "assets"
    ]

    for dir_path in dirs:
        full_path = Path(__file__).parent / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {full_path}")

    print("✅ Environment setup complete!")
    print("\nNext steps:")
    print("1. Add reference audio files to coqui/reference_audio/")
    print("2. Add intro/outro music to assets/")
    print("3. Run: python goat_podcast_pipeline.py --test")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GOAT Podcast Pipeline")
    parser.add_argument("--test", action="store_true", help="Run with test topics")
    parser.add_argument("--setup", action="store_true", help="Setup SKG environment")

    args = parser.parse_args()

    if args.setup:
        setup_skg_environment()
    else:
        try:
            output_file = generate_weekly_podcast(test_mode=args.test)
            print(f"\n🎉 Podcast generated successfully: {output_file}")
        except Exception as e:
            print(f"❌ Error generating podcast: {e}")
            sys.exit(1)