# audiobook_engine/workers/audio_worker.py
"""
Audio Processing Worker for Audiobook Engine

Background worker for processing chapter audio and complete projects.
Handles SSML conversion, TTS generation, normalization, and stitching.
"""

import os
import logging
import time
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass

from ..models.audiobook_project import AudiobookProject, ProjectStatus, save_project
from ..models.chapter_audio import ChapterAudio, ChapterStatus, save_chapter_audio
from ..models.voice_profile import get_voice_profile_by_name

from ..core.ssml_converter import convert_text_to_ssml
from ..core.audio_builder import build_audio_from_ssml
from ..core.normalizer import normalize_audio_file

from ..utils.temp_manager import TempFileManager

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class AudioProcessingTask:
    """Task for processing a single chapter."""
    chapter: ChapterAudio
    quality_preset: str = "standard"
    normalize_audio: bool = True
    remove_artifacts: bool = True


@dataclass
class ProjectProcessingTask:
    """Task for processing an entire project."""
    project: AudiobookProject
    quality_preset: str = "standard"
    normalize_audio: bool = True
    remove_artifacts: bool = True


def process_chapter_audio(
    chapter: ChapterAudio,
    quality_preset: str = "standard",
    normalize_audio: bool = True,
    remove_artifacts: bool = True
):
    """
    Process a single chapter to generate audio.

    Args:
        chapter: ChapterAudio object to process
        quality_preset: Quality preset for audio generation
        normalize_audio: Whether to normalize the audio
        remove_artifacts: Whether to remove audio artifacts
    """
    try:
        logger.info(f"Starting audio processing for chapter: {chapter.chapter_id}")

        # Update chapter status
        chapter.update_status(ChapterStatus.PROCESSING_SSML)
        save_chapter_audio(chapter)

        # Get voice profile
        voice_profile = get_voice_profile_by_name(chapter.voice_profile_name)
        if not voice_profile:
            raise ValueError(f"Voice profile not found: {chapter.voice_profile_name}")

        # Convert text to SSML
        ssml_text = convert_text_to_ssml(chapter.content, chapter.voice_profile_name)
        chapter.set_ssml(ssml_text)

        # Update status
        chapter.update_status(ChapterStatus.GENERATING_AUDIO)
        save_chapter_audio(chapter)

        # Generate raw audio
        temp_manager = TempFileManager()
        raw_audio_result = build_audio_from_ssml(
            ssml_text,
            voice_profile,
            quality_preset=quality_preset
        )

        if not raw_audio_result.success:
            raise RuntimeError(f"Audio generation failed: {raw_audio_result.error_message}")

        chapter.set_raw_audio(raw_audio_result.audio_path)

        # Normalize audio if requested
        if normalize_audio:
            chapter.update_status(ChapterStatus.NORMALIZING)
            save_chapter_audio(chapter)

            normalized_result = normalize_audio_file(
                raw_audio_result.audio_path,
                remove_artifacts=remove_artifacts
            )

            if not normalized_result.success:
                logger.warning(f"Audio normalization failed: {normalized_result.error_message}")
                # Continue with raw audio
                chapter.set_normalized_audio(raw_audio_result.audio_path)
            else:
                chapter.set_normalized_audio(normalized_result.output_path)

        else:
            # Use raw audio as normalized
            chapter.set_normalized_audio(raw_audio_result.audio_path)

        # Update metadata
        chapter.duration_seconds = raw_audio_result.duration_seconds
        chapter.word_count = len(chapter.content.split())

        # Mark as completed
        chapter.update_status(ChapterStatus.COMPLETED)
        save_chapter_audio(chapter)

        logger.info(f"Chapter audio processing completed: {chapter.chapter_id}")

    except Exception as e:
        logger.error(f"Chapter audio processing failed for {chapter.chapter_id}: {e}")

        # Mark as failed
        chapter.update_status(ChapterStatus.FAILED)
        chapter.error_message = str(e)
        save_chapter_audio(chapter)

        raise


def process_project_audio(
    project: AudiobookProject,
    quality_preset: str = "standard",
    normalize_audio: bool = True,
    remove_artifacts: bool = True
):
    """
    Process an entire project to generate complete audiobook.

    Args:
        project: AudiobookProject to process
        quality_preset: Quality preset for audio generation
        normalize_audio: Whether to normalize audio
        remove_artifacts: Whether to remove artifacts
    """
    try:
        logger.info(f"Starting project processing: {project.project_id}")

        # Update project status
        project.update_status(ProjectStatus.PROCESSING)
        save_project(project)

        # Get all chapters for the project
        from ..models.chapter_audio import get_project_chapters
        chapters = get_project_chapters(project.project_id)

        if not chapters:
            raise ValueError("No chapters found for project")

        # Sort chapters by number
        chapters.sort(key=lambda c: c.chapter_number)

        total_chapters = len(chapters)
        processed_chapters = 0

        # Process each chapter
        for chapter in chapters:
            try:
                logger.info(f"Processing chapter {chapter.chapter_number}/{total_chapters}: {chapter.chapter_title}")

                # Process the chapter
                process_chapter_audio(
                    chapter,
                    quality_preset,
                    normalize_audio,
                    remove_artifacts
                )

                processed_chapters += 1

                # Update project progress
                progress = int((processed_chapters / total_chapters) * 100)
                logger.info(f"Project progress: {progress}% ({processed_chapters}/{total_chapters})")

            except Exception as e:
                logger.error(f"Failed to process chapter {chapter.chapter_id}: {e}")
                # Continue with other chapters

        # Check if all chapters completed
        completed_chapters = [c for c in chapters if c.status == ChapterStatus.COMPLETED]
        failed_chapters = [c for c in chapters if c.status == ChapterStatus.FAILED]

        if len(completed_chapters) == total_chapters:
            # All chapters completed
            project.update_status(ProjectStatus.COMPLETED)
            logger.info(f"Project processing completed: {project.project_id}")

        elif len(completed_chapters) > 0:
            # Partial completion
            project.update_status(ProjectStatus.PARTIALLY_COMPLETED)
            logger.warning(f"Project partially completed: {len(completed_chapters)}/{total_chapters} chapters")

        else:
            # All failed
            project.update_status(ProjectStatus.FAILED)
            logger.error(f"Project processing failed: all chapters failed")

        # Update project metadata
        project.total_chapters = total_chapters
        project.completed_chapters = len(completed_chapters)
        project.failed_chapters = len(failed_chapters)

        # Calculate total duration
        total_duration = sum(c.duration_seconds for c in completed_chapters)
        project.total_duration_seconds = total_duration

        save_project(project)

    except Exception as e:
        logger.error(f"Project processing failed for {project.project_id}: {e}")

        # Mark project as failed
        project.update_status(ProjectStatus.FAILED)
        project.error_message = str(e)
        save_project(project)

        raise


def process_chapter_batch(
    chapters: list[ChapterAudio],
    quality_preset: str = "standard",
    normalize_audio: bool = True,
    remove_artifacts: bool = True,
    max_concurrent: int = 2
):
    """
    Process multiple chapters concurrently.

    Args:
        chapters: List of ChapterAudio objects
        quality_preset: Quality preset
        normalize_audio: Whether to normalize
        remove_artifacts: Whether to remove artifacts
        max_concurrent: Maximum concurrent processing
    """
    import concurrent.futures
    import threading

    logger.info(f"Processing {len(chapters)} chapters with max {max_concurrent} concurrent")

    # Use ThreadPoolExecutor for concurrent processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        # Submit all tasks
        futures = [
            executor.submit(
                process_chapter_audio,
                chapter,
                quality_preset,
                normalize_audio,
                remove_artifacts
            )
            for chapter in chapters
        ]

        # Wait for completion
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Will raise exception if task failed
            except Exception as e:
                logger.error(f"Chapter processing task failed: {e}")


def get_processing_status(project_id: str) -> Dict[str, Any]:
    """
    Get processing status for a project.

    Args:
        project_id: Project ID

    Returns:
        Status dictionary
    """
    from ..models.audiobook_project import get_project
    from ..models.chapter_audio import get_project_chapters

    project = get_project(project_id)
    if not project:
        return {"error": "Project not found"}

    chapters = get_project_chapters(project_id)

    status_counts = {}
    for chapter in chapters:
        status = chapter.status.value
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        "project_id": project_id,
        "project_status": project.status.value,
        "total_chapters": len(chapters),
        "chapter_status_counts": status_counts,
        "progress_percentage": project.get_progress_percentage(),
        "total_duration_seconds": project.total_duration_seconds
    }


def cancel_processing(project_id: str) -> bool:
    """
    Cancel processing for a project.

    Args:
        project_id: Project ID to cancel

    Returns:
        True if cancelled successfully
    """
    try:
        from ..models.audiobook_project import get_project

        project = get_project(project_id)
        if not project:
            return False

        # Update status to cancelled
        project.update_status(ProjectStatus.CANCELLED)
        save_project(project)

        logger.info(f"Processing cancelled for project: {project_id}")
        return True

    except Exception as e:
        logger.error(f"Failed to cancel processing for {project_id}: {e}")
        return False