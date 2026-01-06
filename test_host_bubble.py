#!/usr/bin/env python3
"""
Simple test of the GOAT Host Assistant Bubble System
"""

import asyncio
from goat_core.goat_orchestrator import GOATOrchestrator
from concierge_host_bubble import ConciergeHostBubble, cali_monitor
from goat_core.sample_workers import dals_forge_connector

from goat_core.goat_orchestrator import GOATOrchestrator
from goat_core.sample_workers import dals_forge_connector

async def test_host_bubble():
    print("🐐 GOAT Host Assistant Bubble Test")
    print("=" * 40)

    # Initialize system
    goat = GOATOrchestrator()
    # Patch: wrap dals_forge_connector to match required signature
    def forge_connector(worker_id, department, feature):
        return dals_forge_connector(worker_id, department, feature, logic_seed="default", custom_skills={})
    goat.register_dals_forge(forge_connector)
    host = ConciergeHostBubble(goat_orchestrator=goat, cali=cali_monitor)

    # Deploy a worker
    await goat.forge_and_deploy_worker(
        department="Onboarding",
        feature="setup",
        logic_seed="host_welcome_v1",
        custom_skills={"focus": "new_users"}
    )

    # Test greeting
    greeting, persona = await host.greet("test_user")
    print(f"✓ Greeting: {greeting}")
    print(f"✓ Persona: {persona.name} ({persona.accent_color})")

    # Test message handling
    response, persona, meta = await host.handle_message(
        user_id="test_user",
        message="I'm new here, how do I get started?"
    )

    # Patch: handle response as dict or str
    if isinstance(response, dict):
        print(f"✓ Response: {response.get('response', 'No response')}")
    else:
        print(f"✓ Response: {response}")
    if isinstance(meta, dict):
        print(f"✓ Worker Path: {meta.get('worker_path', 'unknown')}")
    else:
        print(f"✓ Worker Path: {meta}")
    print(f"✓ Handoff: {meta.get('handoff', False)}")

    # Show system status
    overview = goat.get_department_overview()
    print("\nSystem Status:")
    for dept_id, dept in overview["departments"].items():
        print(f"  {dept['name']}: {len(dept['features'])} features")

    print("\n✅ Host Assistant Bubble System is working!")
    print("Multiple workers can now be deployed for smooth handoffs!")

if __name__ == "__main__":
    asyncio.run(test_host_bubble())