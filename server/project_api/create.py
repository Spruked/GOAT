import os
import json
from fastapi import APIRouter, HTTPException
from .gproj_schema import new_gproj, validate_gproj

router = APIRouter()

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../workspace'))
PROJECTS_DIR = os.path.join(WORKSPACE_ROOT, 'projects')

@router.post('/api/project/create_from_onboarding')
def create_project_from_onboarding(payload: dict):
    """Create a new project folder and project.gproj from onboarding selections."""
    project_id = payload.get('project_id')
    owner = payload.get('owner')
    title = payload.get('title')
    artifact_goal = payload.get('artifact_goal')
    audience = payload.get('audience')
    structure_type = payload.get('structure_type')
    retention_mode = payload.get('retention_mode')
    onboarding_selections = payload.get('onboarding_selections', {})
    if not all([project_id, owner, title, artifact_goal, audience, structure_type, retention_mode]):
        raise HTTPException(status_code=400, detail='Missing required onboarding fields')
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    if os.path.exists(project_dir):
        raise HTTPException(status_code=409, detail='Project already exists')
    os.makedirs(project_dir, exist_ok=True)
    gproj = new_gproj(
        project_id=project_id,
        owner=owner,
        title=title,
        artifact_goal=artifact_goal,
        audience=audience,
        structure_type=structure_type,
        retention_mode=retention_mode,
        onboarding_selections=onboarding_selections
    )
    validate_gproj(gproj)
    gproj_path = os.path.join(project_dir, 'project.gproj')
    with open(gproj_path, 'w', encoding='utf-8') as f:
        json.dump(gproj, f, indent=2)
    return { 'project_id': project_id, 'message': 'Project created', 'gproj': gproj }
