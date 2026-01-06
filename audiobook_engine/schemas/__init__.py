# audiobook_engine/schemas/__init__.py
"""
Audiobook Engine Data Schemas

Pydantic models and JSON schemas for API validation and serialization.
"""

from .audiobook_schemas import (
    ProjectCreateSchema, ProjectUpdateSchema, ChapterCreateSchema,
    VoiceProfileCreateSchema, AudioProcessSchema, ExportSchema
)

__all__ = [
    # Project schemas
    "ProjectCreateSchema", "ProjectUpdateSchema",

    # Chapter schemas
    "ChapterCreateSchema",

    # Voice profile schemas
    "VoiceProfileCreateSchema",

    # Processing schemas
    "AudioProcessSchema", "ExportSchema"
]