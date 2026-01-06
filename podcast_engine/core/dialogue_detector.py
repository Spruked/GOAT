import re
from dataclasses import dataclass
from typing import List, Optional

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

from ..utils.glyph_tracer import create_glyph_commit


@dataclass
class DialogueLine:
    speaker: str
    text: str
    glyph_id: str


class DialogueDetector:
    """
    Detects speakers in text for dual-voice podcast creation.
    Supports patterns like:
    - "A: Hello there"
    - "B says, 'I agree.'"
    - Narrative lines with no speaker
    """

    SPEAKER_REGEX = re.compile(
        r"^(?P<speaker>[A-Za-z0-9 _\-]+):\s*(?P<text>.+)$"
    )

    QUOTE_REGEX = re.compile(
        r"(?P<speaker>[A-Za-z0-9 _\-]+)\s*(said|says|replied|asked),?\s*['\"](?P<text>.+?)['\"]",
        re.IGNORECASE
    )

    DEFAULT_SPEAKER = "Narrator"

    def detect(self, raw_text: str) -> List[DialogueLine]:

        lines = raw_text.split("\n")
        detected: List[DialogueLine] = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # 1. Pattern: A: Text
            match = self.SPEAKER_REGEX.match(stripped)
            if match:
                speaker = match.group("speaker").strip()
                text = match.group("text").strip()

                glyph = create_glyph_commit(
                    content=f"Dialogue: {speaker}: {text}",
                    metadata={
                        "event_type": "podcast_dialogue_detected",
                        "speaker": speaker,
                        "text": text
                    }
                )

                detected.append(DialogueLine(speaker, text, glyph))
                continue

            # 2. Pattern: A said, "Text"
            match2 = self.QUOTE_REGEX.search(stripped)
            if match2:
                speaker = match2.group("speaker").strip()
                text = match2.group("text").strip()

                glyph = create_glyph_commit(
                    content=f"Dialogue: {speaker} said \"{text}\"",
                    metadata={
                        "event_type": "podcast_dialogue_detected",
                        "speaker": speaker,
                        "text": text
                    }
                )

                detected.append(DialogueLine(speaker, text, glyph))
                continue

            # 3. Default: Narrator voice
            glyph = create_glyph_commit(
                content=f"Narration: {stripped}",
                metadata={
                    "event_type": "podcast_narration_detected",
                    "text": stripped
                }
            )

            detected.append(DialogueLine(self.DEFAULT_SPEAKER, stripped, glyph))

        logger.info(f"[DialogueDetector] Detected {len(detected)} dialogue lines")
        return detected