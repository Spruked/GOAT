# TrueMark Certificate Forge - Docker Image
FROM python:3.11-slim

LABEL maintainer="Bryan A. Spruk <bryan@truemark.io>"
LABEL description="TrueMark Enterprise Certificate Forge v2.0 with SKG Integration"

# Set working directory
WORKDIR /app

# Install system dependencies for ReportLab and Pillow
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/vault/certificates/issued \
    /app/vault/events \
    /app/vault/skg \
    /app/keys \
    /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV VAULT_PATH=/app/vault

# Expose port for future API integration
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command shows help
CMD ["python", "certificate_forge.py", "--help"]
