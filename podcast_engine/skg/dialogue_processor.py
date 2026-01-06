import re
from typing import List, Dict, Tuple, Optional
import spacy  # For attribution detection

nlp = spacy.load("en_core_web_sm")

class DialogueProcessor:
    def __init__(self, skg_manager):
        self.skg = skg_manager
        self.quote_patterns = {
            "double": re.compile(r'"([^"]*?)"'),
            "single": re.compile(r"'([^']*?)'"),
            "guillemet": re.compile(r'«(.*?)»')  # French style
        }
        self.attribution_patterns = re.compile(
            r'\b(said|whispered|shouted|asked|replied|murmured|cried|laughed)\b',
            re.IGNORECASE
        )

    def parse_scene(self, text: str, chapter_context: Dict) -> List[Dict]:
        """
        Parse a scene into narration/dialogue segments with speaker identification.

        Returns: [
            {
                "type": "narration"|"dialogue",
                "text": "He walked into the room.",
                "speaker": None,
                "emotion": None
            },
            {
                "type": "dialogue",
                "text": "Welcome back.",
                "speaker": "elder_wizard_gandarf",
                "emotion": "warm",
                "attribution": "he said softly."
            }
        ]
        """
        segments = []
        lines = text.split('\n')

        for line_idx, line in enumerate(lines):
            line = line.strip()
            if not line:
                segments.append({"type": "pause", "duration": 0.5})
                continue

            # Check for dialogue
            dialogue_info = self._extract_dialogue(line)

            if dialogue_info:
                # Found quoted speech
                speaker_id, emotion = self._identify_speaker(
                    dialogue_info["line_text"],
                    chapter_context,
                    line_idx
                )

                segments.append({
                    "type": "dialogue",
                    "text": dialogue_info["quote_text"],
                    "speaker": speaker_id,
                    "emotion": emotion,
                    "attribution": dialogue_info["attribution_text"]
                })

                # If there's narration around the quote
                if dialogue_info["pre_text"]:
                    segments.insert(-1, {
                        "type": "narration",
                        "text": dialogue_info["pre_text"],
                        "speaker": chapter_context["narrator"]
                    })

            else:
                # Pure narration
                segments.append({
                    "type": "narration",
                    "text": line,
                    "speaker": chapter_context["narrator"]
                })

            # Voice consistency tracking
            self._update_character_stats(chapter_context, speaker_id)

        return segments

    def _extract_dialogue(self, line: str) -> Optional[Dict]:
        """Extract quote and attribution from a line"""

        for style, pattern in self.quote_patterns.items():
            match = pattern.search(line)
            if match:
                quote = match.group(1)
                pre_text = line[:match.start()].strip()
                post_text = line[match.end():].strip()

                # Check post-text for attribution
                attribution = ""
                if self.attribution_patterns.search(post_text):
                    attribution = post_text

                return {
                    "quote_text": quote,
                    "style": style,
                    "pre_text": pre_text,
                    "attribution_text": attribution
                }

        return None

    def _identify_speaker(self, line_context: str, chapter_context: Dict, line_num: int) -> Tuple[str, Optional[str]]:
        """Intelligently identify who's speaking"""

        # 1. Check explicit attribution in recent lines
        if "he said" in line_context.lower():
            # Look for most recent male character
            return self._find_character_by_gender("male", chapter_context), None
        elif "she said" in line_context.lower():
            return self._find_character_by_gender("female", chapter_context), None

        # 2. Check for name mentions
        for char_id, char_data in chapter_context["active_characters"].items():
            if char_data["name"].lower() in line_context.lower():
                return char_id, None

        # 3. Use chapter context (most recent speaker)
        recent_speaker = chapter_context.get("last_speaker")
        if recent_speaker:
            return recent_speaker, None

        # 4. Default fallback
        return chapter_context["narrator"], None

    def _find_character_by_gender(self, gender: str, context: Dict) -> str:
        """Find most active character of specified gender"""
        candidates = [
            char_id for char_id, char in context["active_characters"].items()
            if char.get("gender") == gender
        ]
        return candidates[0] if candidates else context["narrator"]

    def _update_character_stats(self, chapter_context: Dict, speaker_id: str):
        """Track character line counts for voice consistency"""
        if speaker_id in chapter_context["character_stats"]:
            chapter_context["character_stats"][speaker_id]["lines_spoken"] += 1

        chapter_context["last_speaker"] = speaker_id

    def apply_emotion_markers(self, text: str, emotion: str, character_id: str) -> str:
        """Pre-process text with emotional prompts for Coqui"""

        # Coqui responds well to leading emotional cues
        emotion_prompts = {
            "angry": "[angry voice] ",
            "whispering": "[whispering] ",
            "excited": "[excited tone] ",
            "sad": "[sadly] "
        }

        return emotion_prompts.get(emotion, "") + text