#!/usr/bin/env python3
"""
Simple GOAT backend starter
"""

import sys
import os

# Add paths
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
dals_path = os.path.join(os.path.dirname(__file__), 'DALS')

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
if dals_path not in sys.path:
    sys.path.insert(0, dals_path)

print("Starting GOAT Backend...")
print(f"Backend path: {backend_path}")
print(f"DALS path: {dals_path}")

try:
    from app.main import app
    print("App imported successfully")

    import uvicorn
    print("Starting server on http://0.0.0.0:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()