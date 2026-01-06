# models.py
"""
Podcast Engine Data Models
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class LegacyInput:
    """User input for legacy creation"""
    topic: str
    notes: str
    source_materials: List[str]
    intent: str  # "book", "course", "masterclass", etc.
    audience: str
    output_format: str
    tone: str = "professional"
    length_estimate: str = "medium"
    create_audiobook: bool = False
    voice: Optional[str] = None

@dataclass
class StructuredContent:
    """Auto-structured content"""
    title: str
    sections: List[Dict[str, Any]]
    key_points: List[str]
    flow: List[str]
    metadata: Dict[str, Any]

@dataclass
class ExpandedArtifact:
    """Final expanded content"""
    content_type: str
    title: str
    full_content: str
    sections: List[Dict[str, Any]]
    word_count: int
    estimated_time: str
