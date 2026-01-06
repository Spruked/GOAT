# engines/structural_engine.py
"""
GOAT Structural Engine - Story Shape Analysis
Phase 1, Module 2: Understands story structure and narrative arcs

Analyzes story shape, detects missing transitions, identifies arcs,
and provides structural improvement suggestions.
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re
from collections import Counter, defaultdict

from .deep_parser import DeepParser, ParsedText

class ArcType(Enum):
    """Types of narrative arcs"""
    RISING = "rising"
    FALLING = "falling"
    FLAT = "flat"
    COMPLEX = "complex"

class PacingType(Enum):
    """Types of pacing"""
    FAST = "fast"
    SLOW = "slow"
    VARIABLE = "variable"
    INCONSISTENT = "inconsistent"

@dataclass
class ChapterAnalysis:
    """Analysis of a single chapter"""
    chapter_number: int
    title: str
    word_count: int
    sentence_count: int
    dialogue_ratio: float
    emotion_score: float
    conflict_level: float
    pacing_indicators: List[str]
    themes_present: List[str]
    characters_active: List[str]

@dataclass
class StructuralAnalysis:
    """Complete structural analysis of a story"""
    chapters: List[ChapterAnalysis]
    overall_arc: ArcType
    pacing_profile: PacingType
    missing_transitions: List[Dict[str, Any]]
    structural_issues: List[str]
    improvement_suggestions: List[str]
    narrative_flow_score: float

class StructuralEngine:
    """
    GOAT's structural analysis engine - understands story shape and narrative flow
    """

    def __init__(self):
        self.deep_parser = DeepParser()

        # Keywords for detecting structural elements
        self.conflict_keywords = [
            'fight', 'battle', 'conflict', 'struggle', 'problem', 'crisis',
            'argument', 'dispute', 'clash', 'confrontation', 'tension'
        ]

        self.transition_keywords = [
            'however', 'but', 'although', 'despite', 'nevertheless',
            'meanwhile', 'suddenly', 'then', 'after', 'before',
            'later', 'next', 'following', 'subsequently'
        ]

        self.pacing_indicators = {
            'fast': ['rushed', 'quickly', 'suddenly', 'abruptly', 'racing'],
            'slow': ['slowly', 'gradually', 'lingering', 'deliberately', 'methodically']
        }

    def analyze(self, text: str) -> StructuralAnalysis:
        """
        Main analysis function - performs complete structural analysis
        """
        # Parse the text first
        parsed = self.deep_parser.parse(text)

        # Analyze each chapter
        chapters = []
        for i, chapter_data in enumerate(parsed.chapters):
            chapter_analysis = self._analyze_chapter(chapter_data, parsed, i + 1)
            chapters.append(chapter_analysis)

        # Analyze overall structure
        overall_arc = self._detect_overall_arc(chapters)
        pacing_profile = self._analyze_pacing(chapters)
        missing_transitions = self._detect_missing_transitions(chapters, parsed)
        structural_issues = self._identify_structural_issues(chapters, parsed)
        improvement_suggestions = self._generate_improvement_suggestions(chapters, parsed)
        narrative_flow_score = self._calculate_narrative_flow_score(chapters, parsed)

        return StructuralAnalysis(
            chapters=chapters,
            overall_arc=overall_arc,
            pacing_profile=pacing_profile,
            missing_transitions=missing_transitions,
            structural_issues=structural_issues,
            improvement_suggestions=improvement_suggestions,
            narrative_flow_score=narrative_flow_score
        )

    def _analyze_chapter(self, chapter_data: Dict[str, Any], parsed: ParsedText, chapter_num: int) -> ChapterAnalysis:
        """Analyze a single chapter"""
        content = chapter_data['content']

        # Basic metrics
        word_count = len(content.split())
        sentences = self.deep_parser._split_sentences(content)
        sentence_count = len(sentences)

        # Dialogue ratio
        dialogues_in_chapter = [d for d in parsed.dialogues
                              if chapter_data['start_line'] <= self._find_line_number(d['context'], parsed)
                              <= chapter_data['end_line']]
        dialogue_words = sum(len(d['quote'].split()) for d in dialogues_in_chapter)
        dialogue_ratio = dialogue_words / word_count if word_count > 0 else 0

        # Emotion score (average intensity)
        emotions_in_chapter = [e for e in parsed.emotions
                             if self._sentence_in_chapter(e['sentence_index'], sentences, chapter_data)]
        emotion_score = sum(e['intensity'] for e in emotions_in_chapter) / len(sentences) if sentences else 0

        # Conflict level
        conflict_words = sum(1 for word in content.lower().split() if word in self.conflict_keywords)
        conflict_level = conflict_words / word_count if word_count > 0 else 0

        # Pacing indicators
        pacing_indicators = []
        content_lower = content.lower()
        for pace_type, indicators in self.pacing_indicators.items():
            for indicator in indicators:
                if indicator in content_lower:
                    pacing_indicators.append(f"{pace_type}: {indicator}")

        # Themes and characters in this chapter
        themes_present = self._extract_chapter_themes(content, parsed.themes)
        characters_active = self._extract_chapter_characters(content, parsed.characters)

        return ChapterAnalysis(
            chapter_number=chapter_num,
            title=chapter_data['title'],
            word_count=word_count,
            sentence_count=sentence_count,
            dialogue_ratio=dialogue_ratio,
            emotion_score=emotion_score,
            conflict_level=conflict_level,
            pacing_indicators=pacing_indicators,
            themes_present=themes_present,
            characters_active=characters_active
        )

    def _detect_overall_arc(self, chapters: List[ChapterAnalysis]) -> ArcType:
        """Detect the overall narrative arc"""
        if len(chapters) < 2:
            return ArcType.FLAT

        # Analyze conflict progression
        conflict_levels = [c.conflict_level for c in chapters]
        emotion_levels = [c.emotion_score for c in chapters]

        # Simple arc detection based on conflict and emotion patterns
        if conflict_levels[-1] > conflict_levels[0] and emotion_levels[-1] > emotion_levels[0]:
            return ArcType.RISING
        elif conflict_levels[-1] < conflict_levels[0] and emotion_levels[-1] < emotion_levels[0]:
            return ArcType.FALLING
        elif max(conflict_levels) > 0.1 and min(conflict_levels) < 0.05:
            return ArcType.COMPLEX
        else:
            return ArcType.FLAT

    def _analyze_pacing(self, chapters: List[ChapterAnalysis]) -> PacingType:
        """Analyze overall pacing profile"""
        if len(chapters) < 2:
            return PacingType.INCONSISTENT

        word_counts = [c.word_count for c in chapters]
        avg_words = sum(word_counts) / len(word_counts)
        variance = sum((w - avg_words) ** 2 for w in word_counts) / len(word_counts)

        # High variance indicates inconsistent pacing
        if variance > avg_words * 0.5:
            return PacingType.INCONSISTENT
        elif variance < avg_words * 0.1:
            return PacingType.VARIABLE
        elif avg_words > 3000:
            return PacingType.SLOW
        else:
            return PacingType.FAST

    def _detect_missing_transitions(self, chapters: List[ChapterAnalysis], parsed: ParsedText) -> List[Dict[str, Any]]:
        """Detect missing transitions between chapters"""
        missing_transitions = []

        for i in range(len(chapters) - 1):
            current_chapter = chapters[i]
            next_chapter = chapters[i + 1]

            # Check for transition keywords at chapter boundaries
            transition_found = False
            boundary_content = parsed.chapters[i]['content'][-500:] + parsed.chapters[i + 1]['content'][:500]

            for keyword in self.transition_keywords:
                if keyword.lower() in boundary_content.lower():
                    transition_found = True
                    break

            if not transition_found:
                # Check if themes or characters changed dramatically
                theme_overlap = set(current_chapter.themes_present) & set(next_chapter.themes_present)
                character_overlap = set(current_chapter.characters_active) & set(next_chapter.characters_active)

                if len(theme_overlap) == 0 or len(character_overlap) == 0:
                    missing_transitions.append({
                        'between_chapters': f"{i + 1} → {i + 2}",
                        'reason': 'abrupt_theme_change' if len(theme_overlap) == 0 else 'character_discontinuity',
                        'severity': 'high'
                    })

        return missing_transitions

    def _identify_structural_issues(self, chapters: List[ChapterAnalysis], parsed: ParsedText) -> List[str]:
        """Identify structural problems in the story"""
        issues = []

        # Check chapter length consistency
        word_counts = [c.word_count for c in chapters]
        avg_length = sum(word_counts) / len(word_counts)
        for i, count in enumerate(word_counts):
            if count < avg_length * 0.3:
                issues.append(f"Chapter {i + 1} is unusually short ({count} words vs avg {avg_length:.0f})")
            elif count > avg_length * 2.5:
                issues.append(f"Chapter {i + 1} is unusually long ({count} words vs avg {avg_length:.0f})")

        # Check dialogue balance
        dialogue_ratios = [c.dialogue_ratio for c in chapters]
        avg_dialogue = sum(dialogue_ratios) / len(dialogue_ratios)
        for i, ratio in enumerate(dialogue_ratios):
            if ratio > avg_dialogue * 2:
                issues.append(f"Chapter {i + 1} has excessive dialogue ({ratio:.1%} vs avg {avg_dialogue:.1%})")

        # Check character distribution
        all_characters = set()
        for chapter in chapters:
            all_characters.update(chapter.characters_active)

        for character in all_characters:
            appearances = sum(1 for c in chapters if character in c.characters_active)
            if appearances == 1:
                issues.append(f"Character '{character}' only appears in one chapter - consider developing further")

        return issues

    def _generate_improvement_suggestions(self, chapters: List[ChapterAnalysis], parsed: ParsedText) -> List[str]:
        """Generate specific improvement suggestions"""
        suggestions = []

        # Arc-based suggestions
        arc = self._detect_overall_arc(chapters)
        if arc == ArcType.FLAT:
            suggestions.append("Consider adding more conflict to create a clearer narrative arc")
        elif arc == ArcType.RISING:
            suggestions.append("Strong rising arc - ensure the climax provides satisfying resolution")

        # Pacing suggestions
        pacing = self._analyze_pacing(chapters)
        if pacing == PacingType.INCONSISTENT:
            suggestions.append("Work on consistent chapter lengths to improve pacing flow")
        elif pacing == PacingType.FAST:
            suggestions.append("Consider slowing down key moments with more descriptive passages")

        # Character development suggestions
        character_counts = [len(c.characters_active) for c in chapters]
        if max(character_counts) > 5:
            suggestions.append("Too many characters introduced at once - consider spacing out introductions")

        # Theme development
        theme_counts = [len(c.themes_present) for c in chapters]
        if sum(theme_counts) < len(chapters) * 2:
            suggestions.append("Consider deepening thematic exploration throughout the story")

        return suggestions

    def _calculate_narrative_flow_score(self, chapters: List[ChapterAnalysis], parsed: ParsedText) -> float:
        """Calculate overall narrative flow score (0-1)"""
        if len(chapters) < 2:
            return 0.5

        score = 1.0

        # Penalize for missing transitions
        missing_transitions = len(self._detect_missing_transitions(chapters, parsed))
        score -= missing_transitions * 0.1

        # Penalize for structural issues
        structural_issues = len(self._identify_structural_issues(chapters, parsed))
        score -= structural_issues * 0.05

        # Penalize for pacing inconsistency
        pacing = self._analyze_pacing(chapters)
        if pacing == PacingType.INCONSISTENT:
            score -= 0.2

        # Reward for good arc development
        arc = self._detect_overall_arc(chapters)
        if arc in [ArcType.RISING, ArcType.COMPLEX]:
            score += 0.1

        return max(0.0, min(1.0, score))

    def _find_line_number(self, text: str, parsed: ParsedText) -> int:
        """Find which line number a piece of text appears in"""
        # Simple approximation - count newlines
        return text.count('\n')

    def _sentence_in_chapter(self, sentence_index: int, chapter_sentences: List[str], chapter_data: Dict[str, Any]) -> bool:
        """Check if a sentence index falls within a chapter"""
        # This is a simplified check - in practice you'd need more sophisticated tracking
        return True

    def _extract_chapter_themes(self, content: str, global_themes: List[str]) -> List[str]:
        """Extract themes present in chapter content"""
        content_lower = content.lower()
        return [theme for theme in global_themes if theme in content_lower]

    def _extract_chapter_characters(self, content: str, global_characters: List[str]) -> List[str]:
        """Extract characters active in chapter content"""
        content_lower = content.lower()
        return [char for char in global_characters if char.lower() in content_lower]

# Convenience function
def analyze_structure(text: str) -> StructuralAnalysis:
    """Quick structural analysis function"""
    engine = StructuralEngine()
    return engine.analyze(text)