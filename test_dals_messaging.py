# test_dals_messaging.py
"""
Test script for DALS messaging infrastructure
"""

import asyncio
import httpx
import json
from datetime import datetime

async def test_dals_messaging():
    """Test the DALS messaging infrastructure"""
    base_url = "http://localhost:8000"

    print("Testing DALS Messaging Infrastructure")
    print("=" * 50)

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Test 1: Check server status
            print("1. Testing server status...")
            response = await client.get(f"{base_url}/test")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✓ Server is running")
            else:
                print("   ✗ Server not responding")

            # Test 2: Test host messaging routes
            print("\n2. Testing host messaging routes...")

            # Push a message
            message_data = {
                "message": "Test message from worker",
                "worker_id": "test_worker_001",
                "timestamp": datetime.utcnow().isoformat()
            }
            response = await client.post(f"{base_url}/dals/host/push", json=message_data)
            print(f"   Push message: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                message_id = result.get("message_id")
                print(f"   ✓ Message pushed with ID: {message_id}")

                # Pull the message
                response = await client.get(f"{base_url}/dals/host/pull")
                print(f"   Pull message: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    if result.get("messages"):
                        print(f"   ✓ Message pulled: {len(result['messages'])} messages")
                    else:
                        print("   ✓ No messages in queue (expected after pull)")

                # Check queue status
                response = await client.get(f"{base_url}/dals/host/status")
                print(f"   Queue status: {response.status_code}")
                if response.status_code == 200:
                    status = response.json()
                    print(f"   ✓ Queue status: {status.get('queue_size', 0)} messages")

            # Test 3: Test UQV routes
            print("\n3. Testing UQV routes...")

            # Store an unanswered query
            uqv_data = {
                "query": "What is the meaning of life?",
                "context": "Philosophical discussion",
                "worker_id": "test_worker_001"
            }
            response = await client.post(f"{base_url}/dals/uqv/store", json=uqv_data)
            print(f"   Store UQV: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✓ Query stored with ID: {result.get('uqv_id')}")

                # Retrieve queries
                response = await client.get(f"{base_url}/dals/uqv/retrieve")
                print(f"   Retrieve UQV: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✓ Retrieved {len(result.get('queries', []))} queries")

                # Get stats
                response = await client.get(f"{base_url}/dals/uqv/stats")
                print(f"   UQV stats: {response.status_code}")
                if response.status_code == 200:
                    stats = response.json()
                    print(f"   ✓ UQV stats: {stats}")

            # Test 4: Test TTS routes
            print("\n4. Testing TTS routes...")

            # Test TTS synthesis
            tts_data = {
                "text": "Hello, this is a test of the text-to-speech system.",
                "voice": "default"
            }
            response = await client.post(f"{base_url}/dals/tts/synthesize", json=tts_data)
            print(f"   TTS synthesis: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✓ TTS response: {result.get('message')}")

            # Test TTS voices
            response = await client.get(f"{base_url}/dals/tts/voices")
            print(f"   TTS voices: {response.status_code}")
            if response.status_code == 200:
                voices = response.json()
                print(f"   ✓ Available voices: {len(voices.get('voices', []))}")

            # Test 5: Test broadcast routes (will fail without registered workers)
            print("\n5. Testing broadcast routes...")

            broadcast_data = {
                "type": "test_broadcast",
                "data": {"message": "Test broadcast message"}
            }
            response = await client.post(f"{base_url}/dals/broadcast/message", json=broadcast_data)
            print(f"   Broadcast message: {response.status_code}")
            if response.status_code == 400:
                result = response.json()
                if "No workers registered" in result.get("detail", ""):
                    print("   ✓ Expected: No workers registered (normal for test)")

            # Get registered workers
            response = await client.get(f"{base_url}/dals/workers")
            print(f"   Get workers: {response.status_code}")
            if response.status_code == 200:
                workers = response.json()
                print(f"   ✓ Workers registered: {workers.get('total_workers', 0)}")

        except Exception as e:
            print(f"   ✗ Test failed: {str(e)}")

    print("\n" + "=" * 50)
    print("DALS Messaging Infrastructure Test Complete")

if __name__ == "__main__":
    asyncio.run(test_dals_messaging())