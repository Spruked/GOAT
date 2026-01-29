#!/usr/bin/env python3
"""
Start script for the backend FastAPI server
"""

import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import and run the app
from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("start_backend:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["backend"])