@echo off
echo Starting GOAT Backend...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Start the backend server
echo Starting server on http://0.0.0.0:5000
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 5000 --reload

pause