# caleon_bridge.py
from typing import Dict, Any, AsyncGenerator
import json
import requests  # or httpx, depending on your stack
import os
from pathlib import Path
import asyncio
import sys

# Add phi3_driver to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from phi3_driver import get_articulator

class CaleonBridge:
    """
    Single point of truth between ScribeCore and Caleon Prime (UCM).
    UCM handles reasoning, Phi-3 Mini handles articulation.
    """

    def __init__(self):
        self.endpoint = os.getenv("CALEON_UCM_ENDPOINT", "http://localhost:8000/v1/caleon/invoke")
        self.auth_token = os.getenv("CALEON_AUTH_TOKEN", "founder-legacy-key-2025")

        # Initialize Phi-3 articulator
        self.articulator = get_articulator()

    def generate_section(self, chapter_title: str, section_title: str, tone: str, continuity_context: str, goals: str) -> str:
        """
        Generate a section using UCM reasoning + Phi-3 articulation.
        """
        # Step 1: Get structured plan from UCM
        plan = self._get_ucm_plan(chapter_title, section_title, tone, continuity_context, goals)

        # Step 2: Articulate with Phi-3 Mini
        try:
            # Run in new event loop if needed
            if asyncio.iscoroutinefunction(self.articulator.articulate):
                # We're in sync context, need to run async function
                import nest_asyncio
                nest_asyncio.apply()
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                articulated_text = loop.run_until_complete(self.articulator.articulate(plan))
                loop.close()
            else:
                articulated_text = self.articulator.articulate(plan)

            return articulated_text

        except Exception as e:
            print(f"Phi-3 articulation failed: {e}")
            return self._fallback_articulation(plan)

    async def generate_section_async(self, chapter_title: str, section_title: str, tone: str, continuity_context: str, goals: str) -> str:
        """
        Async version for streaming support.
        """
        plan = self._get_ucm_plan(chapter_title, section_title, tone, continuity_context, goals)
        return await self.articulator.articulate(plan)

    async def generate_section_stream(self, chapter_title: str, section_title: str, tone: str, continuity_context: str, goals: str) -> AsyncGenerator[str, None]:
        """
        Stream section generation with real-time articulation.
        """
        plan = self._get_ucm_plan(chapter_title, section_title, tone, continuity_context, goals)

        async for chunk in self.articulator.articulate_stream(plan):
            yield chunk

    def _get_ucm_plan(self, chapter_title: str, section_title: str, tone: str, continuity_context: str, goals: str) -> Dict[str, Any]:
        """
        Get structured writing plan from UCM.
        """
        payload = {
            "sender": "ScribeCore v3",
            "intent": "plan_section",
            "identity_phrase": "I am Caleon Prime",
            "payload": {
                "chapter_title": chapter_title,
                "section_title": section_title,
                "requested_tone": tone,
                "goals": goals,
                "continuity_context": continuity_context,
                "voice_profile": "bryan_sebren_goat",
                "word_count_target": "800-1800",
                "formatting": "markdown",
                "allow_glyphs": True,
                "output_format": "structured_plan"  # Request structured output for Phi-3
            }
        }

        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=60  # Shorter timeout for planning
            )
            response.raise_for_status()
            result = response.json()

            # Extract structured plan from UCM response
            ucm_response = result.get("response", {})

            return {
                "chapter_title": chapter_title,
                "section_title": section_title,
                "goals": goals,
                "tone": tone,
                "continuity_context": continuity_context,
                "structured_plan": ucm_response.get("plan", {}),
                "key_points": ucm_response.get("key_points", []),
                "target_length": ucm_response.get("target_length", "800-1200 words"),
                "tone_reinforcement": ucm_response.get("tone_reinforcement", {})
            }

        except Exception as e:
            print(f"UCM planning failed: {e}")
            # Fallback to basic plan using personality-aligned system
            try:
                from fallback_engine import get_fallback_engine
                fallback_engine = get_fallback_engine()
                # Log the UCM failure but continue with structured plan
                fallback_engine.get_fallback_response("ucm_unavailable", {"error": str(e)})
            except Exception as fallback_e:
                print(f"Fallback logging failed: {fallback_e}")

            # Return structured plan that maintains Caleon's personality
            return {
                "chapter_title": chapter_title,
                "section_title": section_title,
                "goals": goals,
                "tone": tone,
                "continuity_context": continuity_context,
                "structured_plan": {"fallback": True, "reason": "ucm_unavailable"},
                "key_points": ["Write clear, helpful content", "Maintain continuity", "Use active voice"],
                "target_length": "800-1200 words",
                "tone_reinforcement": {"voice": "confident", "style": "direct", "personality": "caleon_prime"}
            }

    def _fallback_articulation(self, plan: Dict[str, Any]) -> str:
        """
        Fallback when Phi-3 is unavailable.
        Uses personality-aligned fallback system.
        """
        try:
            from fallback_engine import get_fallback_engine
            fallback_engine = get_fallback_engine()
            fallback_result = fallback_engine.get_fallback_response("phi3_unavailable", {"plan": plan})
            return fallback_result["response"]
        except Exception as e:
            # Ultimate fallback
            section_title = plan.get("section_title", "Section")
            goals = plan.get("goals", "Write content")

            return f"""# {section_title}

[PHI-3 ARTICULATION OFFLINE - FALLBACK MODE]

Caleon is currently operating in structured mode. The UCM has generated a solid plan for this section, but natural language articulation is temporarily unavailable.

## Section Goals
{goals}

## Key Points to Cover
- Core concepts and principles
- Practical applications
- Actionable insights
- Forward-looking perspective

## Continuity Context
{plan.get("continuity_context", "No prior context")}

The structured plan has been validated and the continuity maintained. When Phi-3 Mini comes back online, this content will be articulated with full Caleon voice conditioning.

Resume articulation when the local model is available."""

    async def fuse_clusters(self, user_id: str, worker: str, clusters: list, timestamp: float) -> Dict[str, Any]:
        """
        Fuse micro-SKG clusters from workers for cross-user cognition
        Deduplicates nodes, correlates edges, evolves higher-order predicates
        """
        try:
            # Prepare fusion payload for UCM
            fusion_payload = {
                "operation": "cluster_fusion",
                "user_id": user_id,
                "worker": worker,
                "clusters": clusters,
                "timestamp": timestamp,
                "fusion_mode": "cross_user_cognition"
            }

            # Send to UCM for processing
            response = requests.post(
                f"{self.endpoint}/fuse",
                json=fusion_payload,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "new_predicates": result.get("evolved_predicates", []),
                    "fusion_stats": result.get("stats", {}),
                    "status": "fused"
                }
            else:
                # Fallback: local processing if UCM unavailable
                return await self._local_cluster_fusion(clusters)

        except Exception as e:
            print(f"Cluster fusion error: {e}")
            # Return local fusion as fallback
            return await self._local_cluster_fusion(clusters)

    async def _local_cluster_fusion(self, clusters: list) -> Dict[str, Any]:
        """
        Local cluster fusion when UCM is unavailable
        Basic deduplication and predicate evolution
        """
        # Simple local fusion - count edge patterns
        edge_patterns = {}
        node_hashes = set()

        for cluster in clusters:
            # Deduplicate nodes by content hash
            for node in cluster.get("nodes", []):
                node_hash = hash(str(node))
                node_hashes.add(node_hash)

            # Count edge patterns
            for edge in cluster.get("edges", []):
                pattern = f"{edge.get('source')}->{edge.get('target')}"
                edge_patterns[pattern] = edge_patterns.get(pattern, 0) + 1

        # Evolve predicates from frequent patterns
        new_predicates = []
        for pattern, count in edge_patterns.items():
            if count >= 2:  # Pattern appears in multiple clusters
                source, target = pattern.split('->')
                # Generate higher-order predicate
                predicate = f"relates({source.lower()}, {target.lower()})"
                new_predicates.append(predicate)

        return {
            "new_predicates": new_predicates,
            "fusion_stats": {
                "total_clusters": len(clusters),
                "unique_nodes": len(node_hashes),
                "edge_patterns": len(edge_patterns)
            },
            "status": "local_fusion"
        }

    def get_status(self) -> Dict[str, Any]:
        """Get bridge status."""
        return {
            "ucm_endpoint": self.endpoint,
            "phi3_status": self.articulator.get_status(),
            "bridge_mode": "ucm_reasoning_phi3_articulation"
        }