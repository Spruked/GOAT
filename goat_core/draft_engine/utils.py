import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration"""
    level = getattr(logging, log_level.upper(), logging.INFO)

    handlers: List[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers
    )

def count_words(text: str) -> int:
    """Count words in text"""
    return len(re.findall(r'\b\w+\b', text))

def clean_markdown(text: str) -> str:
    """Clean and normalize markdown text"""
    # Remove extra whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text.strip()

def ensure_directory(path: Path):
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)

def load_json_file(file_path: Path) -> Dict[str, Any]:
    """Load JSON file safely"""
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Failed to load {file_path}: {e}")
    return {}

def save_json_file(file_path: Path, data: Dict[str, Any]):
    """Save JSON file safely"""
    ensure_directory(file_path.parent)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_section_titles(text: str) -> List[str]:
    """Extract section titles from markdown text"""
    titles = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            # Remove markdown headers
            title = re.sub(r'^#+\s*', '', line)
            titles.append(title)
    return titles

def format_timestamp() -> str:
    """Get current timestamp in readable format"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")