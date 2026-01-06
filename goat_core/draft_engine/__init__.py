# goat_core/draft_engine/__init__.py
"""
GOAT Draft Engine - ScribeCore v1
The heart of GOAT's content generation system
"""

from .draft_pipeline import DraftPipeline, generate_goat_content
from .structure_interpreter import StructureInterpreter
from .content_generator import ContentGenerator
from .continuity_manager import ContinuityManager
from .tone_harmonizer import ToneHarmonizer
from .quality_validator import QualityValidator

__version__ = "1.0.0"
__author__ = "GOAT AI"
__description__ = "AI-powered content generation system for long-form writing"

__all__ = [
    "DraftPipeline",
    "generate_goat_content",
    "StructureInterpreter",
    "ContentGenerator",
    "ContinuityManager",
    "ToneHarmonizer",
    "QualityValidator"
]