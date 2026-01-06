# audiobook_engine/__init__.py
"""
Audiobook Engine

A complete SSML → audio → stitching → M4B export pipeline
for generating audiobooks with voice profiles and chapter markers.
"""

__version__ = "1.0.0"
__author__ = "GOAT Audiobook Engine"

from .config import *
from .models import *
from .core import *
from .utils import *

__all__ = [
    # Version info
    "__version__", "__author__"
]