# organizer_engine.py

from pathlib import Path
from typing import List
from fastapi import UploadFile

from .file_classifier import classify_file
from .folder_map import get_base_folders, get_root_folder


def create_base_structure(base_path: Path) -> Path:
    """
    Creates the full folder structure inside a temporary working directory.
    Returns the path to the root folder (e.g., Project_Files).
    """
    root_name = get_root_folder()
    root_dir = base_path / root_name
    root_dir.mkdir(parents=True, exist_ok=True)

    for folder in get_base_folders():
        (root_dir / folder).mkdir(parents=True, exist_ok=True)

    return root_dir


def save_files(base_path: Path, files: List[UploadFile]) -> None:
    """
    Saves incoming files into classified folders inside the structure.
    """
    root_dir = base_path / get_root_folder()

    for file in files:
        category = classify_file(file)
        target_folder = root_dir / category
        target_folder.mkdir(parents=True, exist_ok=True)

        destination = target_folder / file.filename

        with open(destination, "wb") as out:
            out.write(file.file.read())


def cleanup_empty_folders(base_path: Path) -> None:
    """
    Optional: removes empty folders after organizing.
    Useful if some categories receive no files.
    """
    root_dir = base_path / get_root_folder()

    for folder in root_dir.iterdir():
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
