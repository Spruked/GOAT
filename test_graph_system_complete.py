#!/usr/bin/env python3
"""
Comprehensive Graph System Test Suite
Tests the complete graph visualization pipeline from backend to frontend
"""

import requests
import json
import time
import os
import sys
from pathlib import Path

class GraphSystemTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def test_backend_health(self):
        """Test that the backend is running and graph routes are available"""
        print("🔍 Testing backend health...")

        try:
            response = self.session.get(f"{self.base_url}/graphs/test")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend health check passed: {data}")
                return True
            else:
                print(f"❌ Backend health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Backend connection failed: {e}")
            return False

    def test_graph_html_generation(self):
        """Test graph HTML generation with sample data"""
        print("\n🧠 Testing graph HTML generation...")

        test_payload = {
            "concepts": {
                "Abby": ["Love", "Loss", "Courage"],
                "Butch": ["Legacy", "Strength"],
                "Angela": ["Trauma", "Conflict"],
                "Marcus": ["Hope", "Redemption"]
            },
            "graph_type": "concepts",
            "title": "Test Concept Graph"
        }

        try:
            response = self.session.post(
                f"{self.base_url}/graphs/html",
                json=test_payload,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                data = response.json()
                graph_url = data.get('graph_url')
                print(f"✅ Graph HTML generated: {graph_url}")

                # Test that the generated file exists
                if graph_url:
                    file_response = self.session.get(f"{self.base_url}{graph_url}")
                    if file_response.status_code == 200:
                        print("✅ Generated graph file is accessible")
                        return True
                    else:
                        print(f"❌ Generated graph file not accessible: {file_response.status_code}")
                        return False
                else:
                    print("❌ No graph_url in response")
                    return False
            else:
                print(f"❌ Graph generation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Graph generation error: {e}")
            return False

    def test_concept_html_legacy_endpoint(self):
        """Test the legacy concept-html endpoint"""
        print("\n📚 Testing legacy concept-html endpoint...")

        test_payload = {
            "concepts": {
                "Character1": ["Trait1", "Trait2"],
                "Character2": ["Trait3", "Trait4"]
            }
        }

        try:
            response = self.session.post(
                f"{self.base_url}/graphs/concept-html",
                json=test_payload,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                data = response.json()
                graph_url = data.get('graph_url')
                print(f"✅ Legacy endpoint generated: {graph_url}")
                return True
            else:
                print(f"❌ Legacy endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Legacy endpoint error: {e}")
            return False

    def test_uqv_system(self):
        """Test the Unanswered Query Vault system"""
        print("\n🗄️ Testing Unanswered Query Vault system...")

        # Test vaulting a query
        vault_payload = {
            "user_id": "test_user",
            "query_text": "What is the meaning of life?",
            "vault_reason": "No matching concepts found"
        }

        try:
            response = self.session.post(
                f"{self.base_url}/uqv/vault",
                json=vault_payload,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print("✅ Query successfully vaulted")
            else:
                print(f"⚠️ Query vaulting failed: {response.status_code} - {response.text}")

            # Test retrieving vaulted queries
            response = self.session.get(f"{self.base_url}/uqv/queries/test_user")
            if response.status_code == 200:
                queries = response.json()
                print(f"✅ Retrieved {len(queries)} vaulted queries")
                return True
            else:
                print(f"❌ Query retrieval failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ UQV system error: {e}")
            return False

    def test_frontend_accessibility(self):
        """Test that frontend can access the graph demo page"""
        print("\n🌐 Testing frontend accessibility...")

        try:
            # Test if the frontend is serving (this assumes frontend is on port 3000)
            frontend_url = "http://localhost:3000"
            response = self.session.get(f"{frontend_url}/graph-demo", allow_redirects=True)

            if response.status_code == 200:
                print("✅ Frontend graph demo page is accessible")
                return True
            else:
                print(f"⚠️ Frontend may not be running or accessible: {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️ Frontend connection failed (may not be running): {e}")
            return False

    def run_full_test_suite(self):
        """Run the complete test suite"""
        print("🚀 Starting GOAT Graph System Test Suite")
        print("=" * 50)

        tests = [
            ("Backend Health", self.test_backend_health),
            ("Graph HTML Generation", self.test_graph_html_generation),
            ("Legacy Concept-HTML", self.test_concept_html_legacy_endpoint),
            ("UQV System", self.test_uqv_system),
            ("Frontend Accessibility", self.test_frontend_accessibility)
        ]

        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                results.append((test_name, False))

        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)

        passed = 0
        total = len(results)

        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
            if result:
                passed += 1

        print(f"\nOverall: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! Graph system is fully operational.")
            return True
        else:
            print("⚠️ Some tests failed. Check the output above for details.")
            return False

def main():
    """Main test runner"""
    import argparse

    parser = argparse.ArgumentParser(description="GOAT Graph System Test Suite")
    parser.add_argument("--url", default="http://localhost:8000",
                       help="Base URL of the GOAT backend (default: http://localhost:8000)")
    parser.add_argument("--quick", action="store_true",
                       help="Run only critical tests (backend health and graph generation)")

    args = parser.parse_args()

    tester = GraphSystemTester(args.url)

    if args.quick:
        print("🏃 Running quick test suite...")
        success = (
            tester.test_backend_health() and
            tester.test_graph_html_generation()
        )
    else:
        success = tester.run_full_test_suite()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()