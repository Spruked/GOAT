"""
Podcast Engine with UCM (thinking) and DALS (workers/routing) integration
"""
import json
import os
import uuid
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

from .models import LegacyInput, StructuredContent, ExpandedArtifact
from .bridges import UCMBridge, DALSBridge
from shared.voice_service import generate_voice
from .skg import SpeakerKnowledgeGraph, DandyShowGenerator


def speak(text: str, voice: str = "cali", style: str = "narration") -> bytes:
    """Wrapper for Phonatory Output Module speak function"""
    # For now, use the POM phonate method and return file content as bytes
    import sys
    sys.path.append(str(Path(__file__).parent.parent / "Phonatory_Output_Module"))
    from phonitory_output_module import PhonatoryOutputModule
    
    pom = PhonatoryOutputModule()
    output_path = pom.phonate(text)
    
    # Read the file as bytes
    with open(output_path, 'rb') as f:
        return f.read()


class PodcastEngine:
    """Core engine for GOAT legacy creation with UCM/DALS integration"""

    def __init__(
        self,
        output_dir: str = "./deliverables/podcast_engine",
        use_ucm: bool = False,
        use_dals: bool = False,
        ucm_url: Optional[str] = None,
        dals_url: Optional[str] = None
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Bridge initialization
        self.use_ucm = use_ucm
        self.use_dals = use_dals
        self.ucm_bridge = UCMBridge(ucm_url) if use_ucm and ucm_url else None
        self.dals_bridge = DALSBridge(dals_url) if use_dals and dals_url else None

        # SKG initialization for podcast generation
        try:
            self.skg = SpeakerKnowledgeGraph()
            self.dandy_generator = DandyShowGenerator(self.skg)
            print("✅ SKG system initialized for podcast generation")
        except Exception as e:
            print(f"⚠️  SKG system not available: {e}")
            self.skg = None
            self.dandy_generator = None

    def create_legacy(self, user_input: LegacyInput) -> Dict[str, Any]:
        """Main pipeline: COLLECT → STRUCTURE → EXPAND → ARCHIVE → PRESERVE"""

        # Step 1: COLLECT - Already done via user_input
        if self.dals_bridge:
            self.dals_bridge.dispatch({
                "type": "workflow_start",
                "stage": "collect",
                "topic": user_input.topic,
                "intent": user_input.intent
            })

        # Step 2: STRUCTURE - Auto-organize content
        structured = self._structure_content(user_input)

        # UCM THINKING: Analyze structure quality
        if self.ucm_bridge:
            analysis = self.ucm_bridge.analyze({
                "stage": "structure",
                "content": asdict(structured),
                "user_input": asdict(user_input)
            })
            # Use analysis to refine structure if needed
            if analysis.get("suggestions"):
                structured = self._refine_structure(structured, analysis["suggestions"])

        # Step 3: EXPAND - Generate full artifact
        artifact = self._expand_content(structured, user_input)

        # UCM THINKING: Review content quality
        if self.ucm_bridge:
            content_analysis = self.ucm_bridge.analyze({
                "stage": "expand",
                "artifact": asdict(artifact),
                "quality_check": True
            })

        # Step 3.5: Generate audiobook if requested
        audiobook_path = None
        if user_input.create_audiobook:
            if self.dals_bridge:
                self.dals_bridge.dispatch({
                    "type": "audio_generation_start",
                    "title": artifact.title,
                    "word_count": artifact.word_count
                })

            audiobook_path = self._generate_audiobook(
                artifact, user_input.voice, user_input.output_format
            )

            if self.dals_bridge:
                self.dals_bridge.dispatch(payload={
                    "type": "audio_generation_complete",
                    "job_type": "audiobook",
                    "path": audiobook_path
                })

        # Step 4: ARCHIVE - Save to vault
        archived = self._archive_artifact(artifact, user_input, audiobook_path)

        if self.dals_bridge:
            self.dals_bridge.dispatch(payload={
                "type": "archive_complete",
                "job_type": "archive",
                "legacy_id": archived["legacy_id"],
                "path": archived["path"]
            })

        # Step 5: PRESERVE - Prepare for minting
        preserved = self._prepare_preservation(archived)

        # Final UCM summary
        if self.ucm_bridge:
            final_summary = self.ucm_bridge.analyze({
                "stage": "complete",
                "legacy_id": archived["legacy_id"],
                "artifact": asdict(artifact),
                "audiobook_generated": audiobook_path is not None
            })

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

    def _refine_structure(self, structured: StructuredContent, suggestions: List[str]) -> StructuredContent:
        """Refine structure based on UCM suggestions"""
        # In production, this would apply AI-driven improvements
        # For now, just return the original structure
        return structured

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
        """Generate audiobook or podcast-style audio using SKG system"""
        if not self.dandy_generator or not self.skg:
            # Fallback to basic audio generation
            return self._generate_fallback_audiobook(artifact, voice, audio_type)

        try:
            from skg.audiobook_generator import AudiobookGenerator
            audiobook_gen = AudiobookGenerator(self.skg)

            # Prepare manuscript from artifact
            manuscript = self._artifact_to_manuscript(artifact)

            # Configure audiobook generation
            config = {
                "title": artifact.title,
                "author": "GOAT User",  # Could be extracted from user input
                "narrator_id": voice or "phil_dandy",
                "genre": "non-fiction" if artifact.content_type != "fiction" else "fiction",
                "character_voice_map": {}  # Add character mapping if fiction
            }

            return audiobook_gen.generate_audiobook(manuscript, config)

        except Exception as e:
            print(f"⚠️  SKG audiobook generation failed: {e}")
            return self._generate_fallback_audiobook(artifact, voice, audio_type)

    def _generate_fallback_audiobook(self, artifact: ExpandedArtifact, voice: Optional[str], audio_type: str) -> str:
        """Fallback audiobook generation when SKG is not available"""
        from pydub import AudioSegment

        # Generate audio file path
        audio_filename = f"{artifact.title.replace(' ', '_')}_{audio_type}.wav"
        audio_path = self.output_dir / "temp" / audio_filename
        audio_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate audio for each section and combine
        combined_audio = AudioSegment.empty()

        for section in artifact.sections:
            segment_text = section['content']
            # Use shared voice service
            voice_style = "narration" if audio_type == 'podcast' else "audiobook"
            segment_path = generate_voice(segment_text, voice=voice or "cali", style=voice_style)

            # Load audio from file
            segment_audio = AudioSegment.from_wav(segment_path)
            combined_audio += segment_audio
            # Clean up temp file
            os.remove(segment_path)

        # Export combined audio
        combined_audio.export(str(audio_path), format="wav")

        return str(audio_path)

    def _artifact_to_manuscript(self, artifact: ExpandedArtifact) -> str:
        """Convert ExpandedArtifact to manuscript format for audiobook generation"""
        manuscript = f"# {artifact.title}\n\n"

        for section in artifact.sections:
            manuscript += f"## {section['title']}\n\n{section['content']}\n\n"

        return manuscript

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
        section_title = section['title']
        
        # For podcasts, generate conversational dialogue
        if user_input.output_format == 'podcast' or 'podcast' in user_input.intent.lower():
            content = self._generate_podcast_dialogue(section_title, user_input)
        else:
            # Standard article-style content
            content = f"This section explores {section_title.lower()} in the context of {user_input.topic}.\n\n"
            for point in section["key_points"]:
                content += f"• {point}\n"
            content += f"\nDrawing from {user_input.audience} perspective, {user_input.topic} represents a crucial foundation for understanding modern approaches to this field."

        return content

    def _generate_podcast_dialogue(self, section_title: str, user_input: LegacyInput) -> str:
        """Generate conversational podcast dialogue using SKG system"""
        if not self.dandy_generator:
            # Fallback to original hardcoded dialogue if SKG not available
            return self._generate_fallback_dialogue(section_title, user_input)

        topic = user_input.topic

        # Create topic dict for SKG system
        topic_data = {
            "title": topic,
            "description": user_input.notes[:200] if user_input.notes else "",
            "submitter": "GOAT User",
            "category": user_input.intent,
            "key_points": self._extract_key_points(user_input.notes or "")
        }

        try:
            # Generate episode segment using SKG
            segments = self.dandy_generator.generate_episode_segment(topic_data)

            # Combine all text segments into dialogue
            dialogue_parts = []
            for segment in segments:
                dialogue_parts.append(f"{self.skg.get_persona(segment['speaker'])['name']}: {segment['text']}")

            return "\n\n".join(dialogue_parts)

        except Exception as e:
            print(f"⚠️  SKG generation failed, using fallback: {e}")
            return self._generate_fallback_dialogue(section_title, user_input)

    def _generate_fallback_dialogue(self, section_title: str, user_input: LegacyInput) -> str:
        """Fallback dialogue generation when SKG is not available"""
        topic = user_input.topic
        tone = user_input.tone

        # Generate dialogue based on section
        if "Introduction" in section_title or "Welcome" in section_title or "Opening" in section_title:
            return f"""[THEME MUSIC FADES]

Phil: Hey everyone, welcome back to {topic}! I'm Phil Dandy.

Jim: And I'm Jim Dandy, and boy do we have an exciting show for you today!

Phil: That's right Jim. We're going to be talking all about {topic.lower()}, and trust me, you're going to want to stick around for this one.

Jim: Absolutely. We've got some incredible stories, some hard-won wisdom, and maybe even a few laughs along the way.

Phil: So grab yourself a cold drink, get comfortable, and let's dive right in!"""

        elif "Conclusion" in section_title or "Summary" in section_title:
            return f"""Phil: Well Jim, I think that's going to wrap up our show for today.

Jim: What an incredible journey we've been on! I hope everyone listening learned as much as I did.

Phil: Absolutely. The key takeaway here is that {topic.lower()} is really about dedication, passion, and always being willing to learn something new.

Jim: Couldn't have said it better myself, brother.

Phil: So to all our listeners out there - thank you so much for joining us today.

Jim: Get out there, apply what you've learned, and most importantly, have fun with it!

Phil: Until next time, this is Phil Dandy...

Jim: And Jim Dandy...

Both: Signing off!

[THEME MUSIC RISES]"""

        else:
            # Generate content segment with back-and-forth dialogue
            return f"""Phil: So Jim, let's talk about {section_title.lower()}. What's your take on this?

Jim: Well Phil, I've spent years working on this, and I can tell you - it's absolutely fascinating. When it comes to {topic.lower()}, this is one of the most important aspects.

Phil: I couldn't agree more. You know, our {user_input.audience} audience really needs to understand this because it forms the foundation of everything else.

Jim: Exactly! Let me share a quick story. There was this one time when I was really getting into {topic.lower()}, and I realized that {section_title.lower()} was the key to taking things to the next level.

Phil: That's a great point. And what I love about this is how accessible it is. Anyone can learn this with the right {tone} approach.

Jim: Absolutely. The key is to stay focused, be patient with yourself, and remember why you started this journey in the first place.

Phil: Well said, brother. Now, there's another aspect to this that I think our listeners will find really valuable...

Jim: Oh yes, this is where it gets really interesting! See, when you combine what we just discussed with practical application, that's when the magic happens.

Phil: And that's what makes {topic.lower()} so rewarding. It's not just theory - it's real-world experience that you can use right away.

Jim: Couldn't have said it better myself!"""

    def _extract_key_points(self, notes: str) -> List[str]:
        """Extract key points from notes for SKG topic analysis"""
        if not notes:
            return ["innovation", "technology", "implementation"]

        words = notes.lower().split()
        key_points = []

        # Look for technical keywords
        tech_keywords = ["ai", "machine learning", "software", "platform", "system", "tool", "application"]
        for word in words:
            if any(keyword in word for keyword in tech_keywords) or len(word) > 5:
                key_points.append(word.title())

        return key_points[:5] if key_points else ["innovation", "technology", "implementation"]

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
