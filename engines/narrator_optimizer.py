# engines/narrator_optimizer.py
"""
Narrator Optimizer: Optimizes narrator voice for clarity and engagement in audiobooks
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
import asyncio
import statistics

@dataclass
class TextSegment:
    """Segment of text with metadata"""
    text: str
    segment_type: str  # "main", "footnote", "quote", "heading", "list_item"
    complexity_score: float
    technical_terms: List[str]
    emotional_tone: str
    reading_speed: str  # "slow", "normal", "fast"

@dataclass
class NarratorProfile:
    """Narrator voice profile optimized for content type"""
    profile_id: str
    content_type: str  # "fiction", "nonfiction", "poetry", "technical"
    clarity_settings: Dict[str, Any]
    engagement_settings: Dict[str, Any]
    pacing_profiles: Dict[str, Dict[str, Any]]
    technical_enhancements: Dict[str, Any]

class NarratorOptimizer:
    """
    Optimizes narrator voice for different content types and reading contexts
    """

    def __init__(self, voice_engine):
        self.voice_engine = voice_engine
        self.narrator_profiles: Dict[str, NarratorProfile] = {}
        self.technical_terms_db = self._load_technical_terms()
        self.content_patterns = self._load_content_patterns()

    def _load_technical_terms(self) -> Dict[str, Dict[str, Any]]:
        """Load database of technical terms and pronunciation guides"""
        return {
            "algorithm": {"pronunciation": "AL-go-rithm", "category": "computer_science"},
            "neural": {"pronunciation": "NOO-rul", "category": "neuroscience"},
            "quantum": {"pronunciation": "KWON-tum", "category": "physics"},
            "photosynthesis": {"pronunciation": "foh-toh-SIN-thuh-sis", "category": "biology"},
            "entrepreneur": {"pronunciation": "ahn-truh-pruh-NUR", "category": "business"},
            "epistemology": {"pronunciation": "ih-pis-tuh-MOL-uh-jee", "category": "philosophy"},
            "quasar": {"pronunciation": "KWAY-sar", "category": "astronomy"},
            "cryptocurrency": {"pronunciation": "krip-toh-KUR-uhn-see", "category": "finance"}
        }

    def _load_content_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load content type patterns and optimization rules"""
        return {
            "fiction": {
                "emotional_range": ["neutral", "dramatic", "intimate", "suspenseful"],
                "pacing": {"dialogue": "fast", "description": "moderate", "action": "fast"},
                "clarity_boost": 0.7,
                "engagement_boost": 0.9
            },
            "nonfiction": {
                "emotional_range": ["neutral", "authoritative", "enthusiastic"],
                "pacing": {"explanation": "moderate", "examples": "normal", "conclusion": "slow"},
                "clarity_boost": 1.0,
                "engagement_boost": 0.6
            },
            "poetry": {
                "emotional_range": ["lyrical", "dramatic", "intimate"],
                "pacing": {"verse": "slow", "chorus": "moderate", "pause": "long"},
                "clarity_boost": 0.8,
                "engagement_boost": 1.0
            },
            "technical": {
                "emotional_range": ["neutral", "precise"],
                "pacing": {"definition": "slow", "example": "normal", "formula": "very_slow"},
                "clarity_boost": 1.2,
                "engagement_boost": 0.4
            }
        }

    async def create_narrator_profile(
        self,
        content_type: str,
        name: str = "default",
        custom_settings: Optional[Dict[str, Any]] = None
    ) -> NarratorProfile:
        """
        Create an optimized narrator profile for a specific content type
        """
        profile_id = f"narrator_{content_type}_{name}"

        # Get base settings for content type
        base_patterns = self.content_patterns.get(content_type, self.content_patterns["nonfiction"])

        # Create voice profile
        voice_result = await self.voice_engine.create_voice_profile(
            creation_method="parameter",
            name=f"{name}_{content_type}_narrator",
            description=f"Optimized narrator voice for {content_type} content",
            voice_type="narrator",
            param_config=self._build_narrator_voice_params(content_type, custom_settings)
        )

        # Build narrator profile
        profile = NarratorProfile(
            profile_id=profile_id,
            content_type=content_type,
            clarity_settings=self._build_clarity_settings(content_type, base_patterns),
            engagement_settings=self._build_engagement_settings(content_type, base_patterns),
            pacing_profiles=self._build_pacing_profiles(content_type, base_patterns),
            technical_enhancements=self._build_technical_enhancements(content_type)
        )

        self.narrator_profiles[profile_id] = profile
        return profile

    def _build_narrator_voice_params(self, content_type: str, custom_settings: Optional[Dict] = None) -> Dict:
        """Build voice synthesis parameters for narrator"""
        base_params = {
            "tension": 0.6,
            "breathiness": 0.2,
            "vibrato_rate": 4.0,
            "lip_rounding": 0.4,
            "articulation_precision": 0.9,
            "tongue_position": "alveolar",
            "sharpness": 0.8,
            "nasal": False,
            "nasalization": 0.0
        }

        # Adjust based on content type
        adjustments = {
            "fiction": {
                "articulation_precision": 1.0,
                "breathiness": 0.25,
                "vibrato_rate": 4.2
            },
            "nonfiction": {
                "articulation_precision": 1.1,
                "tension": 0.65,
                "lip_rounding": 0.45
            },
            "poetry": {
                "breathiness": 0.3,
                "vibrato_rate": 4.5,
                "articulation_precision": 0.95
            },
            "technical": {
                "articulation_precision": 1.2,
                "tension": 0.7,
                "sharpness": 0.9
            }
        }

        if content_type in adjustments:
            for param, value in adjustments[content_type].items():
                base_params[param] = value

        # Apply custom settings
        if custom_settings:
            base_params.update(custom_settings)

        return base_params

    def _build_clarity_settings(self, content_type: str, base_patterns: Dict) -> Dict[str, Any]:
        """Build clarity enhancement settings"""
        clarity_boost = base_patterns["clarity_boost"]

        return {
            "articulation_enhancement": clarity_boost,
            "pause_insertion": True,
            "emphasis_markers": content_type in ["technical", "nonfiction"],
            "pronunciation_guides": content_type == "technical",
            "speed_adjustment": {
                "complex_sentences": 0.9,
                "technical_terms": 0.8,
                "quotes": 0.95
            }
        }

    def _build_engagement_settings(self, content_type: str, base_patterns: Dict) -> Dict[str, Any]:
        """Build engagement enhancement settings"""
        engagement_boost = base_patterns["engagement_boost"]

        return {
            "prosody_variation": engagement_boost,
            "emotional_markers": content_type == "fiction",
            "rhythm_enhancement": content_type == "poetry",
            "intonation_curves": {
                "questions": "rising",
                "exclamation": "peak",
                "statements": "declining"
            },
            "pause_dynamics": {
                "sentence_end": 0.5,
                "paragraph_end": 1.0,
                "chapter_end": 2.0
            }
        }

    def _build_pacing_profiles(self, content_type: str, base_patterns: Dict) -> Dict[str, Dict[str, Any]]:
        """Build pacing profiles for different text types"""
        base_pacing = base_patterns["pacing"]

        profiles = {}
        for segment_type, speed in base_pacing.items():
            profiles[segment_type] = {
                "base_speed": speed,
                "variability": 0.1,
                "pause_after": self._get_pause_duration(segment_type),
                "emphasis_boost": self._get_emphasis_boost(segment_type, content_type)
            }

        return profiles

    def _get_pause_duration(self, segment_type: str) -> float:
        """Get recommended pause duration after segment type"""
        pauses = {
            "dialogue": 0.3,
            "description": 0.2,
            "action": 0.1,
            "explanation": 0.4,
            "examples": 0.3,
            "conclusion": 0.6,
            "verse": 0.5,
            "chorus": 0.3,
            "definition": 0.5,
            "formula": 0.8
        }
        return pauses.get(segment_type, 0.2)

    def _get_emphasis_boost(self, segment_type: str, content_type: str) -> float:
        """Get emphasis boost for segment type"""
        if content_type == "fiction":
            emphasis = {
                "dialogue": 1.2,
                "action": 1.1,
                "description": 0.9
            }
        elif content_type == "technical":
            emphasis = {
                "definition": 1.1,
                "formula": 1.3,
                "examples": 1.0
            }
        else:
            emphasis = {segment_type: 1.0}

        return emphasis.get(segment_type, 1.0)

    def _build_technical_enhancements(self, content_type: str) -> Dict[str, Any]:
        """Build technical enhancement settings"""
        return {
            "pronunciation_database": content_type == "technical",
            "jargon_detection": True,
            "abbreviation_expansion": content_type in ["technical", "nonfiction"],
            "number_pronunciation": {
                "years": "expanded",  # "nineteen eighty-four" vs "1984"
                "percentages": "with_word",  # "25 percent"
                "fractions": "verbal"  # "one half"
            },
            "foreign_word_handling": "phonetic_guides"
        }

    async def analyze_text_segments(self, text: str, content_type: str) -> List[TextSegment]:
        """
        Analyze text and break into optimized segments for narration
        """
        # Split text into logical segments
        segments = self._segment_text(text)

        analyzed_segments = []
        for segment_text, segment_type in segments:
            segment = TextSegment(
                text=segment_text,
                segment_type=segment_type,
                complexity_score=self._calculate_complexity(segment_text),
                technical_terms=self._identify_technical_terms(segment_text),
                emotional_tone=self._detect_emotional_tone(segment_text),
                reading_speed=self._determine_reading_speed(segment_text, segment_type, content_type)
            )
            analyzed_segments.append(segment)

        return analyzed_segments

    def _segment_text(self, text: str) -> List[Tuple[str, str]]:
        """Split text into logical segments"""
        segments = []

        # Split by paragraphs first
        paragraphs = text.split('\n\n')

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Classify paragraph type
            para_type = self._classify_paragraph(para)

            if para_type == "dialogue":
                # Split dialogue into individual lines
                dialogue_lines = re.findall(r'"([^"]*)"', para)
                for line in dialogue_lines:
                    segments.append((line, "dialogue"))
            else:
                segments.append((para, para_type))

        return segments

    def _classify_paragraph(self, paragraph: str) -> str:
        """Classify paragraph type"""
        para_lower = paragraph.lower().strip()

        # Check for dialogue
        if '"' in paragraph or "'" in paragraph:
            return "dialogue"

        # Check for headings
        if len(paragraph.split()) < 10 and not paragraph.endswith('.'):
            return "heading"

        # Check for lists
        if re.match(r'^[\s]*[-\*•]\s', paragraph):
            return "list_item"

        # Check for quotes
        if paragraph.startswith('"') or paragraph.startswith("'"):
            return "quote"

        # Default to main content
        return "main"

    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score"""
        words = text.split()
        if not words:
            return 0.0

        # Factors: sentence length, word length, technical terms
        avg_word_length = sum(len(word) for word in words) / len(words)
        avg_sentence_length = len(words)  # Simplified

        technical_count = len(self._identify_technical_terms(text))

        # Normalize to 0-1 scale
        complexity = (
            min(avg_word_length / 8.0, 1.0) * 0.4 +
            min(avg_sentence_length / 25.0, 1.0) * 0.4 +
            min(technical_count / 5.0, 1.0) * 0.2
        )

        return min(complexity, 1.0)

    def _identify_technical_terms(self, text: str) -> List[str]:
        """Identify technical terms in text"""
        words = re.findall(r'\b\w+\b', text.lower())
        technical_terms = []

        for word in words:
            if word in self.technical_terms_db:
                technical_terms.append(word)

        return technical_terms

    def _detect_emotional_tone(self, text: str) -> str:
        """Detect emotional tone of text"""
        text_lower = text.lower()

        # Simple emotion detection
        if any(word in text_lower for word in ["excited", "amazing", "wonderful", "thrilled"]):
            return "excited"
        elif any(word in text_lower for word in ["sad", "unhappy", "depressed", "mournful"]):
            return "sad"
        elif any(word in text_lower for word in ["angry", "furious", "enraged", "mad"]):
            return "angry"
        elif any(word in text_lower for word in ["calm", "peaceful", "serene", "quiet"]):
            return "calm"
        else:
            return "neutral"

    def _determine_reading_speed(self, text: str, segment_type: str, content_type: str) -> str:
        """Determine optimal reading speed for segment"""
        complexity = self._calculate_complexity(text)

        # Base speed on complexity and segment type
        if complexity > 0.7 or segment_type in ["definition", "formula"]:
            return "slow"
        elif complexity < 0.3 and segment_type == "dialogue":
            return "fast"
        else:
            return "normal"

    async def optimize_narration(
        self,
        text_segments: List[TextSegment],
        narrator_profile: NarratorProfile
    ) -> Dict[str, Any]:
        """
        Optimize narration settings for text segments
        """
        optimizations = []

        for i, segment in enumerate(text_segments):
            optimization = {
                "segment_id": i,
                "text": segment.text,
                "segment_type": segment.segment_type,
                "narrator_settings": self._get_segment_narrator_settings(
                    segment, narrator_profile
                ),
                "technical_enhancements": self._apply_technical_enhancements(
                    segment, narrator_profile
                ),
                "pacing_adjustments": self._calculate_pacing_adjustments(
                    segment, narrator_profile
                )
            }
            optimizations.append(optimization)

        return {
            "total_segments": len(optimizations),
            "optimizations": optimizations,
            "summary": self._generate_optimization_summary(optimizations)
        }

    def _get_segment_narrator_settings(
        self,
        segment: TextSegment,
        profile: NarratorProfile
    ) -> Dict[str, Any]:
        """Get narrator settings for specific segment"""
        pacing_profile = profile.pacing_profiles.get(
            segment.segment_type,
            profile.pacing_profiles.get("main", {})
        )

        return {
            "reading_speed": segment.reading_speed,
            "articulation_precision": profile.clarity_settings["articulation_enhancement"],
            "emotional_tone": segment.emotional_tone,
            "pause_after": pacing_profile.get("pause_after", 0.2),
            "emphasis_boost": pacing_profile.get("emphasis_boost", 1.0)
        }

    def _apply_technical_enhancements(
        self,
        segment: TextSegment,
        profile: NarratorProfile
    ) -> Dict[str, Any]:
        """Apply technical enhancements to segment"""
        enhancements = {
            "pronunciation_guides": [],
            "speed_adjustments": [],
            "emphasis_markers": []
        }

        if profile.technical_enhancements["pronunciation_database"]:
            for term in segment.technical_terms:
                if term in self.technical_terms_db:
                    guide = self.technical_terms_db[term]
                    enhancements["pronunciation_guides"].append({
                        "term": term,
                        "pronunciation": guide["pronunciation"],
                        "category": guide["category"]
                    })

        return enhancements

    def _calculate_pacing_adjustments(
        self,
        segment: TextSegment,
        profile: NarratorProfile
    ) -> Dict[str, Any]:
        """Calculate pacing adjustments for segment"""
        base_speed = {
            "slow": 0.8,
            "normal": 1.0,
            "fast": 1.2
        }.get(segment.reading_speed, 1.0)

        # Adjust for complexity
        complexity_adjustment = 1.0 - (segment.complexity_score * 0.2)

        # Adjust for technical terms
        technical_adjustment = 1.0 - (len(segment.technical_terms) * 0.05)

        final_speed = base_speed * complexity_adjustment * technical_adjustment

        return {
            "base_speed": base_speed,
            "complexity_adjustment": complexity_adjustment,
            "technical_adjustment": technical_adjustment,
            "final_speed": final_speed,
            "recommended_pause": self._get_pause_duration(segment.segment_type)
        }

    def _generate_optimization_summary(self, optimizations: List[Dict]) -> Dict[str, Any]:
        """Generate summary of optimization results"""
        speeds = [opt["pacing_adjustments"]["final_speed"] for opt in optimizations]
        segment_types = [opt["segment_type"] for opt in optimizations]

        return {
            "average_speed": statistics.mean(speeds) if speeds else 1.0,
            "speed_range": {
                "min": min(speeds) if speeds else 1.0,
                "max": max(speeds) if speeds else 1.0
            },
            "segment_distribution": {
                segment_type: segment_types.count(segment_type)
                for segment_type in set(segment_types)
            },
            "technical_terms_found": sum(
                len(opt["technical_enhancements"]["pronunciation_guides"])
                for opt in optimizations
            )
        }

    async def generate_narrator_audio(
        self,
        text: str,
        narrator_profile: NarratorProfile,
        segment_type: str = "main",
        technical_terms: Optional[List[str]] = None
    ) -> bytes:
        """
        Generate optimized narrator audio
        """
        profile_id = f"vp_narrator_{narrator_profile.content_type}_{narrator_profile.profile_id.split('_')[-1]}"

        # Create voice profile for narrator if it doesn't exist
        try:
            voice_profile = await self.voice_engine.get_profile(profile_id)
        except FileNotFoundError:
            result = await self.voice_engine.create_voice_profile(
                creation_method="parameter",
                name=f"{narrator_profile.content_type} narrator",
                description=f"Optimized narrator voice for {narrator_profile.content_type} content",
                voice_type="narrator",
                param_config=self._build_narrator_voice_params(narrator_profile.content_type, None)
            )
            voice_profile = await self.voice_engine.get_profile(result["profile_id"])
            profile_id = result["profile_id"]

        audio_bytes = await self.voice_engine.synthesize_with_narrator_voice(
            text=text,
            narrator_profile=voice_profile,
            section_type=segment_type,
            technical_terms=technical_terms or []
        )

        return audio_bytes

    def get_profile_summary(self) -> Dict[str, Any]:
        """Get summary of all narrator profiles"""
        return {
            "total_profiles": len(self.narrator_profiles),
            "profiles": [
                {
                    "profile_id": profile.profile_id,
                    "content_type": profile.content_type,
                    "clarity_boost": profile.clarity_settings["articulation_enhancement"],
                    "engagement_boost": profile.engagement_settings["prosody_variation"]
                }
                for profile in self.narrator_profiles.values()
            ]
        }