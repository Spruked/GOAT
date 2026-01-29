#!/usr/bin/env python3
"""
GOAT Book Builder Test Script
Demonstrates the book creation system
"""

import sys
import os
from pathlib import Path

# Add the book_builder directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from book_builder import BookBuilder, BookInput, BookGenre, ExportFormat

def test_book_creation():
    """Test the book creation system"""

    print("🐐 GOAT Book Builder Test")
    print("=" * 50)

    # Create book builder instance
    builder = BookBuilder()

    # Create sample book input
    book_input = BookInput(
        title='The Future of AI: A Comprehensive Guide',
        author='GOAT AI Assistant',
        genre=BookGenre.NON_FICTION,
        topic='Artificial Intelligence',
        target_audience='technology enthusiasts and professionals',
        word_count_goal=25000,
        tone='professional',
        writing_style='analytical',
        key_themes=['AI evolution', 'machine learning', 'ethics', 'future applications'],
        source_materials=['research papers', 'industry reports', 'expert interviews']
    )

    print("🚀 Creating book outline...")
    outline = builder.create_outline(book_input)

    print(f"📖 Book: {outline.title}")
    print(f"👤 Author: {outline.author}")
    print(f"📚 Genre: {outline.genre.value}")
    print(f"🎯 Topic: {outline.topic}")
    print(f"👥 Audience: {outline.target_audience}")
    print(f"📊 Estimated Chapters: {outline.estimated_chapters}")
    print(f"📝 Estimated Word Count: {outline.estimated_word_count:,}")
    print(f"🎭 Premise: {outline.premise[:150]}...")
    print()

    print("📋 Chapter Outline:")
    for i, chapter in enumerate(outline.chapters[:8], 1):
        print(f"  {i}. {chapter['title']}")
    if len(outline.chapters) > 8:
        print(f"  ... and {len(outline.chapters) - 8} more chapters")
    print()

    print("📝 Generating sample chapter...")
    chapter = builder.generate_chapter(outline, 1)
    print(f"Chapter 1: {chapter.title}")
    print(f"Word Count: {chapter.word_count}")
    print(f"Content Preview: {chapter.content[:300]}...")
    print()

    print("📚 Compiling book...")
    chapters = [chapter]  # Just compile with one chapter for demo
    compiled_book = builder.compile_book(outline, chapters)
    print(f"✅ Book compiled: {compiled_book.title}")
    print(f"Total chapters: {len(compiled_book.chapters)}")
    print(f"Total word count: {compiled_book.total_word_count}")
    print()

    print("💾 Exporting book...")
    output_dir = Path("./deliverables/book_builder")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export as TXT
    txt_path = output_dir / "ai_future_guide.txt"
    txt_export = builder.export_book(compiled_book, ExportFormat.TXT, txt_path)
    print(f"📄 TXT export: {txt_path} ({txt_export.file_size} bytes)")

    # Export as HTML
    html_path = output_dir / "ai_future_guide.html"
    html_export = builder.export_book(compiled_book, ExportFormat.HTML, html_path)
    print(f"🌐 HTML export: {html_path} ({html_export.file_size} bytes)")

    print()
    print("🎉 Book creation test completed successfully!")
    print(f"📂 Check the deliverables/book_builder/ directory for exported files")

if __name__ == "__main__":
    test_book_creation()</content>
<parameter name="filePath">c:\dev\GOAT\test_book_creation.py