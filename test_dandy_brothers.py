"""Test script for the Phil and Jim Dandy Show podcast"""
from podcast_engine import PodcastEngine, LegacyInput

def test_dandy_brothers_show():
    """Generate a sample episode of The Phil and Jim Dandy Show"""
    
    engine = PodcastEngine()
    
    user_input = LegacyInput(
        topic="The Phil and Jim Dandy Show - Daily Fishing Adventures",
        notes="Phil and Jim Dandy are fishing brothers who share their daily fishing stories, techniques, and adventures on the water",
        source_materials=[],
        intent="podcast",
        audience="fishing enthusiasts and outdoor lovers",
        tone="casual and entertaining",
        length_estimate="medium",
        create_audiobook=True,
        voice=None,
        output_format="podcast"
    )
    
    print("🎙️  Generating The Phil and Jim Dandy Show...")
    result = engine.create_legacy(user_input)
    
    print(f"\n✅ Episode Created!")
    print(f"📁 Archive: {result['archive_path']}")
    print(f"🎵 Audio: {result['audiobook_path']}")
    print(f"📊 Word Count: {result['artifact']['word_count']}")
    print(f"⏱️  Duration: {result['artifact']['estimated_time']}")
    
    # Show a preview of the content
    print("\n📝 Content Preview:")
    print("=" * 60)
    content = result['artifact']['full_content']
    preview = content[:800] + "..." if len(content) > 800 else content
    print(preview)
    print("=" * 60)

if __name__ == "__main__":
    test_dandy_brothers_show()
