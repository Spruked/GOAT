from datetime import datetime
from uuid import UUID

class AudioManifest:
    def __init__(
        self,
        project_id: UUID,
        book_id: UUID,
        title: str,
        author: str,
        narrator: str,
        chapters: list,
        glyph_master: str,
        total_duration_sec: float,
    ):
        self.spec = "goat-audiobook-v1"
        self.project_id = str(project_id)
        self.book_id = str(book_id)
        self.title = title
        self.author = author
        self.narrator = narrator
        self.created_at = datetime.utcnow().isoformat()
        self.total_duration_sec = total_duration_sec
        self.chapters = chapters
        self.glyph_master = glyph_master

    def to_dict(self):
        return self.__dict__