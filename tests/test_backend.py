#!/usr/bin/env python3
"""
Test script for SKG GOAT Edition backend
"""
import asyncio
import httpx
import json
import sys
from pathlib import Path

async def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:8000/api/v1"

    print("🧪 Testing SKG GOAT Edition Backend")
    print("=" * 50)

    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✅ Health check passed")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False

        # Test video creation endpoint (without auth for now)
        print("2. Testing video creation endpoint...")
        video_data = {
            "title": "Test Legacy Video",
            "description": "A test video for legacy preservation",
            "template": "documentary",
            "voice": "male_narrator",
            "content": "This is a test of the SKG GOAT video generation system."
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/video/create",
                json=video_data,
                headers={"Content-Type": "application/json"}
            )
            print(f"Video creation response: {response.status_code}")
            if response.status_code in [200, 201, 401]:  # 401 is expected without auth
                print("✅ Video endpoint accessible")
            else:
                print(f"❌ Video endpoint failed: {response.status_code}")
                print(response.text)

        print("3. Testing triples endpoint...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/triples/")
            print(f"Triples response: {response.status_code}")
            if response.status_code in [200, 401]:
                print("✅ Triples endpoint accessible")
            else:
                print(f"❌ Triples endpoint failed: {response.status_code}")

        print("\n🎉 Backend tests completed!")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_backend())
    sys.exit(0 if success else 1)