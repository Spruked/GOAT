# zip_builder.py

import os
import zipfile
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

def generate_file_checksum(file_path: Path) -> str:
    """Generate SHA256 checksum for a file"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def create_manifest(source_folder: Path, session_id: str, user_id: str = None) -> Dict[str, Any]:
    """Create a manifest JSON with file metadata and checksums"""
    manifest = {
        "manifest_version": "1.0",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "session_id": session_id,
        "user_id": user_id or "anonymous",
        "source": "GOAT Organizer",
        "total_files": 0,
        "total_size": 0,
        "files": []
    }

    for root, _, files in os.walk(source_folder):
        for file in files:
            full_path = Path(root) / file
            rel_path = full_path.relative_to(source_folder)
            file_size = full_path.stat().st_size
            checksum = generate_file_checksum(full_path)

            manifest["files"].append({
                "path": str(rel_path),
                "size": file_size,
                "checksum_sha256": checksum,
                "modified": datetime.fromtimestamp(full_path.stat().st_mtime).isoformat()
            })

            manifest["total_files"] += 1
            manifest["total_size"] += file_size

    return manifest

def create_zip_with_manifest(source_folder: Path, zip_path: Path, session_id: str, user_id: str = None) -> Dict[str, Any]:
    """
    Creates a ZIP archive with manifest and checksums.
    Returns the manifest data.
    """
    manifest = create_manifest(source_folder, session_id, user_id)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add manifest first
        manifest_json = json.dumps(manifest, indent=2)
        zipf.writestr("manifest.json", manifest_json)

        # Add all files
        for root, _, files in os.walk(source_folder):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(source_folder)
                zipf.write(full_path, arcname=rel_path)

    return manifest

def create_zip(source_folder: Path, zip_path: Path) -> None:
    """
    Legacy function for backward compatibility.
    Creates a ZIP archive from the contents of source_folder.
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(source_folder)
                zipf.write(full_path, arcname=rel_path)
