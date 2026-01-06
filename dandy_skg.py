# =================================================
# PHIL & JIM DANDY SKG v3.1
# Multi-Persona Podcast & Social Content Engine for GOAT Channels
# =================================================

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
import numpy as np
from datetime import datetime
import json
import hashlib
import asyncio
from collections import defaultdict
import uuid
import random

# =================================================
# 1. DUAL PERSONA DATA MODELS
# =================================================

@dataclass
class PersonaProfile:
    """Phil or Jim's distinct voice and style"""
    persona_id: str  # "phil" or "jim"
    name: str
    trait_vector: Dict[str, float]  # "witty": 0.92, "technical": 0.71
    speech_patterns: List[str]  # "You know what I love about this..."
    catchphrases: List[str]  # "That's a Jim Dandy idea!"
    critique_style: str  # "constructive", "playful", "deep_dive"
    expertise_areas: List[str]  # "frontend", "design", "devops"
    goofball_factor: float  # 0.0 to 1.0 (Jim is higher)
