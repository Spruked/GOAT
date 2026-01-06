# audiobook_engine/workers/__init__.py
"""
Audiobook Engine Background Workers
"""

from .audio_worker import (
    process_chapter_audio, process_project_audio,
    AudioProcessingTask, ProjectProcessingTask
)
from .tasks import (
    audio_processing_queue, project_processing_queue,
    start_worker, stop_worker
)

__all__ = [
    # Audio Worker
    "process_chapter_audio", "process_project_audio",
    "AudioProcessingTask", "ProjectProcessingTask",

    # Task Management
    "audio_processing_queue", "project_processing_queue",
    "start_worker", "stop_worker"
]