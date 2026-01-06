# cali_scripts/__init__.py
"""
Caleon Scripted Response System (CALI Scripts)
Provides consistent, non-LLM responses across the GOAT platform.
"""

__version__ = "1.0.0"
__author__ = "Caleon Prime"

from .engine import CaliScripts

__all__ = ["CaliScripts"]