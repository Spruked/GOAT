# models/user.py
"""
User model for GOAT platform
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, func
from sqlalchemy.orm import relationship
from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=True)  # for @handles
    bio = Column(String, default="")
    profile_image = Column(String, default="/defaults/avatar-goat.png")
    cover_image = Column(String, nullable=True)
    theme = Column(String, default="dark")  # "dark" | "light" | "amoled" | "custom"
    accent_color = Column(String, default="#ff4f8f")  # GOAT pink
    ui_mode = Column(String, default="pro")  # "simple" | "pro"
    preferences = Column(JSON, default={
        "sidebar_collapsed": False,
        "notifications": True,
        "auto_preview": True,
        "default_download_format": "pdf"
    })

    file_count = Column(Integer, default=0)
    processed_count = Column(Integer, default=0)
    last_active_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    files = relationship("UserFile", back_populates="user", cascade="all, delete")

    @property
    def stats(self):
        """Computed stats for dashboard"""
        return {
            "total_files": self.file_count,
            "processed_files": self.processed_count,
            "favorites": sum(1 for f in self.files if f.is_favorite),
            "recent_uploads": len([f for f in self.files if (func.now() - f.created_at).days <= 7])
        }