# routes/podcast_engine.py
"""
Podcast Engine API Routes
GOAT's core legacy creation system
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import json
import tempfile
import os
from pathlib import Path

from podcast_engine import PodcastEngine, LegacyInput
# from services.visidata_service import visidata_service
from routes.auth import get_current_user_dependency
import pyttsx3

podcast_engine = PodcastEngine()

router = APIRouter()

@router.get("/podcast/voices")
async def get_available_voices():
    """Get available TTS voices for audiobook creation"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        available_voices = []
        for i, voice in enumerate(voices[:5]):  # Limit to 5 voices
            available_voices.append({
                "id": voice.id,
                "name": voice.name,
                "language": getattr(voice, 'languages', ['en'])[0] if hasattr(voice, 'languages') else 'en',
                "gender": "Female" if "female" in voice.name.lower() or "zira" in voice.name.lower() else "Male"
            })
        return {"voices": available_voices}
    except Exception as e:
        # Fallback voices if TTS fails
        return {"voices": [
            {"id": "voice_1", "name": "Default Male", "language": "en", "gender": "Male"},
            {"id": "voice_2", "name": "Default Female", "language": "en", "gender": "Female"},
            {"id": "voice_3", "name": "Alternative Male", "language": "en", "gender": "Male"}
        ]}

@router.post("/podcast/create-legacy")
async def create_legacy(
    topic: str = Form(...),
    notes: str = Form(...),
    intent: str = Form(...),
    audience: str = Form(...),
    output_format: str = Form(...),
    tone: str = Form("professional"),
    length_estimate: str = Form("medium"),
    create_audiobook: bool = Form(False),
    voice: Optional[str] = Form(None),
    source_files: Optional[list[UploadFile]] = File(None),
    current_user: dict = Depends(get_current_user_dependency)
):
    """Create a legacy using the podcast engine pipeline"""

    try:
        # Process uploaded source files
        source_materials = []
        if source_files:
            for file in source_files:
                # Save temporarily for analysis
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp:
                    content = await file.read()
                    temp.write(content)
                    temp_path = temp.name

                # Analyze with VisiData
                # analysis = visidata_service.analyze_file(temp_path)
                analysis = {"type": "mock", "insights": "Sample analysis"}
                source_materials.append({
                    "filename": file.filename,
                    "path": temp_path,
                    "analysis": analysis
                })

        # Create legacy input
        user_input = LegacyInput(
            topic=topic,
            notes=notes,
            source_materials=[s["filename"] for s in source_materials],
            intent=intent,
            audience=audience,
            output_format=output_format,
            tone=tone,
            length_estimate=length_estimate,
            create_audiobook=create_audiobook,
            voice=voice
        )

        # Run podcast engine
        result = podcast_engine.create_legacy(user_input)

        # Add VisiData insights to result
        if source_materials:
            result["visidata_insights"] = [s["analysis"] for s in source_materials]

            # Get structure suggestions
            structure_suggestions = []
            for analysis in result["visidata_insights"]:
                # suggestion = visidata_service.suggest_structure(analysis, intent)
                suggestion = "Mock structure suggestion"
                structure_suggestions.append(suggestion)

            result["structure_suggestions"] = structure_suggestions

        # Clean up temp files
        for source in source_materials:
            try:
                os.remove(source["path"])
            except:
                pass

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Legacy creation failed: {str(e)}")

@router.post("/podcast/analyze-data")
async def analyze_data_file(file: UploadFile = File(...)):
    """Analyze a data file with VisiData"""

    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp:
            content = await file.read()
            temp.write(content)
            temp_path = temp.name

        # Analyze with VisiData
        # analysis = visidata_service.analyze_file(temp_path)
        analysis = {"type": "mock", "insights": "Sample analysis"}

        # Get knowledge graph representation
        # knowledge_graph = visidata_service.convert_to_knowledge_graph(analysis)
        knowledge_graph = {"nodes": [], "edges": []}

        # Clean up
        os.remove(temp_path)

        return JSONResponse(content={
            "analysis": analysis,
            "knowledge_graph": knowledge_graph,
            "structure_suggestions": {
                "book": "Mock book structure",
                "course": "Mock course structure",
                "masterclass": "Mock masterclass structure"
            }
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data analysis failed: {str(e)}")

@router.get("/podcast/legacy/{legacy_id}")
async def get_legacy(legacy_id: str):
    """Get a created legacy"""

    try:
        # Find legacy in output directory
        legacy_path = podcast_engine.output_dir / legacy_id

        if not legacy_path.exists():
            raise HTTPException(status_code=404, detail="Legacy not found")

        # Read metadata
        metadata_file = legacy_path / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {"legacy_id": legacy_id, "error": "Metadata not found"}

        # Read content
        content_file = legacy_path / "full_content.md"
        content = ""
        if content_file.exists():
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()

        return JSONResponse(content={
            "legacy_id": legacy_id,
            "metadata": metadata,
            "content": content,
            "files": [f.name for f in legacy_path.iterdir() if f.is_file()]
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve legacy: {str(e)}")

@router.get("/podcast/caleon-guidance/{step}")
async def get_caleon_guidance(step: str, context: Optional[str] = None):
    """Get Caleon's guidance for a specific step"""

    try:
        context_dict = json.loads(context) if context else {}
        guidance = podcast_engine.get_caleon_guidance(step, context_dict)

        return JSONResponse(content={
            "step": step,
            "guidance": guidance,
            "context": context_dict
        })

    except Exception as e:
        return JSONResponse(content={
            "step": step,
            "guidance": "I'm here to guide you through creating your greatest work.",
            "error": str(e)
        })

@router.get("/podcast/minting-suggestions/{content_type}")
async def get_minting_suggestions(content_type: str):
    """Get minting suggestions for a content type"""

    suggestions = podcast_engine._get_minting_suggestions(content_type)

    return JSONResponse(content={
        "content_type": content_type,
        "suggestions": suggestions,
        "partners": ["certsig", "truemark"]
    })