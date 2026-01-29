#!/usr/bin/env python3
"""
Test script for SKG GOAT Edition frontend
"""
import subprocess
import sys
import time
import requests
from pathlib import Path

def test_frontend():
    """Test the frontend build and basic functionality"""
    print("🧪 Testing SKG GOAT Edition Frontend")
    print("=" * 50)

    frontend_dir = Path("frontend")

    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False

    try:
        # Check if package.json exists
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            print("❌ package.json not found in frontend directory")
            return False

        print("1. Installing frontend dependencies...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ npm install failed: {result.stderr}")
            return False

        print("✅ Dependencies installed successfully")

        print("2. Building frontend...")
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ Build failed: {result.stderr}")
            return False

        print("✅ Frontend built successfully")

        print("3. Checking build output...")
        dist_dir = frontend_dir / "dist"
        if not dist_dir.exists():
            print("❌ dist directory not created")
            return False

        index_html = dist_dir / "index.html"
        if not index_html.exists():
            print("❌ index.html not found in dist")
            return False

        print("✅ Build artifacts verified")

        print("\n🎉 Frontend tests completed!")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_frontend()
    sys.exit(0 if success else 1)