from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Any, Dict
import asyncio

# Import the host bubble system
from .concierge_host_bubble import ConciergeHostBubble, cali_monitor
import sys
import os
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
if ROOT_PATH not in sys.path:
    sys.path.insert(0, ROOT_PATH)
from goat_core.goat_orchestrator import GOATOrchestrator
from goat_core.sample_workers import dals_forge_connector

# Singleton for host system
goat = GOATOrchestrator()
goat.register_dals_forge(dals_forge_connector)
host = ConciergeHostBubble(goat_orchestrator=goat, cali=cali_monitor)

router = APIRouter()

class GreetRequest(BaseModel):
    user_id: str

class MessageRequest(BaseModel):
    user_id: str
    message: str
    context_hints: Dict[str, Any] = None

@router.post("/greet")
async def greet_user(req: GreetRequest):
    greeting, persona = await host.greet(req.user_id)
    return {"greeting": greeting, "persona": persona.get_signature_dict()}

@router.post("/message")
async def handle_message(req: MessageRequest):
    response, persona, meta = await host.handle_message(
        user_id=req.user_id,
        message=req.message,
        context_hints=req.context_hints
    )
    return {
        "response": response.get("response", response),
        "persona": persona.get_signature_dict(),
        "metadata": meta
    }
