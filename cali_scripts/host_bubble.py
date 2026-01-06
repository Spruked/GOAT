# cali_scripts/host_bubble.py
"""
Host Bubble - CALI X One Integration
Cognitive feedback loop connecting SKG clusters to UCM telemetry
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from .engine import CaliScripts
from learning.ucm_bridge import UCMBridge

class HostBubble:
    """
    CALI X One Host Bubble - Cognitive feedback loop
    Pipes SKG clustering results into UCM telemetry for real-time adaptation
    """

    def __init__(self):
        self.ucm_bridge = UCMBridge()
        self.active_sessions = {}
        self.cognitive_cycles = []

    async def initialize_session(self, user_id: str, context: Dict[str, Any]) -> str:
        """
        Initialize a new cognitive session for user
        Returns session ID
        """
        session_id = f"bubble_{user_id}_{int(datetime.utcnow().timestamp())}"

        self.active_sessions[session_id] = {
            "user_id": user_id,
            "context": context,
            "start_time": datetime.utcnow(),
            "skg_clusters": [],
            "ucm_telemetry": [],
            "cognitive_state": "initializing"
        }

        # Welcome message from CALI
        welcome_msg = CaliScripts.say("greetings", "cognitive_session_start",
                                    user_name=context.get("display_name", "explorer"))

        return session_id

    async def process_skg_cluster(self, session_id: str, cluster_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process SKG clustering results and pipe to UCM telemetry
        """
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.active_sessions[session_id]

        # Store cluster data
        session["skg_clusters"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "cluster": cluster_data
        })

        # 🚀 Send clusters to Caleon for cross-user cognition fusion
        await self._send_clusters_to_caleon(session["user_id"], cluster_data)

        # Extract insights for UCM
        insights = self._extract_cluster_insights(cluster_data)

        # Send to UCM telemetry
        ucm_response = await self._send_to_ucm_telemetry(session["user_id"], insights)

        # Store UCM response
        session["ucm_telemetry"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "insights": insights,
            "ucm_response": ucm_response
        })

        # Update cognitive state
        session["cognitive_state"] = self._determine_cognitive_state(session)

        # Generate CALI response based on cognitive state
        response = self._generate_cali_response(session)

        return {
            "session_id": session_id,
            "cognitive_state": session["cognitive_state"],
            "insights": insights,
            "cali_response": response,
            "ucm_feedback": ucm_response
        }

    def _extract_cluster_insights(self, cluster_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract actionable insights from SKG cluster data
        """
        insights = {
            "patterns_detected": len(cluster_data.get("clusters", [])),
            "confidence_score": cluster_data.get("confidence", 0.0),
            "novel_predicates": cluster_data.get("new_predicates", []),
            "cognitive_load": cluster_data.get("complexity", "medium"),
            "learning_opportunities": cluster_data.get("gaps", [])
        }

        return insights

    async def _send_to_ucm_telemetry(self, user_id: str, insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send insights to UCM telemetry system
        """
        try:
            # This would integrate with actual UCM telemetry endpoint
            telemetry_data = {
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": "skg_cluster_processed",
                "insights": insights
            }

            # For now, simulate UCM response
            return {
                "status": "processed",
                "adaptation_suggestions": [
                    "Increase learning pace for high-confidence patterns",
                    "Focus attention on novel predicate discovery"
                ],
                "cognitive_adjustments": {
                    "attention_weight": insights.get("confidence_score", 0.5),
                    "curiosity_boost": len(insights.get("novel_predicates", [])) * 0.1
                }
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _send_clusters_to_caleon(self, user_id: str, cluster_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send micro-SKG clusters to Caleon for cross-user cognition fusion
        """
        try:
            import requests
            import time

            # Prepare cluster payload for Caleon
            caleon_payload = {
                "user_id": user_id,
                "worker": "host_bubble",  # This worker's identifier
                "clusters": [cluster_data],  # Wrap in list for API consistency
                "timestamp": time.time()
            }

            # Send to Caleon ingestion endpoint
            response = requests.post(
                "http://localhost:8000/api/caleon/ingest_clusters",
                json=caleon_payload,
                timeout=3
            )

            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "ingested",
                    "ingested_count": result.get("ingested_count", 0),
                    "new_predicates": result.get("new_predicates", [])
                }
            else:
                return {"status": "caleon_error", "code": response.status_code}

        except Exception as e:
            # Don't fail the whole process if Caleon is unavailable
            return {"status": "caleon_unavailable", "error": str(e)}

    def _determine_cognitive_state(self, session: Dict[str, Any]) -> str:
        """
        Determine current cognitive state based on session data
        """
        clusters = session.get("skg_clusters", [])
        telemetry = session.get("ucm_telemetry", [])

        if len(clusters) == 0:
            return "initializing"
        elif len(clusters) < 3:
            return "learning"
        elif any(t.get("insights", {}).get("patterns_detected", 0) > 5 for t in telemetry):
            return "mastering"
        else:
            return "adapting"

    def _generate_cali_response(self, session: Dict[str, Any]) -> str:
        """
        Generate CALI response based on cognitive state
        """
        state = session.get("cognitive_state", "learning")

        if state == "initializing":
            return CaliScripts.say("onboarding", "cognitive_warmup")
        elif state == "learning":
            return CaliScripts.say("encouragement", "cognitive_progress")
        elif state == "mastering":
            return CaliScripts.say("wisdom", "cognitive_mastery")
        else:  # adapting
            return CaliScripts.say("transitions", "cognitive_adaptation")

    async def end_session(self, session_id: str) -> Dict[str, Any]:
        """
        End cognitive session and generate summary
        """
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.active_sessions[session_id]
        session["end_time"] = datetime.utcnow()

        # Generate session summary
        summary = {
            "session_id": session_id,
            "duration_seconds": (session["end_time"] - session["start_time"]).total_seconds(),
            "total_clusters": len(session["skg_clusters"]),
            "final_state": session["cognitive_state"],
            "insights_generated": len(session["ucm_telemetry"])
        }

        # Clean up session
        del self.active_sessions[session_id]

        return summary

# Global Host Bubble instance
host_bubble = HostBubble()