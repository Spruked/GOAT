#!/usr/bin/env python3
"""
GOAT Orchestrator - Hybrid pipeline for podcasts and audiobooks
"""
import sys
import os
from pathlib import Path
from typing import Dict, Any
import argparse
import json

# Add paths for imports
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

from skg import SpeakerKnowledgeGraph, DandyShowGenerator, AudiobookGenerator, FictionAudiobookGenerator
from skg.acx_packager import ACXPackager
from skg.podcast_director import PodcastDirector
from skg.narrative_director import NarrativeDirector

class GOATOrchestrator:
    def __init__(self):
        self.skg = SpeakerKnowledgeGraph()
        self.podcast_gen = DandyShowGenerator(self.skg)
        self.audiobook_gen = AudiobookGenerator(self.skg)
        self.fiction_audiobook_gen = None  # Lazy-loaded
        self.acx_packager = ACXPackager(self.skg)
        self.podcast_director = PodcastDirector(self.skg)
        self.narrative_director = NarrativeDirector(self.skg)

    def process_submission(self, submission: Dict) -> str:
        """
        Process a user submission and generate appropriate content

        submission: {
            "type": "podcast_topic" | "audiobook_manuscript",
            "content": {...},
            "user_id": "..."
        }
        """

        content_type = self._classify_content(submission)

        if content_type == "podcast_topic":
            return self._handle_podcast(submission)
        elif content_type == "audiobook_manuscript":
            return self._handle_audiobook(submission)

    def generate_content(self, submission: Dict) -> str:
        """Unified entry point for all content generation"""

        content_type = submission.get("type", "podcast_topic")

        if content_type == "podcast_topic":
            # Use Podcast Director
            segments = self.podcast_director.direct_conversation_segment(submission["content"])
            return self._assemble_podcast(segments, submission.get("title", "Episode"))

        elif content_type == "audiobook_manuscript":
            # Use Narrative Director for narration
            chapter_context = {
                "title": submission["content"].get("title", "Chapter"),
                "chapter_number": submission["content"].get("chapter_number", 1),
                "genre": submission["content"].get("genre", "fiction")
            }

            narrator_id = self._select_narrator(submission["content"])
            text = submission["content"].get("text", "")

            if not text:
                raise ValueError("No text provided for narration")

            audio_segments = self.narrative_director.direct_narration(text, narrator_id, chapter_context)

            # Package with ACX compliance if requested
            if submission["content"].get("acx_package", False):
                # Convert segments to chapter format for ACX
                chapters = [{
                    "title": chapter_context["title"],
                    "audio_path": seg["audio_path"]
                } for seg in audio_segments]

                package_config = {
                    "title": submission["content"].get("title", "Audiobook"),
                    "author": submission["content"].get("author", "Unknown"),
                    "narrator_id": narrator_id,
                    "copyright": submission["content"].get("copyright", "2024"),
                    "isbn": submission["content"].get("isbn"),
                    "chapters": chapters,
                    "retail_sample_duration": 300
                }

                return self.acx_packager.package_audiobook_for_acx(package_config)

            return self._assemble_audiobook(audio_segments, submission["content"].get("title", "Audiobook"))

        else:
            raise ValueError(f"Unknown content type: {content_type}")

    def _assemble_podcast(self, segments: List[Dict], title: str) -> str:
        """Assemble directed podcast segments into final episode"""
        print(f"🎙️ Assembling podcast episode: {title}")

        # Concatenate all segments with pauses
        all_audio_paths = []
        for segment in segments:
            all_audio_paths.append(segment["audio_path"])
            # Add pause if specified
            if segment.get("pause_after", 0) > 0:
                pause_path = self.audiobook_gen._generate_pause(segment["pause_after"])
                if pause_path:
                    all_audio_paths.append(pause_path)

        # Final concatenation
        output_path = f"output/podcasts/{title.replace(' ', '_')}.mp3"
        final_path = self.audiobook_gen._concatenate_chapters(all_audio_paths, output_path)

        print(f"✅ Podcast assembled: {final_path}")
        return final_path

    def _assemble_audiobook(self, segments: List[Dict], title: str) -> str:
        """Assemble narrated segments into audiobook chapter"""
        print(f"📖 Assembling audiobook chapter: {title}")

        all_audio_paths = [seg["audio_path"] for seg in segments]

        output_path = f"output/audiobooks/{title.replace(' ', '_')}.mp3"
        final_path = self.audiobook_gen._concatenate_chapters(all_audio_paths, output_path)

        print(f"✅ Audiobook chapter assembled: {final_path}")
        return final_path

    def _classify_content(self, submission: Dict) -> str:
        """Classify content type based on submission data"""
        content = submission.get("content", {})

        # Explicit type override
        if "type" in submission:
            return submission["type"]

        # Heuristic classification
        if "manuscript" in content or "text" in content:
            text_length = len(content.get("text", ""))
            if text_length > 5000:  # Long form content
                return "audiobook_manuscript"

        # Check for podcast indicators
        if any(keyword in str(content).lower() for keyword in ["topic", "discussion", "interview"]):
            return "podcast_topic"

        # Default to podcast for shorter content
        return "podcast_topic"

    def _handle_podcast(self, submission: Dict) -> str:
        print("🎙️ Detected: Podcast topic")

        # Convert submission to topic format
        topic_data = {
            "title": submission["content"].get("title", "User Topic"),
            "description": submission["content"].get("description", ""),
            "submitter": submission.get("user_id", "GOAT User"),
            "category": submission["content"].get("category", "General"),
            "key_points": submission["content"].get("key_points", [])
        }

        segments = self.podcast_gen.generate_episode_segment(topic_data)
        return self._package_podcast(segments)

    def _handle_audiobook(self, submission: Dict) -> str:
        print("📚 Detected: Audiobook manuscript")

        # Determine genre
        genre = submission["content"].get("genre", "non-fiction")

        if genre == "fiction":
            # Use fiction-specific generator
            manuscript_path = submission["content"].get("manuscript_path")
            if not manuscript_path:
                raise ValueError("Fiction audiobooks require manuscript_path")

            if not self.fiction_audiobook_gen:
                self.fiction_audiobook_gen = FictionAudiobookGenerator(self.skg, manuscript_path)

            config = {
                "title": submission["content"]["title"],
                "author": submission["content"]["author"],
                "narrator_id": "phil_dandy",
                "auto_detect_characters": True,
                "character_map": submission["content"].get("character_map", {})
            }

            audio_path = self.fiction_audiobook_gen.generate_fiction_audiobook(config)
        else:
            # Non-fiction path
            config = {
                "title": submission["content"].get("title", "Untitled Book"),
                "author": submission["content"].get("author", "Anonymous"),
                "narrator_id": self._select_narrator(submission["content"]),
                "genre": genre,
                "character_voice_map": submission["content"].get("character_voice_map", {})
            }

            manuscript = submission["content"].get("text", "")
            if not manuscript:
                raise ValueError("No manuscript text provided")

            audio_path = self.audiobook_gen.generate_audiobook(
                manuscript=manuscript,
                config=config
            )

        # ACX packaging if requested
        if submission["content"].get("acx_package", False):
            chapters = self._extract_chapters_from_audio(audio_path, config)
            package_config = {
                "title": config["title"],
                "author": config["author"],
                "narrator_id": config["narrator_id"],
                "copyright": submission["content"].get("copyright", "2024"),
                "isbn": submission["content"].get("isbn"),
                "chapters": chapters,
                "retail_sample_duration": 300
            }

            final_package = self.acx_packager.package_audiobook_for_acx(package_config)
            return final_package

        return audio_path

    def _extract_chapters_from_audio(self, audio_path: str, config: Dict) -> List[Dict]:
        """Extract chapter information from generated audio for ACX packaging"""
        # For now, create a single chapter. In a full implementation,
        # this would split the audio into chapters based on the manuscript structure
        from pydub import AudioSegment
        import os

        audio = AudioSegment.from_file(audio_path)
        duration_seconds = len(audio) / 1000

        # Split into chapters (simple time-based splitting for demo)
        chapter_duration = duration_seconds / 10  # Assume 10 chapters max
        chapters = []

        for i in range(min(10, int(duration_seconds / chapter_duration) + 1)):
            start_time = i * chapter_duration * 1000
            end_time = min((i + 1) * chapter_duration * 1000, len(audio))

            if end_time > start_time:
                chapter_audio = audio[start_time:end_time]
                chapter_path = f"output/temp/chapter_{i+1:02d}.wav"
                os.makedirs("output/temp", exist_ok=True)
                chapter_audio.export(chapter_path, format="wav")

                chapters.append({
                    "title": f"Chapter {i+1}",
                    "audio_path": chapter_path
                })

        return chapters

    def _select_narrator(self, content: Dict) -> str:
        """Intelligently match narrator to content"""
        genre = content.get("genre", "").lower()

        # For business/tech content, use Phil or Jim
        if genre in ["business", "technology", "self-help"]:
            return "phil_dandy"

        # For creative/writing content, use Jim
        if genre in ["creative", "lifestyle", "memoir"]:
            return "jim_dandy"

        # For fiction, use dedicated fiction narrator
        if genre in ["fiction", "fantasy", "mystery"]:
            return "fiction_narrator"

        # Default to dedicated narrator
        return "nonfiction_narrator"

    def _package_podcast(self, segments: list) -> str:
        """Package podcast segments into final episode"""
        try:
            from pydub import AudioSegment
        except ImportError:
            raise RuntimeError("pydub required for podcast packaging")

        if not segments:
            raise ValueError("No segments to package")

        # Concatenate segments
        audio_paths = [s["audio_path"] for s in segments if s.get("audio_path")]
        if not audio_paths:
            raise ValueError("No audio files in segments")

        final_audio = self.skg.concatenate_audio_segments(audio_paths)

        # Add intro/outro if available
        final_audio = self._add_production_audio(final_audio)

        # Export as MP3
        output_dir = Path(__file__).parent / "output" / "podcasts"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"episode_{abs(hash(str(segments)))}.mp3"
        final_audio.export(str(output_path), format="mp3")

        return str(output_path)

    def _add_production_audio(self, audio):
        """Add intro/outro music and effects"""
        try:
            from pydub import AudioSegment

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

        except Exception as e:
            print(f"⚠️  Production audio addition failed: {e}")

        return audio

def process_batch_submissions(json_file: str):
    """Process a batch of submissions from JSON file"""
    with open(json_file, 'r') as f:
        submissions = json.load(f)

    orchestrator = GOATOrchestrator()

    results = []
    for i, submission in enumerate(submissions, 1):
        print(f"\n🔄 Processing submission {i}/{len(submissions)}")
        try:
            output_path = orchestrator.process_submission(submission)
            results.append({
                "submission_id": submission.get("id", i),
                "output_path": output_path,
                "status": "success"
            })
            print(f"✅ Generated: {output_path}")
        except Exception as e:
            results.append({
                "submission_id": submission.get("id", i),
                "error": str(e),
                "status": "failed"
            })
            print(f"❌ Failed: {e}")

    # Save results
    results_file = Path(json_file).parent / f"{Path(json_file).stem}_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📊 Batch processing complete. Results saved to: {results_file}")

def main():
    parser = argparse.ArgumentParser(description="GOAT Orchestrator - Hybrid content generation")
    parser.add_argument("--submission", "-s", help="Process single submission (JSON string)")
    parser.add_argument("--batch", "-b", help="Process batch submissions from JSON file")
    parser.add_argument("--test", action="store_true", help="Run test generation")

    args = parser.parse_args()

    orchestrator = GOATOrchestrator()

    if args.test:
        # Generate test content
        print("🧪 Running test generation...")

        # Test podcast
        podcast_submission = {
            "type": "podcast_topic",
            "content": {
                "title": "AI-Powered Code Review",
                "description": "Intelligent tool for automated code reviews",
                "category": "AI/ML",
                "key_points": ["AI", "machine learning", "code review"]
            }
        }

        try:
            podcast_output = orchestrator.process_submission(podcast_submission)
            print(f"✅ Podcast test: {podcast_output}")
        except Exception as e:
            print(f"❌ Podcast test failed: {e}")

        # Test audiobook (short excerpt)
        audiobook_submission = {
            "type": "audiobook_manuscript",
            "content": {
                "title": "Test Book",
                "author": "Test Author",
                "genre": "non-fiction",
                "text": "# Chapter 1: Introduction\n\nThis is a test manuscript for audiobook generation.\n\n\"Hello world,\" said the character.\n\nThis demonstrates the voice switching capability."
            }
        }

        try:
            audiobook_output = orchestrator.process_submission(audiobook_submission)
            print(f"✅ Audiobook test: {audiobook_output}")
        except Exception as e:
            print(f"❌ Audiobook test failed: {e}")

    elif args.submission:
        # Process single submission
        submission = json.loads(args.submission)
        output_path = orchestrator.process_submission(submission)
        print(f"✅ Generated: {output_path}")

    elif args.batch:
        # Process batch file
        process_batch_submissions(args.batch)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()