from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import json
import glob
import uuid
import random
from collections import defaultdict
from dandy_skg_models import PersonaProfile, BuildReview, PodcastSegment

class DandySKG:
    # =================================================
    # 6. MULTI-PLATFORM DISTRIBUTION
    # =================================================
    async def generate_social_content(
        self,
        build: BuildReview,
        platforms: List[str]
    ) -> Dict[str, str]:
        content = {}
        for platform in platforms:
            phil_segment = await self.generate_podcast_segment(build, "phil", platform)
            jim_segment = await self.generate_podcast_segment(build, "jim", platform)
            if platform == "tiktok":
                content[platform] = self._tiktok_format(phil_segment, jim_segment)
            elif platform == "youtube":
                content[platform] = self._youtube_format(phil_segment, jim_segment)
            elif platform == "instagram":
                content[platform] = self._instagram_format(phil_segment, jim_segment)
            else:
                content[platform] = self._generic_format(phil_segment, jim_segment)
        return content

    def _tiktok_format(self, phil: PodcastSegment, jim: PodcastSegment) -> str:
        intro = "🔥 Dandy Brothers Review a GOAT Build!\n\n"
        phil_part = f"Phil: {phil.script[:150]}...\n\n"
        jim_part = f"Jim: {jim.script[:150]}...\n\n"
        cta = "Full review on GOAT Channels! #GOAT #DevReview"
        return intro + phil_part + jim_part + cta

    def _youtube_format(self, phil: PodcastSegment, jim: PodcastSegment) -> str:
        intro = f"Today on Dandy Dev Reviews: {phil.build_review.project_name}\n\n"
        phil_full = f"Phil's Take: {phil.script}\n\n"
        jim_full = f"Jim's Response: {jim.script}\n\n"
        links = f"🔗 Try it: {phil.build_review.preview_url or 'N/A'}"
        return intro + phil_full + jim_full + links

    def _instagram_format(self, phil: PodcastSegment, jim: PodcastSegment) -> str:
        quote = f"“{phil.script[:100]}...” — Phil Dandy\n\n"
        quote += f"“{jim.script[:100]}...” — Jim Dandy\n\n"
        quote += f"📱 GOAT Build: {phil.build_review.project_name}"
        return quote

    def _generic_format(self, phil: PodcastSegment, jim: PodcastSegment) -> str:
        return f"Phil & Jim review {phil.build_review.project_name} on GOAT Channels! 🎙️"

    # =================================================
    # 5. CONTENT GENERATION (The Magic)
    # =================================================
    async def generate_podcast_segment(
        self,
        build: BuildReview,
        speaker: str,
        platform: str = "youtube"
    ) -> PodcastSegment:
        persona = self.phil if speaker == "phil" else self.jim
        template = self.platform_templates[platform]
        script = await self._write_script(
            build=build,
            persona=persona,
            max_length=template["max_length"],
            style=template["style"]
        )
        return PodcastSegment(
            segment_id=f"seg_{uuid.uuid4().hex[:8]}",
            build_review=build,
            speaker=speaker,
            script=script,
            duration_seconds=len(script.split()) // 3,
            tone=template["style"],
            platform_optimized={platform: script}
        )

    async def _write_script(
        self,
        build: BuildReview,
        persona: PersonaProfile,
        max_length: int,
        style: str
    ) -> str:
        context = {
            "project_name": build.project_name,
            "tech_stack": ", ".join(build.tech_stack[:3]),
            "summary": build.summary[:200],
            "persona_name": persona.name,
            "style": style
        }
        templates = {
            "opening": persona.speech_patterns[0] if persona.speech_patterns else "So check this out...",
            "tech_praise": f"The {context['tech_stack']} stack here is solid!",
            "playful_jab": "Now Jim might say the CSS is a bit... adventurous, but I love the creativity!",
            "catchphrase": random.choice(persona.catchphrases),
            "closing": "That's a Dandy build if I've ever seen one!"
        }
        script_parts = [
            templates["opening"],
            f"Today we're looking at {context['project_name']}.",
            templates["tech_praise"],
            f"Here's what makes it special: {context['summary']}",
            templates["playful_jab"],
            templates["catchphrase"],
            templates["closing"]
        ]
        script = " ".join(script_parts)
        words = script.split()
        if len(words) > max_length:
            script = " ".join(words[:max_length]) + "..."
        return script
        # =================================================
        # 4. BUILD REVIEW SUBMISSION & SELECTION
        # =================================================

        async def submit_build_for_review(self, build_data: Dict[str, Any]) -> str:
            """User submits a build for Phil & Jim to review"""
            review_id = f"review_{uuid.uuid4().hex[:8]}"
            review = BuildReview(
                build_id=review_id,
                user_id=build_data["user_id"],
                project_name=build_data["project_name"],
                summary=build_data["summary"],
                tech_stack=build_data["tech_stack"],
                code_snippets=build_data.get("code_snippets", []),
                preview_url=build_data.get("preview_url")
            )
            self.build_reviews[review_id] = review
            return review_id

        async def select_builds_for_episode(self, count: int = 3) -> List[BuildReview]:
            """Curate builds that showcase different tech/skill levels"""
            scored = []
            for review in self.build_reviews.values():
                if review.review_status == "pending":
                    score = self._score_build(review)
                    scored.append((review, score))
            scored.sort(key=lambda x: x[1], reverse=True)
            return [r for r, _ in scored[:count]]

        def _score_build(self, review: BuildReview) -> float:
            """Score build for entertainment/educational value"""
            score = 0.0
            score += len(review.tech_stack) * 0.1
            score += min(len(review.summary) / 1000, 1.0)
            if review.code_snippets:
                score += 0.5
            if review.preview_url:
                score += 0.3
            return score
    """
    SKG that holds Phil & Jim's personas AND generates their content.
    Ingests their podcast history, builds knowledge graph of their style,
    and generates platform-specific reviews.
    """
    def __init__(self, seed_vault_path: str):
        self.seed_vault_path = seed_vault_path
        self.phil: Optional[PersonaProfile] = None
        self.jim: Optional[PersonaProfile] = None
        self.build_reviews: Dict[str, BuildReview] = {}
        self.podcast_history: List[Dict[str, Any]] = []
        self.knowledge_graph: Dict[str, Dict[str, Any]] = {}
        self.platform_templates = {
            "tiktok": {"max_length": 60, "style": "punchy_humorous"},
            "youtube": {"max_length": 600, "style": "detailed_enthusiastic"},
            "instagram": {"max_length": 90, "style": "visual_highlight"},
            "facebook": {"max_length": 120, "style": "community_focused"},
            "x": {"max_length": 30, "style": "witty_bite"}
        }

    async def ingest_podcast_history(self, history_manifest: Dict[str, Any]) -> Dict[str, int]:
        stats = {"episodes": 0, "segments": 0, "style_patterns": 0}
        if "podcast_episodes" in history_manifest:
            files = glob.glob(history_manifest["podcast_episodes"])
            results = await asyncio.gather(*[self._ingest_episode(f) for f in files])
            stats["episodes"] = sum(results)
        await self._crystallize_personas()
        stats["style_patterns"] = len(self.knowledge_graph)
        return stats

    async def _ingest_episode(self, filepath: str) -> int:
        with open(filepath, 'r') as f:
            episode = json.load(f)
            for segment in episode["segments"]:
                self.podcast_history.append({
                    "speaker": segment["speaker"],
                    "text": segment["text"],
                    "topic": segment.get("topic", "general"),
                    "tone": segment.get("tone", "neutral"),
                    "timestamp": segment.get("timestamp")
                })
            return len(episode["segments"])

    async def _crystallize_personas(self):
        phil_segments = [s for s in self.podcast_history if s["speaker"] == "phil"]
        jim_segments = [s for s in self.podcast_history if s["speaker"] == "jim"]
        phil_traits = await self._extract_persona_traits(phil_segments, "phil")
        self.phil = PersonaProfile(
            persona_id="phil",
            name="Phil Dandy",
            trait_vector=phil_traits,
            speech_patterns=self._extract_patterns(phil_segments),
            catchphrases=["You know what I love about this...", "That's the Dandy way!"],
            critique_style="constructive",
            expertise_areas=["backend", "architecture"],
            goofball_factor=0.3
        )
        jim_traits = await self._extract_persona_traits(jim_segments, "jim")
        self.jim = PersonaProfile(
            persona_id="jim",
            name="Jim Dandy",
            trait_vector=jim_traits,
            speech_patterns=self._extract_patterns(jim_segments),
            catchphrases=["That's a Jim Dandy idea!", "Boom, roasted!"],
            critique_style="playful",
            expertise_areas=["frontend", "design"],
            goofball_factor=0.8
        )
        self._build_style_knowledge_graph()

    async def _extract_persona_traits(self, segments: List[Dict], persona: str) -> Dict[str, float]:
        traits = defaultdict(float)
        trait_keywords = {
            "witty": ["funny", "joke", "hilarious", "banter"],
            "technical": ["code", "architecture", "performance"],
            "enthusiastic": ["love", "amazing", "excited", "awesome"],
            "patient": ["let me explain", "step by step", "carefully"],
            "critical": ["issue", "problem", "could be better", "but"]
        }
        for segment in segments:
            text_lower = segment["text"].lower()
            for trait, keywords in trait_keywords.items():
                if any(kw in text_lower for kw in keywords):
                    traits[trait] += 1
        total = sum(traits.values())
        if total > 0:
            traits = {k: v/total for k, v in traits.items()}
        return dict(traits)

    def _extract_patterns(self, segments: List[Dict]) -> List[str]:
        patterns = []
        for seg in segments:
            text = seg["text"]
            if text.startswith("You know"):
                patterns.append("You know what I love about this...")
            if "that's a" in text.lower():
                patterns.append("That's a Jim Dandy idea!")
        return list(set(patterns))

    def _build_style_knowledge_graph(self):
        for segment in self.podcast_history:
            topic = segment.get("topic", "general")
            if topic not in self.knowledge_graph:
                self.knowledge_graph[topic] = {
                    "phil_preferred_tone": "technical",
                    "jim_preferred_tone": "playful",
                    "common_phrases": [],
                    "avg_segment_length": 0
                }
