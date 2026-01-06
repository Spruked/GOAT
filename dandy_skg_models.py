from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class BuildReview:
    """A user build that Phil & Jim will review"""
    build_id: str
    user_id: str
    project_name: str
    summary: str
    tech_stack: List[str]
    code_snippets: List[str]
    preview_url: Optional[str] = None
    submitted_at: datetime = field(default_factory=datetime.now)
    review_status: str = "pending"  # pending, reviewed, aired

@dataclass
class PodcastSegment:
    """Generated segment for Phil & Jim's show"""
    segment_id: str
    build_review: BuildReview
    speaker: str  # "phil" or "jim"
    script: str  # Generated dialogue
    duration_seconds: int
    tone: str  # "enthusiastic", "playful", "technical"
    platform_optimized: Dict[str, str]  # tiktok, youtube, etc.
