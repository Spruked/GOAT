import os
from fastapi import APIRouter, HTTPException

router = APIRouter()

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../workspace'))
PROJECTS_DIR = os.path.join(WORKSPACE_ROOT, 'projects')

@router.post('/api/project/purge')
def purge_project(project_id: str):
    """Delete all files for a project (temporary mode)."""
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_dir):
        raise HTTPException(status_code=404, detail='Project not found')
    for root, dirs, files in os.walk(project_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for d in dirs:
            os.rmdir(os.path.join(root, d))
    os.rmdir(project_dir)
    return { 'message': f'Project {project_id} purged.' }
