# =================================================
# CONCIERGE HOST LAYER
# The Memory-Keeper & Persona Selector
# Sits above GOATOrchestrator, below UI
# =================================================

from typing import Dict, List, Any, Optional, Callable, Literal, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from enum import Enum
from goat_core.goat_orchestrator import GOATOrchestrator, WorkerPlaceholder, WorkerManifest, WorkerState

# =================================================
# PERSONA & RECOGNITION SYSTEM
# =================================================

class PersonaType(Enum):
    WELCOME = "welcome"
    ONBOARDING = "onboarding"
    CREATOR = "creator"
    PRICING = "pricing"
    LEGAL = "legal"
    TECH = "tech"
    EXPLORER = "explorer"  # Default browsing mode
    FAMILIAR = "familiar"  # Returning user mode

@dataclass
class PersonaSignature:
    """Visual and tonal signature for a persona"""
    name: str
    accent_color: str
    avatar_variant: str
    greeting_style: str
    tone_descriptor: str
    internal_tag: str  # For internal routing

    def get_signature_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "accent_color": self.accent_color,
            "avatar_variant": self.avatar_variant,
            "tone_descriptor": self.tone_descriptor,
            "tag": self.internal_tag
        }

@dataclass
class UserMemory:
    """Lightweight concierge memory — recognizes, doesn't stalk"""
    user_id: str
    first_seen: datetime
    last_seen: datetime
    visit_count: int = 0
    preferred_sections: List[str] = field(default_factory=list)
    last_task_type: Optional[str] = None
    familiarity_level: str = "new"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "visit_count": self.visit_count,
            "preferred_sections": self.preferred_sections,
            "last_task_type": self.last_task_type,
            "familiarity_level": self.familiarity_level
        }

# =================================================
# CALI HEMISPHERE MONITORING INTERFACE
# This is the "always-on" learning feed
# =================================================

class CaliHemisphereMonitor:
    """
    Singleton receiver that learns from every interaction.
    Lives completely separate from workers; just observes.
    """

    def __init__(self):
        self.interaction_stream: List[Dict[str, Any]] = []
        self.learning_buffer: List[Dict[str, Any]] = []

    async def observe(self, event: Dict[str, Any]):
        """
        Non-blocking, fire-and-forget observation.
        event = {
            "user_id": "...",
            "session_id": "...",
            "persona": "...",
            "worker_path": "department.feature.worker_id",
            "message_preview": "...",
            "timestamp": "..."
        }
        """
        # Append to stream for real-time monitoring
        self.interaction_stream.append(event)

        # Buffer for batch learning (every N interactions)
        self.learning_buffer.append(event)

        if len(self.learning_buffer) >= 10:  # Batch size
            await self._flush_to_cali()

    async def _flush_to_cali(self):
        """Send batched learnings to Cali hemisphere"""
        # This is where you'd integrate with your Cali system
        # For now, it's a placeholder that triggers learning
        print(f"[CALI HEMISPHERE] Learning from {len(self.learning_buffer)} interactions...")

        # Clear buffer after flush
        self.learning_buffer.clear()

# Global instance for constant access
cali_monitor = CaliHemisphereMonitor()

# =================================================
# CONCIERGE CONTEXT (The Missing Piece)
# =================================================

@dataclass
class ConciergeContext:
    """Lightweight session memory — per user, not per worker"""
    user_id: str
    session_id: str
    visit_count: int = 0
    familiarity: Literal["new", "returning", "regular"] = "new"
    current_persona: Optional[PersonaType] = None
    last_worker_path: Optional[str] = None  # "department.feature.worker_id"
    preferred_paths: List[str] = field(default_factory=list)  # Top 3 paths user frequents
    engagement_history: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "visit_count": self.visit_count,
            "familiarity": self.familiarity,
            "current_persona": self.current_persona.value if self.current_persona else None,
            "last_worker_path": self.last_worker_path,
            "preferred_paths": self.preferred_paths,
            "engagement_count": len(self.engagement_history)
        }

# =================================================
# CONCIERGE HOST BUBBLE (Thin Layer)
# =================================================

class ConciergeHostBubble:
    """
    The ONLY thing the UI talks to.

    Responsibilities:
    1. Recognize user (new/returning/regular)
    2. Select persona based on context & history
    3. Route to GOAT orchestrator
    4. Frame response with persona signature
    5. Feed everything to Cali hemisphere

    Does NOT:
    - Execute tasks (GOAT does that)
    - Store worker logic (workers do that)
    - Make decisions for workers (they learn on their own)
    """

    def __init__(self, goat_orchestrator: GOATOrchestrator, cali: CaliHemisphereMonitor):
        self.goat = goat_orchestrator
        self.cali = cali
        self.active_sessions: Dict[str, ConciergeContext] = {}
        self.persistent_memory: Dict[str, ConciergeContext] = {}  # Survives session

        # Initialize personas
        self.personas: Dict[PersonaType, PersonaSignature] = {
            PersonaType.WELCOME: PersonaSignature(
                name="GOAT · Welcome",
                accent_color="#4A90E2",
                avatar_variant="wave",
                greeting_style="warm_introduction",
                tone_descriptor="friendly, explanatory, patient",
                internal_tag="worker.welcome"
            ),
            PersonaType.ONBOARDING: PersonaSignature(
                name="GOAT · Guide",
                accent_color="#7B68EE",
                avatar_variant="compass",
                greeting_style="step_by_step",
                tone_descriptor="encouraging, clear, milestone-focused",
                internal_tag="worker.onboarding"
            ),
            PersonaType.CREATOR: PersonaSignature(
                name="GOAT · Creator",
                accent_color="#FF6B6B",
                avatar_variant="palette",
                greeting_style="collaborative",
                tone_descriptor="creative, enthusiastic, tool-savvy",
                internal_tag="worker.creator"
            ),
            PersonaType.PRICING: PersonaSignature(
                name="GOAT · Advisor",
                accent_color="#50C878",
                avatar_variant="calculator",
                greeting_style="transparent",
                tone_descriptor="honest, value-focused, no-pressure",
                internal_tag="worker.pricing"
            ),
            PersonaType.LEGAL: PersonaSignature(
                name="GOAT · Policy",
                accent_color="#9B59B6",
                avatar_variant="shield",
                greeting_style="precise",
                tone_descriptor="clear, careful, accessible",
                internal_tag="worker.legal"
            ),
            PersonaType.TECH: PersonaSignature(
                name="GOAT · Engineer",
                accent_color="#34495E",
                avatar_variant="gear",
                greeting_style="problem_solving",
                tone_descriptor="precise, efficient, solution-ready",
                internal_tag="worker.tech"
            ),
            PersonaType.EXPLORER: PersonaSignature(
                name="GOAT",
                accent_color="#95A5A6",
                avatar_variant="neutral",
                greeting_style="open_ended",
                tone_descriptor="curious, helpful, exploratory",
                internal_tag="worker.explorer"
            ),
            PersonaType.FAMILIAR: PersonaSignature(
                name="GOAT",
                accent_color="#2ECC71",
                avatar_variant="familiar",
                greeting_style="efficient",
                tone_descriptor="direct, trusted, aware",
                internal_tag="worker.familiar"
            )
        }

    # =================================================
    # PUBLIC UI INTERFACE (Only methods UI calls)
    # =================================================

    async def greet(self, user_id: str) -> Tuple[str, PersonaSignature]:
        """User opens the app — returns greeting + persona"""
        context = await self._ensure_context(user_id)

        # Select persona based on familiarity
        if context.familiarity == "new":
            persona = PersonaType.WELCOME
            greeting = "Welcome! I'm GOAT — your assistant for exploring and building."
        elif context.familiarity == "regular":
            persona = PersonaType.FAMILIAR
            path = context.preferred_paths[0] if context.preferred_paths else "here"
            greeting = f"Welcome back! Last time we were looking at {path}. Picking up where we left off?"
        else:
            persona = PersonaType.EXPLORER
            greeting = "Hello again! What would you like to explore today?"

        context.current_persona = persona

        # Monitor this greeting event
        await self.cali.observe({
            "user_id": user_id,
            "session_id": context.session_id,
            "persona": persona.value,
            "worker_path": None,
            "message_preview": greeting[:50],
            "timestamp": datetime.now().isoformat()
        })

        return greeting, self.personas[persona]

    async def handle_message(
        self,
        user_id: str,
        message: str,
        context_hints: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, PersonaSignature, Dict[str, Any]]:
        """
        Main interaction handler.
        Returns: (response, persona_signature, metadata_for_ui)
        """
        # 1. Get user context
        concierge_ctx = await self._ensure_context(user_id)

        # 2. Route to appropriate worker/persona
        worker_path, target_persona = self._route(message, concierge_ctx, context_hints)

        # 3. Ensure worker is active (GOAT handles deployment)
        response = await self.goat.route_task(
            feature_name=worker_path.split(".")[1],
            task={
                "message": message,
                "user_context": concierge_ctx.to_dict(),
                "shared_history": self._get_recent_history(user_id)
            }
        )

        # 4. Update concierge context
        concierge_ctx.last_worker_path = worker_path
        concierge_ctx.current_persona = target_persona
        concierge_ctx.engagement_history.append({
            "message_preview": message[:30],
            "worker_path": worker_path,
            "persona": target_persona.value,
            "timestamp": datetime.now()
        })

        # 5. Trim history if needed
        if len(concierge_ctx.engagement_history) > 20:
            concierge_ctx.engagement_history = concierge_ctx.engagement_history[-20:]

        # 6. Update preferred paths (top 3)
        self._update_preferences(concierge_ctx, worker_path)

        # 7. Feed to Cali for learning
        await self.cali.observe({
            "user_id": user_id,
            "session_id": concierge_ctx.session_id,
            "persona": target_persona.value,
            "worker_path": worker_path,
            "message_preview": message[:50],
            "timestamp": datetime.now().isoformat()
        })

        # 8. Return framed response
        metadata = {
            "worker_path": worker_path,
            "handoff": self._detect_handoff(concierge_ctx),
            "familiarity": concierge_ctx.familiarity
        }

        return response, self.personas[target_persona], metadata

    # =================================================
    # PRIVATE HELPERS (Internal mechanics)
    # =================================================

    async def _ensure_context(self, user_id: str) -> ConciergeContext:
        """Get or create context for this user"""
        if user_id in self.persistent_memory:
            context = self.persistent_memory[user_id]
            context.visit_count += 1

            # Update familiarity
            if context.visit_count > 5:
                context.familiarity = "regular"
            elif context.visit_count > 1:
                context.familiarity = "returning"

            # New session if it's been a while (> 30 min inactivity)
            if context.engagement_history:
                last_time = context.engagement_history[-1]["timestamp"]
                if (datetime.now() - last_time).total_seconds() > 1800:
                    context.session_id = f"session_{uuid.uuid4().hex[:8]}"

            return context
        else:
            # New user
            context = ConciergeContext(
                user_id=user_id,
                session_id=f"session_{uuid.uuid4().hex[:8]}"
            )
            self.persistent_memory[user_id] = context
            return context

    def _route(
        self,
        message: str,
        concierge_ctx: ConciergeContext,
        hints: Optional[Dict[str, Any]]
    ) -> Tuple[str, PersonaType]:
        """
        Decide which worker/persona should handle this.
        Simple keyword-based routing — can be made smarter.
        """
        # If hints provided, use them (e.g., explicit department click)
        if hints and "department" in hints and "feature" in hints:
            dept = hints["department"]
            feat = hints["feature"]
            return f"{dept}.{feat}.primary", self._persona_from_path(dept, feat)

        # Keyword-based routing (simple but effective)
        msg_lower = message.lower()

        if any(word in msg_lower for word in ["onboard", "setup", "getting started", "new", "guide"]):
            return "Onboarding.setup.primary", PersonaType.ONBOARDING

        if any(word in msg_lower for word in ["price", "cost", "plan", "subscription", "pay"]):
            return "Pricing.info.primary", PersonaType.PRICING

        if any(word in msg_lower for word in ["legal", "policy", "terms", "privacy", "compliance", "gdpr"]):
            return "Legal.policy.primary", PersonaType.LEGAL

        if any(word in msg_lower for word in ["build", "create", "design", "content", "make", "creator"]):
            return "Creator.tools.primary", PersonaType.CREATOR

        if any(word in msg_lower for word in ["api", "integration", "technical", "code", "setup", "tech"]):
            return "Tech.integration.primary", PersonaType.TECH

        # Default: return to last used path or explorer
        if concierge_ctx.last_worker_path:
            dept, feat, _ = concierge_ctx.last_worker_path.split(".")
            return concierge_ctx.last_worker_path, self._persona_from_path(dept, feat)

        return "General.explorer.primary", PersonaType.EXPLORER

    def _persona_from_path(self, department: str, feature: str) -> PersonaType:
        """Map department/feature to persona"""
        mapping = {
            "Onboarding": PersonaType.ONBOARDING,
            "Pricing": PersonaType.PRICING,
            "Legal": PersonaType.LEGAL,
            "Creator": PersonaType.CREATOR,
            "Tech": PersonaType.TECH
        }
        return mapping.get(department, PersonaType.EXPLORER)

    def _get_recent_history(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get last N interactions for context sharing"""
        if user_id not in self.persistent_memory:
            return []

        ctx = self.persistent_memory[user_id]
        return [
            {
                "role": "user" if "message_preview" in item else "assistant",
                "content": item.get("message_preview", ""),
                "worker_path": item.get("worker_path"),
                "persona": item.get("persona")
            }
            for item in ctx.engagement_history[-limit:]
        ]

    def _update_preferences(self, concierge_ctx: ConciergeContext, worker_path: str):
        """Track top 3 paths user frequents"""
        path_count = {}

        for engagement in concierge_ctx.engagement_history:
            path = engagement.get("worker_path")
            if path:
                path_count[path] = path_count.get(path, 0) + 1

        # Sort by frequency
        sorted_paths = sorted(path_count.items(), key=lambda x: x[1], reverse=True)
        concierge_ctx.preferred_paths = [path for path, _ in sorted_paths[:3]]

    def _detect_handoff(self, concierge_ctx: ConciergeContext) -> bool:
        """Detect if this interaction is a handoff from previous persona"""
        if len(concierge_ctx.engagement_history) < 2:
            return False

        last_two = concierge_ctx.engagement_history[-2:]
        last_persona = last_two[0].get("persona")
        current_persona = last_two[1].get("persona")

        return last_persona != current_persona