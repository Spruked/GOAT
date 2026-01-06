# folder_map.py

from typing import List, Dict, Any
from .file_classifier import get_project_structure, get_root_folder_name

def get_base_folders() -> List[str]:
    """
    Returns the list of folder names defined in the project structure config.
    Falls back to safe defaults if missing.
    """
    structure = get_project_structure()
    return structure.get("folders", ["Code", "Documents", "Media", "Data", "Archives", "Notes", "Misc"])


def get_root_folder() -> str:
    """
    Returns the root folder name, such as 'Project_Files'.
    """
    return get_root_folder_name()


def build_folder_map() -> Dict[str, Any]:
    """
    Returns the entire project structure as a dictionary:
    {
        "root": "Project_Files",
        "folders": [...],
        "rules": {...},
        "special_filenames": {...}
    }
    """
    return get_project_structure()
