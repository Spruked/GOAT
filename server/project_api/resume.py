
import os
import zipfile
import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from cryptography.fernet import Fernet
from .gproj_schema import validate_gproj, decrypt_gproj

router = APIRouter()

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../workspace'))
ENCRYPTION_KEY = os.environ.get('PROJECT_ENCRYPTION_KEY', Fernet.generate_key())
fernet = Fernet(ENCRYPTION_KEY)



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
    return { 'project': gproj_data, 'message': 'Project restored (demo)' }
