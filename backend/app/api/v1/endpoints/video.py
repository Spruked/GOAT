# backend/app/api/v1/endpoints/video.py
"""
Video generation endpoints
"""

from fastapi import APIRouter, Depends, File, UploadFile, Form, BackgroundTasks
from typing import List, Optional
import json
from pathlib import Path
from app.core.video_engine import video_engine
from app.core.content_ai import content_ai, content_generator
from app.security.auth import dual_auth
from app.config import settings

router = APIRouter(prefix="/video", tags=["Video Generation"])

@router.post("/generate-memory")
async def generate_memory_video(
    clips: str = Form(...),  # JSON string of clips
    template: str = Form(default="legacy"),
    voice_style: str = Form(default="sean_connery"),
    background_tasks: BackgroundTasks = None,
    token: dict = Depends(dual_auth)
):
    """
    Generate a memory video from clips
    """
    clips_data = json.loads(clips)

    # Queue the job
    job_id = f"video_{token['tenant_id']}_{json.dumps(clips_data)[:10].replace('/', '')}"

    background_tasks.add_task(
        video_engine.generate_memory_video,
        clips=clips_data,
        template=template,
        voice_style=voice_style
    )

    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Video generation started. Check back for results."
    }

@router.post("/parse-existing")
async def parse_existing_videos(
    files: List[UploadFile] = File(...),
    highlights: str = Form(...),  # JSON string of timestamps
    metadata: str = Form(...),
    token: dict = Depends(dual_auth)
):
    """
    Upload existing videos and splice them into memory video
    """
    highlights_data = json.loads(highlights)
    metadata_data = json.loads(metadata)

    # Save files temporarily
    file_paths = []
    for file in files:
        path = settings.VIDEOS_DIR / f"temp_{file.filename}"
        with open(path, "wb") as f:
            f.write(await file.read())
        file_paths.append(str(path))

    # Process
    output_path = video_engine.parse_and_splice(
        source_videos=file_paths,
        highlights=highlights_data,
        metadata=metadata_data
    )

    # Cleanup
    for path in file_paths:
        Path(path).unlink(missing_ok=True)

    return {
        "video_url": f"/storage/videos/{Path(output_path).name}",
        "status": "complete"
    }

@router.post("/ai-generate-dialog")
async def generate_dialog(
    media_metadata: str = Form(...),
    token: dict = Depends(dual_auth)
):
    """
    AI generates narration script and metadata from media
    """
    metadata = json.loads(media_metadata)

    result = content_generator.generate_memory_dialog(metadata)

    return result

@router.get("/job/{job_id}")
async def get_job_status(job_id: str, token: dict = Depends(dual_auth)):
    """
    Check video generation job status
    """
    # Check Redis for job status
    status_data = video_engine.redis.get(f"job:{job_id}")

    if not status_data:
        return {"error": "Job not found"}

    return json.loads(status_data)

@router.get("/templates")
async def get_templates():
    """
    Get available video templates
    """
    return {
        "templates": [
            {"id": "legacy", "name": "Timeless Legacy", "description": "Sepia tones, film grain, classical feel"},
            {"id": "modern", "name": "Clean Modern", "description": "High contrast, crisp, contemporary"},
            {"id": "nostalgic", "name": "Soft Nostalgia", "description": "Dreamy blur, warm colors, sentimental"}
        ],
        "voice_styles": [
            {"id": "sean_connery", "name": "Deep & Authoritative", "description": "Classic legacy voice"},
            {"id": "warm_female", "name": "Warm & Comforting", "description": "Nurturing storytelling"},
            {"id": "wise_older", "name": "Wise & Experienced", "description": "Grandfatherly wisdom"}
        ]
    }