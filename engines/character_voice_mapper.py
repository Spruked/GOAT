# engines/character_voice_mapper.py
"""
Character Voice Mapper: Maps characters to voice profiles for audiobook production
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
import asyncio

@dataclass
class CharacterProfile:
    """Character profile with voice mapping"""
    name: str
    voice_profile_id: str
    description: str
    gender: str
    age_range: str
    personality_traits: List[str]
    voice_characteristics: Dict[str, Any]
    dialogue_patterns: List[str]
    emotional_range: List[str]

@dataclass
class DialogueSegment:
    """Segment of dialogue with character and emotion"""
    character: str
    text: str
    emotion: str
    context: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None

class CharacterVoiceMapper:
    """
    Maps characters to voice profiles and processes dialogue for audiobook production
    """

    def __init__(self, voice_engine):
        self.voice_engine = voice_engine
        self.characters: Dict[str, CharacterProfile] = {}
        self.voice_mappings: Dict[str, str] = {}  # character_name -> voice_profile_id
        self.emotion_patterns = self._load_emotion_patterns()

    def _load_emotion_patterns(self) -> Dict[str, List[str]]:
        """Load emotion detection patterns"""
        return {
            "angry": [
                r"\b(angry|mad|furious|enraged|irate)\b",
                r"\b(yell|shout|scream)\b",
                r"[!?]{2,}",
                r"\b(damn|hell|shit)\b"
            ],
            "weary": [
                r"\b(tired|exhausted|weary|fatigued)\b",
                r"\b(sigh|groan)\b",
                r"\b(oh god|dear lord)\b"
            ],
            "excited": [
                r"\b(excited|thrilled|amazing|wonderful)\b",
                r"\b(oh my|wow|fantastic)\b",
                r"[!]{2,}",
                r"\b(yes|yeah|great)\b"
            ],
            "calm": [
                r"\b(calm|peaceful|serene|quiet)\b",
                r"\b(softly|gently|quietly)\b"
            ],
            "neutral": []  # Default emotion
        }

    async def create_character_profile(
        self,
        name: str,
        description: str,
        gender: str,
        age_range: str,
        personality_traits: List[str],
        voice_characteristics: Dict[str, Any]
    ) -> CharacterProfile:
        """
        Create a character profile with voice mapping
        """
        # Auto-generate voice profile based on character traits
        voice_profile_id = await self._create_matching_voice_profile(
            name, description, gender, age_range, personality_traits, voice_characteristics
        )

        character = CharacterProfile(
            name=name,
            voice_profile_id=voice_profile_id,
            description=description,
            gender=gender,
            age_range=age_range,
            personality_traits=personality_traits,
            voice_characteristics=voice_characteristics,
            dialogue_patterns=self._extract_dialogue_patterns(description),
            emotional_range=self._determine_emotional_range(personality_traits)
        )

        self.characters[name] = character
        self.voice_mappings[name] = voice_profile_id

        return character

    async def _create_matching_voice_profile(
        self,
        name: str,
        description: str,
        gender: str,
        age_range: str,
        personality_traits: List[str],
        voice_characteristics: Dict[str, Any]
    ) -> str:
        """
        Create or find a matching voice profile for the character
        """
        # Check if similar profile already exists
        existing_profile = await self._find_similar_voice_profile(
            gender, age_range, personality_traits
        )

        if existing_profile:
            return existing_profile

        # Create new voice profile based on character traits
        param_config = self._build_voice_params_from_characteristics(
            gender, age_range, personality_traits, voice_characteristics
        )

        result = await self.voice_engine.create_voice_profile(
            creation_method="parameter",
            name=f"{name}_voice",
            description=f"Voice profile for character: {name}",
            voice_type="character",
            param_config=param_config
        )

        return result["profile_id"]

    async def _find_similar_voice_profile(
        self,
        gender: str,
        age_range: str,
        personality_traits: List[str]
    ) -> Optional[str]:
        """
        Find existing voice profile that matches character traits
        """
        # Search through existing profiles
        profiles_path = Path("./voices/profiles")
        if not profiles_path.exists():
            return None

        for profile_file in profiles_path.glob("*.json"):
            try:
                with open(profile_file, 'r') as f:
                    profile = json.load(f)

                if profile["voice_type"] != "character":
                    continue

                # Check if profile matches character traits
                if self._profile_matches_character(
                    profile, gender, age_range, personality_traits
                ):
                    return profile["profile_id"]

            except (json.JSONDecodeError, KeyError):
                continue

        return None

    def _profile_matches_character(
        self,
        profile: Dict,
        gender: str,
        age_range: str,
        personality_traits: List[str]
    ) -> bool:
        """
        Check if voice profile matches character characteristics
        """
        # Simple matching logic - in real implementation, this would be more sophisticated
        profile_desc = profile.get("description", "").lower()

        # Check gender
        if gender.lower() not in profile_desc:
            return False

        # Check age range
        if age_range.lower() not in profile_desc:
            return False

        # Check personality traits (at least one match)
        profile_traits = [trait.lower() for trait in personality_traits]
        if not any(trait in profile_desc for trait in profile_traits):
            return False

        return True

    def _build_voice_params_from_characteristics(
        self,
        gender: str,
        age_range: str,
        personality_traits: List[str],
        voice_characteristics: Dict[str, Any]
    ) -> Dict:
        """
        Build voice synthesis parameters from character characteristics
        """
        # Base parameters
        params = {
            "tension": 0.6,
            "breathiness": 0.2,
            "vibrato_rate": 4.0,
            "lip_rounding": 0.3,
            "articulation_precision": 0.8,
            "tongue_position": "alveolar",
            "sharpness": 0.7,
            "nasal": False,
            "nasalization": 0.0
        }

        # Adjust based on gender
        if gender.lower() == "male":
            params["tension"] = 0.7
            params["breathiness"] = 0.15
        elif gender.lower() == "female":
            params["tension"] = 0.5
            params["breathiness"] = 0.25
            params["vibrato_rate"] = 4.5

        # Adjust based on age
        if "child" in age_range.lower() or "young" in age_range.lower():
            params["tension"] = params["tension"] * 0.8
            params["breathiness"] = params["breathiness"] * 1.3
        elif "elderly" in age_range.lower() or "old" in age_range.lower():
            params["tension"] = params["tension"] * 1.2
            params["breathiness"] = params["breathiness"] * 1.5
            params["vibrato_rate"] = params["vibrato_rate"] * 0.8

        # Adjust based on personality traits
        trait_adjustments = {
            "aggressive": {"tension": 1.3, "breathiness": 0.8},
            "calm": {"tension": 0.7, "breathiness": 0.3},
            "excitable": {"vibrato_rate": 1.2, "breathiness": 1.2},
            "weary": {"tension": 0.5, "breathiness": 1.4},
            "formal": {"articulation_precision": 1.2, "lip_rounding": 0.4},
            "rough": {"sharpness": 0.5, "tension": 1.1}
        }

        for trait in personality_traits:
            trait_lower = trait.lower()
            if trait_lower in trait_adjustments:
                for param, multiplier in trait_adjustments[trait_lower].items():
                    params[param] *= multiplier

        # Apply voice characteristics overrides
        for char, value in voice_characteristics.items():
            if char in params:
                params[char] = value

        return params

    def _extract_dialogue_patterns(self, description: str) -> List[str]:
        """Extract dialogue patterns from character description"""
        # Simple pattern extraction - in real implementation, this would use NLP
        patterns = []
        desc_lower = description.lower()

        if "formal" in desc_lower or "proper" in desc_lower:
            patterns.append("formal_speech")
        if "slang" in desc_lower or "casual" in desc_lower:
            patterns.append("casual_speech")
        if "accent" in desc_lower:
            patterns.append("accented_speech")

        return patterns or ["neutral_speech"]

    def _determine_emotional_range(self, personality_traits: List[str]) -> List[str]:
        """Determine emotional range based on personality traits"""
        base_emotions = ["neutral", "angry", "weary", "excited", "calm"]

        trait_emotions = {
            "hot-tempered": ["angry"],
            "calm": ["calm"],
            "excitable": ["excited"],
            "stoic": ["neutral"],
            "weary": ["weary"]
        }

        additional_emotions = []
        for trait in personality_traits:
            trait_lower = trait.lower()
            if trait_lower in trait_emotions:
                additional_emotions.extend(trait_emotions[trait_lower])

        return list(set(base_emotions + additional_emotions))

    async def process_dialogue_script(
        self,
        script_text: str,
        book_metadata: Optional[Dict] = None
    ) -> List[DialogueSegment]:
        """
        Process a dialogue script and assign voices/emotions to segments
        """
        segments = self._parse_dialogue_script(script_text)

        # Assign emotions to segments
        for segment in segments:
            segment.emotion = self._detect_emotion(segment.text, segment.context)

        return segments

    def _parse_dialogue_script(self, script_text: str) -> List[DialogueSegment]:
        """
        Parse dialogue script into segments
        Supports formats like:
        - CHARACTER: "Dialogue text"
        - "Dialogue text," said CHARACTER.
        """
        segments = []

        # Pattern 1: CHARACTER: "Dialogue"
        pattern1 = r'^([A-Z][A-Za-z\s]+):\s*"([^"]+)"'
        matches1 = re.findall(pattern1, script_text, re.MULTILINE)

        for character, dialogue in matches1:
            character = character.strip()
            segments.append(DialogueSegment(
                character=character,
                text=dialogue,
                emotion="neutral"  # Will be detected later
            ))

        # Pattern 2: "Dialogue," said CHARACTER.
        pattern2 = r'"([^"]+)",?\s*(said|asked|replied|whispered|shouted)\s+([A-Z][A-Za-z\s]+)'
        matches2 = re.findall(pattern2, script_text, re.IGNORECASE)

        for dialogue, verb, character in matches2:
            character = character.strip()
            segments.append(DialogueSegment(
                character=character,
                text=dialogue,
                emotion="neutral",
                context=verb
            ))

        return segments

    def _detect_emotion(self, text: str, context: Optional[str] = None) -> str:
        """
        Detect emotion from text and context
        """
        text_lower = text.lower()
        context_lower = context.lower() if context else ""

        # Check emotion patterns
        for emotion, patterns in self.emotion_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower) or re.search(pattern, context_lower):
                    return emotion

        return "neutral"

    async def generate_character_audio(
        self,
        character_name: str,
        text: str,
        emotion: str = "neutral",
        context: Optional[Dict] = None
    ) -> bytes:
        """
        Generate audio for a specific character's dialogue
        """
        if character_name not in self.characters:
            raise ValueError(f"Character '{character_name}' not found. Create profile first.")

        character = self.characters[character_name]
        voice_profile = await self.voice_engine.get_profile(character.voice_profile_id)

        # Validate emotion
        if emotion not in character.emotional_range:
            emotion = "neutral"

        # Generate audio
        audio_bytes = await self.voice_engine.synthesize_with_character_voice(
            text=text,
            voice_profile=voice_profile,
            character_emotion=emotion,
            context=context
        )

        return audio_bytes

    async def batch_generate_dialogue_audio(
        self,
        dialogue_segments: List[DialogueSegment]
    ) -> Dict[str, bytes]:
        """
        Generate audio for multiple dialogue segments
        """
        audio_segments = {}

        for i, segment in enumerate(dialogue_segments):
            segment_id = f"dialogue_{i:03d}"
            try:
                audio = await self.generate_character_audio(
                    character_name=segment.character,
                    text=segment.text,
                    emotion=segment.emotion,
                    context={"position": i, "total": len(dialogue_segments)}
                )
                audio_segments[segment_id] = audio
            except Exception as e:
                print(f"Failed to generate audio for segment {segment_id}: {e}")
                continue

        return audio_segments

    def get_character_summary(self) -> Dict[str, Any]:
        """Get summary of all character profiles"""
        return {
            "total_characters": len(self.characters),
            "characters": [
                {
                    "name": char.name,
                    "voice_profile": char.voice_profile_id,
                    "gender": char.gender,
                    "age_range": char.age_range,
                    "traits": char.personality_traits,
                    "emotions": char.emotional_range
                }
                for char in self.characters.values()
            ],
            "voice_mappings": self.voice_mappings
        }

    async def save_character_mappings(self, filepath: str):
        """Save character mappings to file"""
        data = {
            "characters": {
                name: {
                    "voice_profile_id": char.voice_profile_id,
                    "description": char.description,
                    "gender": char.gender,
                    "age_range": char.age_range,
                    "personality_traits": char.personality_traits,
                    "voice_characteristics": char.voice_characteristics,
                    "dialogue_patterns": char.dialogue_patterns,
                    "emotional_range": char.emotional_range
                }
                for name, char in self.characters.items()
            },
            "voice_mappings": self.voice_mappings
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    async def load_character_mappings(self, filepath: str):
        """Load character mappings from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Reconstruct character profiles
        for name, char_data in data["characters"].items():
            character = CharacterProfile(
                name=name,
                voice_profile_id=char_data["voice_profile_id"],
                description=char_data["description"],
                gender=char_data["gender"],
                age_range=char_data["age_range"],
                personality_traits=char_data["personality_traits"],
                voice_characteristics=char_data["voice_characteristics"],
                dialogue_patterns=char_data["dialogue_patterns"],
                emotional_range=char_data["emotional_range"]
            )
            self.characters[name] = character

        self.voice_mappings = data["voice_mappings"]