#!/bin/bash
# GOAT v2.1 Quick Start Script for Unix/Linux/Mac

echo "🐐 GOAT v2.1 - The Proven Teacher"
echo "================================="
echo ""

# Check if Docker is running
echo "Checking Docker..."
if docker info > /dev/null 2>&1; then
    echo "✓ Docker is running"
else
    echo "✗ Docker is not running. Please start Docker."
    exit 1
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ Created .env - Please edit with your keys!"
fi

# Create data directories
echo "Creating data directories..."
mkdir -p data/vault
mkdir -p data/knowledge
echo "✓ Data directories created"

# Build and start services
echo ""
echo "Building and starting services..."
echo "This may take a few minutes on first run..."
echo ""

docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ GOAT v2.1 is running!"
    echo ""
    echo "Access the application:"
    echo "  Frontend:  http://localhost:5173"
    echo "  API:       http://localhost:5000"
    echo "  API Docs:  http://localhost:5000/docs"
    echo "  Neo4j:     http://localhost:7474"
    echo ""
    echo "To view logs:  docker-compose logs -f"
    echo "To stop:       docker-compose down"
    echo ""
else
    echo "✗ Failed to start services"
    exit 1
fi
