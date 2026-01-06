# book_builder_routes.py
"""
GOAT Book Builder API Routes
FastAPI endpoints for book creation workflow
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import uuid
from datetime import datetime

from ..book_builder import (
    BookBuilder, BookInput, BookOutline, BookChapter, CompiledBook, BookExport,
    BookGenre, ExportFormat
)
from ..exporters.book_exporters import AdvancedBookExporter
from dataclasses import asdict

router = APIRouter(prefix="/api/book-builder", tags=["book-builder"])

# Pydantic models for API
class BookInputRequest(BaseModel):
    title: str
    author: str
    genre: BookGenre
    topic: str
    target_audience: str
    word_count_goal: int = 50000
    tone: str = "professional"
    writing_style: str = "narrative"
    key_themes: List[str] = []
    source_materials: List[str] = []
    outline_structure: Optional[Dict[str, Any]] = None
    deadline: Optional[str] = None

class ChapterRequest(BaseModel):
    chapter_number: int

class ExportRequest(BaseModel):
    format: ExportFormat
    output_filename: Optional[str] = None
    audio_files: Optional[List[str]] = None

# Global book builder instance
book_builder = BookBuilder()
advanced_exporter = AdvancedBookExporter()

# In-memory storage for demo (would use database in production)
active_books: Dict[str, Dict[str, Any]] = {}

@router.post("/create-outline", response_model=Dict[str, Any])
async def create_book_outline(request: BookInputRequest):
    """Create a book outline from user input"""
    try:
        # Convert request to BookInput
        book_input = BookInput(**request.dict())

        # Generate outline
        outline = book_builder.create_outline(book_input)

        # Store in active books
        book_id = str(uuid.uuid4())
        active_books[book_id] = {
            "input": book_input,
            "outline": outline,
            "chapters": {},
            "compiled": None,
            "exports": [],
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

        return {
            "book_id": book_id,
            "outline": asdict(outline),
            "status": "outline_created",
            "next_steps": ["generate_chapters", "compile_book"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create outline: {str(e)}")

@router.post("/generate-chapter/{book_id}")
async def generate_chapter(book_id: str, request: ChapterRequest):
    """Generate content for a specific chapter"""
    if book_id not in active_books:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = active_books[book_id]
    outline = book_data["outline"]

    try:
        chapter = book_builder.generate_chapter(outline, request.chapter_number)

        # Store chapter
        book_data["chapters"][str(request.chapter_number)] = chapter

        return {
            "chapter": asdict(chapter),
            "status": "chapter_generated",
            "book_id": book_id
        }

    except IndexError:
        raise HTTPException(status_code=400, detail=f"Chapter {request.chapter_number} not found in outline")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate chapter: {str(e)}")

@router.post("/generate-all-chapters/{book_id}")
async def generate_all_chapters(book_id: str, background_tasks: BackgroundTasks):
    """Generate all chapters for a book (background task)"""
    if book_id not in active_books:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = active_books[book_id]
    outline = book_data["outline"]

    # Start background generation
    background_tasks.add_task(_generate_all_chapters_background, book_id, outline)

    return {
        "message": "Chapter generation started in background",
        "book_id": book_id,
        "total_chapters": len(outline.chapters),
        "status": "generating"
    }

def _generate_all_chapters_background(book_id: str, outline: BookOutline):
    """Background task to generate all chapters"""
    try:
        chapters = {}
        for i, chapter_outline in enumerate(outline.chapters, 1):
            chapter = book_builder.generate_chapter(outline, i)
            chapters[str(i)] = chapter

        active_books[book_id]["chapters"] = chapters
        active_books[book_id]["chapters_generated_at"] = datetime.utcnow().isoformat() + "Z"

    except Exception as e:
        # Log error (would use proper logging in production)
        print(f"Error generating chapters for book {book_id}: {str(e)}")

@router.post("/compile-book/{book_id}")
async def compile_book(book_id: str):
    """Compile all chapters into a complete book"""
    if book_id not in active_books:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = active_books[book_id]
    outline = book_data["outline"]
    chapters = list(book_data["chapters"].values())

    if not chapters:
        raise HTTPException(status_code=400, detail="No chapters generated yet")

    try:
        compiled_book = book_builder.compile_book(outline, chapters)
        book_data["compiled"] = compiled_book

        return {
            "compiled_book": asdict(compiled_book),
            "status": "book_compiled",
            "book_id": book_id,
            "next_steps": ["export_book"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compile book: {str(e)}")

@router.post("/export-book/{book_id}")
async def export_book(book_id: str, request: ExportRequest):
    """Export compiled book to specified format"""
    if book_id not in active_books:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = active_books[book_id]
    compiled_book = book_data.get("compiled")

    if not compiled_book:
        raise HTTPException(status_code=400, detail="Book not compiled yet")

    try:
        # Create output directory if needed
        output_dir = Path("deliverables") / "book_builder"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = request.output_filename or f"{compiled_book.title.replace(' ', '_')}_{book_id}.{request.format.value}"
        output_path = output_dir / filename

        # Export book based on format
        if request.format in [ExportFormat.EPUB, ExportFormat.M4B]:
            # Use advanced exporter for EPUB/M4B
            audio_files = getattr(request, 'audio_files', None) if request.format == ExportFormat.M4B else None
            book_export = advanced_exporter.export_book(compiled_book, request.format.value, output_path, audio_files)
        else:
            # Use standard exporter for TXT/HTML/JSON
            book_export = book_builder.export_book(compiled_book, request.format, output_path)

        # Store export info
        book_data["exports"].append(book_export)

        return {
            "export": asdict(book_export),
            "download_url": f"/api/book-builder/download/{book_id}/{filename}",
            "status": "book_exported",
            "book_id": book_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export book: {str(e)}")

@router.get("/download/{book_id}/{filename}")
async def download_book(book_id: str, filename: str):
    """Download exported book file"""
    file_path = Path("deliverables") / "book_builder" / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    from fastapi.responses import FileResponse
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

@router.get("/status/{book_id}")
async def get_book_status(book_id: str):
    """Get the current status of a book project"""
    if book_id not in active_books:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = active_books[book_id]

    status = {
        "book_id": book_id,
        "has_outline": "outline" in book_data,
        "chapters_generated": len(book_data.get("chapters", {})),
        "total_chapters": len(book_data["outline"].chapters) if "outline" in book_data else 0,
        "compiled": book_data.get("compiled") is not None,
        "exports_count": len(book_data.get("exports", [])),
        "created_at": book_data["created_at"]
    }

    if book_data.get("chapters_generated_at"):
        status["chapters_generated_at"] = book_data["chapters_generated_at"]

    if book_data.get("compiled"):
        status["compiled_at"] = book_data["compiled"].compiled_at
        status["total_word_count"] = book_data["compiled"].total_word_count

    return status

@router.get("/list-books")
async def list_books():
    """List all active book projects"""
    books = []
    for book_id, book_data in active_books.items():
        outline = book_data.get("outline")
        if outline:
            books.append({
                "book_id": book_id,
                "title": outline.title,
                "author": outline.author,
                "genre": outline.genre.value,
                "chapters_generated": len(book_data.get("chapters", {})),
                "total_chapters": len(outline.chapters),
                "compiled": book_data.get("compiled") is not None,
                "exports_count": len(book_data.get("exports", [])),
                "created_at": book_data["created_at"]
            })

    return {"books": books, "total": len(books)}

@router.delete("/delete-book/{book_id}")
async def delete_book(book_id: str):
    """Delete a book project and all associated files"""
    if book_id not in active_books:
        raise HTTPException(status_code=404, detail="Book not found")

    # Remove from active books
    del active_books[book_id]

    # Clean up files (would implement proper cleanup in production)
    # For now, just return success

    return {"message": f"Book {book_id} deleted successfully"}

@router.get("/genres")
async def get_available_genres():
    """Get list of available book genres"""
    return {
        "genres": [
            {"value": genre.value, "label": genre.value.replace("_", " ").title()}
            for genre in BookGenre
        ]
    }

@router.get("/export-formats")
async def get_export_formats():
    """Get list of available export formats"""
    return {
        "formats": [
            {"value": "txt", "label": "Plain Text (.txt)", "description": "Universal baseline format"},
            {"value": "html", "label": "HTML (.html)", "description": "Self-contained styled web format"},
            {"value": "json", "label": "JSON (.json)", "description": "Full structured payload for downstream processing"},
            {"value": "epub", "label": "EPUB (.epub)", "description": "Standard eBook format for e-readers"},
            {"value": "m4b", "label": "M4B (.m4b)", "description": "Enhanced audiobook format with chapters"}
        ]
    }