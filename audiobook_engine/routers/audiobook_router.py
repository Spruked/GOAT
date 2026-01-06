# audiobook_engine/routers/audiobook_router.py
"""
Audiobook Engine API Router

FastAPI router providing REST endpoints for audiobook generation,
management, and export operations.
"""

import os
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from ..models.audiobook_project import (
    AudiobookProject, ProjectStatus, save_project, get_project,
    list_projects, delete_project
)
from ..models.chapter_audio import (
    ChapterAudio, ChapterStatus, save_chapter_audio, get_chapter_audio,
    get_project_chapters, list_chapter_audio, delete_project_chapters
)
from ..models.voice_profile import (
    VoiceProfile, PRESET_PROFILES, save_voice_profile, get_voice_profile,
    get_voice_profile_by_name, list_voice_profiles, delete_voice_profile
)
from ..models.audio_manifest import AudioManifest, create_manifest_from_project

from ..core.ssml_converter import convert_text_to_ssml
from ..core.audio_builder import build_audio_from_ssml, build_audio_from_text
from ..core.normalizer import normalize_audio_file
from ..core.stitching_engine import stitch_audiobook_chapters
from ..core.export_manager import export_audiobook_project

from ..workers.audio_worker import process_chapter_audio, process_project_audio
from ..utils.temp_manager import TempFileManager

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/audiobooks", tags=["audiobooks"])

# Pydantic models for API
class ProjectCreateRequest(BaseModel):
    """Request model for creating a new audiobook project."""
    title: str = Field(..., description="Audiobook title")
    author: str = Field(..., description="Book author")
    description: Optional[str] = Field(None, description="Project description")
    default_voice: str = Field("Narrator", description="Default voice profile name")

class ProjectUpdateRequest(BaseModel):
    """Request model for updating a project."""
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    default_voice: Optional[str] = None
    status: Optional[ProjectStatus] = None

class ChapterCreateRequest(BaseModel):
    """Request model for creating a chapter."""
    chapter_title: str = Field(..., description="Chapter title")
    chapter_number: int = Field(..., description="Chapter number")
    content: str = Field(..., description="Chapter text content")
    voice_profile: Optional[str] = Field(None, description="Voice profile name")

class VoiceProfileCreateRequest(BaseModel):
    """Request model for creating a voice profile."""
    name: str = Field(..., description="Voice profile name")
    tts_config: Dict[str, Any] = Field(..., description="TTS configuration")
    emotion_config: Optional[Dict[str, Any]] = Field(None, description="Emotion configuration")

class AudioProcessRequest(BaseModel):
    """Request model for audio processing."""
    quality_preset: str = Field("standard", description="Quality preset")
    normalize_audio: bool = Field(True, description="Whether to normalize audio")
    remove_artifacts: bool = Field(True, description="Whether to remove artifacts")

# Routes
@router.post("/", response_model=Dict[str, Any])
async def create_project(request: ProjectCreateRequest):
    """Create a new audiobook project."""
    try:
        project = AudiobookProject(
            title=request.title,
            author=request.author,
            description=request.description,
            default_voice=request.default_voice
        )

        save_project(project)

        logger.info(f"Created project: {project.project_id}")
        return {
            "project_id": project.project_id,
            "status": project.status.value,
            "created_at": project.created_at.isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to create project: {e}")
        raise HTTPException(status_code=500, detail="Failed to create project")

@router.get("/", response_model=List[Dict[str, Any]])
async def list_audiobook_projects():
    """List all audiobook projects."""
    try:
        projects = list_projects()
        return [
            {
                "project_id": p.project_id,
                "title": p.title,
                "author": p.author,
                "status": p.status.value,
                "progress_percentage": p.get_progress_percentage(),
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat()
            }
            for p in projects
        ]

    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        raise HTTPException(status_code=500, detail="Failed to list projects")

@router.get("/{project_id}", response_model=Dict[str, Any])
async def get_audiobook_project(project_id: str):
    """Get a specific audiobook project."""
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        return {
            "project_id": project.project_id,
            "title": project.title,
            "author": project.author,
            "description": project.description,
            "status": project.status.value,
            "progress_percentage": project.get_progress_percentage(),
            "default_voice": project.default_voice,
            "glyph_lineage": project.glyph_lineage,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get project")

@router.put("/{project_id}", response_model=Dict[str, Any])
async def update_project(project_id: str, request: ProjectUpdateRequest):
    """Update an audiobook project."""
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Update fields
        if request.title is not None:
            project.title = request.title
        if request.author is not None:
            project.author = request.author
        if request.description is not None:
            project.description = request.description
        if request.default_voice is not None:
            project.default_voice = request.default_voice
        if request.status is not None:
            project.update_status(request.status)

        save_project(project)

        return {"message": "Project updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update project")

@router.delete("/{project_id}")
async def delete_audiobook_project(project_id: str):
    """Delete an audiobook project."""
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Delete associated chapters
        delete_project_chapters(project_id)

        # Delete project
        delete_project(project_id)

        return {"message": "Project deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete project")

@router.post("/{project_id}/chapters", response_model=Dict[str, Any])
async def create_chapter(project_id: str, request: ChapterCreateRequest):
    """Create a new chapter for a project."""
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        chapter = ChapterAudio(
            project_id=project_id,
            chapter_title=request.chapter_title,
            chapter_number=request.chapter_number,
            content=request.content,
            voice_profile_name=request.voice_profile or project.default_voice
        )

        save_chapter_audio(chapter)

        return {
            "chapter_id": chapter.chapter_id,
            "status": chapter.status.value,
            "created_at": chapter.created_at.isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create chapter for project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to create chapter")

@router.get("/{project_id}/chapters", response_model=List[Dict[str, Any]])
async def list_project_chapters(project_id: str):
    """List all chapters for a project."""
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        chapters = get_project_chapters(project_id)
        return [
            {
                "chapter_id": c.chapter_id,
                "chapter_title": c.chapter_title,
                "chapter_number": c.chapter_number,
                "status": c.status.value,
                "word_count": c.word_count,
                "duration_seconds": c.duration_seconds,
                "created_at": c.created_at.isoformat()
            }
            for c in chapters
        ]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to list chapters for project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to list chapters")

@router.post("/{project_id}/chapters/{chapter_id}/process", response_model=Dict[str, Any])
async def process_chapter(
    project_id: str,
    chapter_id: str,
    request: AudioProcessRequest,
    background_tasks: BackgroundTasks
):
    """Process a chapter to generate audio."""
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        chapter = get_chapter_audio(chapter_id)
        if not chapter or chapter.project_id != project_id:
            raise HTTPException(status_code=404, detail="Chapter not found")

        # Start background processing
        background_tasks.add_task(
            process_chapter_audio,
            chapter,
            request.quality_preset,
            request.normalize_audio,
            request.remove_artifacts
        )

        return {"message": "Chapter processing started"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process chapter {chapter_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chapter")

@router.post("/{project_id}/process", response_model=Dict[str, Any])
async def process_entire_project(
    project_id: str,
    request: AudioProcessRequest,
    background_tasks: BackgroundTasks
):
    """Process entire project to generate audiobook."""
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Start background processing
        background_tasks.add_task(
            process_project_audio,
            project,
            request.quality_preset,
            request.normalize_audio,
            request.remove_artifacts
        )

        return {"message": "Project processing started"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process project")

@router.post("/{project_id}/export", response_model=Dict[str, Any])
async def export_project(project_id: str):
    """Export completed project as M4B audiobook."""
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if project.status != ProjectStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Project must be completed before export")

        # Get chapters
        chapters = get_project_chapters(project_id)
        if not chapters:
            raise HTTPException(status_code=400, detail="No chapters found for project")

        # Stitch audio
        stitched_result = stitch_audiobook_chapters(chapters)
        if not stitched_result.success:
            raise HTTPException(status_code=500, detail="Failed to stitch audio")

        # Export
        export_result = export_audiobook_project(project, stitched_result.output_path)
        if not export_result.success:
            raise HTTPException(status_code=500, detail="Failed to export audiobook")

        return {
            "export_path": str(export_result.audiobook_path),
            "manifest_path": str(export_result.manifest_path),
            "checksum": export_result.checksum,
            "file_size": export_result.file_size_bytes,
            "vault_commit": export_result.vault_commit_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to export project")

@router.get("/{project_id}/download")
async def download_audiobook(project_id: str):
    """Download the exported audiobook file."""
    try:
        project = get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # For now, return a placeholder
        # In practice, this would serve the actual exported file
        raise HTTPException(status_code=501, detail="Download not implemented yet")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to download audiobook for project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to download audiobook")

# Voice profile endpoints
@router.post("/voices", response_model=Dict[str, Any])
async def create_voice_profile(request: VoiceProfileCreateRequest):
    """Create a new voice profile."""
    try:
        profile = VoiceProfile(
            name=request.name,
            tts_config=request.tts_config,
            emotion_config=request.emotion_config or {}
        )

        save_voice_profile(profile)

        return {
            "profile_id": profile.profile_id,
            "name": profile.name,
            "created_at": profile.created_at.isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to create voice profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to create voice profile")

@router.get("/voices", response_model=List[Dict[str, Any]])
async def list_voice_profiles_endpoint():
    """List all voice profiles."""
    try:
        profiles = list_voice_profiles()
        return [
            {
                "profile_id": p.profile_id,
                "name": p.name,
                "usage_count": p.usage_count,
                "last_used": p.last_used.isoformat() if p.last_used else None,
                "created_at": p.created_at.isoformat()
            }
            for p in profiles
        ]

    except Exception as e:
        logger.error(f"Failed to list voice profiles: {e}")
        raise HTTPException(status_code=500, detail="Failed to list voice profiles")

@router.get("/voices/presets", response_model=Dict[str, Dict[str, Any]])
async def get_voice_presets():
    """Get available voice presets."""
    return {
        name: {
            "name": profile.name,
            "tts_config": profile.tts_config,
            "emotion_config": profile.emotion_config
        }
        for name, profile in PRESET_PROFILES.items()
    }

# Utility endpoints
@router.post("/convert-ssml", response_model=Dict[str, str])
async def convert_text_to_ssml_endpoint(text: str = Form(...), voice: str = Form("Narrator")):
    """Convert plain text to SSML."""
    try:
        ssml = convert_text_to_ssml(text, voice)
        return {"ssml": ssml}

    except Exception as e:
        logger.error(f"Failed to convert text to SSML: {e}")
        raise HTTPException(status_code=500, detail="Failed to convert text")

@router.post("/test-audio")
async def test_audio_generation(
    text: str = Form(...),
    voice: str = Form("Narrator"),
    quality: str = Form("draft")
):
    """Generate test audio from text."""
    try:
        voice_profile = get_voice_profile_by_name(voice)
        if not voice_profile:
            raise HTTPException(status_code=404, detail="Voice profile not found")

        result = build_audio_from_text(text, voice_profile, quality_preset=quality)
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error_message)

        # Return audio file
        return FileResponse(
            result.audio_path,
            media_type="audio/wav",
            filename="test_audio.wav"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate test audio: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate audio")