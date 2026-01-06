from .skg_manager import SpeakerKnowledgeGraph
from typing import List, Dict, Optional
import re
import time
from pathlib import Path

class AudiobookGenerator:
    def __init__(self, skg: SpeakerKnowledgeGraph):
        self.skg = skg
        self.cooldown_interval = 50  # Sentences before voice stability check

    def generate_audiobook(self, manuscript: str, config: Dict) -> str:
        """
        Generate a complete audiobook from manuscript

        config: {
            "title": "The Lean Startup",
            "author": "Eric Ries",
            "narrator_id": "phil_dandy",  // or "nonfiction_narrator"
            "genre": "non-fiction",
            "character_voice_map": {} // For fiction
        }
        """

        print(f"📚 Generating audiobook: {config['title']}")

        # 1. Pre-process manuscript
        chapters = self._segment_chapters(manuscript)

        # 2. Select voice mode and set narrator
        narrator_id = config["narrator_id"]
        self.skg.set_mode(narrator_id, "audiobook")  # Switch to audiobook traits

        chapter_audio_paths = []

        for i, chapter in enumerate(chapters, 1):
            print(f"   Chapter {i}/{len(chapters)}: {chapter['title'][:50]}...")

            # Generate chapter intro
            narrator = self.skg.get_persona(narrator_id)
            intro_template = narrator.get("mode_specific_traits", {}).get("audiobook", {}).get("chapter_intro_template", "Chapter {n}: {title}")
            intro_text = intro_template.format(n=i, title=chapter["title"])

            intro_path = self.skg.synthesize_as_persona(
                text=intro_text,
                persona_id=narrator_id,
                style="formal_announcement"
            )
            chapter_audio_paths.append(intro_path)

            # Generate chapter content with stability management
            content_path = self._generate_stable_long_form(
                text=chapter["content"],
                narrator_id=narrator_id,
                character_map=config.get("character_voice_map", {})
            )
            chapter_audio_paths.append(content_path)

            # Voice stability checkpoint
            if i % self.cooldown_interval == 0:
                self._voice_stability_checkpoint(narrator_id)

        # 3. Concatenate all chapters
        final_path = self._concatenate_chapters(
            chapter_audio_paths,
            output_filename=f"output/audiobooks/{config['title'].replace(' ', '_')}.mp3"
        )

        # 4. Embed metadata (for Audible/ACX compliance)
        self._embed_audiobook_metadata(final_path, config)

        return final_path

    def _segment_chapters(self, manuscript: str) -> List[Dict]:
        """Split manuscript into chapters using markdown or numbered headings"""
        chapters = []

        # Regex for chapter detection
        patterns = [
            r'^# (Chapter \d+: )?(.+)$',  # Markdown: # Chapter 1: Title
            r'^CHAPTER (\d+)\s*$[\s\S]*?^(?=\nCHAPTER \d+|\Z)'  # ALL CAPS
        ]

        for pattern in patterns:
            matches = list(re.finditer(pattern, manuscript, re.MULTILINE))
            if len(matches) > 3:  # Reasonable book length
                for i, match in enumerate(matches):
                    start = match.end()
                    end = matches[i+1].start() if i+1 < len(matches) else len(manuscript)
                    chapters.append({
                        "number": i+1,
                        "title": match.group(2).strip() if match.group(2) else f"Chapter {i+1}",
                        "content": manuscript[start:end].strip()
                    })
                break

        # Fallback: split by length if no clear chapters
        if not chapters:
            chunks = manuscript.split('\n\n')
            chunk_size = 10  # paragraphs per chunk
            for i in range(0, len(chunks), chunk_size):
                chapters.append({
                    "number": (i//chunk_size)+1,
                    "title": f"Part {(i//chunk_size)+1}",
                    "content": '\n\n'.join(chunks[i:i+chunk_size])
                })

        return chapters

    def _generate_stable_long_form(self, text: str, narrator_id: str, character_map: Dict) -> str:
        """
        Generate hours of audio with consistent voice quality.
        Coqui XTTS v2 has drift issues in long sessions—mitigate with segmentation.
        """
        paragraphs = text.split('\n\n')
        segment_paths = []

        for para_idx, paragraph in enumerate(paragraphs):
            # Handle direct speech (character voices for fiction)
            if character_map and '"' in paragraph:
                para_segments = self._handle_dialogue(paragraph, narrator_id, character_map)
                segment_paths.extend(para_segments)
            else:
                # Straight narration
                segment_path = self.skg.synthesize_as_persona(
                    text=paragraph,
                    persona_id=narrator_id,
                    style="audiobook_narration"
                )
                segment_paths.append(segment_path)

            # Insert natural pause between paragraphs
            narrator = self.skg.get_persona(narrator_id)
            pause_duration = narrator.get("mode_specific_traits", {}).get("audiobook", {}).get("pause_after_paragraph", 0.8)

            if pause_duration > 0:
                pause_path = self._generate_pause(duration=pause_duration)
                segment_paths.append(pause_path)

            # Progress indicator
            if para_idx % 20 == 0:
                print(f"     → {para_idx}/{len(paragraphs)} paragraphs complete")

        # Join segments
        return self.skg.concatenate_audio_segments(segment_paths)

    def _handle_dialogue(self, paragraph: str, narrator_id: str, character_map: Dict) -> List[str]:
        """
        Process quoted text with character-specific voices
        Example: He said, "I'll be back." → Narrator voice + Character voice
        """
        segments = []
        parts = re.split(r'(["][^"]*["])', paragraph)

        for part in parts:
            if part.startswith('"') and part.endswith('"'):
                # This is dialogue - find speaker
                speaker = self._identify_speaker(part, character_map)
                if speaker:
                    # Remove quotes and synthesize in character voice
                    char_text = part[1:-1]
                    path = self.skg.synthesize_as_character(
                        text=char_text,
                        character_id=speaker,
                        base_narrator_id=narrator_id
                    )
                    segments.append(path)
                    continue

            # Narration
            if part.strip():
                path = self.skg.synthesize_as_persona(part, narrator_id)
                segments.append(path)

        return segments

    def _identify_speaker(self, dialogue: str, character_map: Dict) -> Optional[str]:
        """Identify which character is speaking based on context"""
        # Simple heuristic: look for character names before quotes
        dialogue_lower = dialogue.lower()

        for char_name, char_id in character_map.items():
            if char_name.lower() in dialogue_lower:
                return char_id

        # Default to first character if none identified
        return list(character_map.values())[0] if character_map else None

    def _generate_pause(self, duration: float) -> str:
        """Generate a silent audio segment for pauses"""
        try:
            from pydub import AudioSegment
            pause = AudioSegment.silent(duration=int(duration * 1000))  # Convert to ms
            output_path = f"output/temp/pause_{abs(hash(str(duration)))}.wav"
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            pause.export(output_path, format="wav")
            return output_path
        except ImportError:
            print("⚠️  pydub not available for pause generation")
            return ""

    def _voice_stability_checkpoint(self, narrator_id: str):
        """
        Coqui XTTS can drift after ~1000 sentences. Re-clone voice to reset.
        """
        print("🔧 Voice stability checkpoint—recalibrating...")
        try:
            persona = self.skg.get_persona(narrator_id)
            if persona["voice_profile"].get("long_form_stabilization"):
                reference_wavs = persona["voice_profile"]["reference_wavs"]

                # Force re-clone to refresh voice model
                if self.skg.emitter and reference_wavs:
                    existing_refs = [wav for wav in reference_wavs if Path(wav).exists()]
                    if existing_refs:
                        self.skg.emitter.clone_voice(
                            speaker_wav=existing_refs[0],
                            speaker=persona["voice_profile"]["speaker_id"] + "_refresh"
                        )
                        time.sleep(2)  # Let GPU cool down
        except Exception as e:
            print(f"⚠️  Voice stability checkpoint failed: {e}")

    def _concatenate_chapters(self, chapter_paths: List[str], output_filename: str) -> str:
        """Concatenate chapter audio files into final audiobook"""
        try:
            from pydub import AudioSegment

            if not chapter_paths:
                raise ValueError("No audio segments to concatenate")

            # Load first segment
            combined = AudioSegment.from_wav(chapter_paths[0])

            # Add remaining segments
            for path in chapter_paths[1:]:
                if path and Path(path).exists():
                    segment = AudioSegment.from_wav(path)
                    combined += segment

            # Ensure output directory exists
            output_path = Path(output_filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Export final audiobook
            combined.export(str(output_path), format="mp3")

            # Clean up temporary files
            for path in chapter_paths:
                if path and Path(path).exists() and "temp" in path:
                    try:
                        Path(path).unlink()
                    except:
                        pass

            return str(output_path)

        except ImportError:
            print("❌ pydub required for audio concatenation")
            raise
        except Exception as e:
            print(f"❌ Audio concatenation failed: {e}")
            raise

    def _embed_audiobook_metadata(self, audio_path: str, config: Dict):
        """Embed metadata for audiobook platforms (Audible, ACX, etc.)"""
        try:
            from pydub import AudioSegment

            audio = AudioSegment.from_mp3(audio_path)

            # Add metadata tags
            tags = {
                "title": config["title"],
                "artist": config.get("author", "Unknown Author"),
                "album": config["title"],
                "genre": config.get("genre", "Audiobook"),
                "comment": f"Narrated by {self.skg.get_persona(config['narrator_id'])['name']}"
            }

            # Re-export with metadata
            audio.export(audio_path, format="mp3", tags=tags)

        except ImportError:
            print("⚠️  pydub not available for metadata embedding")
        except Exception as e:
            print(f"⚠️  Metadata embedding failed: {e}")


class FictionAudiobookGenerator(AudiobookGenerator):
    def __init__(self, skg: SpeakerKnowledgeGraph, manuscript_path: str):
        super().__init__(skg)
        from .dialogue_processor import DialogueProcessor
        self.dialogue_processor = DialogueProcessor(skg)
        self.manuscript_path = manuscript_path
        self.character_stats = {}  # Persistent across chapters

    def generate_fiction_audiobook(self, config: Dict) -> str:
        """
        config: {
            "title": "The Name of the Wind",
            "author": "Patrick Rothfuss",
            "narrator_id": "phil_dandy",
            "character_map": {
                "Kvothe": "young_heroine_lyra",
                "Gandarf": "elder_wizard_gandarf"
            },
            "auto_detect_characters": true
        }
        """

        # 1. Pre-scan manuscript to auto-detect characters
        if config.get("auto_detect_characters"):
            config["character_map"] = self._auto_detect_characters()

        # 2. Initialize character tracking
        self._initialize_character_tracking(config["character_map"])

        # 3. Process chapters with dialogue parsing
        chapters = self._load_and_parse_manuscript()

        for chapter in chapters:
            print(f"📖 Chapter {chapter['number']}: {chapter['title']}")

            # Build context for this chapter
            chapter_context = {
                "narrator": config["narrator_id"],
                "active_characters": self.character_stats,
                "last_speaker": None,
                "character_stats": self.character_stats
            }

            # Parse into segments
            segments = self.dialogue_processor.parse_scene(
                chapter["content"],
                chapter_context
            )

            # Generate audio per segment
            chapter_audio = self._generate_segmented_audio(segments, config)

            # Store for final assembly
            self.chapter_audio_paths.append(chapter_audio)

        return self._final_assemble_audiobook(config)

    def _auto_detect_characters(self) -> Dict[str, str]:
        """Use NLP to find character names and assign voices"""

        with open(self.manuscript_path, 'r') as f:
            text = f.read()

        # Extract proper nouns that appear before dialogue
        doc = nlp(text)
        character_names = {}

        for sent in doc.sents:
            if '"' in sent.text:
                # Find names in this sentence
                names = [ent.text for ent in sent.ents if ent.label_ == "PERSON"]
                if names:
                    char_name = names[0]
                    if char_name not in character_names:
                        # Assign voice from registry based on name patterns
                        char_id = self._assign_voice_by_name_pattern(char_name)
                        character_names[char_name] = char_id

        return character_names

    def _assign_voice_by_name_pattern(self, char_name: str) -> str:
        """Heuristic voice assignment based on character name"""

        # Check against SKG character registry rules
        skg_data = self.skg.skg_data
        rules = skg_data.get("character_voice_rules", {}).get("auto_assignment_rules", {})

        # Name pattern matching
        name_patterns = rules.get("name_patterns", {})
        for pattern, voice_id in name_patterns.items():
            if re.search(pattern, char_name, re.IGNORECASE):
                return voice_id

        # Vowel-starting names get lighter voices
        if char_name and char_name[0].upper() in "AEIOU":
            return "young_heroine_lyra"

        return "sly_merchant"  # Default

    def _load_and_parse_manuscript(self) -> List[Dict]:
        """Load manuscript and segment into chapters"""
        with open(self.manuscript_path, 'r') as f:
            manuscript = f.read()

        return self._segment_chapters(manuscript)

    def _generate_segmented_audio(self, segments: List[Dict], config: Dict) -> str:
        """Generate audio for each segment with proper voice handling"""

        segment_paths = []

        for seg in segments:
            if seg["type"] == "narration":
                path = self.skg.synthesize_as_persona(
                    text=seg["text"],
                    persona_id=config["narrator_id"],
                    style="audiobook_narration"
                )

            elif seg["type"] == "dialogue":
                # Apply emotion markers
                if seg["emotion"]:
                    text = self.dialogue_processor.apply_emotion_markers(
                        seg["text"], seg["emotion"], seg["speaker"]
                    )
                else:
                    text = seg["text"]

                path = self.skg.synthesize_as_character(
                    text=text,
                    character_id=seg["speaker"],
                    base_narrator_id=config["narrator_id"],
                    emotion=seg.get("emotion")
                )

            elif seg["type"] == "pause":
                path = self._generate_pause(seg["duration"])

            segment_paths.append(path)

        return self.skg.concatenate_audio_segments(segment_paths, crossfade=100)

    def _initialize_character_tracking(self, character_map: Dict):
        """Set up persistent stats for each character"""
        for char_name, char_id in character_map.items():
            self.character_stats[char_id] = {
                "name": char_name,
                "lines_spoken": 0,
                "first_appearance": None,
                "voice_consistency_hash": f"{char_id}_v1"
            }

    def _final_assemble_audiobook(self, config: Dict) -> str:
        """Assemble final audiobook with metadata"""
        output_filename = f"output/audiobooks/{config['title'].replace(' ', '_')}_fiction.mp3"
        final_path = self._concatenate_chapters(self.chapter_audio_paths, output_filename)
        self._embed_audiobook_metadata(final_path, config)
        return final_path