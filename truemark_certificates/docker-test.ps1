#!/usr/bin/env pwsh
# Docker Build & Test Script for TrueMark Certificate Forge

Write-Host "🔨 Building TrueMark Certificate Forge Docker Image..." -ForegroundColor Cyan

# Build the image
docker build -t truemark/certificate-forge:v2.0 .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
    
    Write-Host "`n📦 Image Details:" -ForegroundColor Cyan
    docker images truemark/certificate-forge:v2.0
    
    Write-Host "`n🚀 Starting container with docker-compose..." -ForegroundColor Cyan
    docker-compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Container started successfully!" -ForegroundColor Green
        
        Start-Sleep -Seconds 3
        
        Write-Host "`n📊 Testing SKG metrics..." -ForegroundColor Cyan
        docker exec truemark-certificate-forge python certificate_forge.py --skg
        
        Write-Host "`n🎉 Docker deployment complete!" -ForegroundColor Green
        Write-Host "`nUseful commands:" -ForegroundColor Yellow
        Write-Host "  docker exec truemark-certificate-forge python certificate_forge.py --help"
        Write-Host "  docker exec truemark-certificate-forge python certificate_forge.py --stats"
        Write-Host "  docker logs truemark-certificate-forge"
        Write-Host "  docker-compose down"
    }
} else {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}
