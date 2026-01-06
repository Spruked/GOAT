# engines/audiobook_renderer.py
"""
Audiobook Renderer: Combines voice synthesis, character mapping, and narrator optimization
for complete audiobook production
"""

import os
import json
import asyncio
import tempfile
import re
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
import wave
import struct
import numpy as np
from datetime import datetime

@dataclass
class AudiobookSegment:
    """Individual segment of the audiobook"""
    segment_id: str
    segment_type: str  # "narrator", "character_dialogue", "sound_effect"
    text: str
    audio_data: bytes
    duration: float
    start_time: float
    end_time: float
    metadata: Dict[str, Any]

@dataclass
class AudiobookChapter:
    """Chapter containing multiple segments"""
    chapter_number: int
    title: str
    segments: List[AudiobookSegment]
    total_duration: float
    metadata: Dict[str, Any]

class AudiobookRenderer:
    """
    Renders complete audiobooks by combining voice synthesis, character mapping,
    and narrator optimization
    """

    def __init__(self, voice_engine, character_mapper, narrator_optimizer, cpu_mode=True):
        self.voice_engine = voice_engine
        self.character_mapper = character_mapper
        self.narrator_optimizer = narrator_optimizer

        # CPU optimization settings
        self.cpu_mode = cpu_mode
        self.CHUNK_SIZE = 200 if cpu_mode else 1000  # Characters per chunk
        self.BATCH_SIZE = 1 if cpu_mode else 5       # Chunks to process simultaneously
        self.REST_INTERVAL = 5 if cpu_mode else 1    # Seconds between chunks

        self.temp_dir = Path("./temp")
        self.temp_dir.mkdir(exist_ok=True)

    async def render_audiobook_from_book(
        self,
        book_data: Dict[str, Any],
        output_path: str,
        narrator_profile_id: str = "narrator_nonfiction_default"
    ) -> Dict[str, Any]:
        """
        Render complete audiobook from book data structure
        """
        print("🎵 Starting audiobook rendering process...")

        # 1. Extract chapters and content
        chapters = self._extract_chapters(book_data)

        # 2. Get narrator profile
        narrator_profile = self.narrator_optimizer.narrator_profiles.get(narrator_profile_id)
        if not narrator_profile:
            narrator_profile = await self.narrator_optimizer.create_narrator_profile(
                content_type="nonfiction",
                name="default"
            )

        # 3. Process each chapter
        audiobook_chapters = []
        total_duration = 0.0

        for chapter_num, chapter_data in enumerate(chapters, 1):
            print(f"📖 Processing chapter {chapter_num}: {chapter_data['title']}")

            if self.cpu_mode:
                # Use CPU-safe chunked rendering
                chapter = await self._render_chapter_cpu_safe(
                    chapter_data, narrator_profile, chapter_num
                )
            else:
                # Use standard rendering
                chapter = await self._render_chapter(
                    chapter_data, narrator_profile, chapter_num
                )

            audiobook_chapters.append(chapter)
            total_duration += chapter.total_duration

            # CPU: Add rest between chapters to prevent overheating
            if self.cpu_mode and chapter_num < len(chapters):
                print(f"⏸️ Chapter rest period... ({self.REST_INTERVAL * 2} seconds)")
                await asyncio.sleep(self.REST_INTERVAL * 2)

        # 4. Combine chapters into final audiobook
        final_audio = await self._combine_chapters(audiobook_chapters)

        # 5. Export final audiobook
        await self._export_audiobook(final_audio, output_path, book_data, total_duration)

        # 6. Generate metadata
        metadata = self._generate_audiobook_metadata(
            book_data, audiobook_chapters, total_duration
        )

        print("✅ Audiobook rendering complete!")
        return {
            "output_path": output_path,
            "total_duration": total_duration,
            "chapters": len(audiobook_chapters),
            "total_segments": sum(len(chapter.segments) for chapter in audiobook_chapters),
            "metadata": metadata
        }

    async def _render_chapter(
        self,
        chapter_data: Dict[str, Any],
        narrator_profile,
        chapter_num: int
    ) -> AudiobookChapter:
        """
        Render a single chapter
        """
        segments = []
        current_time = 0.0

        # Add chapter title
        if chapter_data.get("title"):
            title_audio = await self.narrator_optimizer.generate_narrator_audio(
                text=f"Chapter {chapter_num}: {chapter_data['title']}",
                narrator_profile=narrator_profile,
                segment_type="heading"
            )

            title_duration = self._get_audio_duration(title_audio)
            segments.append(AudiobookSegment(
                segment_id=f"ch{chapter_num}_title",
                segment_type="narrator",
                text=f"Chapter {chapter_num}: {chapter_data['title']}",
                audio_data=title_audio,
                duration=title_duration,
                start_time=current_time,
                end_time=current_time + title_duration,
                metadata={"segment_type": "chapter_title"}
            ))
            current_time += title_duration + 1.0  # 1 second pause

        # Process chapter content
        content_segments = await self._process_chapter_content(
            chapter_data["content"], narrator_profile
        )

        for segment in content_segments:
            segment.start_time = current_time
            segment.end_time = current_time + segment.duration
            segments.append(segment)
            current_time += segment.duration + 0.5  # 0.5 second pause between segments

        return AudiobookChapter(
            chapter_number=chapter_num,
            title=chapter_data["title"],
            segments=segments,
            total_duration=current_time,
            metadata={
                "content_type": chapter_data.get("content_type", "mixed"),
                "word_count": chapter_data.get("word_count", 0)
            }
        )

    async def _render_chapter_cpu_safe(
        self,
        chapter_data: Dict[str, Any],
        narrator_profile,
        chapter_num: int
    ) -> AudiobookChapter:
        """
        CPU-safe chapter rendering with small chunks and rest intervals
        """
        print(f"🖥️ CPU-Safe rendering chapter {chapter_num}: {chapter_data['title']}")

        segments = []
        current_time = 0.0

        # Add chapter title (process immediately, no chunking needed)
        if chapter_data.get("title"):
            title_audio = await self.narrator_optimizer.generate_narrator_audio(
                text=f"Chapter {chapter_num}: {chapter_data['title']}",
                narrator_profile=narrator_profile,
                segment_type="heading"
            )

            title_duration = self._get_audio_duration(title_audio)
            segments.append(AudiobookSegment(
                segment_id=f"ch{chapter_num}_title",
                segment_type="narrator",
                text=f"Chapter {chapter_num}: {chapter_data['title']}",
                audio_data=title_audio,
                duration=title_duration,
                start_time=current_time,
                end_time=current_time + title_duration,
                metadata={"segment_type": "chapter_title"}
            ))
            current_time += title_duration + 1.0  # 1 second pause

        # Process chapter content in small chunks
        content = chapter_data["content"]
        content_chunks = self._split_text_into_chunks(content, self.CHUNK_SIZE)

        print(f"📦 Split chapter into {len(content_chunks)} chunks of ~{self.CHUNK_SIZE} characters each")

        for i, chunk in enumerate(content_chunks):
            print(f"🔄 Processing chunk {i+1}/{len(content_chunks)}: {chunk[:50]}...")

            # Process one chunk at a time
            chunk_segments = await self._process_chapter_chunk_cpu_safe(
                chunk, narrator_profile, chapter_num, i
            )

            # Add segments with timing
            for segment in chunk_segments:
                segment.start_time = current_time
                segment.end_time = current_time + segment.duration
                segments.append(segment)
                current_time += segment.duration + 0.5  # 0.5 second pause

            # CPU REST: Prevent thermal throttling
            if i % 3 == 0 and i > 0:  # Every 3 chunks
                print(f"⏸️ CPU rest period... ({self.REST_INTERVAL} seconds)")
                await asyncio.sleep(self.REST_INTERVAL)

        return AudiobookChapter(
            chapter_number=chapter_num,
            title=chapter_data["title"],
            segments=segments,
            total_duration=current_time,
            metadata={
                "content_type": chapter_data.get("content_type", "mixed"),
                "word_count": chapter_data.get("word_count", 0),
                "cpu_optimized": True,
                "chunks_processed": len(content_chunks)
            }
        )

    def _split_text_into_chunks(self, text: str, chunk_size: int) -> List[str]:
        """
        Split text into chunks of approximately chunk_size characters,
        trying to break at sentence boundaries
        """
        import re

        chunks = []
        remaining = text

        while len(remaining) > chunk_size:
            # Find the best break point within the chunk size
            chunk = remaining[:chunk_size]

            # Try to break at sentence end
            sentence_end = re.search(r'[.!?]\s', chunk[::-1])
            if sentence_end:
                break_pos = chunk_size - sentence_end.start()
                chunk = remaining[:break_pos]
                remaining = remaining[break_pos:].lstrip()
            else:
                # Break at word boundary
                word_boundary = re.search(r'\s\S*$', chunk)
                if word_boundary:
                    break_pos = word_boundary.start()
                    chunk = remaining[:break_pos]
                    remaining = remaining[break_pos:].lstrip()
                else:
                    # Force break
                    chunk = remaining[:chunk_size]
                    remaining = remaining[chunk_size:]

            chunks.append(chunk)

        if remaining.strip():
            chunks.append(remaining.strip())

        return chunks

    async def _process_chapter_chunk_cpu_safe(
        self,
        chunk: str,
        narrator_profile,
        chapter_num: int,
        chunk_index: int
    ) -> List[AudiobookSegment]:
        """
        Process a single text chunk into audio segments (CPU-safe)
        """
        segments = []

        # For CPU mode, treat everything as narrator text to avoid voice switching complexity
        # This prevents the "single voice" issue by using consistent narration

        if chunk.strip():
            # Generate audio for this chunk
            audio_data = await self.narrator_optimizer.generate_narrator_audio(
                text=chunk,
                narrator_profile=narrator_profile,
                segment_type="narrative"
            )

            duration = self._get_audio_duration(audio_data)

            segments.append(AudiobookSegment(
                segment_id=f"ch{chapter_num}_chunk{chunk_index}",
                segment_type="narrator",
                text=chunk,
                audio_data=audio_data,
                duration=duration,
                start_time=0.0,  # Will be set by caller
                end_time=duration,
                metadata={
                    "segment_type": "narrative_chunk",
                    "cpu_chunk": True,
                    "chunk_index": chunk_index
                }
            ))

        return segments

    async def _process_chapter_content(
        self,
        content: str,
        narrator_profile
    ) -> List[AudiobookSegment]:
        """
        Process chapter content into audio segments
        """
        segments = []

        # Check if content contains dialogue
        if self._has_dialogue(content):
            # Process as fiction with dialogue
            dialogue_segments = await self.character_mapper.process_dialogue_script(content)

            for i, dialogue_segment in enumerate(dialogue_segments):
                try:
                    audio_data = await self.character_mapper.generate_character_audio(
                        character_name=dialogue_segment.character,
                        text=dialogue_segment.text,
                        emotion=dialogue_segment.emotion
                    )

                    duration = self._get_audio_duration(audio_data)
                    segments.append(AudiobookSegment(
                        segment_id=f"dialogue_{i:03d}",
                        segment_type="character_dialogue",
                        text=dialogue_segment.text,
                        audio_data=audio_data,
                        duration=duration,
                        start_time=0.0,  # Will be set by caller
                        end_time=0.0,
                        metadata={
                            "character": dialogue_segment.character,
                            "emotion": dialogue_segment.emotion,
                            "context": dialogue_segment.context
                        }
                    ))
                except Exception as e:
                    print(f"Failed to generate dialogue audio for {dialogue_segment.character}: {e}")
                    continue
        else:
            # Process as nonfiction narration
            text_segments = await self.narrator_optimizer.analyze_text_segments(
                content, narrator_profile.content_type
            )

            optimizations = await self.narrator_optimizer.optimize_narration(
                text_segments, narrator_profile
            )

            for i, opt in enumerate(optimizations["optimizations"]):
                try:
                    audio_data = await self.narrator_optimizer.generate_narrator_audio(
                        text=opt["text"],
                        narrator_profile=narrator_profile,
                        segment_type=opt["segment_type"],
                        technical_terms=[guide["term"] for guide in opt["technical_enhancements"]["pronunciation_guides"]]
                    )

                    duration = self._get_audio_duration(audio_data)
                    segments.append(AudiobookSegment(
                        segment_id=f"narrator_{i:03d}",
                        segment_type="narrator",
                        text=opt["text"],
                        audio_data=audio_data,
                        duration=duration,
                        start_time=0.0,
                        end_time=0.0,
                        metadata={
                            "segment_type": opt["segment_type"],
                            "complexity_score": opt.get("complexity_score", 0.0),
                            "reading_speed": opt["narrator_settings"]["reading_speed"],
                            "technical_terms": len(opt["technical_enhancements"]["pronunciation_guides"])
                        }
                    ))
                except Exception as e:
                    print(f"Failed to generate narrator audio for segment {i}: {e}")
                    continue

        return segments

    def _has_dialogue(self, content: str) -> bool:
        """Check if content contains dialogue"""
        # Look for quotation marks and dialogue patterns
        dialogue_indicators = [
            r'"[^"]*"',  # Double quotes
            r"'[^']*'",  # Single quotes
            r'[A-Z][a-z]+:\s*".*"',  # CHARACTER: "dialogue"
            r'"[^"]*",?\s*(said|asked|replied)',  # "dialogue," said
        ]

        for pattern in dialogue_indicators:
            if re.search(pattern, content):
                return True

        return False

    async def _combine_chapters(self, chapters: List[AudiobookChapter]) -> bytes:
        """
        Combine chapter audio into single audiobook file
        """
        print("🔗 Combining chapters into final audiobook...")

        all_audio_data = []

        for chapter in chapters:
            # Add chapter intro pause (2 seconds)
            all_audio_data.extend([0] * int(22050 * 2))  # 2 seconds of silence at 22kHz

            for segment in chapter.segments:
                # Convert audio bytes to numpy array
                audio_array = self._bytes_to_audio_array(segment.audio_data)
                all_audio_data.extend(audio_array)

                # Add segment pause (0.5 seconds)
                all_audio_data.extend([0] * int(22050 * 0.5))

        # Convert back to bytes
        return self._audio_array_to_bytes(np.array(all_audio_data))

    async def _export_audiobook(
        self,
        audio_data: bytes,
        output_path: str,
        book_metadata: Dict[str, Any],
        total_duration: float
    ):
        """
        Export final audiobook with metadata
        """
        print(f"💾 Exporting audiobook to {output_path}...")

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Write WAV file
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(22050)
            wav_file.writeframes(audio_data)

        # Generate metadata file
        metadata_path = Path(output_path).with_suffix('.json')
        metadata = {
            "book_title": book_metadata.get("title", "Unknown Title"),
            "author": book_metadata.get("author", "Unknown Author"),
            "total_duration_seconds": total_duration,
            "total_duration_formatted": self._format_duration(total_duration),
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "voice_engine": "GOAT POM 2.0 Integration",
            "sample_rate": 22050,
            "channels": 1,
            "bit_depth": 16
        }

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def _generate_audiobook_metadata(
        self,
        book_data: Dict[str, Any],
        chapters: List[AudiobookChapter],
        total_duration: float
    ) -> Dict[str, Any]:
        """
        Generate comprehensive audiobook metadata
        """
        return {
            "book_info": {
                "title": book_data.get("title", "Unknown"),
                "author": book_data.get("author", "Unknown"),
                "genre": book_data.get("genre", "Unknown"),
                "description": book_data.get("description", "")
            },
            "audiobook_info": {
                "total_duration": total_duration,
                "total_chapters": len(chapters),
                "total_segments": sum(len(chapter.segments) for chapter in chapters),
                "average_chapter_duration": total_duration / len(chapters) if chapters else 0,
                "generated_at": datetime.utcnow().isoformat() + "Z"
            },
            "voice_info": {
                "engine": "GOAT Voice Engine with POM 2.0",
                "character_voices": len(self.character_mapper.characters),
                "narrator_profiles": len(self.narrator_optimizer.narrator_profiles)
            },
            "chapters": [
                {
                    "number": chapter.chapter_number,
                    "title": chapter.title,
                    "duration": chapter.total_duration,
                    "segments": len(chapter.segments),
                    "content_type": chapter.metadata.get("content_type", "unknown")
                }
                for chapter in chapters
            ]
        }

    def _extract_chapters(self, book_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract chapters from book data"""
        chapters = []

        # Try different chapter formats
        if "chapters" in book_data:
            chapters = book_data["chapters"]
        elif "content" in book_data:
            # Split content into chapters if not already split
            content = book_data["content"]
            if isinstance(content, str):
                # Simple chapter detection
                chapter_texts = re.split(r'(?=Chapter \d+)', content)
                for i, chapter_text in enumerate(chapter_texts):
                    if chapter_text.strip():
                        chapters.append({
                            "title": f"Chapter {i+1}",
                            "content": chapter_text.strip(),
                            "content_type": "nonfiction"
                        })
            else:
                chapters = content
        else:
            # Treat entire book as one chapter
            chapters = [{
                "title": "Main Content",
                "content": book_data.get("text", ""),
                "content_type": "nonfiction"
            }]

        return chapters

    def _get_audio_duration(self, audio_bytes: bytes) -> float:
        """Calculate duration of audio data in seconds"""
        # Assuming 16-bit mono at 22kHz
        sample_rate = 22050
        bytes_per_sample = 2
        num_samples = len(audio_bytes) // bytes_per_sample
        return num_samples / sample_rate

    def _bytes_to_audio_array(self, audio_bytes: bytes) -> np.ndarray:
        """Convert audio bytes to numpy array"""
        # Assuming 16-bit signed integers
        return np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

    def _audio_array_to_bytes(self, audio_array: np.ndarray) -> bytes:
        """Convert numpy array to audio bytes"""
        # Convert back to 16-bit signed integers
        return (audio_array * 32767).astype(np.int16).tobytes()

    def _format_duration(self, seconds: float) -> str:
        """Format duration in HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return "04d"

    async def render_preview(
        self,
        text: str,
        voice_profile_id: str,
        output_path: str,
        emotion: str = "neutral"
    ) -> Dict[str, Any]:
        """
        Render a short preview of voice synthesis
        """
        print("🎧 Generating voice preview...")

        # Check if profile exists, create default narrator profile if not
        try:
            profile = await self.voice_engine.get_profile(voice_profile_id)
        except FileNotFoundError:
            if "narrator" in voice_profile_id:
                # Create a default narrator profile
                result = await self.voice_engine.create_voice_profile(
                    creation_method="parameter",
                    name="Default Narrator",
                    description="Default narrator voice for previews",
                    voice_type="narrator",
                    param_config={
                        "tension": 0.6,
                        "breathiness": 0.2,
                        "vibrato_rate": 4.0,
                        "lip_rounding": 0.4,
                        "articulation_precision": 0.8
                    }
                )
                voice_profile_id = result["profile_id"]

        # Generate preview audio
        audio_bytes = await self.voice_engine.preview_voice(
            profile_id=voice_profile_id,
            text=text,
            emotion=emotion
        )

        duration = self._get_audio_duration(audio_bytes)

        # Save preview
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(22050)
            wav_file.writeframes(audio_bytes)

        return {
            "output_path": output_path,
            "duration": duration,
            "voice_profile": voice_profile_id,
            "emotion": emotion,
            "text": text
        }

    async def batch_render_segments(
        self,
        segments: List[Dict[str, Any]],
        output_dir: str
    ) -> List[Dict[str, Any]]:
        """
        Render multiple segments in batch
        """
        results = []

        for i, segment_data in enumerate(segments):
            try:
                if segment_data["type"] == "character":
                    audio_bytes = await self.character_mapper.generate_character_audio(
                        character_name=segment_data["character"],
                        text=segment_data["text"],
                        emotion=segment_data.get("emotion", "neutral")
                    )
                else:  # narrator
                    narrator_profile = self.narrator_optimizer.narrator_profiles[
                        segment_data.get("narrator_profile", "narrator_nonfiction_default")
                    ]
                    audio_bytes = await self.narrator_optimizer.generate_narrator_audio(
                        text=segment_data["text"],
                        narrator_profile=narrator_profile,
                        segment_type=segment_data.get("segment_type", "main")
                    )

                output_path = os.path.join(output_dir, f"segment_{i:03d}.wav")
                with wave.open(output_path, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(22050)
                    wav_file.writeframes(audio_bytes)

                results.append({
                    "segment_id": i,
                    "output_path": output_path,
                    "duration": self._get_audio_duration(audio_bytes),
                    "status": "success"
                })

            except Exception as e:
                results.append({
                    "segment_id": i,
                    "error": str(e),
                    "status": "failed"
                })

        return results