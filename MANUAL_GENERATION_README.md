# MANUAL_GENERATION_README.md
# GOAT Manual Generation System

## Overview

GOAT now supports generating various types of manuals as a separate offering from book creation. This includes user manuals, owner's manuals, training manuals, and other instructional documents.

## Features

- **User Manuals**: Product guides, software documentation, service instructions
- **Owner's Manuals**: Equipment maintenance, vehicle guides, appliance instructions
- **Training Manuals**: Educational content, course materials, workshop guides
- **Structured Output**: Consistent formatting with sections, subsections, and clear navigation

## API Endpoints

### Generate User Manual
```
POST /manuals/user-manual
```
**Request Body:**
```json
{
  "product_name": "GOAT Writing Assistant",
  "features": ["AI-powered content generation", "Multi-format output"],
  "instructions": {
    "getting_started": "Install and create account",
    "basic_usage": "Select template and write",
    "troubleshooting": "Check connection and restart"
  }
}
```

### Generate Owner's Manual
```
POST /manuals/owner-manual
```
**Request Body:**
```json
{
  "product_name": "Industrial Coffee Machine",
  "specifications": {
    "power": "220V, 50Hz",
    "capacity": "50 cups/hour"
  },
  "maintenance": {
    "daily_cleaning": "Wipe exterior",
    "weekly_maintenance": "Descale with vinegar"
  }
}
```

### Generate Training Manual
```
POST /manuals/training-manual
```
**Request Body:**
```json
{
  # GOAT Manual Generation System

  This document provides a quick reference for the Manual Generation features in GOAT. A fuller, interactive developer guide is available at `docs/manuals.md` (new in this branch/local workspace).

  ## Overview

  GOAT supports generating several types of manuals as a separate offering from book creation: user manuals, owner's manuals, and training manuals. These outputs are structured for clarity and usability rather than narrative storytelling.

  ## Features

  - User Manuals: Product guides, software docs, service instructions
  - Owner's Manuals: Equipment maintenance, installation, warranty
  - Training Manuals: Course outlines, exercises, assessments
  - Structured Output: Sections such as Introduction, Getting Started, Usage, Troubleshooting, and Maintenance

  ## Quick API Summary

  - POST `/manuals/user-manual` — generate a user manual
  - POST `/manuals/owner-manual` — generate an owner's manual
  - POST `/manuals/training-manual` — generate a training manual
  - GET  `/manuals/types` — list supported manual types and required fields

  See `docs/manuals.md` for examples, sample requests, and integration notes.

  ## Testing

  Run the included quick tests:

  ```pwsh
  python test_manual_generation.py
  ```

  ## Next Steps

  - Export templates (PDF/DOCX/HTML)
  - Multi-language support
  - Template selection and customization

  ---

  Note: This file is a companion README and the full developer documentation is in `docs/manuals.md`.