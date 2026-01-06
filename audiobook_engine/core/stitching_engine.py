import os
import hashlib
from pathlib import Path
from dataclasses import dataclass
from typing import List
from uuid import UUID

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from ..models.audiobook_project import AudiobookProject
from ..models.chapter_audio import ChapterAudio
from ..utils.glyph_tracer import create_glyph_commit


@dataclass
class StitchResult:
    m4b_path: Path
    total_duration_sec: float
    checksum_sha256: str
    chapter_markers: List[dict]
    glyph_master: str


class StitchingEngine:

    def __init__(self):
        self.output_dir = Path("storage/audiobooks")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _merge_audio(self, chapters: List[ChapterAudio]) -> (AudioSegment, List[dict]):
        """
        Combine normalized chapter WAVs into one long AudioSegment.
        Returns merged audio + chapter marker metadata.
        """
        if not AudioSegment:
            raise ImportError("pydub not available - required for audio stitching")

        combined = AudioSegment.empty()
        chapter_markers = []
        current_start = 0.0

        for ch in chapters:
            seg = AudioSegment.from_wav(ch.normalized_audio_path)
            combined += seg

            chapter_markers.append({
                "chapter": ch.chapter_number,
                "title": f"Chapter {ch.chapter_number}",
                "start_sec": current_start,
                "duration_sec": ch.duration_sec,
                "checksum": ch.checksum_sha256,
            })

            current_start += ch.duration_sec

        return combined, chapter_markers

    def stitch_m4b(
        self,
        project: AudiobookProject,
        chapters: List[ChapterAudio]
    ) -> StitchResult:

        logger.info(f"[StitchingEngine] Stitching {len(chapters)} chapters for project {project.id}")

        # Sort chapters 1 → N
        chapters_sorted = sorted(chapters, key=lambda c: c.chapter_number)

        merged_audio, chapter_markers = self._merge_audio(chapters_sorted)

        out_path = self.output_dir / f"{project.id}.m4b"
        merged_audio.export(out_path, format="mp4", codec="aac")

        # Build checksum
        checksum = hashlib.sha256(out_path.read_bytes()).hexdigest()

        # Master glyph lineage
        glyph_master = create_glyph_commit(
            content=f"Master M4B audiobook for project {project.id}",
            metadata={
                "event_type": "audiobook_master_m4b",
                "project_id": str(project.id),
                "total_chapters": len(chapters_sorted),
                "total_duration_sec": sum(c.duration_sec for c in chapters_sorted),
                "checksum_sha256": checksum
            }
        )

        logger.info(f"[StitchingEngine] Completed M4B: {out_path}")

        return StitchResult(
            m4b_path=out_path,
            total_duration_sec=sum(c.duration_sec for c in chapters_sorted),
            checksum_sha256=checksum,
            chapter_markers=chapter_markers,
            glyph_master=glyph_master
        )