#!/usr/bin/env python3
"""
Test script for CALI Scripts and Caleon Generative API endpoints
"""

import requests
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

BASE_URL = "http://localhost:5000"

def test_cali_scripts_api():
    """Test CALI Scripts API endpoints"""
    print("🧪 Testing CALI Scripts API")
    print("=" * 40)

    # Test basic script endpoint
    try:
        response = requests.post(f"{BASE_URL}/api/cali-scripts/", json={
            "category": "greetings",
            "entry": "welcome_dashboard",
            "variables": {"name": "TestUser"}
        })
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Basic script: {data['script'][:50]}...")
        else:
            print(f"❌ Basic script failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Basic script error: {e}")

    # Test categories endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/cali-scripts/categories")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Categories: {len(data['categories'])} available")
        else:
            print(f"❌ Categories failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Categories error: {e}")

    # Test convenience endpoints
    try:
        response = requests.post(f"{BASE_URL}/api/cali-scripts/greet", json={
            "category": "greetings",
            "entry": "first_time",
            "variables": {}
        })
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Convenience endpoint: {data['script'][:50]}...")
        else:
            print(f"❌ Convenience endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Convenience endpoint error: {e}")

def test_caleon_generative_api():
    """Test Caleon Generative API endpoints"""
    print("\n🧠 Testing Caleon Generative API")
    print("=" * 40)

    # Test generate endpoint
    try:
        response = requests.post(f"{BASE_URL}/api/caleon/generate", json={
            "message": "Hello Caleon, how are you?",
            "context": {"test": True},
            "timestamp": "2025-11-25T12:00:00Z"
        })
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generate response: {data['response'][:50]}...")
        else:
            print(f"❌ Generate failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Generate error: {e}")

    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/caleon/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

    # Test streaming endpoint (basic connectivity)
    try:
        response = requests.post(f"{BASE_URL}/api/caleon/stream", json={
            "message": "Test streaming",
            "context": {},
            "timestamp": "2025-11-25T12:00:00Z"
        }, stream=True)
        if response.status_code == 200:
            print("✅ Streaming endpoint connected")
            # Don't read the full stream for this test
        else:
            print(f"❌ Streaming failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Streaming error: {e}")

def test_server_health():
    """Test basic server health"""
    print("\n🏥 Testing Server Health")
    print("=" * 40)

    try:
        response = requests.get(f"{BASE_URL}/test")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server health: {data['status']}")
            return True
        else:
            print(f"❌ Server health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server connection error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 CALI Scripts & Caleon Generative API Test Suite")
    print("=" * 60)

    # Check server health first
    if not test_server_health():
        print("\n❌ Server not running. Please start the server first:")
        print("cd server && python -m uvicorn main:app --host 0.0.0.0 --port 5000")
        sys.exit(1)

    # Run API tests
    test_cali_scripts_api()
    test_caleon_generative_api()

    print("\n🎉 API Tests Complete!")
    print("\n📋 Summary:")
    print("- CALI Scripts provide consistent, non-LLM responses")
    print("- Caleon Generative provides dynamic AI responses")
    print("- Frontend can use both via React hooks")
    print("- Bubble Assistant now has dual intelligence modes")

if __name__ == "__main__":
    main()