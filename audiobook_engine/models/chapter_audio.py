from uuid import UUID
from datetime import datetime

class ChapterAudio:
    def __init__(
        self,
        project_id: UUID,
        chapter_number: int,
        ssml_glyph: str,
        raw_audio_path: str = "",
        normalized_audio_path: str = "",
        duration_sec: float = 0.0,
        checksum_sha256: str = "",
        glyph_raw: str = "",
        glyph_normalized: str = "",
    ):
        self.project_id = project_id
        self.chapter_number = chapter_number
        self.ssml_glyph = ssml_glyph

        # Paths will be filled as the pipeline progresses
        self.raw_audio_path: str = raw_audio_path
        self.normalized_audio_path: str = normalized_audio_path

        self.duration_sec: float = duration_sec
        self.checksum_sha256: str = checksum_sha256

        self.glyph_raw: str = glyph_raw
        self.glyph_normalized: str = glyph_normalized

        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()