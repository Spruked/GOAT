# podcast_engine.py
"""
GOAT Podcast Engine - SKG-Powered Production System
Uses Structured Knowledge Graph for professional podcast production
COLLECT → STRUCTURE → EXPAND → ARCHIVE → PRESERVE
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import pyttsx3

# Import SKG orchestrator
try:
    from skg_podcast_orchestrator import SKGPodcastOrchestrator
    SKG_AVAILABLE = True
except ImportError:
    SKG_AVAILABLE = False
    print("⚠️  SKG Orchestrator not available, using legacy mode")

@dataclass
class LegacyInput:
    """User input for legacy creation"""
    topic: str
    notes: str
    source_materials: List[str]
    intent: str  # "book", "course", "masterclass", etc.
    audience: str
    output_format: str
    tone: str = "professional"
    length_estimate: str = "medium"
    create_audiobook: bool = False
    voice: Optional[str] = None

@dataclass
class StructuredContent:
    """Auto-structured content"""
    title: str
    sections: List[Dict[str, Any]]
    key_points: List[str]
    flow: List[str]
    metadata: Dict[str, Any]

@dataclass
class ExpandedArtifact:
    """Final expanded content"""
    content_type: str
    title: str
    full_content: str
    sections: List[Dict[str, Any]]
    word_count: int
    estimated_time: str

class PodcastEngine:
    """Core engine for GOAT podcast production with SKG integration"""

    def __init__(self, output_dir: str = "./deliverables/podcast_engine", skg_config: Optional[str] = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize SKG orchestrator if config provided
        self.skg_orchestrator = None
        if skg_config and SKG_AVAILABLE:
            try:
                self.skg_orchestrator = SKGPodcastOrchestrator(skg_config)
                print(f"✅ SKG Orchestrator initialized with {skg_config}")
            except Exception as e:
                print(f"⚠️  Failed to initialize SKG: {e}")
    
    def generate_script(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate podcast script from context
        Used by SKG orchestrator
        """
        # Build script segments based on episode type
        segments = []
        
        # Opening
        if context.get('opening_hook'):
            segments.append({
                'speaker': 'host',
                'text': context['opening_hook']
            })
        
        # Main content from outline
        if context.get('episode_outline'):
            outline_lines = context['episode_outline'].split('\n')
            for line in outline_lines:
                if line.strip():
                    segments.append({
                        'speaker': 'host',
                        'text': line.strip()
                    })
        
        # Talking points
        if context.get('key_talking_points'):
            points = context['key_talking_points'].split('\n')
            for point in points:
                if point.strip():
                    segments.append({
                        'speaker': 'host',
                        'text': point.strip()
                    })
        
        # Closing
        if context.get('closing_statement'):
            segments.append({
                'speaker': 'host',
                'text': context['closing_statement']
            })
        
        return {
            'segments': segments,
            'total_segments': len(segments)
        }
    
    def synthesize_speech(self, text: str, voice_id: str, speaking_rate: float = 1.0) -> bytes:
        """
        Synthesize speech from text
        Used by SKG orchestrator
        """
        # Placeholder for actual voice synthesis
        # TODO: Integrate with ElevenLabs, OpenAI TTS, or other provider
        return b''  # Return audio bytes

    def create_legacy(self, user_input: LegacyInput) -> Dict[str, Any]:
        """Main pipeline: COLLECT → STRUCTURE → EXPAND → ARCHIVE → PRESERVE"""

        # Step 1: COLLECT - Already done via user_input

        # Step 2: STRUCTURE - Auto-organize content
        structured = self._structure_content(user_input)

        # Step 3: EXPAND - Generate full artifact
        artifact = self._expand_content(structured, user_input)

        # Step 3.5: Generate audiobook if requested
        audiobook_path = None
        if user_input.create_audiobook:
            audiobook_path = self._generate_audiobook(artifact, user_input.voice, user_input.output_format)

        # Step 4: ARCHIVE - Save to vault
        archived = self._archive_artifact(artifact, user_input, audiobook_path)

        # Step 5: PRESERVE - Prepare for minting
        preserved = self._prepare_preservation(archived)

        return {
            "legacy_id": archived["legacy_id"],
            "structured_content": asdict(structured),
            "artifact": asdict(artifact),
            "audiobook_path": audiobook_path,
            "archive_path": archived["path"],
            "preservation_ready": preserved,
            "minting_suggestions": self._get_minting_suggestions(user_input.intent)
        }

    def _structure_content(self, user_input: LegacyInput) -> StructuredContent:
        """Step 2: Auto-structure the content using AI patterns"""

        # Extract key themes from notes
        themes = self._extract_themes(user_input.notes)

        # Create logical flow
        flow = self._create_flow(themes, user_input.intent)

        # Structure into sections
        sections = self._create_sections(flow, user_input)

        return StructuredContent(
            title=self._generate_title(user_input),
            sections=sections,
            key_points=themes,
            flow=flow,
            metadata={
                "intent": user_input.intent,
                "audience": user_input.audience,
                "tone": user_input.tone,
                "source_count": len(user_input.source_materials)
            }
        )

    def _expand_content(self, structured: StructuredContent, user_input: LegacyInput) -> ExpandedArtifact:
        """Step 3: Expand outline into full content"""

        # Generate full content for each section
        expanded_sections = []
        full_content = ""

        for section in structured.sections:
            expanded_text = self._expand_section(section, user_input)
            expanded_sections.append({
                "title": section["title"],
                "content": expanded_text,
                "word_count": len(expanded_text.split())
            })
            full_content += f"## {section['title']}\n\n{expanded_text}\n\n"

        return ExpandedArtifact(
            content_type=user_input.intent,
            title=structured.title,
            full_content=full_content,
            sections=expanded_sections,
            word_count=len(full_content.split()),
            estimated_time=self._estimate_reading_time(full_content)
        )

    def _generate_audiobook(self, artifact: ExpandedArtifact, voice: Optional[str], audio_type: str = 'podcast') -> str:
        """Generate audiobook or podcast-style audio using TTS"""
        engine = pyttsx3.init()

        # Get available voices and select from first 3
        voices = engine.getProperty('voices')
        available_voices = [v.id for v in voices[:3]]  # Limit to 3 voices

        if voice and voice in available_voices:
            engine.setProperty('voice', voice)
        elif available_voices:
            engine.setProperty('voice', available_voices[0])  # Default to first
        else:
            raise ValueError("No TTS voices available")

        # Set speech rate based on audio type
        engine.setProperty('rate', 180 if audio_type == 'podcast' else 150)  # Faster for podcast

        # Generate audio file path
        audio_filename = f"{artifact.title.replace(' ', '_')}_{audio_type}.mp3"
        audio_path = self.output_dir / "temp" / audio_filename
        audio_path.parent.mkdir(parents=True, exist_ok=True)

        # Save to file
        engine.save_to_file(artifact.full_content, str(audio_path))
        engine.runAndWait()

        return str(audio_path)

    def _archive_artifact(self, artifact: ExpandedArtifact, user_input: LegacyInput, audiobook_path: Optional[str] = None) -> Dict[str, Any]:
        """Step 4: Archive the completed artifact"""

        legacy_id = str(uuid.uuid4())
        archive_path = self.output_dir / legacy_id
        archive_path.mkdir(exist_ok=True)

        # Save different formats
        files_created = {
            "full_content.md": artifact.full_content,
            "metadata.json": json.dumps({
                "legacy_id": legacy_id,
                "created_at": datetime.utcnow().isoformat(),
                "user_input": asdict(user_input),
                "artifact": asdict(artifact)
            }, indent=2, default=str)
        }

        # Add audiobook if generated
        if audiobook_path and os.path.exists(audiobook_path):
            import shutil
            audio_dest = archive_path / f"{artifact.title.replace(' ', '_')}_audiobook.mp3"
            shutil.copy2(audiobook_path, audio_dest)
            files_created["audiobook.mp3"] = str(audio_dest)

        # Create structured export
        if artifact.content_type == "book":
            files_created["book_outline.md"] = self._create_book_outline(artifact)
        elif artifact.content_type == "course":
            files_created["course_modules.json"] = json.dumps(self._create_course_structure(artifact), indent=2)
        elif artifact.content_type == "masterclass":
            files_created["masterclass_sessions.json"] = json.dumps(self._create_masterclass_structure(artifact), indent=2)

        # Write files
        for filename, content in files_created.items():
            if not filename.endswith('.mp3'):  # Skip copying audio again
                with open(archive_path / filename, 'w', encoding='utf-8') as f:
                    f.write(content)

        return {
            "legacy_id": legacy_id,
            "path": str(archive_path),
            "files": list(files_created.keys())
        }

    def _prepare_preservation(self, archived: Dict[str, Any]) -> Dict[str, Any]:
        """Step 5: Prepare for preservation/minting"""

        return {
            "ready_for_minting": True,
            "legacy_id": archived["legacy_id"],
            "archive_path": archived["path"],
            "certification_options": ["certsig", "truemark"]
        }

    def _extract_themes(self, notes: str) -> List[str]:
        """Extract key themes from user notes"""
        # Simple keyword extraction - in real implementation, use NLP
        words = notes.lower().split()
        themes = []

        # Look for common content indicators
        indicators = ["chapter", "section", "topic", "point", "idea", "concept", "principle"]
        for word in words:
            if any(ind in word for ind in indicators) or len(word) > 6:
                themes.append(word.title())

        return themes[:8] if themes else ["Introduction", "Core Concepts", "Key Principles", "Practical Applications", "Conclusion"]

    def _create_flow(self, themes: List[str], intent: str) -> List[str]:
        """Create logical content flow"""
        if intent == "book":
            return ["Introduction"] + themes + ["Conclusion", "Appendices"]
        elif intent == "course":
            return ["Overview"] + [f"Module {i+1}: {theme}" for i, theme in enumerate(themes)] + ["Final Project"]
        elif intent == "masterclass":
            return ["Welcome"] + [f"Session {i+1}: {theme}" for i, theme in enumerate(themes)] + ["Q&A", "Resources"]
        else:
            return ["Opening"] + themes + ["Summary"]

    def _create_sections(self, flow: List[str], user_input: LegacyInput) -> List[Dict[str, Any]]:
        """Create detailed sections"""
        sections = []
        for i, section_title in enumerate(flow):
            sections.append({
                "number": i + 1,
                "title": section_title,
                "estimated_words": 500 if "introduction" in section_title.lower() else 800,
                "key_points": self._generate_section_points(section_title, user_input)
            })
        return sections

    def _generate_title(self, user_input: LegacyInput) -> str:
        """Generate compelling title"""
        base = user_input.topic.title()
        if user_input.intent == "book":
            return f"{base}: A Complete Guide"
        elif user_input.intent == "course":
            return f"{base} Mastery Course"
        elif user_input.intent == "masterclass":
            return f"Masterclass: {base}"
        else:
            return f"{base} Framework"

    def _expand_section(self, section: Dict[str, Any], user_input: LegacyInput) -> str:
        """Expand section outline into full content"""
        content = f"This section explores {section['title'].lower()} in the context of {user_input.topic}.\n\n"

        for point in section["key_points"]:
            content += f"• {point}\n"

        content += f"\nDrawing from {user_input.audience} perspective, {user_input.topic} represents a crucial foundation for understanding modern approaches to this field."

        return content

    def _generate_section_points(self, section_title: str, user_input: LegacyInput) -> List[str]:
        """Generate key points for a section"""
        return [
            f"Understanding the fundamentals of {section_title.lower()}",
            f"Practical applications in {user_input.topic}",
            f"Common challenges and solutions",
            f"Best practices for implementation"
        ]

    def _estimate_reading_time(self, content: str) -> str:
        """Estimate reading time"""
        words = len(content.split())
        minutes = max(1, words // 200)  # 200 words per minute
        return f"{minutes} minutes"

    def _create_book_outline(self, artifact: ExpandedArtifact) -> str:
        """Create book outline in markdown"""
        outline = f"# {artifact.title}\n\n"
        outline += "## Table of Contents\n\n"

        for section in artifact.sections:
            outline += f"{section['number']}. {section['title']}\n"

        outline += f"\n**Total Word Count:** {artifact.word_count}\n"
        outline += f"**Estimated Reading Time:** {artifact.estimated_time}\n"

        return outline

    def _create_course_structure(self, artifact: ExpandedArtifact) -> Dict[str, Any]:
        """Create course module structure"""
        return {
            "course_title": artifact.title,
            "modules": [
                {
                    "title": section["title"],
                    "content": section["content"],
                    "duration": "30 minutes",
                    "objectives": [f"Understand {section['title'].lower()}"]
                } for section in artifact.sections
            ],
            "total_duration": f"{len(artifact.sections) * 30} minutes"
        }

    def _create_masterclass_structure(self, artifact: ExpandedArtifact) -> Dict[str, Any]:
        """Create masterclass session structure"""
        return {
            "masterclass_title": artifact.title,
            "sessions": [
                {
                    "title": section["title"],
                    "content": section["content"],
                    "duration": "45 minutes",
                    "format": "Interactive Workshop"
                } for section in artifact.sections
            ],
            "total_duration": f"{len(artifact.sections) * 45} minutes"
        }

    def _get_minting_suggestions(self, intent: str) -> Dict[str, Any]:
        """Get appropriate minting suggestions"""
        suggestions = {
            "book": {
                "certsig": "Perfect for certifying your complete manuscript and establishing permanent authorship.",
                "truemark": "Ideal for proving the knowledge framework and research foundation of your book."
            },
            "course": {
                "certsig": "Certify your course curriculum and teaching methodology as your intellectual property.",
                "truemark": "Validate the educational framework and learning outcomes you've designed."
            },
            "masterclass": {
                "certsig": "Preserve your unique teaching style and masterclass methodology forever.",
                "truemark": "Document the specialized knowledge and expertise you bring to your field."
            }
        }

        return suggestions.get(intent, {
            "certsig": "Certify this work as your permanent intellectual property.",
            "truemark": "Validate the knowledge and expertise foundation of your creation."
        })

    def get_caleon_guidance(self, step: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Get Caleon's guidance for each step"""

        guidance = {
            "collect": "Tell me about your topic, add your notes and source materials. I'll help structure this into something remarkable.",

            "structure": f"I've analyzed your input and created a {(context or {}).get('intent', 'content')} structure. Does this flow work for you, or shall I adjust it?",

            "expand": "Now I'll expand this outline into full content. This might take a moment as I craft each section thoughtfully.",

            "archive": "Your work is complete! I've saved it to your vault. You can access it anytime for editing or sharing.",

            "preserve": "If you'd like to make this version permanent and unchangeable, I can connect you with our minting partners."
        }

        return guidance.get(step, "I'm here to guide you through creating your greatest work.")

def select_content_builder(intent, output_format, topic):
    intent = intent.lower()
    output_format = output_format.lower()
    topic_lower = topic.lower()

    # Podcast routing logic
    if (
        "podcast" in intent
        or "audio" in output_format
        or "podcast" in topic_lower
    ):
        return PodcastBuilder()

    # Framework fallback
    return FrameworkBuilder()

class PodcastBuilder:
    def build(self, topic, audience, tone, length):
        expanded = LongFormExpander().expand(
            topic=topic,
            tone=tone,
            audience=audience,
            length=length,
            mode="podcast"
        )

        narrative = NarrativeComposer().compose(
            content=expanded,
            mode="podcast",
            tone=tone,
            audience=audience
        )

        return narrative

class LongFormExpander:
    def expand(self, topic, tone, audience, length, mode="podcast"):
        base_multiplier = {
            "short": 1.0,
            "medium": 2.0,
            "long": 3.5
        }.get(length, 2.0)

        template = {
            "podcast": PODCAST_EXPANSION_TEMPLATE,
            "framework": FRAMEWORK_TEMPLATE
        }[mode]

        content = ai_generate(
            f"Expand into a detailed {mode} script:\n"
            f"Topic: {topic}\nAudience: {audience}\nTone: {tone}\n"
            f"Length multiplier: {base_multiplier}\n"
            f"Template: {template}\n"
        )

        return content

def generate_tts_voice(text, voice_id=None, output_path="podcast.mp3"):
    engine = pyttsx3.init()
    voice = voice_id or "en-US-JennyNeural"  # or your best Coqui voice
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)  # Use first available voice
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path