"""
GOAT Write Routes - Text Editor Interface
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
from datetime import datetime
import os
from server.auth import get_current_user
from models.user import User

router = APIRouter()

class WriteSession(BaseModel):
    session_id: str
    title: str
    content_type: str = "article"  # article, book, notes, etc.
    initial_content: Optional[str] = ""

class SaveContent(BaseModel):
    content: str
    auto_save: bool = True

@router.post("/start")
async def start_write_session(session: WriteSession, current_user: User = Depends(get_current_user)):
    """
    Start a new writing session
    """
    try:
        # Generate session ID if not provided
        if not session.session_id:
            session.session_id = str(uuid.uuid4())

        # TODO: Initialize vault storage for this session
        # TODO: Set up auto-save mechanism

        vault_path = f"data/vault/write_sessions/{session.session_id}"

        # Ensure directory exists
        os.makedirs(vault_path, exist_ok=True)

        return {
            "status": "started",
            "session_id": session.session_id,
            "vault_path": vault_path,
            "editor_url": f"/write/editor/{session.session_id}",
            "message": "Writing session initialized",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start writing session: {str(e)}")

@router.post("/save/{session_id}")
async def save_content(session_id: str, save_data: SaveContent, current_user: User = Depends(get_current_user)):
    """
    Save content to vault
    """
    try:
        vault_path = f"data/vault/write_sessions/{session_id}"
        content_file = f"{vault_path}/content.md"

        # Save content
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(save_data.content)

        # TODO: Trigger auto-processing if enabled
        # TODO: Update knowledge graph
        # TODO: Generate suggestions

        return {
            "status": "saved",
            "session_id": session_id,
            "file_path": content_file,
            "word_count": len(save_data.content.split()),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save content: {str(e)}")

@router.get("/load/{session_id}")
async def load_content(session_id: str, current_user: User = Depends(get_current_user)):
    """
    Load content from vault
    """
    try:
        vault_path = f"data/vault/write_sessions/{session_id}"
        content_file = f"{vault_path}/content.md"

        if not os.path.exists(content_file):
            return {
                "session_id": session_id,
                "content": "",
                "message": "New session - no content yet"
            }

        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "session_id": session_id,
            "content": content,
            "word_count": len(content.split()),
            "last_modified": datetime.fromtimestamp(os.path.getmtime(content_file)).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load content: {str(e)}")

@router.post("/process/{session_id}")
async def process_content(session_id: str, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
    """
    Process content through UCM for suggestions and structuring
    """
    try:
        # Load content
        vault_path = f"data/vault/write_sessions/{session_id}"
        content_file = f"{vault_path}/content.md"

        if not os.path.exists(content_file):
            raise HTTPException(status_code=404, detail="Content not found")

        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # TODO: Send to UCM for processing
        # TODO: Generate suggestions, structure, etc.

        background_tasks.add_task(process_content_background, session_id, content)

        return {
            "status": "processing",
            "session_id": session_id,
            "message": "Content processing started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process content: {str(e)}")

async def process_content_background(session_id: str, content: str):
    """
    Background processing of content
    """
    try:
        # Use GOAT's content engine for processing
        from podcast_engine import PodcastEngine, LegacyInput

        engine = PodcastEngine()
        user_input = LegacyInput(
            topic=f"Written Content: {session_id}",
            notes=content,
            source_materials=[f"write_session_{session_id}.md"],
            intent="book",
            audience="readers",
            output_format="manuscript",
            tone="professional",
            length_estimate="medium"
        )

        structured = engine._structure_content(user_input)

        # Save processed results to vault
        vault_path = f"data/vault/write_sessions/{session_id}"
        import os
        os.makedirs(vault_path, exist_ok=True)

        # Save structured analysis
        with open(f"{vault_path}/analysis.json", 'w') as f:
            import json
            json.dump({
                "title": structured.title,
                "key_points": structured.key_points,
                "sections": [section.get("title", "Untitled") for section in structured.sections],
                "word_count": len(content.split()),
                "processed_at": str(datetime.utcnow())
            }, f, indent=2)

        print(f"Content processed for session {session_id}: {structured.title}")

    except Exception as e:
        print(f"Error processing content for session {session_id}: {str(e)}")