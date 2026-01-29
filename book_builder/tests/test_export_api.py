# test_export_api.py
"""
Test script for Book Builder export API endpoints
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:5000"

def test_export_formats():
    """Test getting available export formats"""
    response = requests.get(f"{BASE_URL}/api/book-builder/export-formats")
    if response.status_code == 200:
        formats = response.json()
        print("✅ Available export formats:")
        for fmt in formats['formats']:
            print(f"  - {fmt['label']}: {fmt['description']}")
        return True
    else:
        print(f"❌ Failed to get export formats: {response.status_code}")
        return False

def test_book_creation():
    """Test creating a book outline"""
    book_data = {
        "title": "API Test Book",
        "author": "Test Author",
        "genre": "non_fiction",
        "topic": "API Testing",
        "target_audience": "developers",
        "word_count_goal": 5000,
        "key_themes": ["testing", "api", "automation"],
        "source_materials": ["docs", "examples"]
    }

    response = requests.post(
        f"{BASE_URL}/api/book-builder/create-outline",
        json=book_data
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Book outline created: {result['book_id']}")
        return result['book_id']
    else:
        print(f"❌ Failed to create book: {response.status_code}")
        print(response.text)
        return None

def test_chapter_generation(book_id):
    """Test generating chapters"""
    # Generate first chapter
    response = requests.post(
        f"{BASE_URL}/api/book-builder/generate-chapter/{book_id}",
        json={"chapter_number": 1}
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Chapter 1 generated: {result['chapter']['title']}")
        return True
    else:
        print(f"❌ Failed to generate chapter: {response.status_code}")
        return False

def test_book_compilation(book_id):
    """Test compiling the book"""
    response = requests.post(f"{BASE_URL}/api/book-builder/compile-book/{book_id}")

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Book compiled: {result['compiled_book']['total_word_count']} words")
        return True
    else:
        print(f"❌ Failed to compile book: {response.status_code}")
        return False

def test_epub_export(book_id):
    """Test EPUB export"""
    export_data = {
        "format": "epub",
        "output_filename": f"api_test_book_{book_id}.epub"
    }

    response = requests.post(
        f"{BASE_URL}/api/book-builder/export-book/{book_id}",
        json=export_data
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ EPUB exported: {result['export']['file_path']}")

        # Test download
        download_url = result['download_url']
        download_response = requests.get(f"{BASE_URL}{download_url}")
        if download_response.status_code == 200:
            print(f"✅ EPUB download successful: {len(download_response.content)} bytes")
            return True
        else:
            print(f"❌ EPUB download failed: {download_response.status_code}")
            return False
    else:
        print(f"❌ EPUB export failed: {response.status_code}")
        print(response.text)
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Book Builder Export API")
    print("=" * 50)

    # Test 1: Get export formats
    if not test_export_formats():
        return

    # Test 2: Create book
    book_id = test_book_creation()
    if not book_id:
        return

    # Wait a moment for processing
    time.sleep(1)

    # Test 3: Generate chapter
    if not test_chapter_generation(book_id):
        return

    # Test 4: Compile book
    if not test_book_compilation(book_id):
        return

    # Test 5: Export as EPUB
    if not test_epub_export(book_id):
        return

    print("=" * 50)
    print("🎉 All tests passed! Book Builder export API is working correctly.")

if __name__ == "__main__":
    main()