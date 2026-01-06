# models/user_file.py
"""
UserFile model for GOAT platform
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, ForeignKey, ARRAY, JSON, func
from sqlalchemy.orm import relationship
from . import Base


class UserFile(Base):
    __tablename__ = "user_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    original_filename = Column(String, nullable=False)
    clean_filename = Column(String)  # e.g. "my-resume-v3-final-really.pdf" → "Resume.pdf"
    file_type = Column(String, nullable=False)  # "pdf", "image", "docx", etc.
    mime_type = Column(String, nullable=True)  # MIME type like "application/pdf"
    file_size = Column(BigInteger, nullable=False)
    status = Column(String, default="uploaded")  # uploaded | processing | processed | failed
    storage_path = Column(String, nullable=False)
    processed_path = Column(String, nullable=True)
    thumbnail_path = Column(String, nullable=True)
    preview_available = Column(Boolean, default=False)

    tags = Column(ARRAY(String), default=[])  # auto + manual tags
    is_favorite = Column(Boolean, default=False)
    downloaded_at = Column(DateTime(timezone=True), nullable=True)
    skg_clusters = Column(JSON, default=[])  # SKG cluster IDs for this file

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="files")

    @property
    def display_name(self):
        """Return clean filename or original if clean not available"""
        return self.clean_filename or self.original_filename

    @property
    def file_size_display(self):
        """Human-readable file size"""
        size = self.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size // 1024} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size // (1024 * 1024)} MB"
        else:
            return f"{size // (1024 * 1024 * 1024)} GB"

    @property
    def is_image(self):
        """Check if file is an image"""
        return self.file_type in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']

    @property
    def is_document(self):
        """Check if file is a document"""
        return self.file_type in ['pdf', 'doc', 'docx', 'txt', 'rtf']

    @property
    def status_color(self):
        """Status color for UI"""
        status_map = {
            'uploaded': 'yellow',
            'processing': 'blue',
            'processed': 'green',
            'failed': 'red'
        }
        return status_map.get(self.status, 'gray')