from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

class CreateAudiobookRequest(BaseModel):
    book_project_id: UUID
    voice_profile_id: str
    narrator: Optional[str] = "Caleon Default"

class SSMLRequest(BaseModel):
    chapters: Optional[List[int]] = None  # None = all chapters

class GenerateAudioRequest(BaseModel):
    chapters: Optional[List[int]] = None

class StitchRequest(BaseModel):
    include_cover: bool = False

class AudiobookStatusResponse(BaseModel):
    project_id: UUID
    status: str
    total_chapters: int
    completed_chapters: int
    glyph_master: Optional[str] = None

class DownloadResponse(BaseModel):
    download_url: str
    manifest: dict
    glyph_master: str