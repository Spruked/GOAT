#!/usr/bin/env pwsh
# GOAT v2.1 Quick Start Script for Windows PowerShell

Write-Host "🐐 GOAT v2.1 - Greatest Of All Time" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
if (Get-Process "Docker Desktop" -ErrorAction SilentlyContinue) {
    Write-Host "✓ Docker is running" -ForegroundColor Green
} else {
    Write-Host "✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Create .env if it doesn't exist
if (-Not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env - Please edit with your keys!" -ForegroundColor Green
}

# Create data directories
Write-Host "Creating data directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data/vault" | Out-Null
New-Item -ItemType Directory -Force -Path "data/knowledge" | Out-Null
Write-Host "✓ Data directories created" -ForegroundColor Green

# Build and start services
Write-Host ""
Write-Host "Building and starting services..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Gray
Write-Host ""

docker-compose up --build -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ GOAT v2.1 is running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access the application:" -ForegroundColor Cyan
    Write-Host "  Frontend:  http://localhost:5173" -ForegroundColor White
    Write-Host "  API:       http://localhost:5000" -ForegroundColor White
    Write-Host "  API Docs:  http://localhost:5000/docs" -ForegroundColor White
    Write-Host "  Neo4j:     http://localhost:7474" -ForegroundColor White
    Write-Host ""
    Write-Host "To view logs:  docker-compose logs -f" -ForegroundColor Gray
    Write-Host "To stop:       docker-compose down" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "✗ Failed to start services" -ForegroundColor Red
    exit 1
}
