# podcast_engine/__init__.py
"""
GOAT Podcast Engine

Text → Speaker Detection → Multi-Voice Script → Audio Synthesis → Episode Stitching → RSS Export
"""

__version__ = "1.0.0"
__author__ = "GOAT Podcast Engine"

from .engine import PodcastEngine
from .models import LegacyInput, StructuredContent, ExpandedArtifact
from .bridges import UCMBridge, DALSBridge

__all__ = [
    "PodcastEngine",
    "LegacyInput",
    "StructuredContent",
    "ExpandedArtifact",
    "UCMBridge",
    "DALSBridge",
]