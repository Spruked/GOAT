from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional, List, Dict, Any

class AudiobookStatus(str, Enum):
    PENDING = "pending"
    SSML = "ssml"
    GENERATING = "generating"
    STITCHING = "stitching"
    COMPLETED = "completed"
    FAILED = "failed"

class AudiobookProject:
    def __init__(
        self,
        book_project_id: UUID,
        title: str,
        author: str,
        voice_profile_id: str,
        total_chapters: int,
        narrator: str = "Caleon Default"
    ):
        self.id: UUID = uuid4()
        self.book_project_id = book_project_id
        self.title = title
        self.author = author
        self.narrator = narrator
        self.voice_profile_id = voice_profile_id
        self.total_chapters = total_chapters
        self.status = AudiobookStatus.PENDING
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.glyph_master: Optional[str] = None

    @property
    def id(self) -> UUID:
        """Alias for book_project_id."""
        return self.book_project_id

    # Glyph tracing
    glyph_master: Optional[str] = None
    glyph_trace: List[str] = []

    # Error handling
    error_message: Optional[str] = None
    retry_count: int = 0

    # Settings
    settings: Dict[str, Any] = {}

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = AudiobookStatus(self.status)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at.replace('Z', '+00:00'))
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at.replace('Z', '+00:00'))
        if isinstance(self.started_at, str):
            self.started_at = datetime.fromisoformat(self.started_at.replace('Z', '+00:00'))
        if isinstance(self.completed_at, str):
            self.completed_at = datetime.fromisoformat(self.completed_at.replace('Z', '+00:00'))

    def update_status(self, new_status: AudiobookStatus, error: Optional[str] = None):
        """Update project status with timestamp"""
        self.status = new_status
        self.updated_at = datetime.utcnow()

        if new_status == AudiobookStatus.FAILED and error:
            self.error_message = error

        if new_status in [AudiobookStatus.COMPLETED, AudiobookStatus.FAILED]:
            self.completed_at = datetime.utcnow()

        if new_status == AudiobookStatus.GENERATING and not self.started_at:
            self.started_at = datetime.utcnow()

    def add_glyph(self, glyph_uri: str):
        """Add a glyph to the trace"""
        if glyph_uri not in self.glyph_trace:
            self.glyph_trace.append(glyph_uri)

    def get_progress_percentage(self) -> float:
        """Calculate progress percentage"""
        if self.total_chapters == 0:
            return 0.0

        if self.status == AudiobookStatus.COMPLETED:
            return 100.0
        elif self.status == AudiobookStatus.FAILED:
            return 0.0
        else:
            return (self.completed_chapters / self.total_chapters) * 100.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "book_project_id": self.book_project_id,
            "title": self.title,
            "author": self.author,
            "narrator": self.narrator,
            "voice_profile_id": self.voice_profile_id,
            "status": self.status.value,
            "total_chapters": self.total_chapters,
            "completed_chapters": self.completed_chapters,
            "failed_chapters": self.failed_chapters,
            "created_at": self.created_at.isoformat() + "Z",
            "updated_at": self.updated_at.isoformat() + "Z",
            "started_at": self.started_at.isoformat() + "Z" if self.started_at else None,
            "completed_at": self.completed_at.isoformat() + "Z" if self.completed_at else None,
            "output_path": self.output_path,
            "manifest_path": self.manifest_path,
            "total_duration_sec": self.total_duration_sec,
            "file_size_bytes": self.file_size_bytes,
            "glyph_master": self.glyph_master,
            "glyph_trace": self.glyph_trace,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "settings": self.settings,
            "progress_percentage": self.get_progress_percentage()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AudiobookProject':
        """Create from dictionary"""
        # Handle status enum
        if "status" in data:
            data["status"] = AudiobookStatus(data["status"])

        return cls(**data)

    def can_transition_to(self, new_status: AudiobookStatus) -> bool:
        """Check if status transition is valid"""
        valid_transitions = {
            AudiobookStatus.PENDING: [AudiobookStatus.SSML],
            AudiobookStatus.SSML: [AudiobookStatus.GENERATING, AudiobookStatus.FAILED],
            AudiobookStatus.GENERATING: [AudiobookStatus.STITCHING, AudiobookStatus.FAILED],
            AudiobookStatus.STITCHING: [AudiobookStatus.COMPLETED, AudiobookStatus.FAILED],
            AudiobookStatus.COMPLETED: [],  # Terminal state
            AudiobookStatus.FAILED: []  # Terminal state
        }

        return new_status in valid_transitions.get(self.status, [])

# In-memory storage for demo (would use database in production)
_project_store: Dict[str, AudiobookProject] = {}

def save_project(project: AudiobookProject):
    """Save project to storage"""
    _project_store[str(project.book_project_id)] = project

def get_project(project_id: str) -> Optional[AudiobookProject]:
    """Get project by ID"""
    return _project_store.get(project_id)

def list_projects() -> List[AudiobookProject]:
    """List all projects"""
    return list(_project_store.values())

def delete_project(project_id: str) -> bool:
    """Delete project"""
    if project_id in _project_store:
        del _project_store[project_id]
        return True
    return False