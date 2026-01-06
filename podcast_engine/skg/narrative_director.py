from typing import Dict, List, Tuple, Optional
import re
import numpy as np

class NarrativeDirector:
    def __init__(self, skg):
        self.skg = skg
        self.emotion_mapper = EmotionArcMapper()
        self.prosody_engine = ProsodyEngine(skg)
        self.narrative_pacing = NarrativePacingEngine()
        self.genre_profiles = self._load_genre_profiles()

    def direct_narration(self, text: str, narrator_id: str, chapter_context: Dict) -> List[Dict]:
        """
        Main entry: Take raw text, return emotionally-directed narration segments
        """
        print(f"📖 Narrative Director: Directing chapter '{chapter_context.get('title', 'Unknown')}'")

        # 1. Split into narrative units (sentences or clauses)
        units = self._segment_narrative_units(text)

        # 2. Detect emotional arcs and assign emotional states
        units_with_emotion = self.emotion_mapper.map_emotional_arc(units, chapter_context)

        # 3. Apply prosody (stress, intonation, rhythm)
        units_with_prosody = self.prosody_engine.apply_prosody_markers(units_with_emotion, narrator_id)

        # 4. Calculate narrative pacing (slow for tension, fast for action)
        final_directives = self.narrative_pacing.calculate_narrative_tempo(units_with_prosody, chapter_context)

        # 5. Synthesize with narrative performance
        audio_segments = []
        for unit in final_directives:
            performance = unit.get("performance", {})

            audio_path = self.skg.synthesize_as_persona(
                text=unit["text"],
                persona_id=narrator_id,
                performance_directives=performance
            )

            # Apply post-processing effects (reverb, compression) if needed
            if performance.get("effects"):
                audio_path = self._apply_post_effects(audio_path, performance["effects"])

            audio_segments.append({
                "text": unit["text"],
                "audio_path": audio_path,
                "emotion": unit.get("emotion"),
                "prosody": unit.get("prosody"),
                "narrative_tempo": unit.get("tempo", 1.0)
            })

        return audio_segments

    def _segment_narrative_units(self, text: str) -> List[str]:
        """Split text into natural narrative units"""
        # Split on sentence boundaries, but keep related clauses together
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())

        # Further split long sentences on commas for better pacing
        units = []
        for sentence in sentences:
            if len(sentence.split()) > 20:  # Long sentence
                # Split on commas but keep the comma
                parts = re.split(r'(,)', sentence)
                current_unit = ""
                for part in parts:
                    current_unit += part
                    if len(current_unit.split()) > 10:
                        units.append(current_unit.strip())
                        current_unit = ""
                if current_unit.strip():
                    units.append(current_unit.strip())
            else:
                units.append(sentence.strip())

        return [unit for unit in units if unit.strip()]

    def _apply_post_effects(self, audio_path: str, effects: Dict) -> str:
        """Apply post-processing effects like reverb"""
        # This would integrate with audio processing libraries
        # For now, just return the original path
        return audio_path

    def _load_genre_profiles(self) -> Dict:
        """Pre-configured genre-specific narration styles"""

        return {
            "mystery_thriller": {
                "default_tempo": 0.85,  # Slower, deliberate
                "pause_multiplier": 1.5,
                "emphasis_words": ["suddenly", "dark", "shadow", "dead", "knife"],
                "breathiness": 0.4,
                "vocal_fry": 0.3  # Adds gravitas
            },
            "romance": {
                "default_tempo": 0.95,
                "pause_multiplier": 1.2,
                "emphasis_words": ["love", "heart", "touch", "kiss", "whispered"],
                "breathiness": 0.6,
                "warmth": 0.7
            },
            "science_fiction": {
                "default_tempo": 1.0,
                "pause_multiplier": 1.0,
                "emphasis_words": ["ship", "space", "quantum", "future", "alien"],
                "clarity": 0.8,  # Precise articulation
                "staccato": 0.3  # Sharp consonants
            },
            "fantasy_epic": {
                "default_tempo": 0.9,
                "pause_multiplier": 1.3,
                "emphasis_words": ["magic", "king", "sword", "quest", "ancient"],
                "reverb": {"room_size": 0.6, "wet_level": 0.2},
                "dramatic_timing": True
            }
        }


class EmotionArcMapper:
    """Maps emotional states across narrative beats using story theory"""

    def __init__(self):
        self.emotion_lexicon = self._build_emotion_lexicon()
        self.arc_patterns = {
            "three_act": ["establishment", "tension", "climax", "resolution"],
            "hero_journey": ["ordinary_world", "call_adventure", "ordeal", "return"],
            "story_circle": ["you", "need", "go", "search", "find", "take", "return", "change"]
        }

    def map_emotional_arc(self, units: List[str], chapter_context: Dict) -> List[Dict]:
        """Detect narrative structure and assign emotions"""

        # 1. Identify chapter arc pattern
        arc = self._identify_arc(units, chapter_context.get("chapter_number", 1))

        # 2. Assign emotional states to each unit
        units_with_emotion = []

        for i, unit in enumerate(units):
            # Position in arc (0.0 to 1.0)
            arc_position = i / len(units) if len(units) > 1 else 0.5

            # Base emotion from arc
            base_emotion = self._get_arc_emotion(arc, arc_position)

            # Refine with text content
            specific_emotion = self._refine_emotion_from_text(unit, base_emotion)

            # Intensity based on word choice
            intensity = self._calculate_emotional_intensity(unit, specific_emotion)

            units_with_emotion.append({
                "text": unit,
                "emotion": specific_emotion,
                "intensity": intensity,
                "arc_position": arc_position
            })

        return units_with_emotion

    def _identify_arc(self, units: List[str], chapter_num: int) -> str:
        """Guess narrative arc from content and chapter position"""

        # Check for climax indicators
        climax_words = ["suddenly", "then", "finally", "everything", "climbed", "exploded"]
        if any(word in " ".join(units[-3:]).lower() for word in climax_words):
            return "climax"

        # Check for resolution
        if chapter_num > 15 and any(word in units[-1].lower() for word in ["afterward", "finally", "happily", "never"]):
            return "resolution"

        # Default based on chapter number
        if chapter_num <= 3:
            return "establishment"
        elif chapter_num >= 4 and chapter_num <= 10:
            return "tension"

        return "development"

    def _get_arc_emotion(self, arc: str, position: float) -> str:
        """Emotion curve per arc stage"""

        emotion_curves = {
            "establishment": ["calm", "curious", "interested"],
            "tension": ["apprehensive", "anxious", "worried", "fearful"],
            "climax": ["terrified", "exhilarated", "shocked"],
            "resolution": ["relieved", "peaceful", "satisfied"],
            "development": ["curious", "engaged", "invested"]
        }

        stage_emotions = emotion_curves.get(arc, ["neutral"])
        emotion_index = min(len(stage_emotions) - 1, int(position * len(stage_emotions)))
        return stage_emotions[emotion_index]

    def _refine_emotion_from_text(self, text: str, base_emotion: str) -> str:
        """Use NLP to detect specific emotions"""

        text = text.lower()

        # Override rules
        if any(word in text for word in ["dead", "kill", "blood", "scream"]):
            return "horrified"

        if any(word in text for word in ["love", "kiss", "heart", "embrace"]):
            return "affectionate"

        if "!" in text and base_emotion in ["anxious", "worried"]:
            return "alarmed"

        if "?" in text:
            return f"{base_emotion}_curious"

        return base_emotion

    def _calculate_emotional_intensity(self, text: str, emotion: str) -> float:
        """0.0 to 1.0 intensity based on punctuation and word choice"""

        intensity = 0.5  # Baseline

        # Punctuation boost
        if "!" in text:
            intensity += 0.3
        if "?" in text:
            intensity += 0.15

        # Word choice
        strong_words = ["very", "extremely", "absolutely", "completely", "totally"]
        if any(word in text.lower() for word in strong_words):
            intensity += 0.2

        # Exclamation count
        intensity += text.count("!") * 0.1

        # Caps
        if any(word.isupper() for word in text.split()):
            intensity += 0.15

        return min(1.0, intensity)

    def _build_emotion_lexicon(self) -> Dict:
        """Emotion-word mapping for quick lookup"""

        return {
            "joy": ["happy", "excited", "elated", "thrilled", "delighted"],
            "sadness": ["sad", "depressed", "melancholy", "grief", "sorrow"],
            "anger": ["angry", "furious", "rage", "livid", "incensed"],
            "fear": ["scared", "terrified", "horrified", "petrified", "afraid"],
            "surprise": ["shocked", "astonished", "amazed", "stunned", "bewildered"],
            "disgust": ["disgusted", "revolted", "repulsed", "nauseated", "appalled"]
        }


class ProsodyEngine:
    """Controls stress, intonation, rhythm—makes narration musical"""

    def __init__(self, skg):
        self.skg = skg
        self.stress_patterns = self._load_stress_patterns()

    def apply_prosody_markers(self, units: List[Dict], narrator_id: str) -> List[Dict]:
        """Add phonatory control markers for natural speech rhythm"""

        prosody_units = []

        for unit in units:
            text = unit["text"]

            # 1. Identify stress words (important words to emphasize)
            stress_words = self._identify_stress_words(text, unit["emotion"])

            # 2. Determine intonation curve (rising/falling)
            intonation = self._calculate_intonation(text, unit["emotion"])

            # 3. Add rhythmic markers (pauses, elongations)
            rhythm = self._calculate_rhythm(text, unit["emotion"])

            # 4. Build performance directive for POM
            performance = {
                "stress_words": stress_words,
                "intonation_curve": intonation,
                "rhythm_markers": rhythm,
                "base_pitch": self._get_pitch_for_emotion(unit["emotion"]),
                "speaking_rate": self._get_rate_for_emotion(unit["emotion"]),
                "breath_insertion": self._calculate_breath_points(text, unit["emotion"])
            }

            prosody_units.append({
                **unit,
                "prosody": performance,
                "performance": performance  # For compatibility
            })

        return prosody_units

    def _identify_stress_words(self, text: str, emotion: str) -> List[Tuple[str, float]]:
        """Return list of (word, stress_level) tuples"""

        words = text.split()
        stress_markers = []

        for i, word in enumerate(words):
            stress_level = 0.5  # Default

            # Content words get more stress
            if self._is_content_word(word):
                stress_level += 0.2

            # First and last words in phrase
            if i == 0 or i == len(words) - 1:
                stress_level += 0.15

            # Emotion-specific stress
            if emotion == "horrified" and word.lower() in ["blood", "scream", "dead"]:
                stress_level = 1.0

            if emotion == "affectionate" and word.lower() in ["love", "heart", "kiss"]:
                stress_level = 0.9

            # Exclamation marks in the word
            if "!" in word:
                stress_level += 0.3

            stress_markers.append((word, min(1.0, stress_level)))

        return stress_markers

    def _calculate_intonation(self, text: str, emotion: str) -> List[float]:
        """
        Pitch contour over time: [pitch_level_0, pitch_level_1, ...]
        0.5 = baseline, 0.0 = lowest, 1.0 = highest
        """

        # Declarative: falling intonation (high → low)
        if text.strip().endswith("."):
            return [0.6, 0.7, 0.65, 0.55, 0.5]

        # Interrogative: rising intonation (low → high)
        if text.strip().endswith("?"):
            return [0.4, 0.45, 0.5, 0.65, 0.75]

        # Exclamatory: high → low → high
        if text.strip().endswith("!"):
            return [0.5, 0.8, 0.75, 0.6, 0.7]

        # Default: level
        return [0.5, 0.5, 0.5, 0.5]

    def _calculate_rhythm(self, text: str, emotion: str) -> Dict:
        """Control timing of each word/syllable"""

        # Calculate word durations (relative to normal)
        words = text.split()
        rhythm = {"word_durations": {}}

        for i, word in enumerate(words):
            base_duration = 1.0

            # Longer for important words
            if self._is_content_word(word):
                base_duration *= 1.3

            # Shorter for function words (the, a, and)
            if word.lower() in ["the", "a", "an", "and", "or", "but"]:
                base_duration *= 0.7

            # Emotion-specific rhythm
            if emotion == "terrified":
                if word.lower() in ["suddenly", "then", "burst"]:
                    base_duration *= 0.5  # Quick, staccato
            elif emotion == "affectionate":
                if word.lower() in ["softly", "gently", "slowly"]:
                    base_duration *= 1.5  # Drawn out

            rhythm["word_durations"][i] = base_duration

        # Add micro-pauses between clauses
        rhythm["clause_pauses"] = []
        if "," in text:
            comma_positions = [m.start() for m in re.finditer(",", text)]
            for pos in comma_positions:
                # Find which word this comma follows
                before_comma = text[:pos]
                word_count = len(before_comma.split())
                rhythm["clause_pauses"].append(word_count)

        return rhythm

    def _calculate_breath_points(self, text: str, emotion: str) -> List[int]:
        """Where to insert natural breaths"""

        words = text.split()
        breath_points = []

        # Standard: every 10-15 words
        for i in range(12, len(words), 13):
            breath_points.append(i)

        # Shorter breath cycles for fear/anxiety
        if emotion in ["terrified", "anxious"]:
            breath_points = [i for i in range(7, len(words), 8)]

        return breath_points

    def _is_content_word(self, word: str) -> bool:
        """Nouns, verbs, adjectives, adverbs (not function words)"""

        function_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "as", "is", "was", "are", "were", "be", "been"
        }

        return word.lower() not in function_words

    def _get_pitch_for_emotion(self, emotion: str) -> float:
        """Base pitch offset for emotion"""

        pitch_map = {
            "terrified": 1.15,
            "angry": 0.95,
            "sad": 0.88,
            "affectionate": 1.05,
            "neutral": 1.0,
            "horrified": 1.1
        }

        return pitch_map.get(emotion, 1.0)

    def _get_rate_for_emotion(self, emotion: str) -> float:
        """Speaking rate offset for emotion"""

        rate_map = {
            "terrified": 1.15,
            "angry": 1.05,
            "sad": 0.85,
            "affectionate": 0.9,
            "neutral": 1.0,
            "horrified": 1.1
        }

        return rate_map.get(emotion, 1.0)

    def _load_stress_patterns(self) -> Dict:
        """Load pre-defined stress patterns"""
        return {
            "emphasis": [0.8, 1.0, 0.9],
            "question": [0.7, 0.9, 1.0],
            "statement": [0.9, 0.8, 0.6]
        }


class NarrativePacingEngine:
    """Controls macro pacing: scene tension, action vs. reflection"""

    def calculate_narrative_tempo(self, units: List[Dict], chapter_context: Dict) -> List[Dict]:
        """Adjust tempo based on scene type and narrative position"""

        # Detect scene type
        scene_type = self._detect_scene_type(units)
        print(f"   → Detected scene type: {scene_type}")

        paced_units = []

        for i, unit in enumerate(units):
            # Get tempo multiplier
            tempo = self._get_tempo_for_scene(scene_type, i, len(units))

            # Apply to duration
            if "prosody" in unit:
                unit["prosody"]["speaking_rate"] *= tempo

            unit["tempo"] = tempo
            paced_units.append(unit)

        return paced_units

    def _detect_scene_type(self, units: List[Dict]) -> str:
        """Identify if scene is action, dialogue, reflection, or exposition"""

        text = " ".join([u["text"] for u in units])

        # Action indicators
        action_verbs = ["ran", "jumped", "fought", "attacked", "exploded", "raced", "pursued"]
        if any(verb in text.lower() for verb in action_verbs):
            return "action"

        # Dialogue heavy
        quote_count = text.count('"') + text.count("'")
        if quote_count > 5:
            return "dialogue"

        # Reflection (internal monologue)
        reflection_words = ["thought", "felt", "remembered", "wondered", "realized"]
        if any(word in text.lower() for word in reflection_words):
            return "reflection"

        # Description (world-building)
        if "was" in text.lower() or "were" in text.lower():
            return "exposition"

        return "general"

    def _get_tempo_for_scene(self, scene_type: str, position: int, total: int) -> float:
        """Multiplier for speaking rate per scene type"""

        tempo_map = {
            "action": 1.2,      # Fast-paced
            "dialogue": 1.0,    # Natural conversation
            "reflection": 0.75,  # Slower, contemplative
            "exposition": 0.9,  # Measured
            "general": 1.0
        }

        base_tempo = tempo_map.get(scene_type, 1.0)

        # Accelerate toward climax of scene
        if position > total * 0.7:
            base_tempo *= 1.1

        return base_tempo