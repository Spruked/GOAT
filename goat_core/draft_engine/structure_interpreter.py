# goat_core/draft_engine/structure_interpreter.py
"""
GOAT Draft Engine - Structure Interpreter
Converts user outlines and structures into writing blueprints
"""

import json
import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path
import re

class StructureInterpreter:
    """Interprets and converts various input structures into writing blueprints"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else Path(__file__).parent
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Any]:
        """Load structure templates for different content types"""
        return {
            "book": {
                "sections": ["introduction", "main_content", "conclusion"],
                "word_targets": {"introduction": 800, "chapter": 2500, "conclusion": 600},
                "structure": {
                    "front_matter": ["title_page", "table_of_contents", "foreword"],
                    "body": ["chapters"],
                    "back_matter": ["appendices", "index", "about_author"]
                }
            },
            "course": {
                "sections": ["overview", "modules", "assessment"],
                "word_targets": {"module": 1500, "lesson": 800, "assessment": 400},
                "structure": {
                    "introduction": ["course_overview", "learning_objectives"],
                    "content": ["modules"],
                    "conclusion": ["final_assessment", "certification"]
                }
            },
            "framework": {
                "sections": ["foundation", "implementation", "case_studies"],
                "word_targets": {"section": 1200, "subsection": 600},
                "structure": {
                    "theory": ["principles", "concepts"],
                    "practice": ["steps", "tools"],
                    "application": ["examples", "templates"]
                }
            },
            "archive": {
                "sections": ["timeline", "themes", "reflections"],
                "word_targets": {"section": 1000, "subsection": 500},
                "structure": {
                    "chronological": ["early_life", "career", "legacy"],
                    "thematic": ["achievements", "challenges", "lessons"],
                    "personal": ["memories", "relationships", "growth"]
                }
            }
        }

    def interpret_outline(self, outline_text: str, content_type: str = "book") -> Dict[str, Any]:
        """
        Convert text outline into structured writing blueprint

        Args:
            outline_text: Raw outline text from user
            content_type: Type of content (book, course, framework, archive)

        Returns:
            Structured blueprint for the draft engine
        """
        # Parse the outline text
        parsed_sections = self._parse_outline_text(outline_text)

        # Apply content type template
        template = self.templates.get(content_type, self.templates["book"])

        # Build blueprint
        blueprint = {
            "content_type": content_type,
            "title": self._extract_title(outline_text),
            "structure": self._build_structure(parsed_sections, template),
            "metadata": {
                "estimated_word_count": self._estimate_word_count(parsed_sections, template),
                "sections_count": len(parsed_sections),
                "complexity_score": self._calculate_complexity(parsed_sections)
            },
            "writing_plan": self._create_writing_plan(parsed_sections, template)
        }

        return blueprint

    def _parse_outline_text(self, text: str) -> List[Dict[str, Any]]:
        """Parse outline text into structured sections"""
        sections = []
        lines = text.strip().split('\n')

        current_section = None
        current_subsections = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect main sections (Roman numerals, numbers, or main bullets)
            if re.match(r'^[IVXLCDM]+\.|^[A-Z]\.|^[0-9]+\.|^[-*•]\s*[A-Z]', line):
                # Save previous section if exists
                if current_section:
                    current_section["subsections"] = current_subsections
                    sections.append(current_section)

                # Start new section
                title = re.sub(r'^[IVXLCDM0-9A-Z.*•-]+\s*', '', line).strip()
                current_section = {
                    "title": title,
                    "level": 1,
                    "content_type": "section",
                    "estimated_words": 0
                }
                current_subsections = []

            # Detect subsections
            elif re.match(r'^\s*[a-z]\.|\s*[0-9]+\.|\s*[-*•]\s*[a-z]', line):
                if current_section:
                    subsection_title = re.sub(r'^\s*[a-z0-9.*•-]+\s*', '', line).strip()
                    current_subsections.append({
                        "title": subsection_title,
                        "level": 2,
                        "content_type": "subsection",
                        "estimated_words": 0
                    })

        # Add final section
        if current_section:
            current_section["subsections"] = current_subsections
            sections.append(current_section)

        return sections

    def _extract_title(self, text: str) -> str:
        """Extract title from outline text"""
        lines = text.strip().split('\n')
        for line in lines[:5]:  # Check first few lines
            line = line.strip()
            if line and not re.match(r'^[IVXLCDM0-9A-Z.*•-]+\s*$', line):
                # Look for title-like patterns
                if len(line) < 100 and not line.startswith(('Chapter', 'Section', 'Part')):
                    return line

        return "Untitled Work"

    def _build_structure(self, sections: List[Dict[str, Any]], template: Dict[str, Any]) -> Dict[str, Any]:
        """Build complete structure using template"""
        return {
            "front_matter": template["structure"].get("front_matter", []),
            "body": sections,
            "back_matter": template["structure"].get("back_matter", [])
        }

    def _estimate_word_count(self, sections: List[Dict[str, Any]], template: Dict[str, Any]) -> int:
        """Estimate total word count"""
        total = 0
        word_targets = template["word_targets"]

        for section in sections:
            # Main section
            section_words = word_targets.get("chapter", word_targets.get("section", 1000))
            total += section_words

            # Subsections
            for subsection in section.get("subsections", []):
                subsection_words = word_targets.get("subsection", 500)
                total += subsection_words

        return total

    def _calculate_complexity(self, sections: List[Dict[str, Any]]) -> float:
        """Calculate complexity score (0-10)"""
        total_sections = len(sections)
        total_subsections = sum(len(s.get("subsections", [])) for s in sections)

        # Complexity based on structure depth and breadth
        complexity = min(10.0, (total_sections * 0.5) + (total_subsections * 0.3))
        return round(complexity, 1)

    def _create_writing_plan(self, sections: List[Dict[str, Any]], template: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create detailed writing plan for each section"""
        plan = []

        for i, section in enumerate(sections):
            section_plan = {
                "section_number": i + 1,
                "title": section["title"],
                "content_type": section["content_type"],
                "word_target": template["word_targets"].get("chapter", 2000),
                "tone_guidance": "professional, engaging, informative",
                "key_points": [],  # To be filled by content generator
                "dependencies": [],  # Previous sections to reference
                "status": "pending"
            }

            # Add subsection plans
            for j, subsection in enumerate(section.get("subsections", [])):
                subsection_plan = {
                    "section_number": i + 1,
                    "subsection_number": j + 1,
                    "title": subsection["title"],
                    "content_type": subsection["content_type"],
                    "word_target": template["word_targets"].get("subsection", 600),
                    "tone_guidance": "focused, detailed, practical",
                    "key_points": [],
                    "dependencies": [f"section_{i+1}"],
                    "status": "pending"
                }
                plan.append(subsection_plan)

            plan.append(section_plan)

        return plan

    def save_blueprint(self, blueprint: Dict[str, Any], output_path: str):
        """Save blueprint to file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(blueprint, f, indent=2, ensure_ascii=False)

    def load_blueprint(self, blueprint_path: str) -> Dict[str, Any]:
        """Load blueprint from file"""
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            return json.load(f)