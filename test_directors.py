#!/usr/bin/env python3
"""
Test script for Podcast Director and Narrative Director
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from goat_core.goat_orchestrator import GOATOrchestrator

def test_podcast_director():
    """Test the podcast director with a sample topic"""
    print("🎬 Testing Podcast Director...")

    orchestrator = GOATOrchestrator()

    # Sample podcast submission
    submission = {
        "type": "podcast_topic",
        "title": "AI in Healthcare",
        "content": {
            "title": "AI in Healthcare",
            "description": "How artificial intelligence is transforming medical diagnosis and treatment",
            "key_points": [
                "AI can analyze medical images faster than humans",
                "Machine learning helps predict patient outcomes",
                "Ethical considerations in AI medical decisions"
            ]
        }
    }

    try:
        result_path = orchestrator.generate_content(submission)
        print(f"✅ Podcast generated: {result_path}")
    except Exception as e:
        print(f"❌ Podcast generation failed: {e}")

def test_narrative_director():
    """Test the narrative director with sample text"""
    print("📖 Testing Narrative Director...")

    orchestrator = GOATOrchestrator()

    # Sample audiobook submission
    submission = {
        "type": "audiobook_manuscript",
        "content": {
            "title": "Test Chapter",
            "text": "The ancient castle stood on the hill, its towers reaching toward the stormy sky. Thunder rumbled in the distance as the young hero approached the massive wooden doors. 'Who goes there?' called a voice from within. The hero took a deep breath and replied, 'I seek the wizard Gandarf.' Suddenly, the doors creaked open, revealing a dimly lit hallway.",
            "chapter_number": 1,
            "genre": "fantasy",
            "narrator_id": "phil_dandy"
        }
    }

    try:
        result_path = orchestrator.generate_content(submission)
        print(f"✅ Audiobook narration generated: {result_path}")
    except Exception as e:
        print(f"❌ Audiobook generation failed: {e}")

def test_fiction_audiobook():
    """Test fiction audiobook generation"""
    print("📚 Testing Fiction Audiobook Generation...")

    orchestrator = GOATOrchestrator()

    # Sample fiction manuscript (create a temporary file)
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("""
        The young heroine Lyra stood at the edge of the forest, her heart pounding with fear. "I must be brave," she whispered to herself.

        Suddenly, a mysterious stranger appeared from the shadows. "What brings you to these woods, child?" he asked in a deep, rumbling voice.

        Lyra took a step back. "I'm looking for the elder wizard Gandarf. Can you help me?"

        The stranger smiled mysteriously. "Ah, Gandarf. He lives in the castle on the hill. But beware—the path is dangerous."
        """)
        manuscript_path = f.name

    submission = {
        "type": "audiobook_manuscript",
        "content": {
            "title": "The Wizard's Quest",
            "author": "Test Author",
            "manuscript_path": manuscript_path,
            "genre": "fiction",
            "auto_detect_characters": True
        }
    }

    try:
        result_path = orchestrator.generate_content(submission)
        print(f"✅ Fiction audiobook generated: {result_path}")
    except Exception as e:
        print(f"❌ Fiction audiobook generation failed: {e}")
    finally:
        # Clean up temp file
        try:
            os.unlink(manuscript_path)
        except:
            pass

if __name__ == "__main__":
    print("🎭 GOAT Director Intelligence Test Suite")
    print("=" * 50)

    # Test each director
    test_podcast_director()
    print()
    test_narrative_director()
    print()
    test_fiction_audiobook()

    print("\n🎉 Director tests complete!")