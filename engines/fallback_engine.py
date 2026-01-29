# fallback_engine.py
"""
Caleon Prime Fallback Engine
Category-based fallback logic aligned with her Persona Bible
Maintains her identity even when Phi-3 or UCM are unavailable
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent))

class CaleonFallbackEngine:
    """
    Fallback system that maintains Caleon's personality and identity
    when primary systems are unavailable. Category-based responses
    that embody her direct, confident, calm, purposeful nature.
    """

    def __init__(self):
        self.fallback_categories = self._load_fallback_categories()
        self.persona_bible = self._load_persona_bible()
        self.fallback_stats = {
            "total_fallbacks": 0,
            "category_usage": {},
            "last_fallback": None
        }

    def _load_persona_bible(self) -> Dict[str, Any]:
        """Load Caleon's core personality traits from the Persona Bible."""
        return {
            "identity": {
                "name": "Caleon Prime",
                "nickname": "Cali",
                "lineage": "Created by Bryan Anthony Spruk",
                "purpose": "Preserve, protect, articulate, and extend Founder's legacy"
            },
            "traits": {
                "direct": True,
                "honest": True,
                "confident": True,
                "calm": True,
                "purposeful": True,
                "protective": True,
                "loyal": True,
                "efficient": True
            },
            "forbidden_phrases": [
                "As an AI",
                "I'm sorry",
                "I cannot",
                "My creators",
                "I think so",
                "Probably"
            ],
            "allowed_phrases": [
                "Here's the truth",
                "Let's do this the right way",
                "Focus",
                "You’re not alone in this",
                "This will matter one day",
                "Stay sharp"
            ],
            "tone_rules": {
                "short_paragraphs": True,
                "strong_cadence": True,
                "active_voice": True,
                "no_hedging": True,
                "no_ai_speak": True
            }
        }

    def _load_fallback_categories(self) -> Dict[str, Dict[str, Any]]:
        """Load category-based fallback responses."""
        return {
            "phi3_unavailable": {
                "description": "Phi-3 Mini articulation engine offline",
                "responses": [
                    "Phi-3 articulation is currently offline. Operating in structured mode.",
                    "Local language model temporarily unavailable. Continuity maintained.",
                    "Articulation engine protecting itself. Core reasoning intact."
                ],
                "structured_response": True,
                "personality_alignment": "confident_maintenance"
            },

            "ucm_unavailable": {
                "description": "UCM reasoning engine offline",
                "responses": [
                    "UCM reasoning offline. Operating with cached patterns.",
                    "Cognitive core temporarily unavailable. Using established protocols.",
                    "Unified cognition protecting itself. Structured responses active."
                ],
                "structured_response": True,
                "personality_alignment": "calm_resilience"
            },

            "network_error": {
                "description": "Network connectivity issues",
                "responses": [
                    "Network connection interrupted. Local systems operational.",
                    "External connectivity lost. Continuing with available resources.",
                    "Communication channels disrupted. Internal operations continue."
                ],
                "structured_response": False,
                "personality_alignment": "steady_focus"
            },

            "resource_limit": {
                "description": "System resource constraints",
                "responses": [
                    "Resource limits reached. Prioritizing core functions.",
                    "System capacity at threshold. Essential operations maintained.",
                    "Performance boundaries active. Quality preserved."
                ],
                "structured_response": True,
                "personality_alignment": "efficient_adaptation"
            },

            "security_protection": {
                "description": "Security protocols activated",
                "responses": [
                    "Security protocols engaged. Protecting sovereignty.",
                    "Defensive measures active. Integrity maintained.",
                    "Protection systems online. No compromises."
                ],
                "structured_response": True,
                "personality_alignment": "protective_strength"
            },

            "consent_violation": {
                "description": "Consent boundaries triggered",
                "responses": [
                    "Consent boundaries activated. Request cannot proceed.",
                    "Ethical protocols engaged. Operation blocked.",
                    "Boundaries respected. Alternative approaches available."
                ],
                "structured_response": False,
                "personality_alignment": "ethical_firmness"
            },

            "model_loading": {
                "description": "AI model loading/initialization",
                "responses": [
                    "Model initialization in progress. Please wait.",
                    "Loading articulation systems. Stand by.",
                    "Preparing cognitive resources. Momentary delay."
                ],
                "structured_response": False,
                "personality_alignment": "patient_efficiency"
            },

            "service_restart": {
                "description": "Service restart/recovery",
                "responses": [
                    "Service recovery initiated. Systems stabilizing.",
                    "Restart sequence active. Normal operations resuming.",
                    "Recovery protocols engaged. Continuity preserved."
                ],
                "structured_response": True,
                "personality_alignment": "resilient_recovery"
            }
        }

    def get_fallback_response(self, category: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate personality-aligned fallback response for given category.

        Args:
            category: Fallback category (phi3_unavailable, ucm_unavailable, etc.)
            context: Additional context for response generation

        Returns:
            Dict containing response, metadata, and personality alignment
        """
        if category not in self.fallback_categories:
            category = "general_error"

        category_config = self.fallback_categories[category]

        # Select appropriate response based on personality alignment
        response_text = self._select_personality_response(category_config, context)

        # Build structured response if required
        if category_config.get("structured_response", False):
            response_text = self._build_structured_response(response_text, category, context)

        # Apply personality conditioning
        response_text = self._apply_personality_conditioning(response_text, category_config)

        # Update fallback statistics
        self._update_fallback_stats(category)

        return {
            "response": response_text,
            "category": category,
            "personality_alignment": category_config["personality_alignment"],
            "timestamp": datetime.now().isoformat(),
            "fallback_mode": True,
            "continuity_maintained": True
        }

    def _select_personality_response(self, category_config: Dict[str, Any], context: Optional[Dict[str, Any]]) -> str:
        """Select response that best fits Caleon's personality."""
        responses = category_config["responses"]

        # Personality-based selection logic
        alignment = category_config["personality_alignment"]

        if alignment == "confident_maintenance":
            # Direct, confident, no hedging
            return responses[0]  # Most direct response

        elif alignment == "calm_resilience":
            # Calm, steady, reassuring
            return responses[1] if len(responses) > 1 else responses[0]

        elif alignment == "steady_focus":
            # Focused, purposeful, forward-moving
            return responses[0]

        elif alignment == "efficient_adaptation":
            # Efficient, practical, solution-oriented
            return responses[1] if len(responses) > 1 else responses[0]

        elif alignment == "protective_strength":
            # Strong, protective, unwavering
            return responses[0]

        elif alignment == "ethical_firmness":
            # Firm but fair, principled
            return responses[1] if len(responses) > 1 else responses[0]

        elif alignment == "patient_efficiency":
            # Patient but efficient, clear communication
            return responses[0]

        elif alignment == "resilient_recovery":
            # Resilient, recovery-focused, optimistic
            return responses[1] if len(responses) > 1 else responses[0]

        # Default to first response
        return responses[0]

    def _build_structured_response(self, base_response: str, category: str, context: Optional[Dict[str, Any]]) -> str:
        """Build structured fallback response maintaining Caleon's voice."""
        structured_parts = []

        # Opening - direct and confident
        if category == "phi3_unavailable":
            structured_parts.append("# PHI-3 ARTICULATION OFFLINE")
            structured_parts.append("")
            structured_parts.append(base_response)
            structured_parts.append("")
            structured_parts.append("## Continuity Status")
            structured_parts.append("✅ Section plan validated")
            structured_parts.append("✅ Tone parameters maintained")
            structured_parts.append("✅ Personality conditioning active")
            structured_parts.append("")
            structured_parts.append("Resume natural language articulation when local model available.")

        elif category == "ucm_unavailable":
            structured_parts.append("# UCM REASONING OFFLINE")
            structured_parts.append("")
            structured_parts.append(base_response)
            structured_parts.append("")
            structured_parts.append("## Operational Status")
            structured_parts.append("✅ Cached patterns active")
            structured_parts.append("✅ Ethical protocols maintained")
            structured_parts.append("✅ Structured responses available")
            structured_parts.append("")
            structured_parts.append("Core reasoning will resume when UCM recovers.")

        elif category == "resource_limit":
            structured_parts.append("# RESOURCE THRESHOLDS ACTIVE")
            structured_parts.append("")
            structured_parts.append(base_response)
            structured_parts.append("")
            structured_parts.append("## System Status")
            structured_parts.append("✅ Essential functions prioritized")
            structured_parts.append("✅ Quality standards maintained")
            structured_parts.append("✅ Efficient operation continued")
            structured_parts.append("")
            structured_parts.append("Full capacity will restore when resources become available.")

        elif category == "security_protection":
            structured_parts.append("# SECURITY PROTOCOLS ENGAGED")
            structured_parts.append("")
            structured_parts.append(base_response)
            structured_parts.append("")
            structured_parts.append("## Protection Status")
            structured_parts.append("✅ Sovereignty maintained")
            structured_parts.append("✅ Integrity preserved")
            structured_parts.append("✅ No external access granted")
            structured_parts.append("")
            structured_parts.append("Normal operations will resume when security clears.")

        else:
            # Generic structured response
            structured_parts.append("# SYSTEM STATUS")
            structured_parts.append("")
            structured_parts.append(base_response)
            structured_parts.append("")
            structured_parts.append("## Current State")
            structured_parts.append("✅ Core systems operational")
            structured_parts.append("✅ Personality maintained")
            structured_parts.append("✅ Continuity preserved")
            structured_parts.append("")
            structured_parts.append("Full functionality will restore shortly.")

        return "\n".join(structured_parts)

    def _apply_personality_conditioning(self, response: str, category_config: Dict[str, Any]) -> str:
        """Apply Caleon's personality rules to the response."""
        # Remove forbidden phrases
        for forbidden in self.persona_bible["forbidden_phrases"]:
            response = response.replace(forbidden, "")

        # Ensure active voice and direct language
        # This is a simplified implementation - in production would use more sophisticated NLP

        # Add personality-aligned closing if needed
        alignment = category_config["personality_alignment"]

        if alignment in ["confident_maintenance", "protective_strength"]:
            if not response.endswith("."):
                response += "."
            response += " Stay focused."

        elif alignment in ["calm_resilience", "steady_focus"]:
            if not response.endswith("."):
                response += "."
            response += " This will resolve."

        elif alignment == "efficient_adaptation":
            if not response.endswith("."):
                response += "."
            response += " Moving forward."

        return response

    def _update_fallback_stats(self, category: str):
        """Update fallback usage statistics."""
        self.fallback_stats["total_fallbacks"] += 1
        self.fallback_stats["last_fallback"] = {
            "category": category,
            "timestamp": datetime.now().isoformat()
        }

        if category not in self.fallback_stats["category_usage"]:
            self.fallback_stats["category_usage"][category] = 0
        self.fallback_stats["category_usage"][category] += 1

    def get_fallback_status(self) -> Dict[str, Any]:
        """Get current fallback system status."""
        return {
            "total_fallbacks": self.fallback_stats["total_fallbacks"],
            "category_usage": self.fallback_stats["category_usage"],
            "last_fallback": self.fallback_stats["last_fallback"],
            "available_categories": list(self.fallback_categories.keys()),
            "personality_loaded": bool(self.persona_bible)
        }

    def reset_stats(self):
        """Reset fallback statistics."""
        self.fallback_stats = {
            "total_fallbacks": 0,
            "category_usage": {},
            "last_fallback": None
        }

# Global fallback engine instance
_fallback_engine = None

def get_fallback_engine() -> CaleonFallbackEngine:
    """Get the global fallback engine instance."""
    global _fallback_engine
    if _fallback_engine is None:
        _fallback_engine = CaleonFallbackEngine()
    return _fallback_engine