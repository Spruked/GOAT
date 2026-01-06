# routes/organizer.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import shutil
import logging

from organizer.file_classifier import classify_file, get_root_folder, get_target_folders, _load_config
from organizer.zip_builder import create_zip_with_manifest
from knowledge.graph import KnowledgeGraph
from vault.core import Vault
from datetime import datetime
from knowledge.graph import KnowledgeGraph
from vault.core import Glyph
import logging
from routes.auth import get_current_user_dependency
from user_tracker import user_tracker
from fastapi import Form
from vault.core import Vault

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organize", tags=["organize"])


@router.post("/")
async def organize_files(
    files: list[UploadFile] = File(...),
    save_to_vault: bool = Form(False),
    current_user: dict = Depends(get_current_user_dependency)
):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # Track user activity
    user_tracker.track_visit(
        user_id=current_user.get('email', 'anonymous'),
        platform='GOAT',
        session_id=str(uuid.uuid4()),
        page_url='/organizer'
    )
    
    session_id = str(uuid.uuid4())
    work_dir = Path("/tmp/organizer") / session_id
    try:
        work_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created work directory: {work_dir}")
    except Exception as e:
        logger.error(f"Failed to create work directory: {e}")
        raise HTTPException(status_code=500, detail="Failed to create work directory")

    root_folder_path = work_dir / get_root_folder()
    root_folder_path.mkdir(exist_ok=True)

    # Create all subfolders
    for folder in get_target_folders():
        (root_folder_path / folder).mkdir(exist_ok=True)

    # Save each file to its correct folder
    for file in files:
        if not file.filename:
            continue
        try:
            category = classify_file(file)
            target_path = root_folder_path / category / file.filename
            target_path.parent.mkdir(parents=True, exist_ok=True)

            content = await file.read()
            with open(target_path, "wb") as buffer:
                buffer.write(content)
            logger.info(f"Saved file {file.filename} to {category}")
        except Exception as e:
            logger.error(f"Failed to save file {file.filename}: {e}")
            continue

    # Create final ZIP with manifest
    zip_path = work_dir / "organized_files.zip"
    try:
        manifest = create_zip_with_manifest(root_folder_path, zip_path, session_id, current_user.get('email'))
        logger.info(f"Created ZIP with manifest: {zip_path}")
    except Exception as e:
        logger.error(f"Failed to create ZIP: {e}")
        raise HTTPException(status_code=500, detail="Failed to create ZIP")

    # Create glyph trace for UCM compatibility
    glyph_trace = None
    try:
        # Create glyph for the ZIP content
        with open(zip_path, 'rb') as f:
            zip_data = f.read()

        vault = Vault()
        glyph = vault.store_data(zip_data, f"organizer_{session_id}.zip", current_user.get('email', 'anonymous'))
        glyph_trace = f"glyph://{glyph.id}"

        # Link to knowledge graph for UCM compatibility
        kg = KnowledgeGraph()
        org_data = {
            "type": "file_organization",
            "session_id": session_id,
            "user_id": current_user.get('email'),
            "manifest": manifest,
            "glyph_id": glyph.id,
            "created_at": datetime.utcnow().isoformat()
        }
        kg.create_node("FileOrganization", org_data)

        logger.info(f"Created glyph trace: {glyph_trace}")
    except Exception as e:
        logger.warning(f"Failed to create glyph trace: {e}")
        # Don't fail the request if glyph creation fails

    vault_url = None
    if save_to_vault:
        vault_url = f"/vault/{glyph.id}"
        logger.info(f"Saved to vault: {vault_url}")

    return {
        "status": "success",
        "download_url": f"/organizer/organize/download/{session_id}",
        "vault_url": vault_url,
        "glyph_trace": glyph_trace,
        "manifest": manifest,
        "zip_ready": True,
        "saved_to_vault": save_to_vault and vault_url is not None
    }


@router.get("/config")
async def get_config():
    """Get current classification configuration"""
    return _load_config()


@router.post("/preview")
async def preview_organization(files: list[UploadFile] = File(...)):
    """Preview how files would be organized without creating ZIP"""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    preview = {}
    for file in files:
        if not file.filename:
            continue
        category = classify_file(file)
        if category not in preview:
            preview[category] = []
        preview[category].append(file.filename)
    
    return {
        "preview": preview,
        "total_files": len([f for f in files if f.filename]),
        "categories": list(preview.keys())
    }


@router.get("/download/{session_id}")
async def download_zip(session_id: str, current_user: dict = Depends(get_current_user_dependency)):
    """Download the organized ZIP file"""
    zip_path = Path("/tmp/organizer") / session_id / "organized_files.zip"
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="ZIP file not found")
    
    # Verify ownership by checking manifest
    manifest_path = Path("/tmp/organizer") / session_id / "manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            if manifest.get('user_id') != current_user.get('email'):
                raise HTTPException(status_code=403, detail="Access denied")
        except:
            pass  # If manifest can't be read, allow download (backward compatibility)
    
    try:
        return FileResponse(zip_path, media_type='application/zip', filename='organized_files.zip')
    except Exception as e:
        logger.error(f"Failed to serve ZIP: {e}")
        raise HTTPException(status_code=500, detail="Failed to download ZIP")


@router.get("/manifest/{session_id}")
async def get_manifest(session_id: str, current_user: dict = Depends(get_current_user_dependency)):
    """Get manifest for a completed organization session"""
    manifest_path = Path("/tmp/organizer") / session_id / "manifest.json"
    if not manifest_path.exists():
        raise HTTPException(status_code=404, detail="Manifest not found")
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # Verify ownership
        if manifest.get('user_id') != current_user.get('email'):
            raise HTTPException(status_code=403, detail="Access denied")
        
        return manifest
    except Exception as e:
        logger.error(f"Failed to read manifest: {e}")
        raise HTTPException(status_code=500, detail="Failed to read manifest")