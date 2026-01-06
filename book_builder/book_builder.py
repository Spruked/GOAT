# book_builder.py
"""
GOAT Book Builder Core - Complete Book Creation Engine
OUTLINE → CHAPTERS → COMPILE → EXPORT
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class BookGenre(Enum):
    FICTION = "fiction"
    NON_FICTION = "non_fiction"
    BIOGRAPHY = "biography"
    SELF_HELP = "self_help"
    BUSINESS = "business"
    TECHNICAL = "technical"
    MEMOIR = "memoir"
    POETRY = "poetry"

class ExportFormat(Enum):
    PDF = "pdf"
    EPUB = "epub"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    JSON = "json"
    M4B = "m4b"

@dataclass
class BookInput:
    """User input for book creation"""
    title: str
    author: str
    genre: BookGenre
    topic: str
    target_audience: str
    word_count_goal: int = 50000
    tone: str = "professional"
    writing_style: str = "narrative"
    key_themes: Optional[List[str]] = None
    source_materials: Optional[List[str]] = None
    outline_structure: Optional[Dict[str, Any]] = None
    deadline: Optional[str] = None

    def __post_init__(self):
        if self.key_themes is None:
            self.key_themes = []
        if self.source_materials is None:
            self.source_materials = []

@dataclass
class BookOutline:
    """Generated book outline"""
    title: str
    author: str
    genre: BookGenre
    topic: str
    premise: str
    target_audience: str
    key_themes: List[str]
    chapters: List[Dict[str, Any]]
    estimated_word_count: int
    estimated_chapters: int
    created_at: str
    metadata: Dict[str, Any]

@dataclass
class BookChapter:
    """Individual book chapter"""
    number: int
    title: str
    summary: str
    key_points: List[str]
    word_count: int
    content: str
    created_at: str
    updated_at: str
    status: str = "draft"  # draft, revised, final
    notes: Optional[List[str]] = None

    def __post_init__(self):
        if self.notes is None:
            self.notes = []

@dataclass
class CompiledBook:
    """Compiled complete book"""
    title: str
    author: str
    genre: BookGenre
    chapters: List[BookChapter]
    foreword: Optional[str] = None
    introduction: Optional[str] = None
    conclusion: Optional[str] = None
    appendices: Optional[List[Dict[str, Any]]] = None
    total_word_count: int = 0
    compiled_at: str = ""
    version: str = "1.0"
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.appendices is None:
            self.appendices = []
        if self.metadata is None:
            self.metadata = {}

@dataclass
class BookExport:
    """Exported book in various formats"""
    book_id: str
    format: ExportFormat
    file_path: str
    file_size: int
    checksum_sha256: str
    exported_at: str
    metadata: Dict[str, Any]

class BookBuilder:
    """Core book building engine"""

    def __init__(self):
        self.templates_path = Path(__file__).parent / "templates"
        self.templates_path.mkdir(exist_ok=True)

    def create_outline(self, book_input: BookInput) -> BookOutline:
        """Generate comprehensive book outline"""
        # Generate premise
        premise = self._generate_premise(book_input)

        # Generate chapter structure
        chapters = self._generate_chapter_structure(book_input)

        # Calculate estimates
        estimated_word_count = sum(chapter.get('estimated_words', 0) for chapter in chapters)
        estimated_chapters = len(chapters)

        outline = BookOutline(
            title=book_input.title,
            author=book_input.author,
            genre=book_input.genre,
            topic=book_input.topic,
            premise=premise,
            target_audience=book_input.target_audience,
            key_themes=book_input.key_themes or [],
            chapters=chapters,
            estimated_word_count=estimated_word_count,
            estimated_chapters=estimated_chapters,
            created_at=datetime.utcnow().isoformat() + "Z",
            metadata={
                "input_word_goal": book_input.word_count_goal,
                "tone": book_input.tone,
                "writing_style": book_input.writing_style,
                "source_materials_count": len(book_input.source_materials or [])
            }
        )

        return outline

    def _generate_premise(self, book_input: BookInput) -> str:
        """Generate book premise based on input"""
        # This would integrate with AI/Caleon for premise generation
        # For now, create a template-based premise
        templates = {
            BookGenre.NON_FICTION: f"Discover the essential guide to {book_input.topic} that {book_input.target_audience} have been waiting for.",
            BookGenre.BIOGRAPHY: f"The compelling story of {book_input.topic} and their journey that will inspire {book_input.target_audience}.",
            BookGenre.SELF_HELP: f"Transform your life with proven strategies for {book_input.topic} designed specifically for {book_input.target_audience}.",
            BookGenre.BUSINESS: f"Master the art of {book_input.topic} with strategies that have helped {book_input.target_audience} achieve breakthrough results.",
            BookGenre.TECHNICAL: f"The definitive resource for {book_input.topic} that {book_input.target_audience} need to succeed in today's world.",
            BookGenre.MEMOIR: f"A deeply personal journey through {book_input.topic} that will resonate with {book_input.target_audience}.",
            BookGenre.FICTION: f"An unforgettable story of {book_input.topic} that will captivate {book_input.target_audience}.",
            BookGenre.POETRY: f"A collection of verses exploring {book_input.topic} that speaks to the soul of {book_input.target_audience}."
        }

        return templates.get(book_input.genre, f"A comprehensive exploration of {book_input.topic} for {book_input.target_audience}.")

    def _generate_chapter_structure(self, book_input: BookInput) -> List[Dict[str, Any]]:
        """Generate detailed chapter structure"""
        # Base structure templates by genre
        structures = {
            BookGenre.NON_FICTION: [
                {"title": "Introduction", "purpose": "hook_and_overview", "estimated_words": 2500},
                {"title": "The Foundation", "purpose": "basics_setup", "estimated_words": 4000},
                {"title": "Core Concepts", "purpose": "main_content", "estimated_words": 6000},
                {"title": "Practical Application", "purpose": "implementation", "estimated_words": 5000},
                {"title": "Advanced Techniques", "purpose": "deep_dive", "estimated_words": 4500},
                {"title": "Case Studies", "purpose": "real_world_examples", "estimated_words": 4000},
                {"title": "Common Challenges", "purpose": "problem_solving", "estimated_words": 3500},
                {"title": "Future Trends", "purpose": "forward_looking", "estimated_words": 3000},
                {"title": "Conclusion", "purpose": "wrap_up", "estimated_words": 2000},
                {"title": "Action Plan", "purpose": "next_steps", "estimated_words": 2500}
            ],
            BookGenre.BIOGRAPHY: [
                {"title": "Early Life", "purpose": "origins", "estimated_words": 5000},
                {"title": "First Challenges", "purpose": "initial_struggles", "estimated_words": 4500},
                {"title": "Breaking Through", "purpose": "turning_points", "estimated_words": 5500},
                {"title": "Major Achievements", "purpose": "success_stories", "estimated_words": 6000},
                {"title": "Personal Life", "purpose": "behind_the_scenes", "estimated_words": 4000},
                {"title": "Lessons Learned", "purpose": "wisdom_shared", "estimated_words": 3500},
                {"title": "Legacy", "purpose": "lasting_impact", "estimated_words": 3000},
                {"title": "Reflections", "purpose": "final_thoughts", "estimated_words": 2500}
            ],
            BookGenre.SELF_HELP: [
                {"title": "The Problem", "purpose": "identify_pain", "estimated_words": 3000},
                {"title": "The Solution", "purpose": "present_answer", "estimated_words": 4000},
                {"title": "Understanding Yourself", "purpose": "self_awareness", "estimated_words": 4500},
                {"title": "The Mindset Shift", "purpose": "mental_framework", "estimated_words": 4000},
                {"title": "Action Steps", "purpose": "practical_steps", "estimated_words": 5000},
                {"title": "Overcoming Obstacles", "purpose": "barrier_busting", "estimated_words": 3500},
                {"title": "Maintaining Progress", "purpose": "sustainability", "estimated_words": 3000},
                {"title": "Success Stories", "purpose": "inspiration", "estimated_words": 4000},
                {"title": "Your Journey Begins", "purpose": "motivation", "estimated_words": 2500}
            ],
            BookGenre.BUSINESS: [
                {"title": "Market Analysis", "purpose": "industry_overview", "estimated_words": 4000},
                {"title": "Business Fundamentals", "purpose": "core_principles", "estimated_words": 5000},
                {"title": "Strategy Development", "purpose": "planning", "estimated_words": 5500},
                {"title": "Execution Excellence", "purpose": "implementation", "estimated_words": 4500},
                {"title": "Financial Management", "purpose": "money_matters", "estimated_words": 4000},
                {"title": "Team Building", "purpose": "people_power", "estimated_words": 3500},
                {"title": "Scaling Up", "purpose": "growth_strategies", "estimated_words": 4000},
                {"title": "Risk Management", "purpose": "crisis_planning", "estimated_words": 3000},
                {"title": "Innovation", "purpose": "future_proofing", "estimated_words": 3500},
                {"title": "Leadership Legacy", "purpose": "lasting_success", "estimated_words": 3000}
            ]
        }

        # Get base structure or create generic one
        base_structure = structures.get(book_input.genre, self._create_generic_structure(book_input))

        # Customize based on word count goal
        total_estimated = sum(ch.get('estimated_words', 0) for ch in base_structure)
        scale_factor = book_input.word_count_goal / max(total_estimated, 1)

        for chapter in base_structure:
            chapter['estimated_words'] = int(chapter['estimated_words'] * scale_factor)

        return base_structure

    def _create_generic_structure(self, book_input: BookInput) -> List[Dict[str, Any]]:
        """Create generic chapter structure"""
        return [
            {"title": "Introduction", "purpose": "setup", "estimated_words": 3000},
            {"title": "Chapter 1", "purpose": "foundation", "estimated_words": 5000},
            {"title": "Chapter 2", "purpose": "development", "estimated_words": 5000},
            {"title": "Chapter 3", "purpose": "deep_dive", "estimated_words": 5000},
            {"title": "Chapter 4", "purpose": "application", "estimated_words": 5000},
            {"title": "Chapter 5", "purpose": "advanced", "estimated_words": 5000},
            {"title": "Conclusion", "purpose": "wrap_up", "estimated_words": 3000}
        ]

    def generate_chapter(self, outline: BookOutline, chapter_number: int) -> BookChapter:
        """Generate content for a specific chapter"""
        chapter_outline = outline.chapters[chapter_number - 1]

        # This would integrate with AI/Caleon for content generation
        # For now, create placeholder content
        content = self._generate_chapter_content(outline, chapter_outline)

        chapter = BookChapter(
            number=chapter_number,
            title=chapter_outline['title'],
            summary=f"Chapter {chapter_number} explores {chapter_outline.get('purpose', 'key concepts')}.",
            key_points=[
                f"Key point {i+1} for {chapter_outline['title']}"
                for i in range(min(5, chapter_outline.get('estimated_words', 5000) // 1000))
            ],
            word_count=len(content.split()),
            content=content,
            status="draft",
            created_at=datetime.utcnow().isoformat() + "Z",
            updated_at=datetime.utcnow().isoformat() + "Z",
            notes=["Generated automatically", "Ready for editing"]
        )

        return chapter

    def _generate_chapter_content(self, outline: BookOutline, chapter_outline: Dict[str, Any]) -> str:
        """Generate chapter content (placeholder for AI integration)"""
        word_count = chapter_outline.get('estimated_words', 2000)

        # Template-based content generation
        template = f"""# {chapter_outline['title']}

## Overview

This chapter explores {chapter_outline.get('purpose', 'key concepts')} in the context of {outline.topic}.

## Key Concepts

{chr(10).join([f"### Point {i+1}" + chr(10) + f"Detail about point {i+1} related to {outline.topic}." for i in range(5)])}

## Practical Applications

Understanding these concepts allows {outline.target_audience} to:

- Apply the principles in real-world scenarios
- Make informed decisions based on the material
- Build upon the foundation established in this chapter

## Summary

This chapter has provided a comprehensive overview of {chapter_outline['title'].lower()}, setting the stage for the material that follows.

"""

        # Expand to target word count (rough approximation)
        while len(template.split()) < word_count * 0.8:
            template += f"\n## Additional Insights\n\nFurther consideration of {outline.topic} reveals additional layers of complexity that {outline.target_audience} should be aware of.\n\n"

        return template

    def compile_book(self, outline: BookOutline, chapters: List[BookChapter]) -> CompiledBook:
        """Compile all chapters into a complete book"""
        total_word_count = sum(chapter.word_count for chapter in chapters)

        # Generate front/back matter
        foreword = self._generate_foreword(outline)
        introduction = self._generate_introduction(outline)
        conclusion = self._generate_conclusion(outline)

        compiled = CompiledBook(
            title=outline.title,
            author=outline.author,
            genre=outline.genre,
            chapters=chapters,
            foreword=foreword,
            introduction=introduction,
            conclusion=conclusion,
            appendices=[],
            total_word_count=total_word_count,
            compiled_at=datetime.utcnow().isoformat() + "Z",
            version="1.0",
            metadata={
                "outline_created": outline.created_at,
                "chapters_compiled": len(chapters),
                "estimated_vs_actual_words": f"{outline.estimated_word_count} → {total_word_count}",
                "compilation_engine": "GOAT Book Builder v1.0"
            }
        )

        return compiled

    def _generate_foreword(self, outline: BookOutline) -> str:
        """Generate book foreword"""
        return f"""# Foreword

Welcome to *{outline.title}*, a comprehensive exploration of {outline.topic} designed specifically for {outline.target_audience}.

In an age of information overload, this book serves as your trusted guide through the complexities of {outline.topic}. Whether you're just beginning your journey or seeking to deepen your understanding, you'll find practical insights and actionable strategies within these pages.

The author, {outline.author}, brings a unique perspective shaped by extensive experience in {outline.genre.value} writing and deep knowledge of {outline.topic}.

This is more than just a book—it's a companion for your journey toward mastery.

"""

    def _generate_introduction(self, outline: BookOutline) -> str:
        """Generate book introduction"""
        return f"""# Introduction

## Why This Book Matters

*{outline.title}* addresses a critical need in today's world: helping {outline.target_audience} navigate the complexities of {outline.topic}.

## What You'll Learn

By the end of this book, you'll have:

- A comprehensive understanding of {outline.topic}
- Practical strategies for implementation
- Real-world examples and case studies
- Actionable steps for immediate application

## How to Use This Book

Each chapter builds upon the previous one, creating a logical progression from foundational concepts to advanced applications. Take time to reflect on the key points and consider how they apply to your situation.

## The Journey Begins

Turn the page and let's begin this transformative journey together.

"""

    def _generate_conclusion(self, outline: BookOutline) -> str:
        """Generate book conclusion"""
        return f"""# Conclusion

## Reflecting on the Journey

We've covered a great deal of ground in *{outline.title}*. From the foundational concepts to advanced applications, you've gained valuable insights into {outline.topic}.

## Key Takeaways

The most important lessons include:

{chr(10).join([f"- Understanding {theme} and its implications" for theme in outline.key_themes[:5]])}

## Moving Forward

Knowledge is only valuable when applied. Take what you've learned and put it into practice. The real transformation happens not in reading these words, but in living them.

## Final Thoughts

Thank you for joining me on this journey. May the insights you've gained serve you well as you apply them in your life and work.

The future belongs to those who learn, adapt, and take action.

— {outline.author}

"""

    def export_book(self, compiled_book: CompiledBook, format: ExportFormat, output_path: Path) -> BookExport:
        """Export compiled book to specified format"""
        # Handle advanced formats (EPUB, M4B) with dedicated exporters
        if format == ExportFormat.EPUB:
            from .exporters.book_exporters import AdvancedBookExporter
            exporter = AdvancedBookExporter()
            return exporter.export_book(compiled_book, 'epub', output_path)

        # Generate content based on format
        if format == ExportFormat.TXT:
            content = self._export_as_txt(compiled_book)
        elif format == ExportFormat.HTML:
            content = self._export_as_html(compiled_book)
        elif format == ExportFormat.JSON:
            content = self._export_as_json(compiled_book)
        else:
            # Placeholder for PDF, DOCX (would require additional libraries)
            content = self._export_as_txt(compiled_book)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Generate checksum
        import hashlib
        checksum = hashlib.sha256(content.encode('utf-8')).hexdigest()

        export = BookExport(
            book_id=str(uuid.uuid4()),
            format=format,
            file_path=str(output_path),
            file_size=len(content.encode('utf-8')),
            checksum_sha256=checksum,
            exported_at=datetime.utcnow().isoformat() + "Z",
            metadata={
                "book_title": compiled_book.title,
                "author": compiled_book.author,
                "word_count": compiled_book.total_word_count,
                "chapters": len(compiled_book.chapters),
                "export_engine": "GOAT Book Builder v1.0"
            }
        )

        return export

    def _export_as_txt(self, book: CompiledBook) -> str:
        """Export book as plain text"""
        lines = []

        # Title page
        lines.extend([
            "=" * 50,
            f"{book.title.upper()}",
            f"by {book.author}",
            f"Genre: {book.genre.value.replace('_', ' ').title()}",
            f"Compiled: {book.compiled_at}",
            "=" * 50,
            ""
        ])

        # Foreword
        if book.foreword:
            lines.extend([book.foreword, "", "-" * 50, ""])

        # Introduction
        if book.introduction:
            lines.extend([book.introduction, "", "-" * 50, ""])

        # Chapters
        for chapter in book.chapters:
            lines.extend([
                f"Chapter {chapter.number}: {chapter.title}",
                "=" * 40,
                "",
                chapter.content,
                "",
                "-" * 50,
                ""
            ])

        # Conclusion
        if book.conclusion:
            lines.extend([book.conclusion, "", "-" * 50, ""])

        # Appendices
        if book.appendices:
            lines.extend(["APPENDICES", "=" * 40, ""])
            for appendix in book.appendices:
                lines.extend([f"Appendix: {appendix.get('title', 'Untitled')}", appendix.get('content', ''), ""])

        # Metadata
        lines.extend([
            "",
            "BOOK METADATA",
            "=" * 40,
            f"Total Word Count: {book.total_word_count}",
            f"Chapters: {len(book.chapters)}",
            f"Version: {book.version}",
            f"Compiled: {book.compiled_at}"
        ])

        return "\n".join(lines)

    def _export_as_html(self, book: CompiledBook) -> str:
        """Export book as HTML"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book.title}</title>
    <style>
        body {{ font-family: 'Georgia', serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .chapter {{ margin-bottom: 40px; }}
        .metadata {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 30px; }}
    </style>
</head>
<body>
    <h1>{book.title}</h1>
    <h2>by {book.author}</h2>
    <p><em>Genre: {book.genre.value.replace('_', ' ').title()}</em></p>
"""

        if book.foreword:
            html += f"<div class='chapter'>{book.foreword}</div>"

        if book.introduction:
            html += f"<div class='chapter'>{book.introduction}</div>"

        for chapter in book.chapters:
            html += f"""
    <div class='chapter'>
        <h2>Chapter {chapter.number}: {chapter.title}</h2>
        {chapter.content.replace(chr(10), '<br>')}
    </div>
"""

        if book.conclusion:
            html += f"<div class='chapter'>{book.conclusion}</div>"

        html += f"""
    <div class='metadata'>
        <h3>Book Metadata</h3>
        <ul>
            <li>Total Word Count: {book.total_word_count}</li>
            <li>Chapters: {len(book.chapters)}</li>
            <li>Version: {book.version}</li>
            <li>Compiled: {book.compiled_at}</li>
        </ul>
    </div>
</body>
</html>"""

        return html

    def _export_as_json(self, book: CompiledBook) -> str:
        """Export book as JSON"""
        return json.dumps(asdict(book), indent=2, default=str)