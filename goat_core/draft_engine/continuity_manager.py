# goat_core/draft_engine/continuity_manager.py
"""
GOAT Draft Engine - Continuity Manager
Maintains consistency across long-form content generation
"""

import json
import re
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
from datetime import datetime
import hashlib

class ContinuityManager:
    """Manages continuity and consistency across content sections"""

    def __init__(self, continuity_file: str = "continuity_store.json"):
        self.continuity_file = Path(__file__).parent / continuity_file
        self.continuity_data = self._load_continuity_data()

    def _load_continuity_data(self) -> Dict[str, Any]:
        """Load existing continuity data or create new"""
        if self.continuity_file.exists():
            try:
                with open(self.continuity_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Create new continuity structure
        return {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0"
            },
            "key_facts": [],
            "character_details": [],
            "timeline_events": [],
            "themes": [],
            "tone_patterns": [],
            "recurring_phrases": [],
            "relationships": [],
            "locations": [],
            "terminology": {},
            "contradictions": [],
            "section_summaries": []
        }

    def update_from_content(self, section_content: Dict[str, Any]):
        """Update continuity data from newly generated content"""
        content = section_content.get("content", "")
        section_title = section_content.get("section_plan", {}).get("title", "")

        # Extract key information
        facts = self._extract_key_facts(content)
        characters = self._extract_character_details(content)
        events = self._extract_timeline_events(content)
        themes = self._extract_themes(content)
        phrases = self._extract_recurring_phrases(content)
        terms = self._extract_terminology(content)

        # Update continuity data
        self._add_unique_items("key_facts", facts)
        self._add_unique_items("character_details", characters)
        self._add_unique_items("timeline_events", events)
        self._add_unique_items("themes", themes)
        self._add_unique_items("recurring_phrases", phrases)

        # Update terminology
        self.continuity_data["terminology"].update(terms)

        # Add section summary
        section_summary = {
            "title": section_title,
            "word_count": len(content.split()),
            "timestamp": datetime.now().isoformat(),
            "key_points": facts[:3],  # Top 3 facts
            "content_hash": hashlib.md5(content.encode()).hexdigest()
        }
        self.continuity_data["section_summaries"].append(section_summary)

        # Update metadata
        self.continuity_data["metadata"]["last_updated"] = datetime.now().isoformat()

        # Check for contradictions
        self._check_contradictions(content)

        # Save updated data
        self._save_continuity_data()

    def _extract_key_facts(self, content: str) -> List[str]:
        """Extract key factual statements from content"""
        facts = []

        # Look for sentences with strong factual indicators
        sentences = re.split(r'[.!?]+', content)

        fact_indicators = [
            'is', 'are', 'was', 'were', 'has', 'have', 'had',
            'includes', 'contains', 'consists', 'represents',
            'demonstrates', 'shows', 'proves', 'establishes'
        ]

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence.split()) < 5:  # Skip very short sentences
                continue

            # Check if sentence contains fact indicators
            if any(indicator in sentence.lower() for indicator in fact_indicators):
                # Clean and add fact
                fact = re.sub(r'[^\w\s.,-]', '', sentence).strip()
                if len(fact) > 10 and fact not in facts:
                    facts.append(fact)

        return facts[:10]  # Limit to top 10 facts

    def _extract_character_details(self, content: str) -> List[str]:
        """Extract character or person details"""
        details = []

        # Look for proper nouns and associated descriptions
        # This is a simplified implementation
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', content)

        for noun in set(proper_nouns):
            # Find sentences containing this noun
            pattern = rf'([^.!?]*\b{noun}\b[^.!?]*)'
            matches = re.findall(pattern, content, re.IGNORECASE)

            for match in matches[:2]:  # Limit per person
                detail = match.strip()
                if len(detail) > 15 and detail not in details:
                    details.append(f"{noun}: {detail}")

        return details[:5]

    def _extract_timeline_events(self, content: str) -> List[str]:
        """Extract timeline-related events"""
        events = []

        # Look for time-related phrases
        time_indicators = [
            'when', 'after', 'before', 'during', 'since', 'until',
            'first', 'then', 'next', 'later', 'finally', 'initially'
        ]

        sentences = re.split(r'[.!?]+', content)

        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in time_indicators):
                event = sentence.strip()
                if len(event) > 10 and event not in events:
                    events.append(event)

        return events[:5]

    def _extract_themes(self, content: str) -> List[str]:
        """Extract recurring themes"""
        themes = []

        # Common theme words to look for
        theme_words = [
            'growth', 'change', 'success', 'failure', 'learning',
            'development', 'progress', 'challenge', 'opportunity',
            'innovation', 'tradition', 'future', 'past', 'present'
        ]

        content_lower = content.lower()

        for theme in theme_words:
            if theme in content_lower:
                # Count occurrences
                count = content_lower.count(theme)
                if count >= 2:  # Appears multiple times
                    themes.append(theme.title())

        return list(set(themes))[:5]

    def _extract_recurring_phrases(self, content: str) -> List[str]:
        """Extract phrases that appear multiple times"""
        phrases = []

        # Look for 2-4 word phrases that repeat
        words = re.findall(r'\b\w+\b', content.lower())

        for i in range(len(words) - 3):
            phrase = ' '.join(words[i:i+4])
            if len(phrase.split()) >= 2:
                count = content.lower().count(phrase)
                if count >= 2 and len(phrase) > 5:
                    phrases.append(phrase)

        return list(set(phrases))[:5]

    def _extract_terminology(self, content: str) -> Dict[str, str]:
        """Extract technical terms and their definitions"""
        terms = {}

        # Look for patterns like "term (definition)" or "term: definition"
        patterns = [
            r'(\w+)\s*\(([^)]+)\)',
            r'(\w+):\s*([^.!?]+)',
            r'"([^"]+)"\s*means?\s*([^.!?]+)',
            r'(\w+)\s*refers?\s*to\s*([^.!?]+)'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    term, definition = match
                    term = term.strip()
                    definition = definition.strip()
                    if len(term) > 2 and len(definition) > 5:
                        terms[term.lower()] = definition

        return terms

    def _add_unique_items(self, category: str, new_items: List[str]):
        """Add items to continuity data without duplicates"""
        existing = set(self.continuity_data.get(category, []))
        for item in new_items:
            if item not in existing:
                self.continuity_data[category].append(item)
                existing.add(item)

    def _check_contradictions(self, content: str):
        """Check for contradictions with existing continuity"""
        contradictions = []

        # Check against existing facts
        for fact in self.continuity_data.get("key_facts", []):
            # Simple contradiction detection (this could be much more sophisticated)
            if "not" in content.lower() and any(word in content.lower() for word in fact.lower().split()):
                contradictions.append(f"Potential contradiction with established fact: {fact}")

        if contradictions:
            self.continuity_data["contradictions"].extend(contradictions)

    def get_continuity_data(self) -> Dict[str, Any]:
        """Get current continuity data for content generation"""
        return self.continuity_data

    def get_context_for_section(self, section_title: str) -> Dict[str, Any]:
        """Get relevant continuity context for a specific section"""
        return {
            "key_facts": self.continuity_data.get("key_facts", [])[-10:],  # Last 10 facts
            "character_details": self.continuity_data.get("character_details", []),
            "timeline_events": self.continuity_data.get("timeline_events", [])[-5:],
            "themes": self.continuity_data.get("themes", []),
            "recurring_phrases": self.continuity_data.get("recurring_phrases", []),
            "terminology": self.continuity_data.get("terminology", {}),
            "section_summaries": self.continuity_data.get("section_summaries", [])[-3:]  # Last 3 sections
        }

    def validate_continuity(self, content: str) -> Dict[str, Any]:
        """Validate content against continuity requirements"""
        issues = []
        score = 10.0

        # Check if key facts are referenced
        key_facts = self.continuity_data.get("key_facts", [])
        if key_facts:
            referenced_facts = 0
            for fact in key_facts[-5:]:  # Check last 5 facts
                if any(word in content.lower() for word in fact.lower().split()[:3]):
                    referenced_facts += 1

            if referenced_facts == 0:
                score -= 1.0
                issues.append("No reference to established key facts")

        # Check for consistent terminology
        terminology = self.continuity_data.get("terminology", {})
        for term, definition in terminology.items():
            if term in content.lower():
                # Could check if usage is consistent with definition
                pass

        # Check for contradictions
        contradictions = self.continuity_data.get("contradictions", [])
        if contradictions:
            score -= 0.5
            issues.append("Existing contradictions in continuity data")

        return {
            "score": max(0, score),
            "issues": issues,
            "continuity_strength": len(key_facts) + len(self.continuity_data.get("character_details", []))
        }

    def _save_continuity_data(self):
        """Save continuity data to file"""
        with open(self.continuity_file, 'w', encoding='utf-8') as f:
            json.dump(self.continuity_data, f, indent=2, ensure_ascii=False)

    def reset_continuity(self):
        """Reset continuity data for new project"""
        self.continuity_data = self._load_continuity_data()
        self._save_continuity_data()

    def export_continuity_report(self) -> str:
        """Generate a human-readable continuity report"""
        data = self.continuity_data

        report = f"""CONTINUITY REPORT
================

Created: {data['metadata']['created_at']}
Last Updated: {data['metadata']['last_updated']}

KEY FACTS ({len(data.get('key_facts', []))}):
{chr(10).join(f'• {fact}' for fact in data.get('key_facts', [])[-10:])}

CHARACTER DETAILS ({len(data.get('character_details', []))}):
{chr(10).join(f'• {detail}' for detail in data.get('character_details', []))}

TIMELINE EVENTS ({len(data.get('timeline_events', []))}):
{chr(10).join(f'• {event}' for event in data.get('timeline_events', []))}

RECURRING THEMES ({len(data.get('themes', []))}):
{chr(10).join(f'• {theme}' for theme in data.get('themes', []))}

TERMINOLOGY ({len(data.get('terminology', {}))}):
{chr(10).join(f'• {term}: {definition}' for term, definition in data.get('terminology', {}).items())}

CONTRADICTIONS ({len(data.get('contradictions', []))}):
{chr(10).join(f'• {contradiction}' for contradiction in data.get('contradictions', []))}

SECTIONS PROCESSED: {len(data.get('section_summaries', []))}
"""

        return report