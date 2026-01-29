import requests
import sys

def check_service(name, url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name}: OK")
            return True
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: {str(e)[:50]}")
        return False

print("🔍 GOAT System Health Check")
print("=" * 40)

# Check if backend is running
backend_ok = check_service("GOAT Backend API", "http://localhost:8000/health")
docs_ok = check_service("API Documentation", "http://localhost:8000/docs")

# Check DALS
dals_ok = check_service("DALS Dashboard", "http://localhost:8000/dals/host/dashboard")

# Check Vault
vault_ok = check_service("Vault Stats", "http://localhost:8000/api/vault/stats")

# Check frontend
frontend_ok = check_service("Frontend", "http://localhost:5173")

# Summary
print("\n📊 Summary:")
total = 5
working = sum([backend_ok, docs_ok, dals_ok, vault_ok, frontend_ok])
print(f"Working: {working}/{total}")

if working == total:
    print("\n🎉 All systems operational!")
elif backend_ok:
    print("\n⚠️  Backend is running but some features may not be accessible")
else:
    print("\n🚨 Backend is not running - start it with: uvicorn main:app --reload --port 8000")
