# Start GOAT Backend
Write-Host "Starting GOAT Backend..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

# Start the backend server
Write-Host "Starting server on http://0.0.0.0:5000" -ForegroundColor Yellow
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 5000 --reload