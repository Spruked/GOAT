# Book Builder Export Formats

## Overview
The GOAT Book Builder now supports advanced export formats including EPUB and M4B, extending beyond the basic TXT/HTML/JSON formats.

## Supported Formats

### TXT (Plain Text)
- **File Extension**: `.txt`
- **Use Case**: Universal baseline, simple text processing
- **Features**: UTF-8 encoded, readable in any text editor

### HTML (HyperText Markup Language)
- **File Extension**: `.html`
- **Use Case**: Web publishing, self-contained documents
- **Features**: Styled content, responsive design, ready for web hosting

### JSON (JavaScript Object Notation)
- **File Extension**: `.json`
- **Use Case**: API integration, downstream processing by Audiobook/Podcast engines
- **Features**: Full structured data, machine-readable, preserves all metadata

### EPUB (Electronic Publication)
- **File Extension**: `.epub`
- **Use Case**: E-book readers, digital publishing
- **Features**:
  - EPUB 3.0 standard compliance
  - Table of contents (NCX)
  - Chapter navigation
  - Professional formatting
  - Compatible with Kindle, Apple Books, etc.

### M4B (MPEG-4 Audiobook)
- **File Extension**: `.m4b`
- **Use Case**: Audiobook production, enhanced podcasts
- **Features**:
  - Chapter markers embedded in audio file
  - Enhanced metadata
  - Optimized for audio playback
  - Compatible with Apple Books, Audible, etc.

## API Usage

### Get Available Formats
```http
GET /api/book-builder/export-formats
```

### Export Book
```http
POST /api/book-builder/export-book/{book_id}
Content-Type: application/json

{
  "format": "epub",
  "output_filename": "my_book.epub",
  "audio_files": ["chapter1.mp3", "chapter2.mp3"]  // For M4B only
}
```

### Download Export
```http
GET /api/book-builder/download/{book_id}/{filename}
```

## Technical Implementation

### EPUB Structure
```
book.epub (ZIP file)
├── mimetype
├── META-INF/
│   └── container.xml
└── OEBPS/
    ├── content.opf (package document)
    ├── toc.ncx (navigation)
    ├── styles.css
    ├── foreword.xhtml (optional)
    ├── introduction.xhtml (optional)
    ├── chapter1.xhtml
    ├── chapter2.xhtml
    └── conclusion.xhtml (optional)
```

### M4B Structure
- Enhanced MP4 container with audio streams
- Embedded chapter markers
- Rich metadata (title, author, chapters)
- Optimized for audiobook applications

## Integration Points

### Audiobook Engine
- Consumes JSON export for SSML generation
- Uses M4B export for final audio compilation
- Inherits chapter structure and metadata

### Podcast Engine
- Uses JSON export for script generation
- Leverages chapter metadata for dual-voice processing
- Feeds into RSS generation pipeline

### Vault Storage
- All exports stored as immutable glyphs
- Full lineage tracking from outline to final format
- Cryptographic integrity verification

## Quality Assurance

- **EPUB Validation**: Generated files pass EPUBCheck validation
- **M4B Compliance**: Follows audiobook format standards
- **Cross-Platform**: Tested on major e-readers and audio players
- **Performance**: Efficient generation, minimal memory footprint

## Future Extensions

- **PDF Export**: HTML → PDF conversion pipeline
- **DOCX Export**: Microsoft Word format support
- **Advanced EPUB**: Custom styling, embedded fonts
- **Audiobook Chapters**: Automatic chapter marker insertion