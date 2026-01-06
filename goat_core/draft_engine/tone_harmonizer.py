# goat_core/draft_engine/tone_harmonizer.py
"""
GOAT Draft Engine - Tone + Style Harmonizer
Ensures consistent voice and personality across all content
"""

import json
import re
import random
from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml

class ToneHarmonizer:
    """Harmonizes tone and style across content sections"""

    def __init__(self, voice_profile_path: str = "goat_voice_profile.yaml"):
        self.voice_profile_path = Path(__file__).parent / voice_profile_path
        self.voice_profile = self._load_voice_profile()

    def _load_voice_profile(self) -> Dict[str, Any]:
        """Load the GOAT voice profile"""
        if self.voice_profile_path.exists():
            try:
                with open(self.voice_profile_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except (yaml.YAMLError, FileNotFoundError):
                pass

        # Create default GOAT voice profile
        default_profile = {
            "name": "GOAT Legacy Builder",
            "personality": {
                "core_traits": [
                    "Direct and honest",
                    "Traditional but forward-thinking",
                    "Quick-witted with clever humor",
                    "Practical and results-oriented",
                    "Confident but not arrogant"
                ],
                "communication_style": {
                    "formality_level": "conversational_professional",
                    "sentence_structure": "varied_lengths",
                    "vocabulary": "accessible_expert",
                    "humor_style": "dry_witty"
                }
            },
            "voice_characteristics": {
                "tone_markers": [
                    "let me tell you",
                    "here's the thing",
                    "the truth is",
                    "you see",
                    "make no mistake",
                    "bottom line"
                ],
                "avoided_phrases": [
                    "in conclusion",
                    "it is important to note",
                    "furthermore",
                    "additionally",
                    "unfortunately"
                ],
                "preferred_structures": [
                    "Start with direct statement",
                    "Use rhetorical questions",
                    "End with actionable insight",
                    "Include personal anecdotes",
                    "Balance theory with practice"
                ]
            },
            "content_patterns": {
                "section_openings": [
                    "Let's talk about",
                    "Here's what you need to know about",
                    "The key to understanding",
                    "When it comes to",
                    "What most people miss about"
                ],
                "transitions": [
                    "That brings us to",
                    "Which leads me to",
                    "Here's where it gets interesting",
                    "The real power comes from",
                    "Don't get me wrong"
                ],
                "closings": [
                    "Bottom line",
                    "Remember this",
                    "The lesson here",
                    "What matters most",
                    "Take this with you"
                ]
            },
            "quality_checks": {
                "readability_score": "7-9",
                "active_voice_percentage": "80+",
                "personal_pronoun_usage": "moderate",
                "metaphor_frequency": "1_per_500_words"
            }
        }

        # Save default profile
        self._save_voice_profile(default_profile)
        return default_profile

    def harmonize_content(self, content: str, section_context: Dict[str, Any]) -> str:
        """
        Harmonize content to match GOAT voice profile

        Args:
            content: Raw generated content
            section_context: Context about the section being written

        Returns:
            Harmonized content matching voice profile
        """
        harmonized = content

        # Apply voice filters in sequence
        harmonized = self._apply_tone_markers(harmonized)
        harmonized = self._remove_unwanted_phrases(harmonized)
        harmonized = self._adjust_formality(harmonized)
        harmonized = self._add_voice_characteristics(harmonized, section_context)
        harmonized = self._ensure_structural_patterns(harmonized, section_context)

        return harmonized

    def _apply_tone_markers(self, content: str) -> str:
        """Apply characteristic tone markers"""
        tone_markers = self.voice_profile["voice_characteristics"]["tone_markers"]

        # Add tone markers to appropriate places
        sentences = re.split(r'([.!?]+)', content)

        harmonized_sentences = []
        for i, sentence in enumerate(sentences):
            if i % 3 == 0 and random.random() < 0.3:  # Every few sentences, ~30% chance
                marker = random.choice(tone_markers)
                sentence = f"{marker}, {sentence.lower()}"
            harmonized_sentences.append(sentence)

        return ''.join(harmonized_sentences)

    def _remove_unwanted_phrases(self, content: str) -> str:
        """Remove phrases that don't match the voice"""
        avoided_phrases = self.voice_profile["voice_characteristics"]["avoided_phrases"]

        for phrase in avoided_phrases:
            # Replace with more conversational alternatives
            content = re.sub(re.escape(phrase), self._get_alternative_phrase(phrase), content, flags=re.IGNORECASE)

        return content

    def _get_alternative_phrase(self, phrase: str) -> str:
        """Get alternative phrasing for avoided phrases"""
        alternatives = {
            "in conclusion": "bottom line",
            "it is important to note": "here's what matters",
            "furthermore": "on top of that",
            "additionally": "also",
            "unfortunately": "the thing is"
        }
        return alternatives.get(phrase.lower(), phrase)

    def _adjust_formality(self, content: str) -> str:
        """Adjust formality level to match voice profile"""
        formality_level = self.voice_profile["personality"]["communication_style"]["formality_level"]

        if formality_level == "conversational_professional":
            # Convert overly formal phrases
            formal_to_casual = {
                "it is necessary": "you need",
                "one should": "you should",
                "it is recommended": "I recommend",
                "utilize": "use",
                "facilitate": "help",
                "implement": "put in place"
            }

            for formal, casual in formal_to_casual.items():
                content = re.sub(r'\b' + re.escape(formal) + r'\b', casual, content, flags=re.IGNORECASE)

        return content

    def _add_voice_characteristics(self, content: str, section_context: Dict[str, Any]) -> str:
        """Add characteristic voice elements"""
        import random

        # Add section-appropriate openings
        section_type = section_context.get("content_type", "section")
        openings = self.voice_profile["content_patterns"]["section_openings"]

        if section_type == "section":
            # Add opening to first paragraph
            lines = content.split('\n')
            if lines and not lines[0].startswith('#'):
                opening = random.choice(openings)
                lines[0] = f"{opening} {lines[0].lower()}"
                content = '\n'.join(lines)

        # Add transitions between paragraphs
        paragraphs = content.split('\n\n')
        transitions = self.voice_profile["content_patterns"]["transitions"]

        harmonized_paragraphs = [paragraphs[0]]  # Keep first paragraph as-is

        for i, para in enumerate(paragraphs[1:], 1):
            if random.random() < 0.4:  # 40% chance of adding transition
                transition = random.choice(transitions)
                para = f"{transition}, {para.lower()}"
            harmonized_paragraphs.append(para)

        return '\n\n'.join(harmonized_paragraphs)

    def _ensure_structural_patterns(self, content: str, section_context: Dict[str, Any]) -> str:
        """Ensure content follows preferred structural patterns"""
        patterns = self.voice_profile["voice_characteristics"]["preferred_structures"]

        # Check if content follows preferred patterns
        # This is a simplified implementation

        # Ensure balance of theory and practice
        theory_words = ['theory', 'concept', 'principle', 'framework', 'model']
        practice_words = ['practice', 'do', 'implement', 'apply', 'use', 'action']

        theory_count = sum(1 for word in content.lower().split() if word in theory_words)
        practice_count = sum(1 for word in content.lower().split() if word in practice_words)

        # If too theory-heavy, add practical elements
        if theory_count > practice_count * 2:
            content += "\n\nHere's how to put this into practice: Start small, measure results, then scale up."

        return content

    def analyze_voice_consistency(self, content: str) -> Dict[str, Any]:
        """Analyze how well content matches voice profile"""
        analysis = {
            "tone_markers_present": 0,
            "avoided_phrases_used": 0,
            "formality_score": 0,
            "structural_patterns": 0,
            "overall_consistency": 0
        }

        # Check tone markers
        tone_markers = self.voice_profile["voice_characteristics"]["tone_markers"]
        for marker in tone_markers:
            if marker.lower() in content.lower():
                analysis["tone_markers_present"] += 1

        # Check avoided phrases
        avoided_phrases = self.voice_profile["voice_characteristics"]["avoided_phrases"]
        for phrase in avoided_phrases:
            if phrase.lower() in content.lower():
                analysis["avoided_phrases_used"] += 1

        # Calculate formality score (simplified)
        formal_words = ['utilize', 'facilitate', 'implement', 'furthermore', 'additionally']
        formal_count = sum(1 for word in formal_words if word in content.lower())
        analysis["formality_score"] = min(10, formal_count * 2)

        # Check structural patterns
        preferred_structures = self.voice_profile["voice_characteristics"]["preferred_structures"]
        # Simplified check - look for question marks (rhetorical questions)
        if '?' in content:
            analysis["structural_patterns"] += 2

        # Overall consistency score
        max_score = len(tone_markers) + 10  # Max possible markers + formality
        actual_score = analysis["tone_markers_present"] + (10 - analysis["formality_score"])
        analysis["overall_consistency"] = int(min(10, (actual_score / max_score) * 10))

        return analysis

    def update_voice_profile(self, feedback: Dict[str, Any]):
        """Update voice profile based on feedback"""
        # This would allow the system to learn and adapt the voice profile
        # Implementation would depend on feedback collection system
        pass

    def _save_voice_profile(self, profile: Dict[str, Any]):
        """Save voice profile to file"""
        with open(self.voice_profile_path, 'w', encoding='utf-8') as f:
            yaml.dump(profile, f, default_flow_style=False, allow_unicode=True)

    def get_voice_profile_summary(self) -> str:
        """Get a human-readable summary of the voice profile"""
        profile = self.voice_profile

        summary = f"""GOAT VOICE PROFILE SUMMARY
==========================

Name: {profile['name']}

CORE TRAITS:
{chr(10).join(f'• {trait}' for trait in profile['personality']['core_traits'])}

COMMUNICATION STYLE:
• Formality: {profile['personality']['communication_style']['formality_level']}
• Sentence Structure: {profile['personality']['communication_style']['sentence_structure']}
• Vocabulary: {profile['personality']['communication_style']['vocabulary']}
• Humor: {profile['personality']['communication_style']['humor_style']}

VOICE CHARACTERISTICS:
Tone Markers: {', '.join(profile['voice_characteristics']['tone_markers'])}
Avoided Phrases: {', '.join(profile['voice_characteristics']['avoided_phrases'])}

CONTENT PATTERNS:
Section Openings: {', '.join(profile['content_patterns']['section_openings'][:3])}...
Transitions: {', '.join(profile['content_patterns']['transitions'][:3])}...
Closings: {', '.join(profile['content_patterns']['closings'][:3])}...

QUALITY TARGETS:
{chr(10).join(f'• {k}: {v}' for k, v in profile['quality_checks'].items())}
"""

        return summary