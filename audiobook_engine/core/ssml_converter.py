import re
from uuid import UUID
from typing import List

from ..utils.glyph_tracer import create_glyph_commit
from ..models.voice_profile import VoiceProfile

SENTENCE_SPLIT_RE = r'(?<=[.!?])\s+'
DIALOGUE_RE = r'“([^”]+)”'


class SSMLConverter:

    def __init__(self, voice: VoiceProfile):
        self.voice = voice

    # -----------------------------
    # Sentence & Dialogue Processing
    # -----------------------------
    def _sentence_split(self, text: str) -> List[str]:
        sentences = re.split(SENTENCE_SPLIT_RE, text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def _apply_dialogue_tags(self, sentence: str) -> str:
        """Apply SSML emphasis for detected dialogue."""
        def repl(match):
            content = match.group(1)
            return (
                f'<prosody volume="+2dB" pitch="1.1" rate="0.95">'
                f'{content}'
                f'</prosody>'
            )
        return re.sub(DIALOGUE_RE, repl, sentence)

    # -----------------------------
    # SSML Assembly
    # -----------------------------
    def _wrap(self, inner: str) -> str:
        return f"<speak>\n{inner}\n</speak>"

    def _sentence_to_ssml(self, sentence: str) -> str:
        # Apply dialogue and emotional prosody
        sentence = self._apply_dialogue_tags(sentence)

        return (
            f'<p>'
            f'<s>'
            f'<prosody rate="{self.voice.speed}" '
            f'pitch="{self.voice.pitch}" '
            f'volume="medium">'
            f'{sentence}'
            f'</prosody>'
            f'</s>'
            f'<break time="600ms"/>'
            f'</p>'
        )

    # -----------------------------
    # Main API
    # -----------------------------
    def convert_chapter(
        self,
        chapter_text: str,
        chapter_number: int,
        project_id: UUID
    ) -> tuple[str, str]:
        """
        Returns:
            (ssml_text, glyph_trace_id)
        """

        sentences = self._sentence_split(chapter_text)
        ssml_blocks = []

        for sentence in sentences:
            ssml_blocks.append(self._sentence_to_ssml(sentence))

        final_ssml = self._wrap("\n".join(ssml_blocks))

        # -----------------------------
        # Glyph Trace
        # -----------------------------
        glyph = create_glyph_commit(
            content=final_ssml,
            metadata={
                "event_type": "ssml_generation",
                "project_id": str(project_id),
                "chapter": chapter_number,
                "text_preview": chapter_text[:200],
                "ssml_preview": final_ssml[:200]
            }
        )

        return final_ssml, glyph