from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path

router = APIRouter()

@router.post("/ingest/upload")
async def upload_files(
    projectId: str = Form(...),
    files: list[UploadFile] = File(...)
):
    project_path = Path("vaults") / projectId / "raw"
    project_path.mkdir(parents=True, exist_ok=True)

    for file in files:
        contents = await file.read()
        (project_path / file.filename).write_bytes(contents)

    # TODO: trigger background clustering job
    return {"status": "received", "count": len(files)}
