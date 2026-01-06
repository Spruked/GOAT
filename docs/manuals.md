<!-- docs/manuals.md -->
# Manual Generation — GOAT Documentation

This document describes the Manual Generation subsystem introduced in GOAT. It covers the purpose, API endpoints, sample requests, response formats, engine architecture, testing, and integration notes.

## Overview

GOAT now supports programmatic generation of practical documentation as a separate offering from long-form books. The Manual Generation subsystem is optimized for clear, scannable, instructional content such as:

- User Manuals (software, apps, consumer products)
- Owner's Manuals (equipment, appliances, vehicles)
- Training Manuals (courses, workshops, onboarding materials)

Manuals prioritize clarity, safety information, troubleshooting, and maintenance workflows rather than narrative flow.

## Design Principles

- Structured sections for rapid scanning (Introduction, Getting Started, Usage, Troubleshooting, Safety, Maintenance)
- Reuse of GOAT's NLP stack (DeepParser) to structure free-form inputs
- Simple JSON-first API for easy automation and integration
- Separate from the book-generation pipeline so templates and formatting remain focused on technical documentation

## Engine & Files

- Core engine: `engines/manual_engine.py` (ManualEngine)
- API routes: `routes/manuals.py`
- Tests: `test_manual_generation.py`
- Auxiliary: uses `engines/deep_parser.py` and `engines/summarization_engine.py` when helpful

## API Endpoints

Base path: `/manuals`

1) Generate User Manual

  - POST /manuals/user-manual

  Request body (JSON):

  ```json
  {
    "product_name": "GOAT Writing Assistant",
    "features": ["AI-powered content generation", "Multi-format output"],
    "instructions": {
      "getting_started": "Install and create account",
      "basic_usage": "Select template and write",
      "advanced_features": "Use AI suggestions for enhanced content",
      "troubleshooting": "Check internet connection and restart if needed",
      "safety": "Do not share sensitive information"
    }
  }
  ```

  Response (successful):

  ```json
  {
    "success": true,
    "manual_id": "<uuid>",
    "manual": { /* manual JSON structure with `title`, `type`, `generated_at`, and `sections` */ },
    "message": "User manual generated successfully"
  }
  ```

2) Generate Owner's Manual

  - POST /manuals/owner-manual

  Request body (JSON):

  ```json
  {
    "product_name": "Industrial Coffee Machine",
    "specifications": {
      "power": "220V, 50Hz",
      "capacity": "50 cups/hour",
      "dimensions": "30x40x50 cm"
    },
    "maintenance": {
      "daily_cleaning": "Wipe exterior and empty grounds.",
      "weekly_maintenance": "Descale with vinegar solution."
    }
  }
  ```

3) Generate Training Manual

  - POST /manuals/training-manual

  Request body (JSON):

  ```json
  {
    "topic": "Advanced Python Programming",
    "objectives": ["Master object-oriented programming", "Implement design patterns"],
    "content": {
      "prerequisites": "Basic Python knowledge",
      "module_1": "Introduction to OOP principles",
      "module_2": "Design patterns implementation",
      "exercises": "Complete coding assignments for each module"
    }
  }
  ```

4) Get Manual Types

  - GET /manuals/types

  Returns a JSON object describing supported manual types and required fields.

## Examples

Curl (PowerShell / bash):

```bash
curl -X POST "http://localhost:5000/manuals/user-manual" \
  -H "Content-Type: application/json" \
  -d @user_manual_request.json
```

Python example (requests):

```python
import requests

payload = {
    "product_name": "GOAT Writing Assistant",
    "features": ["AI-powered content generation"],
    "instructions": {"getting_started": "Install and run"}
}

resp = requests.post("http://localhost:5000/manuals/user-manual", json=payload)
print(resp.status_code)
print(resp.json())
```

## Testing

Run the included unit-style script for quick validation:

```pwsh
python test_manual_generation.py
```

Or run PyTest if you have tests integrated:

```pwsh
pytest -q
```

## Integration Notes

- Manuals are intentionally separate from the book/authoring pipeline; if you need a combined workflow (e.g., export chapter summaries as manual appendices), call the manual engine explicitly from your orchestration logic.
- Output is JSON-first; downstream systems can convert to PDF, DOCX, or HTML using templating libraries (not included in this release).

## Next Steps / Roadmap

- Add export templates (PDF, DOCX)
- Add multi-language generation
- Add template selection (concise vs. full)
- Add versioning & edit history for manuals

---

IMPORTANT: You asked not to push these changes yet — this documentation is created locally in `docs/manuals.md` and `MANUAL_GENERATION_README.md`. No remote operations were performed.
