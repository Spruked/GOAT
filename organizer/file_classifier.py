# Organizer/file_classifier.py
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from fastapi import UploadFile


CONFIG_PATH = Path(__file__).parent / "templates" / "default_structure.json"


@lru_cache(maxsize=1)
def _load_config() -> Dict[str, Any]:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load {CONFIG_PATH}: {e}")

    print("Using built-in default classification rules")
    return {
        "root_folder": "Project_Files",
        "folders": ["Code", "Documents", "Media", "Data", "Archives", "Notes", "Misc"],
        "rules": {},
        "special_filenames": {}
    }


def classify_file(file: UploadFile) -> str:
    if not file or not file.filename:
        return "Misc"

    config = _load_config()
    filename = file.filename.lower()
    ext = Path(file.filename).suffix.lower()

    # Special filenames first
    for category, names in config.get("special_filenames", {}).items():
        if any(filename == n.lower() or filename.endswith("/" + n.lower()) for n in names):
            return category

    # Then extension rules
    for category, exts in config.get("rules", {}).items():
        if "*" in exts:
            continue
        if ext in [e.lower() for e in exts]:
            return category

    return "Misc"


def get_root_folder() -> str:
    return _load_config().get("root_folder", "Project_Files")


def get_target_folders() -> list[str]:
    return _load_config().get("folders", ["Code", "Documents", "Media", "Data", "Archives", "Notes", "Misc"])


def get_project_structure() -> Dict[str, Any]:
    return _load_config()


def get_root_folder_name() -> str:
    return _load_config().get("root_folder", "Project_Files")