# routes/voice_management.py
"""
Voice Management API Endpoints for GOAT Audiobook System
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import json
import os
from pathlib import Path
from datetime import datetime
import asyncio

# Import voice system components
from engines.voice_engine import VoiceEngine
from engines.character_voice_mapper import CharacterVoiceMapper
from engines.narrator_optimizer import NarratorOptimizer
from engines.audiobook_renderer import AudiobookRenderer

router = APIRouter(prefix="/api/voice", tags=["voice-management"])

# Initialize voice system components
voice_engine = VoiceEngine()
character_mapper = CharacterVoiceMapper(voice_engine)
narrator_optimizer = NarratorOptimizer(voice_engine)
audiobook_renderer = AudiobookRenderer(voice_engine, character_mapper, narrator_optimizer)

# Pydantic models for API requests/responses
class VoiceProfileRequest(BaseModel):
    creation_method: str = Field(..., description="Creation method: 'sample' or 'parameter'")
    name: str = Field(..., description="Voice profile name")
    description: str = Field(..., description="Voice profile description")
    voice_type: str = Field(..., description="Voice type: 'character' or 'narrator'")
    sample_path: Optional[str] = Field(None, description="Path to audio sample (for sample method)")
    param_config: Optional[Dict[str, Any]] = Field(None, description="Parameter configuration (for parameter method)")

class CharacterProfileRequest(BaseModel):
    name: str = Field(..., description="Character name")
    description: str = Field(..., description="Character description")
    gender: str = Field(..., description="Character gender")
    age_range: str = Field(..., description="Age range (e.g., 'adult', 'child', 'elderly')")
    personality_traits: List[str] = Field(..., description="List of personality traits")
    voice_characteristics: Dict[str, Any] = Field(default_factory=dict, description="Voice characteristics")

class NarratorProfileRequest(BaseModel):
    content_type: str = Field(..., description="Content type: 'fiction', 'nonfiction', 'poetry', 'technical'")
    name: str = Field("default", description="Profile name")

class AudiobookRenderRequest(BaseModel):
    book_data: Dict[str, Any] = Field(..., description="Book data structure")
    output_path: str = Field(..., description="Output path for audiobook")
    narrator_profile_id: str = Field("narrator_nonfiction_default", description="Narrator profile ID")

class VoicePreviewRequest(BaseModel):
    profile_id: str = Field(..., description="Voice profile ID")
    text: str = Field(..., description="Preview text")
    emotion: str = Field("neutral", description="Emotion for preview")

class BatchRenderRequest(BaseModel):
    segments: List[Dict[str, Any]] = Field(..., description="List of segments to render")
    output_dir: str = Field(..., description="Output directory")

# Voice Profile Management Endpoints
@router.post("/profiles/create")
async def create_voice_profile(request: VoiceProfileRequest):
    """Create a new voice profile"""
    try:
        result = await voice_engine.create_voice_profile(
            creation_method=request.creation_method,
            name=request.name,
            description=request.description,
            voice_type=request.voice_type,
            sample_path=request.sample_path,
            param_config=request.param_config
        )

        return JSONResponse(
            content=result,
            status_code=201
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create voice profile: {str(e)}")

@router.get("/profiles/{profile_id}")
async def get_voice_profile(profile_id: str):
    """Get voice profile by ID"""
    try:
        profile = await voice_engine.get_profile(profile_id)
        return JSONResponse(content=profile)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Voice profile {profile_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get voice profile: {str(e)}")

@router.get("/profiles")
async def list_voice_profiles():
    """List all voice profiles"""
    try:
        profiles_path = Path("./voices/profiles")
        if not profiles_path.exists():
            return JSONResponse(content={"profiles": []})

        profiles = []
        for profile_file in profiles_path.glob("*.json"):
            try:
                with open(profile_file, 'r') as f:
                    profile = json.load(f)
                    profiles.append({
                        "profile_id": profile["profile_id"],
                        "name": profile["name"],
                        "voice_type": profile["voice_type"],
                        "created_at": profile["metadata"]["created_at"],
                        "usage_count": profile["metadata"]["usage_count"]
                    })
            except Exception:
                continue

        return JSONResponse(content={"profiles": profiles})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list voice profiles: {str(e)}")

@router.delete("/profiles/{profile_id}")
async def delete_voice_profile(profile_id: str):
    """Delete a voice profile"""
    try:
        profile_path = Path(f"./voices/profiles/{profile_id}.json")
        if not profile_path.exists():
            raise HTTPException(status_code=404, detail=f"Voice profile {profile_id} not found")

        profile_path.unlink()
        return JSONResponse(content={"message": f"Voice profile {profile_id} deleted"})

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete voice profile: {str(e)}")

# Character Voice Mapping Endpoints
@router.post("/characters/create")
async def create_character_profile(request: CharacterProfileRequest):
    """Create a character profile with voice mapping"""
    try:
        character = await character_mapper.create_character_profile(
            name=request.name,
            description=request.description,
            gender=request.gender,
            age_range=request.age_range,
            personality_traits=request.personality_traits,
            voice_characteristics=request.voice_characteristics
        )

        return JSONResponse(
            content={
                "character_name": character.name,
                "voice_profile_id": character.voice_profile_id,
                "emotional_range": character.emotional_range,
                "status": "created"
            },
            status_code=201
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create character profile: {str(e)}")

@router.post("/characters/{character_name}/audio")
async def generate_character_audio(
    character_name: str,
    text: str,
    emotion: str = "neutral",
    context: Optional[Dict[str, Any]] = None
):
    """Generate audio for a character"""
    try:
        audio_bytes = await character_mapper.generate_character_audio(
            character_name=character_name,
            text=text,
            emotion=emotion,
            context=context
        )

        # Save temporary file
        temp_path = f"./voices/temp/char_{character_name}_{emotion}_{hash(text)}.wav"
        with open(temp_path, 'wb') as f:
            f.write(audio_bytes)

        return FileResponse(
            path=temp_path,
            media_type="audio/wav",
            filename=f"{character_name}_{emotion}.wav"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate character audio: {str(e)}")

@router.get("/characters")
async def get_character_summary():
    """Get summary of all character profiles"""
    try:
        summary = character_mapper.get_character_summary()
        return JSONResponse(content=summary)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get character summary: {str(e)}")

@router.post("/characters/save")
async def save_character_mappings(filepath: str = "./data/character_mappings.json"):
    """Save character mappings to file"""
    try:
        await character_mapper.save_character_mappings(filepath)
        return JSONResponse(content={"message": f"Character mappings saved to {filepath}"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save character mappings: {str(e)}")

@router.post("/characters/load")
async def load_character_mappings(filepath: str = "./data/character_mappings.json"):
    """Load character mappings from file"""
    try:
        await character_mapper.load_character_mappings(filepath)
        return JSONResponse(content={"message": f"Character mappings loaded from {filepath}"})

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Character mappings file not found: {filepath}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load character mappings: {str(e)}")

# Narrator Optimization Endpoints
@router.post("/narrator/create")
async def create_narrator_profile(request: NarratorProfileRequest):
    """Create a narrator profile for content type"""
    try:
        profile = await narrator_optimizer.create_narrator_profile(
            content_type=request.content_type,
            name=request.name
        )

        return JSONResponse(
            content={
                "profile_id": profile.profile_id,
                "content_type": profile.content_type,
                "status": "created"
            },
            status_code=201
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create narrator profile: {str(e)}")

@router.post("/narrator/analyze")
async def analyze_text_segments(text: str, content_type: str = "nonfiction"):
    """Analyze text and return optimization recommendations"""
    try:
        profile = await narrator_optimizer.create_narrator_profile(content_type)
        segments = await narrator_optimizer.analyze_text_segments(text, content_type)
        optimizations = await narrator_optimizer.optimize_narration(segments, profile)

        return JSONResponse(content=optimizations)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze text: {str(e)}")

@router.post("/narrator/audio")
async def generate_narrator_audio(
    text: str,
    content_type: str = "nonfiction",
    segment_type: str = "main",
    technical_terms: Optional[List[str]] = None
):
    """Generate narrator audio"""
    try:
        profile = await narrator_optimizer.create_narrator_profile(content_type)
        audio_bytes = await narrator_optimizer.generate_narrator_audio(
            text=text,
            narrator_profile=profile,
            segment_type=segment_type,
            technical_terms=technical_terms
        )

        # Save temporary file
        temp_path = f"./voices/temp/narrator_{content_type}_{segment_type}_{hash(text)}.wav"
        with open(temp_path, 'wb') as f:
            f.write(audio_bytes)

        return FileResponse(
            path=temp_path,
            media_type="audio/wav",
            filename=f"narrator_{content_type}.wav"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate narrator audio: {str(e)}")

@router.get("/narrator/profiles")
async def get_narrator_profiles():
    """Get summary of narrator profiles"""
    try:
        summary = narrator_optimizer.get_profile_summary()
        return JSONResponse(content=summary)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get narrator profiles: {str(e)}")

# Audiobook Rendering Endpoints
@router.post("/audiobook/render")
async def render_audiobook(request: AudiobookRenderRequest, background_tasks: BackgroundTasks):
    """Render complete audiobook from book data"""
    try:
        # Start rendering in background
        task_id = f"audiobook_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        background_tasks.add_task(
            audiobook_renderer.render_audiobook_from_book,
            request.book_data,
            request.output_path,
            request.narrator_profile_id
        )

        return JSONResponse(
            content={
                "task_id": task_id,
                "status": "rendering_started",
                "output_path": request.output_path,
                "message": "Audiobook rendering started in background"
            },
            status_code=202
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start audiobook rendering: {str(e)}")

@router.post("/audiobook/preview")
async def render_voice_preview(request: VoicePreviewRequest):
    """Generate voice preview"""
    try:
        result = await audiobook_renderer.render_preview(
            text=request.text,
            voice_profile_id=request.profile_id,
            output_path=f"./voices/temp/preview_{request.profile_id}_{hash(request.text)}.wav",
            emotion=request.emotion
        )

        return FileResponse(
            path=result["output_path"],
            media_type="audio/wav",
            filename=f"preview_{request.profile_id}.wav"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate voice preview: {str(e)}")

@router.post("/audiobook/batch")
async def batch_render_segments(request: BatchRenderRequest, background_tasks: BackgroundTasks):
    """Batch render multiple audio segments"""
    try:
        # Ensure output directory exists
        os.makedirs(request.output_dir, exist_ok=True)

        # Start batch rendering in background
        task_id = f"batch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        background_tasks.add_task(
            audiobook_renderer.batch_render_segments,
            request.segments,
            request.output_dir
        )

        return JSONResponse(
            content={
                "task_id": task_id,
                "status": "batch_rendering_started",
                "output_dir": request.output_dir,
                "segment_count": len(request.segments),
                "message": "Batch rendering started in background"
            },
            status_code=202
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start batch rendering: {str(e)}")

# Utility Endpoints
@router.get("/status")
async def get_voice_system_status():
    """Get status of voice system components"""
    try:
        status = {
            "voice_engine": {
                "available": True,
                "pom_integration": voice_engine.pom.__class__.__name__ != "PhonatoryOutputModule"
            },
            "character_mapper": {
                "characters_loaded": len(character_mapper.characters),
                "voice_mappings": len(character_mapper.voice_mappings)
            },
            "narrator_optimizer": {
                "profiles_available": len(narrator_optimizer.narrator_profiles)
            },
            "directories": {
                "voices": os.path.exists("./voices"),
                "profiles": os.path.exists("./voices/profiles"),
                "temp": os.path.exists("./voices/temp")
            }
        }

        return JSONResponse(content=status)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")

@router.post("/cleanup")
async def cleanup_temp_files():
    """Clean up temporary voice files"""
    try:
        temp_dir = Path("./voices/temp")
        if temp_dir.exists():
            for temp_file in temp_dir.glob("*"):
                if temp_file.is_file():
                    temp_file.unlink()

        return JSONResponse(content={"message": "Temporary files cleaned up"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cleanup temp files: {str(e)}")

# File Upload Endpoint for Voice Samples
@router.post("/upload-sample")
async def upload_voice_sample(file: UploadFile = File(...)):
    """Upload voice sample file"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.wav', '.mp3', '.flac')):
            raise HTTPException(status_code=400, detail="Unsupported file format. Use WAV, MP3, or FLAC.")

        # Save uploaded file
        upload_dir = Path("./voices/samples")
        upload_dir.mkdir(exist_ok=True)

        file_path = upload_dir / f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"

        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)

        return JSONResponse(
            content={
                "filename": file.filename,
                "path": str(file_path),
                "size": len(content),
                "message": "Voice sample uploaded successfully"
            },
            status_code=201
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload voice sample: {str(e)}")