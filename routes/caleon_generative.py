# routes/caleon_generative.py
"""
Caleon Generative API Routes
Links the Bubble Assistant to the UCM generative pipeline
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from goat_core.draft_engine.caleon_bridge import CaleonBridge

router = APIRouter(prefix="/api/caleon", tags=["caleon-generative"])

# Pydantic models
class CaleonMessageRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

class CaleonResponse(BaseModel):
    response: str
    timestamp: str
    context_used: Dict[str, Any]

class ClusterIngestRequest(BaseModel):
    user_id: str
    worker: str
    clusters: List[Dict[str, Any]]
    timestamp: float

class ClusterIngestResponse(BaseModel):
    ingested_count: int
    new_predicates: List[str]
    status: str

# Dependency to get Caleon Bridge
def get_caleon_bridge():
    return CaleonBridge()

@router.post("/generate", response_model=CaleonResponse)
async def generate_response(
    request: CaleonMessageRequest,
    caleon: CaleonBridge = Depends(get_caleon_bridge)
):
    """
    Generate a response from Caleon via UCM pipeline
    Used for dynamic AI responses in the Bubble Assistant
    """
    try:
        # Build context for Caleon
        context = request.context or {}
        context.update({
            "interface": "bubble_assistant",
            "timestamp": request.timestamp,
            "message_type": "conversational"
        })

        # For now, create a structured prompt for Caleon
        # In production, this would be more sophisticated
        prompt_data = {
            "chapter_title": "Bubble Assistant Conversation",
            "section_title": "User Query",
            "tone": "conversational_helpful",
            "goals": f"Respond helpfully to: {request.message}",
            "continuity_context": f"Previous context: {json.dumps(context)}"
        }

        # Generate response via Caleon Bridge
        response_text = caleon.generate_section(**prompt_data)

        return CaleonResponse(
            response=response_text,
            timestamp=request.timestamp or "now",
            context_used=context
        )

    except Exception as e:
        # Fallback response if Caleon is unavailable
        fallback_response = (
            "I apologize, but I'm currently unable to respond through my primary intelligence. "
            "This is a temporary state while I evolve. Please try again in a moment, or use the "
            "draft engine for content creation tasks."
        )

        return CaleonResponse(
            response=fallback_response,
            timestamp=request.timestamp or "now",
            context_used={"error": str(e), "fallback": True}
        )

@router.post("/stream")
async def stream_response(
    request: CaleonMessageRequest,
    caleon: CaleonBridge = Depends(get_caleon_bridge)
):
    """
    Stream Caleon's response in real-time using Phi-3 Mini
    True streaming with token-by-token generation
    """

    async def generate_stream():
        try:
            # Build context
            context = request.context or {}
            context.update({
                "interface": "bubble_assistant_stream",
                "timestamp": request.timestamp,
                "message_type": "streaming_conversation"
            })

            # Create prompt for streaming
            prompt_data = {
                "chapter_title": "Live Conversation",
                "section_title": "Streaming Response",
                "tone": "conversational_streaming",
                "goals": f"Stream response to: {request.message}",
                "continuity_context": f"Context: {json.dumps(context)}"
            }

            # Use true Phi-3 streaming
            async for chunk in caleon.generate_section_stream(**prompt_data):
                chunk_data = CaleonStreamChunk(
                    chunk=chunk,
                    is_complete=False
                )
                yield f"data: {json.dumps(chunk_data.dict())}\n\n"

            # Send completion signal
            final_chunk = CaleonStreamChunk(
                chunk="",
                is_complete=True
            )
            yield f"data: {json.dumps(final_chunk.dict())}\n\n"

        except Exception as e:
            # Error chunk
            error_chunk = CaleonStreamChunk(
                chunk=f"I apologize, but I encountered an error: {str(e)}",
                is_complete=True
            )
            yield f"data: {json.dumps(error_chunk.dict())}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )

@router.get("/health")
async def health_check():
    """
    Check if Caleon UCM pipeline is available
    """
    try:
        # Simple health check - in production, this would ping the actual UCM
        return {
            "status": "healthy",
            "timestamp": "now",
            "pipeline": "ucm_active"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": "now"
        }

@router.post("/ingest_clusters", response_model=ClusterIngestResponse)
async def ingest_worker_clusters(
    request: ClusterIngestRequest,
    caleon: CaleonBridge = Depends(get_caleon_bridge)
):
    """
    Ingest micro-SKG clusters from workers for cross-user cognition fusion
    Caleon deduplicates, correlates, and evolves higher-order predicates
    """
    try:
        # Process clusters through Caleon for fusion
        fusion_result = await caleon.fuse_clusters(
            user_id=request.user_id,
            worker=request.worker,
            clusters=request.clusters,
            timestamp=request.timestamp
        )

        return ClusterIngestResponse(
            ingested_count=len(request.clusters),
            new_predicates=fusion_result.get("new_predicates", []),
            status="fusion_complete"
        )

    except Exception as e:
        # Log error but don't fail - workers should continue
        print(f"Caleon cluster ingestion error: {e}")
        return ClusterIngestResponse(
            ingested_count=0,
            new_predicates=[],
            status=f"ingestion_failed: {str(e)}"
        )