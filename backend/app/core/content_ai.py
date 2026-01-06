# backend/app/core/content_ai.py
import json
from typing import Dict, List
from app.config import settings



# LLM Provider: Local only (GPT4All with local CPU model)
# No OpenAI. No cloud. CPU-resident for privacy + speed.
# Hardware-agnostic: CPU now, GPU later as drop-in upgrade.
LLM_PROVIDER = "local"

class ContentAI:
    def __init__(self, settings):
        self.settings = settings

    async def chat_completion(self, prompt, model=None, **kwargs):
        # TODO: Implement GPT4All local CPU model call here
        raise NotImplementedError("Local LLM integration required (GPT4All)")

    async def summarize(self, text, model=None, **kwargs):
        # TODO: Implement GPT4All local CPU model call here
        raise NotImplementedError("Local LLM integration required (GPT4All)")

    async def extract_keywords(self, text, model=None, **kwargs):
        # TODO: Implement GPT4All local CPU model call here
        raise NotImplementedError("Local LLM integration required (GPT4All)")

# Global instance
content_ai = ContentAI(settings)


class ContentGenerator:
    """Backward-compatible synchronous content generator used by video endpoints.

    This is a lightweight local-only implementation that does not call any
    external LLM. Replace or extend it to call GPT4All with local CPU model.
    Hardware-agnostic: CPU now, GPU later as drop-in upgrade.
    """

    def __init__(self, settings):
        self.settings = settings

    def _simple_keywords(self, text: str, limit: int = 5) -> List[str]:
        if not text:
            return []
        words = [w.strip('.,!?:;()"\'') for w in text.split()]
        candidates = [w for w in words if len(w) > 4]
        seen = []
        for w in candidates:
            lw = w.lower()
            if lw not in seen:
                seen.append(lw)
            if len(seen) >= limit:
                break
        return seen

    def generate_memory_dialog(self, media_metadata: Dict) -> Dict:
        """Generate a simple memory dialog from metadata without external LLMs."""
        desc = media_metadata.get('description') or media_metadata.get('title') or ''
        date = media_metadata.get('date', '')
        people = media_metadata.get('people', []) or []
        location = media_metadata.get('location', '')

        part1 = desc
        if date:
            part1 += f" Recorded on {date}."
        if location:
            part1 += f" Location: {location}."

        if people:
            people_str = ', '.join(people[:5])
            part2 = f"Featuring: {people_str}."
        else:
            part2 = "A personal memory of significance."

        script = f"{part1} {part2} This piece focuses on legacy and timeless emotion."

        # Chapters: use provided clips if any, otherwise single chapter
        chapters = []
        clips = media_metadata.get('clips') or media_metadata.get('items') or []
        if clips and isinstance(clips, list):
            for i, c in enumerate(clips[:10]):
                title = c.get('title') if isinstance(c, dict) else f"Clip {i+1}"
                text = c.get('note') if isinstance(c, dict) else ''
                chapters.append({'title': title or f'Chapter {i+1}', 'text': text or script})
        else:
            chapters = [{'title': 'Main', 'text': script}]

        keywords = self._simple_keywords(desc)

        return {
            'script': script,
            'chapters': chapters,
            'keywords': keywords,
            'summary': script[:300]
        }


# Backwards-compatible global used by older endpoints
content_generator = ContentGenerator(settings)