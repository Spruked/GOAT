# book_builder/__init__.py
"""
GOAT Book Builder Package
Complete book creation engine with outline → chapters → compile → export pipeline
"""

from .book_builder import BookBuilder, BookInput, BookOutline, BookChapter, CompiledBook, BookExport
from .book_builder import BookGenre, ExportFormat
from .exporters.book_exporters import EPUBExporter, M4BExporter, AdvancedBookExporter

__version__ = "1.0.0"
__all__ = [
    "BookBuilder",
    "BookInput",
    "BookOutline",
    "BookChapter",
    "CompiledBook",
    "BookExport",
    "BookGenre",
    "ExportFormat",
    "EPUBExporter",
    "M4BExporter",
    "AdvancedBookExporter"
]