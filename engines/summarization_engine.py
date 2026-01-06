# engines/summarization_engine.py
"""
GOAT Summarization Engine - Intelligent Text Compression
Phase 1, Module 3: Compresses text at multiple scales with different focuses

Provides 1-sentence, 1-paragraph, 3-layer abstraction, theme-focused,
TikTok-ready, and SEO summaries.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
from collections import Counter, defaultdict
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from .deep_parser import DeepParser, ParsedText

class SummaryType(Enum):
    """Types of summaries available"""
    ONE_SENTENCE = "one_sentence"
    ONE_PARAGRAPH = "one_paragraph"
    THREE_LAYER = "three_layer"
    THEME_FOCUSED = "theme_focused"
    TIKTOK_READY = "tiktok_ready"
    SEO_OPTIMIZED = "seo_optimized"

@dataclass
class SummaryResult:
    """Container for summarization results"""
    summary_type: SummaryType
    content: str
    word_count: int
    key_points: List[str]
    compression_ratio: float
    readability_score: float

@dataclass
class MultiScaleSummary:
    """Complete multi-scale summarization"""
    one_sentence: SummaryResult
    one_paragraph: SummaryResult
    three_layer: Dict[str, SummaryResult]
    theme_focused: Dict[str, SummaryResult]
    tiktok_ready: SummaryResult
    seo_optimized: SummaryResult
    metadata: Dict[str, Any]

class SummarizationEngine:
    """
    GOAT's intelligent summarization engine - compresses text at multiple scales
    """

    def __init__(self):
        self.deep_parser = DeepParser()

        # Download required NLTK data
        try:
            nltk.data.find('stopwords')
        except LookupError:
            nltk.download('stopwords')

        self.stop_words = set(stopwords.words('english'))

        # Summary length targets
        self.targets = {
            SummaryType.ONE_SENTENCE: 25,  # words
            SummaryType.ONE_PARAGRAPH: 100,  # words
            SummaryType.TIKTOK_READY: 50,  # words
            SummaryType.SEO_OPTIMIZED: 150,  # words
        }

    def summarize_all(self, text: str) -> MultiScaleSummary:
        """
        Generate all types of summaries for the text
        """
        parsed = self.deep_parser.parse(text)

        # Generate all summary types
        one_sentence = self._generate_one_sentence_summary(parsed)
        one_paragraph = self._generate_one_paragraph_summary(parsed)
        three_layer = self._generate_three_layer_summary(parsed)
        theme_focused = self._generate_theme_focused_summaries(parsed)
        tiktok_ready = self._generate_tiktok_ready_summary(parsed)
        seo_optimized = self._generate_seo_optimized_summary(parsed)

        # Calculate metadata
        metadata = {
            'original_word_count': parsed.metadata['word_count'],
            'original_sentence_count': parsed.metadata['sentence_count'],
            'compression_achieved': True,
            'themes_covered': len(theme_focused),
            'readability_scores': {
                'one_sentence': one_sentence.readability_score,
                'one_paragraph': one_paragraph.readability_score,
                'tiktok_ready': tiktok_ready.readability_score,
                'seo_optimized': seo_optimized.readability_score
            }
        }

        return MultiScaleSummary(
            one_sentence=one_sentence,
            one_paragraph=one_paragraph,
            three_layer=three_layer,
            theme_focused=theme_focused,
            tiktok_ready=tiktok_ready,
            seo_optimized=seo_optimized,
            metadata=metadata
        )

    def _generate_one_sentence_summary(self, parsed: ParsedText) -> SummaryResult:
        """Generate a one-sentence summary"""
        # Extract the most important sentence based on criteria
        sentences = parsed.sentences
        if not sentences:
            return SummaryResult(
                summary_type=SummaryType.ONE_SENTENCE,
                content="No content to summarize.",
                word_count=4,
                key_points=[],
                compression_ratio=1.0,
                readability_score=0.0
            )

        # Score sentences by importance
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = self._score_sentence_importance(sentence, parsed, i)
            sentence_scores.append((score, sentence))

        # Get the highest scoring sentence
        best_sentence = max(sentence_scores, key=lambda x: x[0])[1]

        # Trim to target length if needed
        words = best_sentence.split()
        if len(words) > self.targets[SummaryType.ONE_SENTENCE]:
            words = words[:self.targets[SummaryType.ONE_SENTENCE]]
            best_sentence = ' '.join(words) + '...'

        return SummaryResult(
            summary_type=SummaryType.ONE_SENTENCE,
            content=best_sentence,
            word_count=len(best_sentence.split()),
            key_points=[best_sentence],
            compression_ratio=len(best_sentence.split()) / parsed.metadata['word_count'],
            readability_score=self._calculate_readability(best_sentence)
        )

    def _generate_one_paragraph_summary(self, parsed: ParsedText) -> SummaryResult:
        """Generate a one-paragraph summary"""
        # Extract key elements
        main_characters = parsed.characters[:3]  # Top 3 characters
        main_themes = parsed.themes[:2]  # Top 2 themes
        key_events = self._extract_key_events(parsed)

        # Build summary paragraph
        parts = []

        if main_characters:
            parts.append(f"This story follows {', '.join(main_characters)}")

        if main_themes:
            parts.append(f"exploring themes of {', '.join(main_themes)}")

        if key_events:
            parts.append(f"through {key_events[0]}")

        summary = '. '.join(parts) + '.'

        # Ensure it's within word limit
        words = summary.split()
        if len(words) > self.targets[SummaryType.ONE_PARAGRAPH]:
            words = words[:self.targets[SummaryType.ONE_PARAGRAPH]]
            summary = ' '.join(words) + '...'

        return SummaryResult(
            summary_type=SummaryType.ONE_PARAGRAPH,
            content=summary,
            word_count=len(summary.split()),
            key_points=[summary],
            compression_ratio=len(summary.split()) / parsed.metadata['word_count'],
            readability_score=self._calculate_readability(summary)
        )

    def _generate_three_layer_summary(self, parsed: ParsedText) -> Dict[str, SummaryResult]:
        """Generate three-layer abstraction: micro, meso, macro"""
        summaries = {}

        # Micro: Sentence-level details
        micro_content = self._extract_micro_level(parsed)
        summaries['micro'] = SummaryResult(
            summary_type=SummaryType.THREE_LAYER,
            content=micro_content,
            word_count=len(micro_content.split()),
            key_points=self._extract_key_sentences(parsed, 3),
            compression_ratio=0.3,
            readability_score=self._calculate_readability(micro_content)
        )

        # Meso: Chapter-level overview
        meso_content = self._extract_meso_level(parsed)
        summaries['meso'] = SummaryResult(
            summary_type=SummaryType.THREE_LAYER,
            content=meso_content,
            word_count=len(meso_content.split()),
            key_points=self._extract_chapter_summaries(parsed),
            compression_ratio=0.2,
            readability_score=self._calculate_readability(meso_content)
        )

        # Macro: Story-level arc
        macro_content = self._extract_macro_level(parsed)
        summaries['macro'] = SummaryResult(
            summary_type=SummaryType.THREE_LAYER,
            content=macro_content,
            word_count=len(macro_content.split()),
            key_points=self._extract_story_arc(parsed),
            compression_ratio=0.1,
            readability_score=self._calculate_readability(macro_content)
        )

        return summaries

    def _generate_theme_focused_summaries(self, parsed: ParsedText) -> Dict[str, SummaryResult]:
        """Generate theme-focused summaries"""
        summaries = {}

        for theme in parsed.themes:
            theme_sentences = []
            for i, sentence in enumerate(parsed.sentences):
                if theme.lower() in sentence.lower():
                    theme_sentences.append(sentence)

            if theme_sentences:
                # Combine top theme sentences
                theme_content = ' '.join(theme_sentences[:3])
                summaries[theme] = SummaryResult(
                    summary_type=SummaryType.THEME_FOCUSED,
                    content=theme_content,
                    word_count=len(theme_content.split()),
                    key_points=theme_sentences[:3],
                    compression_ratio=len(theme_content.split()) / parsed.metadata['word_count'],
                    readability_score=self._calculate_readability(theme_content)
                )

        return summaries

    def _generate_tiktok_ready_summary(self, parsed: ParsedText) -> SummaryResult:
        """Generate TikTok-ready hook + summary"""
        # Create engaging, short summary
        hook = self._create_hook(parsed)
        key_points = self._extract_key_sentences(parsed, 2)
        call_to_action = "What happens next? #StoryTime #BookTok"

        content = f"{hook} {key_points[0]} {call_to_action}"

        return SummaryResult(
            summary_type=SummaryType.TIKTOK_READY,
            content=content,
            word_count=len(content.split()),
            key_points=key_points,
            compression_ratio=len(content.split()) / parsed.metadata['word_count'],
            readability_score=self._calculate_readability(content)
        )

    def _generate_seo_optimized_summary(self, parsed: ParsedText) -> SummaryResult:
        """Generate SEO-optimized summary with keywords"""
        # Extract key entities and themes for SEO
        keywords = parsed.characters + parsed.themes
        main_character = parsed.characters[0] if parsed.characters else "character"
        main_theme = parsed.themes[0] if parsed.themes else "story"

        content = f"Discover this compelling {main_theme} story following {main_character}. " \
                 f"Explore themes of {', '.join(parsed.themes[:3])}. " \
                 f"A {len(parsed.sentences)}-sentence journey through {len(parsed.chapters)} chapters."

        return SummaryResult(
            summary_type=SummaryType.SEO_OPTIMIZED,
            content=content,
            word_count=len(content.split()),
            key_points=[f"Features {main_character}", f"Explores {main_theme}"],
            compression_ratio=len(content.split()) / parsed.metadata['word_count'],
            readability_score=self._calculate_readability(content)
        )

    def _score_sentence_importance(self, sentence: str, parsed: ParsedText, index: int) -> float:
        """Score sentence importance for extraction"""
        score = 0.0

        # Length factor (prefer medium-length sentences)
        words = sentence.split()
        if 10 <= len(words) <= 30:
            score += 0.3
        elif len(words) > 30:
            score += 0.1

        # Character mentions
        for character in parsed.characters:
            if character.lower() in sentence.lower():
                score += 0.2

        # Theme mentions
        for theme in parsed.themes:
            if theme.lower() in sentence.lower():
                score += 0.15

        # Dialogue bonus
        if '"' in sentence or "'" in sentence:
            score += 0.1

        # Position bonus (earlier sentences slightly preferred)
        position_factor = 1.0 - (index / len(parsed.sentences)) * 0.2
        score *= position_factor

        return score

    def _extract_key_events(self, parsed: ParsedText) -> List[str]:
        """Extract key events from the story"""
        events = []

        # Look for sentences with action verbs or emotional content
        action_verbs = ['fought', 'loved', 'died', 'won', 'lost', 'discovered', 'learned']

        for sentence in parsed.sentences[:10]:  # Focus on beginning
            for verb in action_verbs:
                if verb in sentence.lower():
                    events.append(sentence)
                    break

        return events[:3]  # Top 3 events

    def _extract_micro_level(self, parsed: ParsedText) -> str:
        """Extract micro-level details (sentence-level)"""
        key_sentences = self._extract_key_sentences(parsed, 5)
        return ' '.join(key_sentences)

    def _extract_meso_level(self, parsed: ParsedText) -> str:
        """Extract meso-level overview (chapter-level)"""
        chapter_summaries = []
        for chapter in parsed.chapters:
            # Simple chapter summary
            words = chapter['content'].split()[:50]  # First 50 words
            summary = ' '.join(words) + '...'
            chapter_summaries.append(f"Chapter {chapter['number']}: {summary}")

        return ' '.join(chapter_summaries)

    def _extract_macro_level(self, parsed: ParsedText) -> str:
        """Extract macro-level arc (story-level)"""
        characters = ', '.join(parsed.characters[:3])
        themes = ', '.join(parsed.themes[:2])
        chapters = len(parsed.chapters)

        return f"This {chapters}-chapter story follows {characters} as they explore {themes}."

    def _extract_key_sentences(self, parsed: ParsedText, count: int) -> List[str]:
        """Extract top N key sentences"""
        sentence_scores = []
        for i, sentence in enumerate(parsed.sentences):
            score = self._score_sentence_importance(sentence, parsed, i)
            sentence_scores.append((score, sentence))

        # Sort by score and return top sentences
        sentence_scores.sort(key=lambda x: x[0], reverse=True)
        return [sentence for score, sentence in sentence_scores[:count]]

    def _extract_chapter_summaries(self, parsed: ParsedText) -> List[str]:
        """Extract chapter-level summaries"""
        summaries = []
        for chapter in parsed.chapters:
            # Get first few sentences from each chapter
            content = chapter['content']
            sentences = content.split('.')[:2]  # First 2 sentences
            summary = '. '.join(sentences).strip()
            if summary:
                summaries.append(f"Chapter {chapter['number']}: {summary}.")
        return summaries[:3]  # Top 3 chapters

    def _extract_story_arc(self, parsed: ParsedText) -> List[str]:
        """Extract story arc elements"""
        return [
            f"Introduces {', '.join(parsed.characters[:2])}",
            f"Explores {', '.join(parsed.themes[:2])}",
            f"Spans {len(parsed.chapters)} chapters"
        ]

    def _create_hook(self, parsed: ParsedText) -> str:
        """Create an engaging hook for social media"""
        if parsed.characters:
            return f"What happens when {parsed.characters[0]} faces their greatest challenge?"
        elif parsed.themes:
            return f"A powerful story about {parsed.themes[0]}..."
        else:
            return "An unforgettable story begins..."

    def _calculate_readability(self, text: str) -> float:
        """Calculate simple readability score (0-1)"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not words or not sentences:
            return 0.0

        avg_words_per_sentence = len(words) / len(sentences)
        avg_syllables_per_word = sum(self._count_syllables(word) for word in words) / len(words)

        # Simple readability formula (lower is easier to read)
        score = 0.39 * avg_words_per_sentence + 11.8 * avg_syllables_per_word - 15.59

        # Convert to 0-1 scale (lower score = higher readability)
        readability = max(0, min(1, 1 - (score / 20)))
        return readability

    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simple approximation)"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"

        if word[0] in vowels:
            count += 1

        for i in range(1, len(word)):
            if word[i] in vowels and word[i - 1] not in vowels:
                count += 1

        if word.endswith("e"):
            count -= 1

        return max(1, count)

# Convenience function
def summarize_text(text: str) -> MultiScaleSummary:
    """Quick summarization function"""
    engine = SummarizationEngine()
    return engine.summarize_all(text)