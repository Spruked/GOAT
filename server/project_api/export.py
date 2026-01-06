
import os
import io
import zipfile
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from cryptography.fernet import Fernet
from .gproj_schema import validate_gproj, encrypt_gproj, GPROJ_VERSION

router = APIRouter()

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../workspace'))
PROJECTS_DIR = os.path.join(WORKSPACE_ROOT, 'projects')

ENCRYPTION_KEY = os.environ.get('PROJECT_ENCRYPTION_KEY', Fernet.generate_key())
fernet = Fernet(ENCRYPTION_KEY)

def get_project_dir(project_id: str) -> str:
    return os.path.join(PROJECTS_DIR, project_id)



@router.get('/api/project/export')
def export_project_zip(project_id: str):
    """Package all project files and encrypted project.gproj into a ZIP for download."""
    project_dir = get_project_dir(project_id)
    if not os.path.exists(project_dir):
        raise HTTPException(status_code=404, detail='Project not found')
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_dir)
                if file == 'project.gproj':
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
