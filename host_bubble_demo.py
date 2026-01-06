#!/usr/bin/env python3
"""
GOAT Host Assistant Bubble System - Main Entry Point
Demonstrates the complete host assistant system with multiple workers
"""

import asyncio
import sys
from typing import Dict, Any

from goat_core.goat_orchestrator import GOATOrchestrator
from concierge_host_bubble import ConciergeHostBubble, cali_monitor
from goat_core.sample_workers import dals_forge_connector

async def demonstrate_host_bubble():
    """Demonstrate the complete host assistant bubble system"""

    print("🐐 GOAT Host Assistant Bubble System")
    print("=" * 50)

    # 1. Initialize GOAT orchestrator
    print("\n1. Initializing GOAT Orchestrator...")
    goat = GOATOrchestrator()

    # 2. Register DALS forge connector
    print("2. Registering DALS forge connector...")
    goat.register_dals_forge(dals_forge_connector)

    # 3. Initialize Concierge Host Bubble
    print("3. Initializing Concierge Host Bubble...")
    host = ConciergeHostBubble(goat_orchestrator=goat, cali=cali_monitor)

    # 4. Deploy initial workers
    print("4. Deploying initial workers...")
    await deploy_initial_workers(goat)

    # 5. Demonstrate user interactions
    print("\n5. Demonstrating user interactions...")
    await demonstrate_interactions(host)

    # 6. Show system status
    print("\n6. System Status:")
    show_system_status(goat, host)

async def deploy_initial_workers(goat: GOATOrchestrator):
    """Deploy some initial workers to different departments"""

    deployments = [
        ("Onboarding", "setup", "host_welcome_v1", {"focus": "new_users"}),
        ("Pricing", "info", "host_pricing_v1", {"transparency": True}),
        ("Creator", "tools", "host_creator_v1", {"creativity": "high"}),
        ("Tech", "integration", "host_tech_v1", {"expertise": "api"}),
        ("Legal", "policy", "host_legal_v1", {"compliance": "gdpr"}),
    ]

    for dept, feat, seed, skills in deployments:
        try:
            worker_id = await goat.forge_and_deploy_worker(
                department=dept,
                feature=feat,
                logic_seed=seed,
                custom_skills=skills
            )
            print(f"  ✓ Deployed {worker_id} to {dept}.{feat}")
        except Exception as e:
            print(f"  ✗ Failed to deploy to {dept}.{feat}: {e}")

async def demonstrate_interactions(host: ConciergeHostBubble):
    """Demonstrate various user interactions"""

    test_users = ["user_123", "user_456", "user_789"]
    test_messages = [
        "I'm new here, how do I get started?",
        "What's the cost of using GOAT?",
        "I want to create some content",
        "How do I integrate with your API?",
        "What are your privacy policies?",
        "I'm back, what were we working on?",
    ]

    for i, user_id in enumerate(test_users):
        print(f"\n--- User {user_id} ---")

        # User greeting
        greeting, persona = await host.greet(user_id)
        print(f"Greeting: {greeting}")
        print(f"Persona: {persona.name} ({persona.accent_color})")

        # Simulate some messages
        for j in range(min(2, len(test_messages) - i * 2)):
            message = test_messages[i * 2 + j]
            print(f"\nUser: {message}")

            response, persona, metadata = await host.handle_message(
                user_id=user_id,
                message=message
            )

            print(f"GOAT: {response.get('response', 'No response')}")
            print(f"Persona: {persona.name}")
            print(f"Worker: {metadata.get('worker_path', 'unknown')}")
            print(f"Handoff: {metadata.get('handoff', False)}")

def show_system_status(goat: GOATOrchestrator, host: ConciergeHostBubble):
    """Display the current system status"""

    print("\nGOAT Department Overview:")
    overview = goat.get_department_overview()

    for dept_id, dept_info in overview["departments"].items():
        print(f"\n{dept_info['name']} Department:")
        for feat_name, feat_info in dept_info["features"].items():
            worker_count = feat_info["current_workers"]
            max_capacity = feat_info["max_capacity"]
            print(f"  {feat_name}: {worker_count}/{max_capacity} workers")

            for worker in feat_info["workers"]:
                score = worker["specialization_score"]
                state = worker["state"]
                print(f"    - {worker['id']}: {score:.2f} specialization, {state}")

    print("\nHost Bubble Status:")
    print(f"  Active Sessions: {len(host.active_sessions)}")
    print(f"  Persistent Memory: {len(host.persistent_memory)} users")
    print(f"  Cali Interactions: {len(cali_monitor.interaction_stream)}")

async def run_interactive_demo():
    """Run an interactive demo where user can chat with the system"""

    print("🐐 Interactive GOAT Host Assistant Demo")
    print("=" * 50)
    print("Type 'quit' to exit, 'status' to see system status")
    print()

    # Initialize system
    goat = GOATOrchestrator()
    goat.register_dals_forge(dals_forge_connector)
    host = ConciergeHostBubble(goat_orchestrator=goat, cali=cali_monitor)

    # Deploy initial workers
    await deploy_initial_workers(goat)

    user_id = "demo_user"

    # Initial greeting
    greeting, persona = await host.greet(user_id)
    print(f"GOAT: {greeting}")
    print(f"[{persona.name}]")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'status':
                show_system_status(goat, host)
                continue
            elif not user_input:
                continue

            # Process message
            response, persona, metadata = await host.handle_message(
                user_id=user_id,
                message=user_input
            )

            print(f"GOAT: {response.get('response', 'No response')}")
            print(f"[{persona.name}] Worker: {metadata.get('worker_path', 'unknown')}")
            if metadata.get('handoff'):
                print("(Handoff occurred)")
            print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # Run interactive demo
        asyncio.run(run_interactive_demo())
    else:
        # Run automated demonstration
        asyncio.run(demonstrate_host_bubble())</content>
<parameter name="filePath">c:\dev\GOAT\host_bubble_demo.py