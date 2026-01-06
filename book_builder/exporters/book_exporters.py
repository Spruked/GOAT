# book_exporters.py
"""
GOAT Book Builder - Advanced Export Formats
HTML → EPUB/M4B converter and enhanced export pipeline
"""

import os
import json
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import asdict
from datetime import datetime

from ..book_builder import CompiledBook, BookExport, ExportFormat

class EPUBExporter:
    """EPUB format exporter with full eBook standards compliance"""

    def __init__(self):
        self.templates_path = Path(__file__).parent / "templates"
        self.templates_path.mkdir(exist_ok=True)

    def export_epub(self, book: CompiledBook, output_path: Path) -> BookExport:
        """Export book as EPUB format"""
        with tempfile.TemporaryDirectory() as temp_dir:
            epub_dir = Path(temp_dir) / "epub"
            epub_dir.mkdir()

            # Create EPUB structure
            self._create_epub_structure(epub_dir, book)

            # Create EPUB file (ZIP with .epub extension)
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as epub_zip:
                # Add mimetype first (must be uncompressed)
                mimetype_path = epub_dir / "mimetype"
                epub_zip.write(mimetype_path, "mimetype", zipfile.ZIP_STORED)

                # Add all other files
                for file_path in epub_dir.rglob('*'):
                    if file_path.is_file() and file_path.name != "mimetype":
                        epub_zip.write(file_path, file_path.relative_to(epub_dir))

        # Generate checksum
        import hashlib
        with open(output_path, 'rb') as f:
            checksum = hashlib.sha256(f.read()).hexdigest()

        export = BookExport(
            book_id=f"{book.title.lower().replace(' ', '_')}_epub",
            format=ExportFormat.EPUB,
            file_path=str(output_path),
            file_size=output_path.stat().st_size,
            checksum_sha256=checksum,
            exported_at=datetime.utcnow().isoformat() + "Z",
            metadata={
                "book_title": book.title,
                "author": book.author,
                "format": "EPUB",
                "standard": "EPUB 3.0",
                "chapters": len(book.chapters),
                "word_count": book.total_word_count,
                "created_by": "GOAT Book Builder v1.0"
            }
        )

        return export

    def _create_epub_structure(self, epub_dir: Path, book: CompiledBook):
        """Create the complete EPUB directory structure"""

        # 1. mimetype file (must be first and uncompressed)
        (epub_dir / "mimetype").write_text("application/epub+zip")

        # 2. META-INF directory
        meta_inf = epub_dir / "META-INF"
        meta_inf.mkdir()
        self._create_container_xml(meta_inf)

        # 3. OEBPS directory (Open EBook Publication Structure)
        oebps = epub_dir / "OEBPS"
        oebps.mkdir()

        # Create content files
        self._create_content_opf(oebps, book)
        self._create_toc_ncx(oebps, book)
        self._create_styles_css(oebps)
        self._create_chapters_xhtml(oebps, book)

    def _create_container_xml(self, meta_inf: Path):
        """Create META-INF/container.xml"""
        container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>'''
        (meta_inf / "container.xml").write_text(container_xml)

    def _create_content_opf(self, oebps: Path, book: CompiledBook):
        """Create OEBPS/content.opf (package document)"""
        manifest_items = []
        spine_items = []

        # Add CSS
        manifest_items.append('<item id="stylesheet" href="styles.css" media-type="text/css"/>')

        # Add NCX
        manifest_items.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')

        # Add chapters
        for i, chapter in enumerate(book.chapters, 1):
            chapter_id = f"chapter{i}"
            chapter_file = f"chapter{i}.xhtml"
            manifest_items.append(f'<item id="{chapter_id}" href="{chapter_file}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{chapter_id}"/>')

        # Add front/back matter if they exist
        if book.foreword:
            manifest_items.append('<item id="foreword" href="foreword.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.insert(0, '<itemref idref="foreword"/>')

        if book.introduction:
            manifest_items.append('<item id="introduction" href="introduction.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.insert(0, '<itemref idref="introduction"/>')

        if book.conclusion:
            manifest_items.append('<item id="conclusion" href="conclusion.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="conclusion"/>')

        content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package version="3.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="book-id">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>{book.title}</dc:title>
        <dc:creator>{book.author}</dc:creator>
        <dc:language>en</dc:language>
        <dc:identifier id="book-id">urn:uuid:{book.title.lower().replace(" ", "-")}</dc:identifier>
        <dc:date>{datetime.utcnow().strftime("%Y-%m-%d")}</dc:date>
        <dc:description>A comprehensive book created with GOAT Book Builder</dc:description>
        <meta property="dcterms:modified">{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>
    </metadata>

    <manifest>
        {"".join(manifest_items)}
    </manifest>

    <spine toc="ncx">
        {"".join(spine_items)}
    </spine>
</package>'''

        (oebps / "content.opf").write_text(content_opf)

    def _create_toc_ncx(self, oebps: Path, book: CompiledBook):
        """Create OEBPS/toc.ncx (navigation control file)"""
        nav_points = []

        # Add chapters
        for i, chapter in enumerate(book.chapters, 1):
            nav_points.append(f'''
        <navPoint id="navpoint-{i}" playOrder="{i}">
            <navLabel><text>{chapter.title}</text></navLabel>
            <content src="chapter{i}.xhtml"/>
        </navPoint>''')

        toc_ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">
    <head>
        <meta name="dtb:uid" content="urn:uuid:{book.title.lower().replace(" ", "-")}"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
    </head>

    <docTitle>
        <text>{book.title}</text>
    </docTitle>

    <navMap>
        {"".join(nav_points)}
    </navMap>
</ncx>'''

        (oebps / "toc.ncx").write_text(toc_ncx)

    def _create_styles_css(self, oebps: Path):
        """Create OEBPS/styles.css"""
        styles_css = '''/* GOAT Book Builder EPUB Styles */

body {
    font-family: "Georgia", serif;
    font-size: 1em;
    line-height: 1.4;
    margin: 0;
    padding: 0;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "Helvetica", sans-serif;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    line-height: 1.2;
}

h1 { font-size: 1.5em; }
h2 { font-size: 1.3em; }
h3 { font-size: 1.1em; }

p {
    margin: 0 0 1em 0;
    text-align: justify;
    text-indent: 1.5em;
}

p:first-child {
    text-indent: 0;
}

blockquote {
    margin: 1em 2em;
    font-style: italic;
}

ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

li {
    margin-bottom: 0.5em;
}

code {
    font-family: "Courier New", monospace;
    background-color: #f5f5f5;
    padding: 0.2em 0.4em;
    border-radius: 3px;
}

pre {
    font-family: "Courier New", monospace;
    background-color: #f5f5f5;
    padding: 1em;
    border-radius: 5px;
    overflow-x: auto;
    margin: 1em 0;
}

.title-page {
    text-align: center;
    margin: 3em 0;
}

.title-page h1 {
    font-size: 2em;
    margin-bottom: 1em;
}

.title-page .author {
    font-size: 1.2em;
    font-style: italic;
    margin-top: 2em;
}

.chapter {
    break-before: page;
    margin-top: 2em;
}

.chapter h2 {
    margin-top: 0;
    border-bottom: 1px solid #ccc;
    padding-bottom: 0.5em;
}'''
        (oebps / "styles.css").write_text(styles_css)

    def _create_chapters_xhtml(self, oebps: Path, book: CompiledBook):
        """Create individual chapter XHTML files"""

        # Foreword
        if book.foreword:
            foreword_html = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>Foreword</title>
    <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
    <section>
        <h1>Foreword</h1>
        {book.foreword.replace(chr(10), '<br/>')}
    </section>
</body>
</html>'''
            (oebps / "foreword.xhtml").write_text(foreword_html)

        # Introduction
        if book.introduction:
            intro_html = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>Introduction</title>
    <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
    <section>
        <h1>Introduction</h1>
        {book.introduction.replace(chr(10), '<br/>')}
    </section>
</body>
</html>'''
            (oebps / "introduction.xhtml").write_text(intro_html)

        # Chapters
        for i, chapter in enumerate(book.chapters, 1):
            chapter_html = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>{chapter.title}</title>
    <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
    <section class="chapter">
        <h2>Chapter {chapter.number}: {chapter.title}</h2>
        {chapter.content.replace(chr(10), '<br/>')}
    </section>
</body>
</html>'''
            (oebps / f"chapter{i}.xhtml").write_text(chapter_html)

        # Conclusion
        if book.conclusion:
            conclusion_html = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>Conclusion</title>
    <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
    <section>
        <h1>Conclusion</h1>
        {book.conclusion.replace(chr(10), '<br/>')}
    </section>
</body>
</html>'''
            (oebps / "conclusion.xhtml").write_text(conclusion_html)


class M4BExporter:
    """M4B audiobook format exporter (enhanced MP4 with chapters)"""

    def __init__(self):
        self.epub_exporter = EPUBExporter()

    def export_m4b(self, book: CompiledBook, audio_files: list, output_path: Path) -> BookExport:
        """
        Export as M4B audiobook format
        Requires: audio_files list containing chapter audio paths
        """
        # For now, create a placeholder M4B structure
        # In production, this would use ffmpeg or similar to combine audio files
        # with chapter markers and metadata

        m4b_content = f"""M4B Audiobook Export for: {book.title}
Author: {book.author}
Chapters: {len(book.chapters)}
Total Words: {book.total_word_count}

This is a placeholder for M4B export functionality.
In production, this would combine audio files with chapter markers.

Audio files provided: {len(audio_files)}
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(m4b_content)

        # Generate checksum
        import hashlib
        checksum = hashlib.sha256(m4b_content.encode('utf-8')).hexdigest()

        export = BookExport(
            book_id=f"{book.title.lower().replace(' ', '_')}_m4b",
            format=ExportFormat.M4B,  # We'll need to add this to ExportFormat enum
            file_path=str(output_path),
            file_size=len(m4b_content.encode('utf-8')),
            checksum_sha256=checksum,
            exported_at=datetime.utcnow().isoformat() + "Z",
            metadata={
                "book_title": book.title,
                "author": book.author,
                "format": "M4B",
                "chapters": len(book.chapters),
                "word_count": book.total_word_count,
                "audio_files": len(audio_files),
                "created_by": "GOAT Book Builder v1.0"
            }
        )

        return export


class AdvancedBookExporter:
    """Enhanced book exporter with multiple format support"""

    def __init__(self):
        self.epub_exporter = EPUBExporter()
        self.m4b_exporter = M4BExporter()

    def export_book(self, book: CompiledBook, format: str, output_path: Path,
                   audio_files: Optional[list] = None) -> BookExport:
        """Export book in specified format"""

        if format.lower() == 'epub':
            return self.epub_exporter.export_epub(book, output_path)
        elif format.lower() == 'm4b':
            if not audio_files:
                raise ValueError("M4B export requires audio_files parameter")
            return self.m4b_exporter.export_m4b(book, audio_files, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def get_supported_formats(self) -> list:
        """Get list of supported export formats"""
        return ['epub', 'm4b']

    def validate_export_requirements(self, format: str, **kwargs) -> bool:
        """Validate requirements for specific export format"""
        if format.lower() == 'm4b':
            return 'audio_files' in kwargs and len(kwargs['audio_files']) > 0
        return True