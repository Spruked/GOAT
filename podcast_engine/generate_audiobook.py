import sys
from pathlib import Path
from skg.skg_manager import SpeakerKnowledgeGraph
from skg.audiobook_generator import AudiobookGenerator

# --- CONFIG ---
MANUSCRIPT_PATH = Path(__file__).parent / "audiobook_input" / "sample_novel.txt"
CONFIG = {
    "title": "Sample Novel",
    "author": "Jane Doe",
    "narrator_id": "fiction_narrator",  # Change to your narrator persona
    "genre": "fiction",
    "character_voice_map": {
        "Alice": "alice_voice",  # Change to your SKG character IDs
        "Bob": "bob_voice"
    }
}

if __name__ == "__main__":
    # 1. Load manuscript
    with open(MANUSCRIPT_PATH, "r", encoding="utf-8") as f:
        manuscript = f.read()

    # 2. Initialize SKG
    skg = SpeakerKnowledgeGraph()

    # 3. Generate audiobook
    generator = AudiobookGenerator(skg)
    output_path = generator.generate_audiobook(manuscript, CONFIG)
    print(f"\n✅ Audiobook generated: {output_path}")
