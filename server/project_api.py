import os
import io
import zipfile
import json
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
from typing import List
from cryptography.fernet import Fernet

router = APIRouter()

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../workspace'))
PROJECTS_DIR = os.path.join(WORKSPACE_ROOT, 'projects')
EXPORTS_DIR = os.path.join(WORKSPACE_ROOT, 'project_exports')

# Utility: get encryption key (in production, use env var or user secret)
ENCRYPTION_KEY = os.environ.get('PROJECT_ENCRYPTION_KEY', Fernet.generate_key())
fernet = Fernet(ENCRYPTION_KEY)

def get_project_dir(project_id: str) -> str:
    return os.path.join(PROJECTS_DIR, project_id)

def get_project_gproj_path(project_id: str) -> str:
    return os.path.join(get_project_dir(project_id), 'project.gproj')

def encrypt_gproj(data: dict) -> bytes:
    raw = json.dumps(data).encode('utf-8')
    return fernet.encrypt(raw)

def decrypt_gproj(data: bytes) -> dict:
    raw = fernet.decrypt(data)
    return json.loads(raw.decode('utf-8'))

@router.post('/api/project/export')
def export_project_zip(project_id: str):
    """Package all project files and encrypted project.gproj into a ZIP for download."""
    project_dir = get_project_dir(project_id)
    if not os.path.exists(project_dir):
        raise HTTPException(status_code=404, detail='Project not found')
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files in project dir
        for root, _, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_dir)
                if file == 'project.gproj':
                    # Encrypt project.gproj
                    with open(file_path, 'r', encoding='utf-8') as f:
                        gproj_data = json.load(f)
                    encrypted = encrypt_gproj(gproj_data)
                    zipf.writestr('project.gproj', encrypted)
                else:
                    zipf.write(file_path, arcname)
    zip_buffer.seek(0)
    filename = f'GOAT_Project_{project_id}.zip'
    return StreamingResponse(zip_buffer, media_type='application/zip', headers={
        'Content-Disposition': f'attachment; filename="{filename}"'
    })

@router.post('/api/project/resume')
def resume_project(file: UploadFile = File(...)):
    """Accept a project ZIP, extract, decrypt project.gproj, and restore state."""
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail='Invalid file type')
    temp_dir = os.path.join(WORKSPACE_ROOT, 'temp_resume')
    os.makedirs(temp_dir, exist_ok=True)
    zip_path = os.path.join(temp_dir, file.filename)
    with open(zip_path, 'wb') as f:
        f.write(file.file.read())
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(temp_dir)
    gproj_path = os.path.join(temp_dir, 'project.gproj')
    if not os.path.exists(gproj_path):
        raise HTTPException(status_code=400, detail='project.gproj missing')
    with open(gproj_path, 'rb') as f:
        encrypted = f.read()
    try:
        gproj_data = decrypt_gproj(encrypted)
    except Exception:
        raise HTTPException(status_code=400, detail='Failed to decrypt project.gproj')
    # Here, you would restore the project to the user's workspace
    # For demo, just return the project metadata
    return { 'project': gproj_data, 'message': 'Project restored (demo)' }
