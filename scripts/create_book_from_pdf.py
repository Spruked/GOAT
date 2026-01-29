#!/usr/bin/env python3
"""
Create Book from PDF Content - GOAT Book Builder
Converts extracted PDF content into a properly formatted book
"""

import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import sys
import os

# Add book_builder to path
sys.path.append(str(Path(__file__).parent / "book_builder"))

from book_builder import (
    BookBuilder, BookInput, BookOutline, BookGenre, ExportFormat,
    BookChapter, CompiledBook
)

def parse_extracted_content(content_file: str) -> Dict[str, Any]:
    """Parse the extracted PDF content into book structure"""

    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content into main sections
    lines = content.split('\n')

    book_data = {
        'title': 'Happy Toes',
        'author': 'Bryan Anthony Spruk',
        'preface': '',
        'foreword': '',
        'chapters': []
    }

    current_section = None
    current_chapter = None
    chapter_content = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Extract preface
        if line.lower() == 'preface':
            current_section = 'preface'
            i += 1
            continue
        elif current_section == 'preface' and line.lower() == 'foreword':
            book_data['preface'] = '\n'.join(chapter_content).strip()
            chapter_content = []
            current_section = 'foreword'
            i += 1
            continue
        elif current_section == 'foreword' and re.match(r'^\d+(?:st|nd|rd|th)\s+chapter', line.lower()):
            book_data['foreword'] = '\n'.join(chapter_content).strip()
            chapter_content = []
            current_section = 'chapters'
            # Don't increment i here, let it be processed as chapter start

        # Process chapters
        if current_section in ['preface', 'foreword']:
            if line:  # Skip empty lines at section boundaries
                chapter_content.append(line)
        elif current_section == 'chapters' or re.match(r'^\d+(?:st|nd|rd|th)\s+chapter', line.lower()):
            if re.match(r'^\d+(?:st|nd|rd|th)\s+chapter', line.lower()):
                # Save previous chapter if exists
                if current_chapter and chapter_content:
                    current_chapter['content'] = '\n'.join(chapter_content).strip()
                    book_data['chapters'].append(current_chapter)

                # Start new chapter
                chapter_match = re.match(r'^(\d+)(?:st|nd|rd|th)\s+chapter', line.lower())
                chapter_num = int(chapter_match.group(1))

                current_chapter = {
                    'number': chapter_num,
                    'title': f"Chapter {chapter_num}",
                    'content': '',
                    'author': '',
                    'type': 'original'
                }
                chapter_content = []
                i += 1
                continue

            # Extract author information
            if "'s interpretation" in line.lower() or 'original poem' in line.lower():
                if "'s interpretation" in line.lower():
                    author_match = re.search(r"(\w+(?:\s+\w+)*)'s Interpretation", line)
                    if author_match:
                        current_chapter['author'] = author_match.group(1)
                        current_chapter['type'] = 'interpretation'
                elif 'original poem' in line.lower():
                    current_chapter['author'] = 'Bryan Anthony Spruk'
                    current_chapter['type'] = 'original'

            if line:  # Add non-empty lines to chapter content
                chapter_content.append(line)

        i += 1

    # Add the last chapter
    if current_chapter and chapter_content:
        current_chapter['content'] = '\n'.join(chapter_content).strip()
        book_data['chapters'].append(current_chapter)

    return book_data

def create_book_from_parsed_data(parsed_data: Dict[str, Any]) -> CompiledBook:
    """Create a CompiledBook from parsed data"""

    chapters = []
    for i, chapter_data in enumerate(parsed_data['chapters'], 1):
        # Count words in content
        word_count = len(chapter_data['content'].split())

        # Extract key points (first few lines as summary)
        content_lines = chapter_data['content'].split('\n')[:10]  # First 10 lines
        key_points = [line.strip() for line in content_lines if line.strip()][:5]  # Up to 5 key points

        chapter = BookChapter(
            number=i,
            title=f"{chapter_data['title']} - {chapter_data['author']}",
            summary=f"{chapter_data['type'].title()} poem by {chapter_data['author']}",
            key_points=key_points,
            word_count=word_count,
            content=chapter_data['content'],
            status="final",
            created_at=datetime.utcnow().isoformat() + "Z",
            updated_at=datetime.utcnow().isoformat() + "Z",
            notes=[f"Extracted from PDF - {chapter_data['type']} content"]
        )
        chapters.append(chapter)

    # Create compiled book
    compiled_book = CompiledBook(
        title=parsed_data['title'],
        author=parsed_data['author'],
        genre=BookGenre.POETRY,
        chapters=chapters,
        foreword=parsed_data.get('foreword', ''),
        introduction=parsed_data.get('preface', ''),
        conclusion="",
        appendices=[],
        total_word_count=sum(ch.word_count for ch in chapters),
        compiled_at=datetime.utcnow().isoformat() + "Z",
        version="1.0",
        metadata={
            "source": "PDF extraction",
            "extraction_date": datetime.utcnow().isoformat() + "Z",
            "total_chapters": len(chapters),
            "book_type": "Poetry Collection with Literary Interpretations"
        }
    )

    return compiled_book

def main():
    """Main function to create book from PDF content"""

    content_file = "extracted_content.txt"

    if not Path(content_file).exists():
        print(f"Error: {content_file} not found. Please run PDF extraction first.")
        return

    print("Parsing extracted PDF content...")
    parsed_data = parse_extracted_content(content_file)

    print(f"Found {len(parsed_data['chapters'])} chapters")
    print(f"Book title: {parsed_data['title']}")
    print(f"Author: {parsed_data['author']}")

    print("\nCreating compiled book...")
    compiled_book = create_book_from_parsed_data(parsed_data)

    print(f"Book compiled with {len(compiled_book.chapters)} chapters")
    print(f"Total word count: {compiled_book.total_word_count}")

    # Create output directory
    output_dir = Path("book_output")
    output_dir.mkdir(exist_ok=True)

    # Initialize book builder for export
    builder = BookBuilder()

    # Export in multiple formats
    formats = [ExportFormat.TXT, ExportFormat.HTML, ExportFormat.JSON, ExportFormat.EPUB]

    for fmt in formats:
        try:
            output_path = output_dir / f"happy_toes.{fmt.value}"
            print(f"\nExporting to {fmt.value}...")
            export_result = builder.export_book(compiled_book, fmt, output_path)

            print(f"✓ Exported {fmt.value} format to {output_path}")
            print(f"  File size: {output_path.stat().st_size} bytes")
            print(f"  Checksum: {export_result.checksum_sha256[:16]}...")

        except Exception as e:
            print(f"✗ Failed to export {fmt.value}: {e}")

    print("\n✓ Book creation complete!")
    print(f"Output files created in: {output_dir.absolute()}")

if __name__ == "__main__":
    main()