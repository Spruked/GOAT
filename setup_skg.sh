#!/bin/bash
echo "Setting up Phil & Jim Dandy Show SKG Environment (Enhanced Dual-Mode)..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p podcast_engine/coqui/reference_audio
mkdir -p podcast_engine/output/segments
mkdir -p podcast_engine/output/temp
mkdir -p podcast_engine/output/podcasts
mkdir -p podcast_engine/output/audiobooks
mkdir -p podcast_engine/output/acx
mkdir -p podcast_engine/assets

# Check if SKG core exists
if [ ! -f "podcast_engine/skg/skg_core.json" ]; then
    echo "❌ SKG core not found. Please ensure the SKG system is properly installed."
    exit 1
fi

echo "✅ Directory structure created!"

# Instructions
echo ""
echo "🎭 Phil & Jim Dandy Show SKG Setup Complete (Dual-Mode)!"
echo ""
echo "Next steps to get started:"
echo ""
echo "1. 🎤 Add Voice Reference Audio:"
echo "   Place voice samples in: podcast_engine/coqui/reference_audio/"
echo "   - phil_sample1.wav (2-3 minutes of Phil speaking - for podcasts)"
echo "   - phil_sample2.wav (different context)"
echo "   - jim_sample1.wav (2-3 minutes of Jim speaking - for podcasts)"
echo "   - jim_sample2.wav (different context)"
echo "   - audiobook_narrator_sample.wav (10-15 minutes for long-form narration)"
echo "   - character_voices/ (optional - for fiction audiobooks)"
echo "     - elder_wizard_sample.wav"
echo "     - young_heroine_sample.wav"
echo "     - sly_merchant_sample.wav"
echo ""
echo "2. 🎵 Add Production Audio (optional):"
echo "   - podcast_engine/assets/intro_music.mp3"
echo "   - podcast_engine/assets/outro_music.mp3"
echo "   - podcast_engine/assets/transition_sting.mp3"
echo ""
echo "3. 🧪 Test the System:"
echo "   cd podcast_engine"
echo "   python goat_orchestrator.py --test"
echo ""
echo "4. 🎛️ Tune Personas (optional):"
echo "   python persona_tuner.py phil_dandy base_pitch 0.98"
echo "   python persona_tuner.py jim_dandy speaking_rate 1.05"
echo ""
echo "5. 🚀 Generate Content:"
echo "   # Podcast from topic"
echo "   python goat_orchestrator.py --submission '{\"type\":\"podcast_topic\",\"content\":{\"title\":\"AI Tools\",\"key_points\":[\"AI\",\"automation\"]}}'"
echo ""
echo "   # Non-fiction audiobook"
echo "   python goat_orchestrator.py --submission '{\"type\":\"audiobook_manuscript\",\"content\":{\"title\":\"My Book\",\"text\":\"# Chapter 1\\n\\nBook content here.\",\"genre\":\"non-fiction\"}}'"
echo ""
echo "   # Fiction audiobook with character voices"
echo "   python goat_orchestrator.py --submission '{\"type\":\"audiobook_manuscript\",\"content\":{\"title\":\"Fantasy Novel\",\"manuscript_path\":\"manuscripts/fantasy_novel.txt\",\"genre\":\"fiction\",\"acx_package\":true}}'"
echo ""
echo "   # Batch processing"
echo "   python goat_orchestrator.py --batch submissions.json"
echo ""
echo "6. 📚 Audiobook Features:"
echo "   - Automatic chapter detection"
echo "   - Character voice switching for fiction"
echo "   - Emotional voice variants (angry, whispering, excited)"
echo "   - Long-form voice stability"
echo "   - ACX/Audible compliance validation"
echo "   - Professional packaging with credits and metadata"
echo "   - Retail sample generation"
echo ""
echo "For more information, see the SKG documentation in podcast_engine/skg/README.md"