import os
import wave
import hashlib
from pathlib import Path
from typing import List, Optional, Any
from uuid import UUID
from dataclasses import dataclass

import torch
# Lazy import TTS to avoid loading issues during import
# from TTS.api import TTS
try:
    from pydub import AudioSegment
    from pydub import effects
except ImportError:
    AudioSegment = None
    effects = None

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from ..models.chapter_audio import ChapterAudio
from ..models.audiobook_project import AudiobookProject
from ..models.voice_profile import VoiceProfile
from ..utils.glyph_tracer import create_glyph_commit
from ..utils.temp_manager import TemporaryDirectory


@dataclass
class SynthesisResult:
    raw_path: Path
    normalized_path: Path
    duration_sec: float
    checksum_sha256: str
    glyph_raw: str
    glyph_norm: str


class AudioBuilder:
    # Global singleton cache: voice_id → TTS instance
    _tts_cache: dict[str, Any] = {}
    _cache_lock = torch.cuda.Event() if torch.cuda.is_available() else None

    def __init__(self, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"AudioBuilder initialized on {self.device}")

    def _get_tts(self, voice: VoiceProfile) -> Any:
        key = voice.cache_key
        if key in self._tts_cache:
            return self._tts_cache[key]

        logger.info(f"Loading TTS model: {voice.model_path or voice.voice_id}")
        # Lazy import
        from TTS.api import TTS
        tts = TTS(
            model_name=voice.model_name or "tts_models/multilingual/multi-dataset/xtts_v2",
            model_path=voice.model_path,
            config_path=voice.config_path,
            progress_bar=False,
            gpu=(self.device == "cuda"),
        ).to(self.device)

        # Warm-up to avoid first-call latency spike
        if voice.warmup_text:
            try:
                tts.tts_to_file(text=voice.warmup_text, file_path=os.devnull, speaker=voice.speaker_name)
            except:
                pass

        self._tts_cache[key] = tts
        return tts

    def _chunk_ssml(self, ssml: str, max_seconds: float = 25.0) -> List[str]:
        """Coqui XTTS performs best with <30s chunks. Split intelligently."""
        from lxml import etree
        root = etree.fromstring(f"<speak>{ssml}</speak>")
        chunks = []
        current = []
        current_duration = 0.0

        for elem in root.iter():
            if elem.tag == "s":
                text = etree.tostring(elem, encoding="unicode")
                est_seconds = len(elem.text or "") / 150 * 60  # crude WPM estimate
                if current_duration + est_seconds > max_seconds and current:
                    chunks.append("".join(current))
                    current = [text]
                    current_duration = est_seconds
                else:
                    current.append(text)
                    current_duration += est_seconds
        if current:
            chunks.append("".join(current))
        return chunks or [ssml]

    def _synthesize_with_retry(
        self,
        tts: Any,
        ssml_chunk: str,
        out_path: Path,
        voice: VoiceProfile,
        max_retries: int = 3
    ) -> Path:
        for attempt in range(max_retries):
            try:
                tts.tts_to_file(
                    text=ssml_chunk,
                    speaker=voice.speaker_name,
                    language=voice.language,
                    file_path=str(out_path),
                    speed=voice.speed_multiplier or 1.0,
                )
                if out_path.stat().st_size > 10_000:  # sanity check
                    return out_path
            except Exception as e:
                logger.warning(f"TTS synthesis failed (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    raise
        return out_path

    def generate_chapter_audio(
        self,
        project: AudiobookProject,
        chapter_number: int,
        ssml_text: str,
        voice_profile: VoiceProfile,
        target_lufs: float = -16.0,
    ) -> ChapterAudio:
        with TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)
            raw_chunks = []
            final_raw = Path(f"storage/audio/raw/{project.id}_ch{chapter_number}.wav")
            final_norm = Path(f"storage/audio/norm/{project.id}_ch{chapter_number}.wav")
            final_raw.parent.mkdir(parents=True, exist_ok=True)
            final_norm.parent.mkdir(parents=True, exist_ok=True)

            tts = self._get_tts(voice_profile)
            chunks = self._chunk_ssml(ssml_text, max_seconds=28.0)

            combined = AudioSegment.empty()
            for i, chunk in enumerate(chunks):
                chunk_path = tmpdir / f"chunk_{i}.wav"
                self._synthesize_with_retry(tts, chunk, chunk_path, voice_profile)
                segment = AudioSegment.from_wav(chunk_path)
                combined += segment
                raw_chunks.append(str(chunk_path))

            # Export raw full chapter
            combined.export(final_raw, format="wav")
            glyph_raw = create_glyph_commit(
                content=f"Raw audio synthesis for chapter {chapter_number}",
                metadata={
                    "event_type": "audio_synthesis_raw",
                    "project_id": str(project.id),
                    "chapter": chapter_number,
                    "chunks": len(chunks),
                    "source": "xtts_v2"
                }
            )

            # Normalization (EBU R128 –16 LUFS)
            if effects:
                normalized = effects.normalize(combined)
            else:
                normalized = combined  # Fallback if pydub not available
            normalized = normalized.apply_gain(target_lufs - normalized.dBFS)
            normalized.export(final_norm, format="wav")

            duration = len(normalized) / 1000.0
            checksum = hashlib.sha256(final_norm.read_bytes()).hexdigest()

            glyph_norm = create_glyph_commit(
                content=f"Normalized audio for chapter {chapter_number}",
                metadata={
                    "event_type": "audio_normalized",
                    "project_id": str(project.id),
                    "chapter": chapter_number,
                    "duration_sec": round(duration, 3),
                    "target_lufs": target_lufs,
                    "checksum_sha256": checksum
                }
            )

            chapter_audio = ChapterAudio(
                project_id=project.id,
                chapter_number=chapter_number,
                ssml_glyph="",  # TODO: Get from database/storage layer
                raw_audio_path=str(final_raw),
                normalized_audio_path=str(final_norm),
                duration_sec=round(duration, 3),
                checksum_sha256=checksum,
                glyph_raw=glyph_raw,
                glyph_normalized=glyph_norm,
            )

            return chapter_audio