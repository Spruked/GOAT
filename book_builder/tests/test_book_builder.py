# test_book_builder.py
"""
Tests for GOAT Book Builder Core
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from book_builder import (
    BookBuilder, BookInput, BookOutline, BookGenre, ExportFormat
)

class TestBookBuilder:
    def setup_method(self):
        """Setup test fixtures"""
        self.builder = BookBuilder()
        self.sample_input = BookInput(
            title="Test Book",
            author="Test Author",
            genre=BookGenre.NON_FICTION,
            topic="Software Development",
            target_audience="developers",
            word_count_goal=30000,
            tone="professional",
            writing_style="technical",
            key_themes=["coding", "best practices", "architecture"],
            source_materials=["books", "articles", "experience"]
        )

    def test_create_outline(self):
        """Test outline creation"""
        outline = self.builder.create_outline(self.sample_input)

        assert isinstance(outline, BookOutline)
        assert outline.title == self.sample_input.title
        assert outline.author == self.sample_input.author
        assert outline.genre == self.sample_input.genre
        assert len(outline.chapters) > 0
        assert outline.estimated_word_count > 0

    def test_generate_chapter(self):
        """Test chapter generation"""
        outline = self.builder.create_outline(self.sample_input)

        chapter = self.builder.generate_chapter(outline, 1)

        assert chapter.number == 1
        assert chapter.title == outline.chapters[0]['title']
        assert len(chapter.content) > 0
        assert chapter.word_count > 0
        assert chapter.status == "draft"

    def test_compile_book(self):
        """Test book compilation"""
        outline = self.builder.create_outline(self.sample_input)

        # Generate a few chapters
        chapters = []
        for i in range(1, min(4, len(outline.chapters) + 1)):
            chapter = self.builder.generate_chapter(outline, i)
            chapters.append(chapter)

        compiled = self.builder.compile_book(outline, chapters)

        assert isinstance(compiled, CompiledBook)
        assert compiled.title == outline.title
        assert len(compiled.chapters) == len(chapters)
        assert compiled.total_word_count > 0
        assert compiled.foreword is not None
        assert compiled.introduction is not None
        assert compiled.conclusion is not None

    def test_export_formats(self):
        """Test different export formats"""
        outline = self.builder.create_outline(self.sample_input)

        # Create minimal compiled book
        chapter = self.builder.generate_chapter(outline, 1)
        compiled = self.builder.compile_book(outline, [chapter])

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Test TXT export
            txt_path = temp_path / "test_book.txt"
            txt_export = self.builder.export_book(compiled, ExportFormat.TXT, txt_path)

            assert txt_path.exists()
            assert txt_export.format == ExportFormat.TXT
            assert len(txt_export.checksum_sha256) == 64  # SHA256 hex length

            # Test HTML export
            html_path = temp_path / "test_book.html"
            html_export = self.builder.export_book(compiled, ExportFormat.HTML, html_path)

            assert html_path.exists()
            assert html_export.format == ExportFormat.HTML

            # Test JSON export
            json_path = temp_path / "test_book.json"
            json_export = self.builder.export_book(compiled, ExportFormat.JSON, json_path)

            assert json_path.exists()
            assert json_export.format == ExportFormat.JSON

    def test_genre_structures(self):
        """Test different genre structures"""
        genres_to_test = [
            BookGenre.NON_FICTION,
            BookGenre.BIOGRAPHY,
            BookGenre.SELF_HELP,
            BookGenre.BUSINESS
        ]

        for genre in genres_to_test:
            input_data = BookInput(
                title=f"{genre.value} Book",
                author="Test Author",
                genre=genre,
                topic="Test Topic",
                target_audience="readers",
                word_count_goal=20000
            )

            outline = self.builder.create_outline(input_data)
            assert len(outline.chapters) > 0
            assert outline.genre == genre

    def test_word_count_scaling(self):
        """Test word count goal affects chapter estimates"""
        small_book = BookInput(
            title="Small Book",
            author="Author",
            genre=BookGenre.NON_FICTION,
            topic="Topic",
            target_audience="readers",
            word_count_goal=10000
        )

        large_book = BookInput(
            title="Large Book",
            author="Author",
            genre=BookGenre.NON_FICTION,
            topic="Topic",
            target_audience="readers",
            word_count_goal=100000
        )

        small_outline = self.builder.create_outline(small_book)
        large_outline = self.builder.create_outline(large_book)

        # Large book should have higher word count estimates
        assert large_outline.estimated_word_count > small_outline.estimated_word_count

if __name__ == "__main__":
    pytest.main([__file__])