# routes/upload.py
"""
Secure file upload routes with pre-signed URLs
"""

import boto3
from botocore.client import Config
from fastapi import APIRouter, Depends, HTTPException
# from slowapi import Limiter
# from slowapi.util import get_remote_address
from server.auth import get_current_user
from models.user import User
from models import get_db
from sqlalchemy.orm import Session
import uuid
import os

router = APIRouter(prefix="/upload", tags=["upload"])

# Rate limiter for uploads
# limiter = Limiter(key_func=get_remote_address)

# Cloudflare R2 / S3 configuration
# In production, move these to environment variables
R2_ENDPOINT = os.getenv("R2_ENDPOINT", "https://<accountid>.r2.cloudflarestorage.com")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY", "your-access-key")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY", "your-secret-key")
R2_BUCKET = os.getenv("R2_BUCKET", "goat-files")

# Initialize R2/S3 client
try:
    r2_client = boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(signature_version="s3v4"),
    )
except Exception as e:
    print(f"R2 client initialization failed: {e}")
    r2_client = None

MAX_FILE_SIZE_MB = 250

@router.post("/presigned-url")
# @limiter.limit("20/minute")  # Rate limit uploads
async def get_presigned_url(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """
    Generate pre-signed URL for secure file upload
    Files are uploaded directly to R2/S3 without touching our servers
    """
    # Validate filename
    if not filename or len(filename.encode()) > 200:
        raise HTTPException(400, "Invalid filename")

    # Generate unique file ID and key
    file_id = str(uuid.uuid4())
    key = f"{current_user.id}/{file_id}/{filename}"

    try:
        # Generate pre-signed URL
        url = r2_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": R2_BUCKET,
                "Key": key,
                "ContentType": "application/octet-stream",
                "Metadata": {
                    "user_id": str(current_user.id),
                    "original_name": filename,
                    "file_id": file_id
                }
            },
            ExpiresIn=600,  # 10 minutes
            HttpMethod="PUT"
        )

        return {
            "upload_url": url,
            "file_id": file_id,
            "key": key,
            "expires_in": 600
        }

    except Exception as e:
        raise HTTPException(500, f"Failed to generate upload URL: {str(e)}")

@router.post("/complete")
async def complete_upload(
    file_id: str,
    filename: str,
    file_size: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Called after successful upload to create database record
    Inject SKG bootstrap for knowledge graph clustering
    """
    from models.user_file import UserFile
    from datetime import datetime

    # Validate file size
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, "File too large")

    # Create database record
    try:
        # Determine file type from extension
        file_type = filename.split('.')[-1].lower() if '.' in filename else 'unknown'

        user_file = UserFile(
            user_id=current_user.id,
            original_filename=filename,
            clean_filename=filename,  # Could be cleaned up later
            file_type=file_type,
            file_size=file_size,
            storage_path=f"r2://{R2_BUCKET}/{current_user.id}/{file_id}/{filename}",
            status="uploaded"
        )

        db.add(user_file)

        # Update user stats
        current_user.file_count += 1

        db.commit()
        db.refresh(user_file)

        # Extract text from uploaded file for SKG processing
        raw_text = ""
        try:
            import tempfile
            # Download file from R2
            r2_obj = r2_client.get_object(Bucket=R2_BUCKET, Key=f"{current_user.id}/{file_id}/{filename}")
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp:
                tmp.write(r2_obj['Body'].read())
                tmp_path = tmp.name

            # Simple text extraction
            if file_type.lower() in ['txt', 'md']:
                with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
                    raw_text = f.read()
            else:
                # For PDFs and other formats, use basic extraction or placeholder
                try:
                    with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
                        raw_text = f.read()
                except:
                    raw_text = f"File uploaded: {filename} ({file_type})"
        except Exception as e:
            print(f"Text extraction error: {e}")
            raw_text = f"File uploaded: {filename} ({file_type})"

        # 🚀 GOAT-local SKG: instant structure
        try:
            from skg import SKGCore
            skg = SKGCore()
            clusters = skg.bootstrap_from_text(raw_text, user_id=str(current_user.id), file_id=str(user_file.id))
            user_file.skg_clusters = [c.id for c in clusters]
        except Exception as e:
            print(f"Local SKG error: {e}")

        # 🧠 Mirror to UCM: second-order cognition
        try:
            import requests
            requests.post("http://localhost:8001/ucm/ingest", json={
                "user_id": str(current_user.id),
                "file_id": str(user_file.id),
                "raw_text": raw_text,
                "local_clusters": [c.to_dict() for c in clusters]
            }, timeout=10)
        except Exception as e:
            print(f"UCM mirror error: {e}")

        # 🧬 Caleon fusion: cross-user cognition evolution
        try:
            import time
            requests.post("http://localhost:8000/api/caleon/ingest_clusters", json={
                "user_id": str(current_user.id),
                "worker": "upload_pipeline",
                "clusters": [c.to_dict() for c in clusters],
                "timestamp": time.time()
            }, timeout=3)
        except Exception as e:
            print(f"Caleon ingestion error: {e}")

        return {
            "file_id": user_file.id,
            "status": "uploaded",
            "message": "File uploaded successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Failed to save file record: {str(e)}")