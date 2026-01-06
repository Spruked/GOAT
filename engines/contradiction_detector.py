# engines/contradiction_detector.py
"""
GOAT Contradiction Detector - Intelligent Consistency Checker
Phase 1, Module 4: Detects logical inconsistencies in stories

Checks for:
- Character logic contradictions
- Timeline alignment issues
- Thematic conflicts
- Plot hole identification
- Internal consistency validation
"""

from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import re
from collections import defaultdict, Counter
from datetime import datetime

from .deep_parser import DeepParser, ParsedText

class ContradictionType(Enum):
    """Types of contradictions that can be detected"""
    CHARACTER_LOGIC = "character_logic"
    TIMELINE_INCONSISTENCY = "timeline_inconsistency"
    THEMATIC_CONFLICT = "thematic_conflict"
    PLOT_HOLE = "plot_hole"
    FACTUAL_ERROR = "factual_error"
    INTERNAL_INCONSISTENCY = "internal_inconsistency"

class Severity(Enum):
    """Severity levels for contradictions"""
    CRITICAL = "critical"  # Breaks story logic completely
    MAJOR = "major"        # Significant plot issue
    MINOR = "minor"        # Small inconsistency
    WARNING = "warning"    # Potential issue to review

@dataclass
class Contradiction:
    """Represents a detected contradiction"""
    type: ContradictionType
    severity: Severity
    description: str
    location: str  # Chapter/sentence reference
    evidence: List[str]  # Supporting evidence
    suggestion: str  # How to fix it
    confidence: float  # 0-1 confidence score

@dataclass
class ConsistencyReport:
    """Complete consistency analysis report"""
    overall_score: float  # 0-1, higher is more consistent
    contradictions: List[Contradiction]
    character_consistency: Dict[str, float]
    timeline_validity: bool
    thematic_coherence: float
    plot_holes: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any]

class ContradictionDetector:
    """
    GOAT's intelligent contradiction detector - finds logical inconsistencies
    """

    def __init__(self):
        self.deep_parser = DeepParser()

        # Character trait keywords
        self.trait_keywords = {
            'brave': ['cowardly', 'fearful', 'timid'],
            'honest': ['deceitful', 'lying', 'dishonest'],
            'intelligent': ['stupid', 'foolish', 'dumb'],
            'kind': ['cruel', 'mean', 'harsh'],
            'strong': ['weak', 'feeble', 'fragile'],
            'loyal': ['traitorous', 'disloyal', 'betraying']
        }

        # Timeline keywords
        self.temporal_keywords = [
            'before', 'after', 'during', 'while', 'when', 'then',
            'yesterday', 'today', 'tomorrow', 'now', 'later', 'earlier',
            'first', 'next', 'finally', 'last', 'previously'
        ]

    def analyze_consistency(self, text: str) -> ConsistencyReport:
        """
        Perform complete consistency analysis on the text
        """
        parsed = self.deep_parser.parse(text)

        # Run all detection methods
        contradictions = []
        contradictions.extend(self._detect_character_contradictions(parsed))
        contradictions.extend(self._detect_timeline_issues(parsed))
        contradictions.extend(self._detect_thematic_conflicts(parsed))
        contradictions.extend(self._detect_plot_holes(parsed))
        contradictions.extend(self._detect_internal_inconsistencies(parsed))

        # Calculate scores
        character_consistency = self._calculate_character_consistency(parsed)
        timeline_validity = self._validate_timeline(parsed)
        thematic_coherence = self._calculate_thematic_coherence(parsed)

        # Overall score (weighted average)
        weights = {
            'character': 0.3,
            'timeline': 0.3,
            'thematic': 0.2,
            'contradictions': 0.2
        }

        char_score = sum(character_consistency.values()) / len(character_consistency) if character_consistency else 1.0
        timeline_score = 1.0 if timeline_validity else 0.0
        contradiction_penalty = min(1.0, len(contradictions) / 10.0)  # Penalty for contradictions

        overall_score = (
            weights['character'] * char_score +
            weights['timeline'] * timeline_score +
            weights['thematic'] * thematic_coherence +
            weights['contradictions'] * (1.0 - contradiction_penalty)
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(contradictions, parsed)

        return ConsistencyReport(
            overall_score=overall_score,
            contradictions=contradictions,
            character_consistency=character_consistency,
            timeline_validity=timeline_validity,
            thematic_coherence=thematic_coherence,
            plot_holes=self._extract_plot_holes(contradictions),
            recommendations=recommendations,
            metadata={
                'total_contradictions': len(contradictions),
                'characters_analyzed': len(character_consistency),
                'chapters_analyzed': len(parsed.chapters),
                'analysis_timestamp': datetime.now().isoformat()
            }
        )

    def _detect_character_contradictions(self, parsed: ParsedText) -> List[Contradiction]:
        """Detect contradictions in character behavior and traits"""
        contradictions = []

        for character in parsed.characters:
            char_sentences = []
            for i, sentence in enumerate(parsed.sentences):
                if character.lower() in sentence.lower():
                    char_sentences.append((i, sentence))

            if len(char_sentences) < 2:
                continue

            # Check for trait contradictions
            traits_found = defaultdict(list)
            for idx, sentence in char_sentences:
                for trait, opposites in self.trait_keywords.items():
                    if trait in sentence.lower():
                        traits_found[trait].append((idx, sentence))
                    for opposite in opposites:
                        if opposite in sentence.lower():
                            traits_found[trait].append((idx, sentence, 'opposite'))

            # Find contradictions
            for trait, occurrences in traits_found.items():
                if len(occurrences) > 1:
                    opposites = [occ for occ in occurrences if len(occ) > 2]
                    if opposites:
                        contradictions.append(Contradiction(
                            type=ContradictionType.CHARACTER_LOGIC,
                            severity=Severity.MAJOR,
                            description=f"Character {character} shows contradictory traits around '{trait}'",
                            location=f"Sentences {occurrences[0][0]}-{occurrences[-1][0]}",
                            evidence=[occ[1] for occ in occurrences],
                            suggestion=f"Clarify {character}'s personality or justify the trait change",
                            confidence=0.8
                        ))

        return contradictions

    def _detect_timeline_issues(self, parsed: ParsedText) -> List[Contradiction]:
        """Detect timeline inconsistencies"""
        contradictions = []

        # Extract timeline events
        timeline_events = []
        for i, sentence in enumerate(parsed.sentences):
            # Look for temporal markers
            has_temporal = any(word in sentence.lower() for word in self.temporal_keywords)
            if has_temporal:
                timeline_events.append((i, sentence))

        # Check for obvious timeline breaks
        for i in range(len(timeline_events) - 1):
            current = timeline_events[i][1].lower()
            next_event = timeline_events[i + 1][1].lower()

            # Simple contradiction detection
            if 'died' in current and 'later' in next_event:
                contradictions.append(Contradiction(
                    type=ContradictionType.TIMELINE_INCONSISTENCY,
                    severity=Severity.CRITICAL,
                    description="Character death followed by later actions",
                    location=f"Sentences {timeline_events[i][0]}-{timeline_events[i+1][0]}",
                    evidence=[timeline_events[i][1], timeline_events[i+1][1]],
                    suggestion="Remove the 'later' action or clarify resurrection/time travel",
                    confidence=0.9
                ))

        return contradictions

    def _detect_thematic_conflicts(self, parsed: ParsedText) -> List[Contradiction]:
        """Detect conflicts between stated themes and story content"""
        contradictions = []

        themes = parsed.themes
        all_text = ' '.join(parsed.sentences).lower()

        # Check for theme vs content conflicts
        theme_conflicts = {
            'peace': ['war', 'violence', 'battle'],
            'love': ['hate', 'revenge', 'betrayal'],
            'justice': ['corruption', 'injustice', 'crime'],
            'freedom': ['oppression', 'control', 'imprisonment']
        }

        for theme in themes:
            if theme.lower() in theme_conflicts:
                conflicts = theme_conflicts[theme.lower()]
                conflict_found = any(conflict in all_text for conflict in conflicts)

                if conflict_found:
                    contradictions.append(Contradiction(
                        type=ContradictionType.THEMATIC_CONFLICT,
                        severity=Severity.MINOR,
                        description=f"Theme '{theme}' conflicts with story elements",
                        location="Throughout story",
                        evidence=[f"Theme: {theme}", f"Conflicting elements: {', '.join(conflicts)}"],
                        suggestion=f"Strengthen theme integration or resolve the conflict",
                        confidence=0.6
                    ))

        return contradictions

    def _detect_plot_holes(self, parsed: ParsedText) -> List[Contradiction]:
        """Detect plot holes and unexplained elements"""
        contradictions = []

        # Look for unexplained elements
        unexplained_patterns = [
            r'but how',
            r'suddenly',
            r'magically',
            r'out of nowhere',
            r'without explanation',
            r'no one knows why'
        ]

        for i, sentence in enumerate(parsed.sentences):
            for pattern in unexplained_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    contradictions.append(Contradiction(
                        type=ContradictionType.PLOT_HOLE,
                        severity=Severity.WARNING,
                        description="Potentially unexplained plot element",
                        location=f"Sentence {i+1}",
                        evidence=[sentence],
                        suggestion="Add explanation or foreshadowing for this element",
                        confidence=0.5
                    ))

        return contradictions

    def _detect_internal_inconsistencies(self, parsed: ParsedText) -> List[Contradiction]:
        """Detect other internal inconsistencies"""
        contradictions = []

        # Check for repeated contradictory statements
        statement_counts = Counter()
        for sentence in parsed.sentences:
            # Simple statement extraction
            if '"' in sentence:
                statements = re.findall(r'"([^"]*)"', sentence)
                for statement in statements:
                    statement_counts[statement.lower()] += 1

        # Find contradictory statements about the same topic
        for statement, count in statement_counts.items():
            if count > 1:
                # Look for direct contradictions
                words = statement.split()
                if len(words) > 3:  # Only check longer statements
                    contradictions.append(Contradiction(
                        type=ContradictionType.INTERNAL_INCONSISTENCY,
                        severity=Severity.MINOR,
                        description="Potentially repeated or inconsistent statement",
                        location="Multiple locations",
                        evidence=[statement],
                        suggestion="Review for consistency or combine similar statements",
                        confidence=0.4
                    ))

        return contradictions

    def _calculate_character_consistency(self, parsed: ParsedText) -> Dict[str, float]:
        """Calculate consistency scores for each character"""
        consistency_scores = {}

        for character in parsed.characters:
            char_sentences = [s for s in parsed.sentences if character.lower() in s.lower()]

            if len(char_sentences) < 2:
                consistency_scores[character] = 1.0  # No contradictions possible
                continue

            # Simple consistency check based on trait stability
            traits_mentioned = set()
            for sentence in char_sentences:
                for trait in self.trait_keywords.keys():
                    if trait in sentence.lower():
                        traits_mentioned.add(trait)

            # More traits = potentially more complex character (slightly lower consistency)
            trait_complexity = min(1.0, len(traits_mentioned) / 5.0)
            consistency_scores[character] = 1.0 - trait_complexity * 0.3

        return consistency_scores

    def _validate_timeline(self, parsed: ParsedText) -> bool:
        """Validate timeline consistency"""
        # Simple timeline validation
        timeline_events = []

        for sentence in parsed.sentences:
            # Look for time references
            time_patterns = [
                r'\b\d{1,2}:\d{2}\b',  # Time like 3:45
                r'\b\d{4}\b',  # Year
                r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b',
                r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
            ]

            for pattern in time_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    timeline_events.append(sentence)
                    break

        # If we have timeline events, assume they're consistent for now
        # More sophisticated timeline analysis would require NLP
        return len(timeline_events) <= len(parsed.sentences) * 0.5  # Not too many time references

    def _calculate_thematic_coherence(self, parsed: ParsedText) -> float:
        """Calculate how coherent the themes are"""
        if not parsed.themes:
            return 1.0

        # Simple coherence based on theme distribution
        theme_counts = Counter()
        for sentence in parsed.sentences:
            for theme in parsed.themes:
                if theme.lower() in sentence.lower():
                    theme_counts[theme] += 1

        if not theme_counts:
            return 0.5  # Themes mentioned but not found

        # Coherence = how evenly themes are distributed
        total_mentions = sum(theme_counts.values())
        expected_per_theme = total_mentions / len(theme_counts)

        variance = sum((count - expected_per_theme) ** 2 for count in theme_counts.values())
        variance /= len(theme_counts)

        # Convert to coherence score (0-1)
        coherence = max(0, 1 - (variance / (expected_per_theme ** 2)))
        return coherence

    def _extract_plot_holes(self, contradictions: List[Contradiction]) -> List[str]:
        """Extract plot hole descriptions"""
        return [c.description for c in contradictions if c.type == ContradictionType.PLOT_HOLE]

    def _generate_recommendations(self, contradictions: List[Contradiction], parsed: ParsedText) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []

        if contradictions:
            critical_count = sum(1 for c in contradictions if c.severity == Severity.CRITICAL)
            if critical_count > 0:
                recommendations.append(f"Address {critical_count} critical contradictions that break story logic")

        if len(parsed.characters) > 5:
            recommendations.append("Consider reducing character count for better focus")

        if len(parsed.themes) > 3:
            recommendations.append("Limit to 2-3 main themes for stronger narrative coherence")

        if not recommendations:
            recommendations.append("Story structure appears solid - consider adding more character development")

        return recommendations

# Convenience function
def check_consistency(text: str) -> ConsistencyReport:
    """Quick consistency check function"""
    detector = ContradictionDetector()
    return detector.analyze_consistency(text)