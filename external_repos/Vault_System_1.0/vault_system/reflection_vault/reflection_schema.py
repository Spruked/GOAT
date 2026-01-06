# reflection_schema.py

from typing import Dict, Any
from dataclasses import dataclass, field
import time

@dataclass
class ReflectionEntry:
    module: str                  # which module the insight came from
    insight: str                 # summary of what she learned
    context: Dict[str, Any]      # any supporting data
    timestamp: float = field(default_factory=time.time)
    cycle_id: int = 0            # reflection cycle number