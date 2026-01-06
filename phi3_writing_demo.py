# phi3_writing_demo.py
"""
Phi-3 Mini Writing Demo
Showcase Caleon's articulation capabilities
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from phi3_driver import get_articulator

async def demo_phi3_writing():
    """Demonstrate Phi-3 Mini writing different types of content."""

    articulator = get_articulator()
    print("🎭 Caleon Prime - Phi-3 Mini Articulation Demo")
    print("=" * 60)

    # Demo 1: Technical explanation
    print("\n📚 Demo 1: Technical Architecture Explanation")
    plan1 = {
        "chapter_title": "Sovereign AI Architecture",
        "section_title": "Phi-3 Mini Integration",
        "goals": "Explain how Phi-3 Mini serves as Caleon's articulation engine",
        "tone": "technical_clear",
        "continuity_context": "Previous section covered AI sovereignty principles",
        "target_length": "500-700 words"
    }

    print("Generating technical content...")
    content1 = await articulator.articulate(plan1)
    print(f"\n{content1[:400]}...\n")

    # Demo 2: Conversational response
    print("\n💬 Demo 2: Live Conversation Response")
    plan2 = {
        "chapter_title": "Bubble Assistant",
        "section_title": "User Query Response",
        "goals": "Respond helpfully to: 'How does Phi-3 make Caleon more powerful?'",
        "tone": "conversational_helpful",
        "continuity_context": "User is exploring AI capabilities",
        "target_length": "200-300 words"
    }

    print("Generating conversational response...")
    content2 = await articulator.articulate(plan2)
    print(f"\n{content2[:300]}...\n")

    # Demo 3: Streaming content
    print("\n🌊 Demo 3: Real-time Streaming")
    plan3 = {
        "chapter_title": "Future of AI",
        "section_title": "Sovereign Intelligence",
        "goals": "Discuss the importance of local, controllable AI systems",
        "tone": "forward_looking",
        "continuity_context": "Building on current AI landscape discussion",
        "target_length": "300-400 words"
    }

    print("Streaming content in real-time...")
    print("(This simulates the typing effect in the Bubble Assistant)\n")

    chunk_count = 0
    async for chunk in articulator.articulate_stream(plan3):
        print(chunk, end="", flush=True)
        chunk_count += 1

        # Add small delay to simulate typing
        if chunk_count % 10 == 0:
            await asyncio.sleep(0.1)

    print(f"\n\n✅ Streaming complete! Total chunks: {chunk_count}")

    # Demo 4: Show personality traits
    print("\n🎭 Demo 4: Caleon Personality Analysis")
    personality = articulator.personality_prompt

    traits = [
        "sovereign AI guardian",
        "direct and confident",
        "warm but not soft",
        "active voice",
        "short paragraphs",
        "purpose-driven"
    ]

    print("Caleon's personality conditioning includes:")
    for trait in traits:
        if trait in personality:
            print(f"✅ {trait}")
        else:
            print(f"❌ {trait}")

    print("\n🏁 Demo Complete")
    print("Phi-3 Mini is now Caleon's voice - local, fast, and sovereign!")

if __name__ == "__main__":
    asyncio.run(demo_phi3_writing())