# engines/deep_parser.py
"""
GOAT Deep Parser - Core Text Processing Engine
Phase 1, Module 1: Foundation for all GOAT intelligence

Tears raw text into usable components for higher-level processing.
"""

import re
import nltk
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import spacy
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

@dataclass
class ParsedText:
    """Container for fully parsed text components"""
    sentences: List[str]
    paragraphs: List[str]
    chapters: List[Dict[str, Any]]
    dialogues: List[Dict[str, Any]]
    characters: List[str]
    themes: List[str]
    emotions: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class DeepParser:
    """
    GOAT's foundation engine - breaks down raw text into structured components
    """

    def __init__(self):
        # Initialize NLP models
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if spaCy model not available
            self.nlp = None

        # Emotion word lists
        self.emotion_words = {
            'joy': ['happy', 'joyful', 'delighted', 'excited', 'thrilled', 'ecstatic'],
            'sadness': ['sad', 'unhappy', 'depressed', 'miserable', 'gloomy', 'heartbroken'],
            'anger': ['angry', 'furious', 'enraged', 'irritated', 'annoyed', 'frustrated'],
            'fear': ['afraid', 'scared', 'terrified', 'anxious', 'nervous', 'frightened'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'startled'],
            'disgust': ['disgusted', 'repulsed', 'revolted', 'nauseated', 'sickened'],
            'love': ['love', 'affection', 'adoration', 'fondness', 'tenderness', 'passion'],
            'trust': ['trust', 'confidence', 'faith', 'belief', 'reliance', 'assurance']
        }

        # Theme keywords
        self.theme_keywords = {
            'love': ['love', 'romance', 'passion', 'affection', 'heart', 'desire'],
            'death': ['death', 'die', 'dying', 'dead', 'mortality', 'end', 'final'],
            'war': ['war', 'battle', 'fight', 'combat', 'soldier', 'army', 'conflict'],
            'peace': ['peace', 'calm', 'tranquil', 'serene', 'harmony', 'quiet'],
            'power': ['power', 'control', 'authority', 'dominance', 'strength', 'might'],
            'freedom': ['freedom', 'liberty', 'independent', 'free', 'autonomy'],
            'justice': ['justice', 'fair', 'righteous', 'equality', 'law', 'moral'],
            'betrayal': ['betray', 'treason', 'deceive', 'lie', 'disloyal', 'traitor']
        }

    def parse(self, text: str) -> ParsedText:
        """
        Main parsing function - breaks down text into all components
        """
        # Basic text cleaning
        text = self._clean_text(text)

        # Parse all components
        sentences = self._split_sentences(text)
        paragraphs = self._split_paragraphs(text)
        chapters = self._detect_chapters(text)
        dialogues = self._extract_dialogues(text)
        characters = self._find_characters(text)
        themes = self._extract_themes(text)
        emotions = self._analyze_emotions(text)
        timeline = self._extract_timeline(text)

        # Calculate metadata
        metadata = {
            'word_count': len(text.split()),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'chapter_count': len(chapters),
            'character_count': len(characters),
            'dialogue_count': len(dialogues),
            'theme_count': len(themes),
            'emotion_count': len(emotions),
            'timeline_events': len(timeline),
            'parsed_at': datetime.utcnow().isoformat()
        }

        return ParsedText(
            sentences=sentences,
            paragraphs=paragraphs,
            chapters=chapters,
            dialogues=dialogues,
            characters=characters,
            themes=themes,
            emotions=emotions,
            timeline=timeline,
            metadata=metadata
        )

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        # Normalize quotes
        text = re.sub(r'["""]', '"', text)
        text = re.sub(r"[''']", "'", text)
        return text.strip()

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        try:
            return nltk.sent_tokenize(text)
        except:
            # Fallback sentence splitting
            sentences = re.split(r'(?<=[.!?])\s+', text)
            return [s.strip() for s in sentences if s.strip()]

    def _split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]

    def _detect_chapters(self, text: str) -> List[Dict[str, Any]]:
        """Detect chapter boundaries and extract chapter info"""
        chapters = []

        # Common chapter patterns
        chapter_patterns = [
            r'Chapter\s+(\d+)',
            r'CHAPTER\s+(\d+)',
            r'Chapter\s+([IVXLCDM]+)',  # Roman numerals
            r'CHAPTER\s+([IVXLCDM]+)',
            r'Part\s+(\d+)',
            r'PART\s+(\d+)',
            r'Book\s+(\d+)',
            r'BOOK\s+(\d+)'
        ]

        lines = text.split('\n')
        current_chapter = None
        chapter_start = 0

        for i, line in enumerate(lines):
            line = line.strip()

            for pattern in chapter_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    # Save previous chapter if exists
                    if current_chapter:
                        chapters.append({
                            'title': current_chapter,
                            'number': len(chapters) + 1,
                            'start_line': chapter_start,
                            'end_line': i - 1,
                            'content': '\n'.join(lines[chapter_start:i])
                        })

                    current_chapter = line
                    chapter_start = i
                    break

        # Add final chapter
        if current_chapter:
            chapters.append({
                'title': current_chapter,
                'number': len(chapters) + 1,
                'start_line': chapter_start,
                'end_line': len(lines) - 1,
                'content': '\n'.join(lines[chapter_start:])
            })

        # If no chapters detected, treat whole text as one chapter
        if not chapters:
            chapters.append({
                'title': 'Chapter 1',
                'number': 1,
                'start_line': 0,
                'end_line': len(lines) - 1,
                'content': text
            })

        return chapters

    def _extract_dialogues(self, text: str) -> List[Dict[str, Any]]:
        """Extract dialogue segments with speaker attribution"""
        dialogues = []

        # Pattern for dialogue: "Quote" he/she said
        dialogue_pattern = r'["""]((?:\\.|[^"\\])*)["""]\s*([^.!?]*[.!?])'

        matches = re.findall(dialogue_pattern, text, re.MULTILINE | re.DOTALL)

        for quote, attribution in matches:
            # Try to extract speaker from attribution
            speaker_match = re.search(r'(\w+)\s+said', attribution, re.IGNORECASE)
            speaker = speaker_match.group(1) if speaker_match else 'Unknown'

            dialogues.append({
                'speaker': speaker,
                'quote': quote.strip(),
                'attribution': attribution.strip(),
                'context': f'"{quote}" {attribution}'
            })

        # Also try alternative patterns
        alt_patterns = [
            r'"([^"]*)"\s*said\s+(\w+)',
            r"'([^']*)'\s*said\s+(\w+)",
            r'"([^"]*)"\s*(\w+)\s+said',
            r"'([^']*)'\s*(\w+)\s+said"
        ]

        for pattern in alt_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    quote, speaker = match
                    dialogues.append({
                        'speaker': speaker,
                        'quote': quote.strip(),
                        'attribution': f'{speaker} said',
                        'context': f'"{quote}" said {speaker}'
                    })

        return dialogues

    def _find_characters(self, text: str) -> List[str]:
        """Find character names in text"""
        characters = set()

        if self.nlp:
            # Use spaCy for named entity recognition
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    characters.add(ent.text)
        else:
            # Fallback: look for capitalized words that might be names
            words = re.findall(r'\b[A-Z][a-z]+\b', text)
            # Filter out common non-name words and chapter headers
            common_words = {
                'The', 'This', 'That', 'What', 'When', 'Where', 'Why', 'How',
                'And', 'But', 'Or', 'For', 'With', 'From', 'Chapter', 'Part',
                'Book', 'Section', 'Volume', 'Act', 'Scene'
            }
            potential_names = [word for word in words if word not in common_words]

            # Count frequency and keep most common potential names
            name_counts = Counter(potential_names)
            characters = [name for name, count in name_counts.most_common(20) if count > 1]

        return list(characters)

    def _extract_themes(self, text: str) -> List[str]:
        """Extract thematic keywords and concepts"""
        found_themes = set()
        text_lower = text.lower()

        for theme, keywords in self.theme_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_themes.add(theme)
                    break

        return list(found_themes)

    def _analyze_emotions(self, text: str) -> List[Dict[str, Any]]:
        """Analyze emotional content throughout the text"""
        emotions_found = []
        sentences = self._split_sentences(text)

        for i, sentence in enumerate(sentences):
            sentence_emotions = []
            sentence_lower = sentence.lower()

            for emotion, words in self.emotion_words.items():
                for word in words:
                    if word in sentence_lower:
                        sentence_emotions.append(emotion)
                        break

            if sentence_emotions:
                emotions_found.append({
                    'sentence_index': i,
                    'sentence': sentence,
                    'emotions': list(set(sentence_emotions)),
                    'intensity': len(sentence_emotions)
                })

        return emotions_found

    def _extract_timeline(self, text: str) -> List[Dict[str, Any]]:
        """Extract timeline events (dates, ages, locations)"""
        timeline_events = []

        # Date patterns
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # MM/DD/YYYY
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # MM-DD-YYYY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{4}\b'  # Years
        ]

        # Age patterns
        age_patterns = [
            r'\b(\d{1,2})\s*(?:years?\s*)?(?:old|years?\s*old)\b',
            r'\bage\s*(\d{1,2})\b'
        ]

        # Location patterns (basic)
        location_patterns = [
            r'\b(?:in|at|from|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        ]

        # Find dates
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                timeline_events.append({
                    'type': 'date',
                    'value': match,
                    'context': self._get_context(text, match)
                })

        # Find ages
        for pattern in age_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                age = match[0] if isinstance(match, tuple) else match
                timeline_events.append({
                    'type': 'age',
                    'value': age,
                    'context': self._get_context(text, age)
                })

        # Find locations
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                timeline_events.append({
                    'type': 'location',
                    'value': match,
                    'context': self._get_context(text, match)
                })

        return timeline_events

    def _get_context(self, text: str, target: str, context_chars: int = 50) -> str:
        """Get surrounding context for a found element"""
        index = text.find(target)
        if index == -1:
            return ""

        start = max(0, index - context_chars)
        end = min(len(text), index + len(target) + context_chars)

        context = text[start:end]
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."

        return context

# Convenience function for quick parsing
def parse_text(text: str) -> ParsedText:
    """Quick parsing function"""
    parser = DeepParser()
    return parser.parse(text)