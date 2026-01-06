"""
GOAT FastAPI Server - Main API backend
React + FastAPI full-stack architecture
"""

import sys
import os

# Add parent directory to path FIRST before any other imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException, Response, Request, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
import asyncio
from datetime import datetime, timedelta
import hashlib
import secrets

# Rate limiting
# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from slowapi.middleware import SlowAPIMiddleware

# Import GOAT modules
from vault.core import Vault
from vault.glyph_svg import generate_svg, generate_badge_svg
from vault.ipfs_gateway import IPFSGateway
from vault.onchain_anchor import OnChainAnchor
from collector.orchestrator import NFTOrchestrator
from collector.glyph_generator import GlyphGenerator
from knowledge.graph import KnowledgeGraph
# from learning.engine import LearningEngine, QuizGenerator, TeachingNFTGenerator
# from learning.legacy_builder import LegacyBuilder
from licenser.verifier import Verifier
from vault_forge.vault_generator import create_vault
from learning.ucm_bridge import UCMBridge


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from CertSig_upsell_manager import minting_manager

# Import ingest endpoint
from endpoints.ingest import router as ingest_router

# Import podcast engine routes
# from routes.podcast_engine import router as podcast_router

# Import auth routes
from routes.auth import router as auth_router

# Import CALI Scripts routes
# from cali_scripts import router as cali_scripts_router

# Import user tracking routes
# from user_tracking import router as user_tracking_router

# Import organizer routes
# from organizer.api import api_router as organizer_router

# Import book builder routes
# from book_builder.api.book_builder_routes import router as book_builder_router

# Import UCM routes
# from routes.ucm import router as ucm_router

# Import user routes
# from routes.user import router as user_router

# Import upload routes
from routes.upload import router as upload_router

# Import CALI X One routes
# from routes.cali_x_one import router as cali_x_one_router

# Import graph routes
# from routes.graph_routes import router as graph_routes_router

# Import UQV routes
# from routes.uqv import router as uqv_router

# Import Caleon generative routes
# from routes.caleon_generative import router as caleon_generative_router

# Import manuals routes
# from routes.manuals import router as manuals_router

# Import vault adapter routes (thin adapter to control embedded Vault System)
# from routes.vault_adapter import router as vault_adapter_router

# Import onboarding routes
from server.routes.capture import router as capture_router
from server.routes.guest import router as guest_router
from server.routes.write import router as write_router

# Import DALS routes
from DALS.api.host_routes import router as host_router
from DALS.api.broadcast_routes import router as broadcast_router
from DALS.api.uqv_routes import router as dals_uqv_router
from DALS.api.tts_routes import router as tts_router

# Authentication & Security
API_KEYS = os.getenv("API_KEYS", "goat_dev_key,goat_prod_key").split(",")
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds

# Rate limiting storage (in production, use Redis)
rate_limit_store = {}

def verify_api_key(api_key: str = None):
    """Verify API key"""
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

def check_rate_limit(client_ip: str):
    """Check and update rate limit"""
    now = datetime.utcnow()
    key = f"rate_limit:{client_ip}"

    if key not in rate_limit_store:
        rate_limit_store[key] = {"count": 0, "reset_time": now + timedelta(seconds=RATE_LIMIT_WINDOW)}

    limit_data = rate_limit_store[key]

    # Reset if window expired
    if now > limit_data["reset_time"]:
        limit_data["count"] = 0
        limit_data["reset_time"] = now + timedelta(seconds=RATE_LIMIT_WINDOW)

    # Check limit
    if limit_data["count"] >= RATE_LIMIT_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    limit_data["count"] += 1

async def get_client_ip(request: Request):
    """Get client IP for rate limiting"""
    return request.client.host if request.client else "unknown"

# Dependency for authenticated endpoints
def require_auth(api_key: str = None):
    """Require authentication"""
    return verify_api_key(api_key)

# Background Job System
job_store = {}
job_counter = 0

def create_job(task_type: str, params: Dict[str, Any]) -> str:
    """Create a background job"""
    global job_counter
    job_counter += 1
    job_id = f"{task_type}_{job_counter}_{int(datetime.utcnow().timestamp())}"

    job_store[job_id] = {
        "id": job_id,
        "type": task_type,
        "status": "pending",
        "params": params,
        "created_at": datetime.utcnow().isoformat(),
        "progress": 0,
        "result": None,
        "error": None
    }

    return job_id

def get_job_status(job_id: str) -> Optional[Dict[str, Any]]:
    """Get job status"""
    return job_store.get(job_id)

async def run_vault_forge_job(job_id: str, project_name: str, tier: str, deliverables_path: str, auto_upload: bool):
    """Run vault forge as background job"""
    try:
        job_store[job_id]["status"] = "running"
        job_store[job_id]["progress"] = 10

        # Simulate progress updates
        await asyncio.sleep(1)
        job_store[job_id]["progress"] = 30

        zip_path = create_vault(project_name, tier, deliverables_path, auto_upload)

        job_store[job_id]["progress"] = 100
        job_store[job_id]["status"] = "completed"
        job_store[job_id]["result"] = {
            "vault_zip": zip_path,
            "tier": tier,
            "auto_upload": auto_upload
        }

    except Exception as e:
        job_store[job_id]["status"] = "failed"
        job_store[job_id]["error"] = str(e)

# Import auth functions
# from server.auth import create_default_admin

# Initialize FastAPI
app = FastAPI(
    title="GOAT API - Greatest Of All Time",
    description="NFT Knowledge Engine with Glyph + Vault Provenance",
    version="2.1.0"
)

# Create default admin user
# create_default_admin()

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for graph visualizations
app.mount("/graphs", StaticFiles(directory="static/graphs"), name="graphs")

# Rate limiting
# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_middleware(SlowAPIMiddleware)


# Mount project API endpoints
app.include_router(ingest_router)
# app.include_router(podcast_router)
app.include_router(auth_router, prefix="/api")
# app.include_router(cali_scripts_router)
# app.include_router(user_tracking_router)
# app.include_router(user_router)
app.include_router(upload_router)
# app.include_router(cali_x_one_router)
# app.include_router(graph_routes_router)
# app.include_router(uqv_router)
# app.include_router(caleon_generative_router)
# Manuals generation (separate from books)
# app.include_router(manuals_router)
# Vault System adapter routes (thin control & status endpoints)
# app.include_router(vault_adapter_router)
# Onboarding routes
app.include_router(capture_router, prefix="/capture", tags=["Capture"])
app.include_router(guest_router, prefix="/guest", tags=["Guest"])
app.include_router(write_router, prefix="/write", tags=["Write"])
# DALS messaging infrastructure
app.include_router(host_router, prefix="/dals", tags=["DALS Host"])
app.include_router(broadcast_router, prefix="/dals", tags=["DALS Broadcast"])
app.include_router(dals_uqv_router, prefix="/dals", tags=["DALS UQV"])
app.include_router(tts_router, prefix="/dals", tags=["DALS TTS"])
# app.include_router(organizer_router)
# app.include_router(book_builder_router)
# app.include_router(ucm_router)
# app.include_router(caleon_generative_router)

# Simple test endpoint
@app.get("/test")
async def test_endpoint():
    return {"status": "ok", "message": "GOAT API is running"}

# Initialize core components
VAULT_PATH = Path(os.getenv("VAULT_PATH", "./data/vault"))
VAULT_KEY = os.getenv("VAULT_ENCRYPTION_KEY", "goat_default_key_change_in_production")
KNOWLEDGE_DB = Path(os.getenv("KNOWLEDGE_DB", "./data/knowledge/graph.db"))

# Initialize UCM Bridge for external cognition service
ucm_bridge = UCMBridge(
    ucm_endpoint=os.getenv("UCM_ENDPOINT", "http://external-ucm-service:8080")
)

vault = Vault(
    storage_path=VAULT_PATH,
    encryption_key=VAULT_KEY,
    private_key=os.getenv("PRIVATE_KEY")
)

# Integrate external SKG-2025 if available
SKG_DIR = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "skg-2025"))
if SKG_DIR.exists():
    # Make the external skg package importable
    sys.path.insert(0, str(SKG_DIR))
    logger.info(f"SKG-2025 directory added to path: {SKG_DIR}")

# Integrate external Vault System (Vault_System_1.0) if available
VAULT_SYSTEM_INSTANCE = None
VAULT_SYSTEM_DIR = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "external_repos", "Vault_System_1.0", "vault_system"))
if VAULT_SYSTEM_DIR.exists():
    # Make the external vault_system package importable
    sys.path.insert(0, str(VAULT_SYSTEM_DIR))
    try:
        from plug_and_play_integration import AdvancedVaultSystem
        VAULT_SYSTEM_ENABLED = os.getenv("VAULT_SYSTEM_ENABLE", "false").lower() in ("1", "true", "yes")
        if VAULT_SYSTEM_ENABLED:
            import threading

            def _start_vault_system():
                global VAULT_SYSTEM_INSTANCE
                master_key = os.getenv("VAULT_SYSTEM_MASTER_KEY", "master_key_2024")
                try:
                    VAULT_SYSTEM_INSTANCE = AdvancedVaultSystem(master_key)
                except Exception as _e:
                    logger.error(f"Failed to initialize AdvancedVaultSystem: {_e}")

            # Start vault system in background to avoid blocking server startup
            threading.Thread(target=_start_vault_system, daemon=True).start()
            logger.info("Vault System integration enabled and starting in background")
        else:
            logger.info("Vault System code is present but not enabled. Set VAULT_SYSTEM_ENABLE=true to enable it.")
    except Exception as e:
        logger.warning(f"Vault System integration not available: {e}")

# knowledge_graph = KnowledgeGraph(KNOWLEDGE_DB)
# learning_engine = LearningEngine(knowledge_graph)
# quiz_gen = QuizGenerator(ucm_bridge=learning_engine.ucm_bridge)
# verifier = Verifier(vault)
# ipfs_gateway = IPFSGateway()
# orchestrator = NFTOrchestrator(vault, ipfs_gateway, GlyphGenerator())
# anchor = OnChainAnchor()
# legacy_builder = LegacyBuilder()

# Pydantic models
class IngestRequest(BaseModel):
    cid: str
    auto_pin: bool = True

class IngestOnChainRequest(BaseModel):
    contract: str
    token_id: str
    rpc_url: Optional[str] = None

class QuizAnswers(BaseModel):
    quiz_id: str
    answers: Dict[str, str]

class FeedbackRequest(BaseModel):
    skill_id: str
    rating: int
    comments: Optional[str] = ""
    difficulty: Optional[str] = "medium"

class AnchorRequest(BaseModel):
    glyph_ids: List[str]

class ManualKnowledgeRequest(BaseModel):
    name: str
    category: str
    description: str
    content: str
    tags: str
    concepts: List[Dict[str, str]] = []
    skill_level: str = "Beginner"

class LegacyBuildRequest(BaseModel):
    user_id: str
    author: str
    title: str
    product_type: str = "book"  # book, course, masterclass, etc.
    data_files: List[str] = []  # Paths to data files for VisiData analysis
    description: Optional[str] = ""

class MintRequest(BaseModel):
    legacy_id: str
    mint_engine: str = "certsig"  # certsig or truemark

# Health check
@app.get("/")
async def root():
    return {
        "message": "GOAT v2.1 - The Proven Legacy Builder",
        "status": "online",
        "features": ["Glyph IDs", "Vault", "On-Chain Anchoring", "AI Teaching"]
    }

@app.get("/api/health")
async def health():
    stats = vault.get_stats()
    return {
        "status": "healthy",
        "vault": stats,
        "knowledge_graph": "active"
    }

# ===== VAULT ENDPOINTS =====

@app.get("/api/vault/stats")
async def get_vault_stats(api_key: str = Depends(require_auth)):
    """Get vault statistics"""
    return vault.get_stats()

@app.get("/api/glyph/{glyph_id}")
async def get_glyph(glyph_id: str, api_key: str = Depends(require_auth)):
    """Get glyph by ID"""
    glyph = vault.retrieve(glyph_id)
    if not glyph:
        raise HTTPException(status_code=404, detail="Glyph not found")
    
    return {
        "id": glyph.id,
        "data_hash": glyph.data_hash,
        "source": glyph.source,
        "timestamp": glyph.timestamp,
        "signer": glyph.signer,
        "signature": glyph.signature,
        "verified": glyph.verified,
        "data": glyph.data
    }

@app.get("/api/vault/proof/{glyph_id}")
async def get_proof(glyph_id: str, api_key: str = Depends(require_auth)):
    """Get cryptographic proof for glyph"""
    proof = vault.get_proof(glyph_id)
    if "error" in proof:
        raise HTTPException(status_code=404, detail=proof["error"])
    return proof

@app.get("/api/vault/list")
async def list_glyphs(
    source: Optional[str] = None,
    limit: int = 100,
    api_key: str = Depends(require_auth)
):
    """List all glyphs"""
    glyphs = vault.list_all(source, limit)
    return {
        "glyphs": [
            {
                "id": g.id,
                "source": g.source,
                "timestamp": g.timestamp,
                "verified": g.verified
            }
            for g in glyphs
        ],
        "count": len(glyphs)
    }

@app.get("/glyph/svg/{glyph_id}")
async def get_glyph_svg(glyph_id: str):
    """Get glyph as SVG image"""
    svg = generate_svg(glyph_id)
    return Response(content=svg, media_type="image/svg+xml")

@app.get("/glyph/badge/{glyph_id}")
async def get_badge_svg(glyph_id: str, label: str = "Verified"):
    """Get verification badge SVG"""
    svg = generate_badge_svg(glyph_id, label)
    return Response(content=svg, media_type="image/svg+xml")

# ===== COLLECTOR ENDPOINTS =====

@app.post("/api/collect/ipfs")
async def ingest_ipfs(request: IngestRequest, api_key: str = Depends(require_auth)):
    """Ingest NFT from IPFS"""
    try:
        glyph = await orchestrator.ingest_ipfs(request.cid, request.auto_pin)
        return {
            "status": "success",
            "glyph_id": glyph.id,
            "source": glyph.source
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/collect/onchain")
async def ingest_onchain(request: IngestOnChainRequest, api_key: str = Depends(require_auth)):
    """Ingest NFT from blockchain"""
    try:
        glyph = await orchestrator.ingest_onchain(
            request.contract,
            request.token_id,
            request.rpc_url or "https://eth-mainnet.g.alchemy.com/v2/demo"
        )
        return {
            "status": "success",
            "glyph_id": glyph.id,
            "contract": request.contract,
            "token_id": request.token_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/collect/manual")
async def ingest_manual_knowledge(request: ManualKnowledgeRequest, api_key: str = Depends(require_auth)):
    """Process manually entered knowledge and generate glyphs"""
    try:
        result = await orchestrator.ingest_manual(request)
        return {
            "status": "success",
            "glyph_id": result.id,
            "glyph_ids": result.data.get("glyph_list", []) if result.data else [],
            "source": "manual",
            "ipfs_metadata": result.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/collect/webhook")
async def webhook_handler(webhook_data: Dict[str, Any], api_key: str = Depends(require_auth)):
    """Handle mint webhooks"""
    try:
        result = await orchestrator.webhook_handler(webhook_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== KNOWLEDGE GRAPH ENDPOINTS =====

@app.get("/api/knowledge/skills")
async def list_skills(api_key: str = Depends(require_auth)):
    """List all skills"""
    graph_data = knowledge_graph.export_graph()
    return graph_data["skills"]

@app.get("/api/knowledge/skill/{skill_id}")
async def get_skill_tree(skill_id: str, api_key: str = Depends(require_auth)):
    """Get skill tree with prerequisites"""
    tree = knowledge_graph.get_skill_tree(skill_id)
    if not tree:
        raise HTTPException(status_code=404, detail="Skill not found")
    return tree

@app.get("/api/knowledge/path/{skill_id}")
async def get_learning_path(
    skill_id: str,
    user_id: Optional[str] = None,
    api_key: str = Depends(require_auth)
):
    """Get learning path to skill"""
    path = knowledge_graph.get_learning_path(skill_id, user_id)
    return {"path": path, "total_steps": len(path)}

@app.get("/api/knowledge/export")
async def export_graph(api_key: str = Depends(require_auth)):
    """Export complete knowledge graph"""
    return knowledge_graph.export_graph()

# ===== LEARNING ENDPOINTS =====

@app.get("/api/teach/recommend/{user_id}")
async def recommend_lesson(
    user_id: str,
    category: Optional[str] = None,
    api_key: str = Depends(require_auth)
):
    """Get personalized lesson recommendation"""
    recommendation = learning_engine.recommend_lesson(user_id, category)
    if not recommendation:
        return {"message": "No recommendations available", "completed_all": True}
    return recommendation

@app.get("/api/teach/explain/{glyph_id}")
async def explain_nft(
    glyph_id: str,
    user_level: str = "beginner",
    style: str = "concise",
    api_key: str = Depends(require_auth)
):
    """Get AI-generated explanation"""
    explanation = learning_engine.generate_explanation(glyph_id, user_level, style)
    return explanation

@app.get("/api/teach/quiz/{skill_id}")
async def generate_quiz(
    skill_id: str,
    difficulty: str = "medium",
    num_questions: int = 5,
    user_id: str = Query(..., description="User ID for personalization"),
    api_key: str = Depends(require_auth)
):
    """Generate quiz for skill"""
    quiz = quiz_gen.generate_quiz(skill_id, difficulty, num_questions, user_id)

    # Store quiz for persistence
    quiz_id = f"quiz_{skill_id}_{user_id}_{int(datetime.utcnow().timestamp())}"
    knowledge_graph.store_quiz(quiz_id, skill_id, user_id, quiz)

    return {**quiz, "id": quiz_id}

@app.post("/api/teach/submit-quiz")
async def submit_quiz(
    submission: QuizAnswers,
    api_key: str = Depends(require_auth)
):
    """Submit quiz answers and get results"""
    try:
        result = knowledge_graph.submit_quiz_answers(submission.quiz_id, submission.answers)

        # Update user progress
        quiz = knowledge_graph.get_quiz(submission.quiz_id)
        if quiz:
            learning_engine.track_progress(quiz["user_id"], quiz["skill_id"], result["score"])

        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/teach/progress/{user_id}")
async def get_progress(
    user_id: str,
    api_key: str = Depends(require_auth)
):
    """Get user learning progress with UCM insights"""
    progress = knowledge_graph.get_user_progress(user_id)
    
    # Enhance with UCM cognition analysis
    ucm_insights = learning_engine.ucm_bridge.get_skill_inference(user_id)
    if ucm_insights:
        progress["ucm_insights"] = ucm_insights
    
    return progress

# ===== VERIFIER ENDPOINTS =====

@app.post("/api/verify/completion")
async def verify_completion(
    user_id: str,
    skill_id: str,
    quiz_score: float,
    glyph_ids: List[str],
    api_key: str = Depends(require_auth)
):
    """Verify quiz completion"""
    verification = verifier.verify_quiz_completion(
        user_id, skill_id, quiz_score, glyph_ids
    )
    return verification

@app.post("/api/verify/mint-badge")
async def mint_badge(
    user_id: str,
    skill_id: str,
    quiz_score: float,
    glyph_ids: List[str],
    api_key: str = Depends(require_auth)
):
    """Verify and mint learner badge"""
    # Verify first
    verification = verifier.verify_quiz_completion(
        user_id, skill_id, quiz_score, glyph_ids
    )
    
    if not verification["verified"]:
        raise HTTPException(status_code=400, detail="Verification failed")
    
    # Mint badge
    badge = verifier.mint_badge(user_id, skill_id, verification)
    
    # Update user mastery
    knowledge_graph.update_user_mastery(user_id, skill_id, quiz_score)
    
    return badge

@app.post("/api/verify/feedback")
async def submit_feedback(
    feedback: FeedbackRequest,
    api_key: str = Depends(require_auth)
):
    """Submit user feedback"""
    result = verifier.feedback_loop(
        feedback.skill_id,
        {
            "rating": feedback.rating,
            "comments": feedback.comments,
            "difficulty": feedback.difficulty
        }
    )
    return result

# ===== VAULT FORGE ENDPOINTS =====

@app.post("/api/vault-forge/create")
async def create_vault_package(
    project_name: str,
    tier: str = "basic",
    deliverables_path: str = "./deliverables",
    auto_upload: bool = False,
    api_key: str = Depends(require_auth)
):
    """Create immutable vault package for permanent storage"""
    try:
        zip_path = create_vault(project_name, tier, deliverables_path, auto_upload)
        return {
            "success": True,
            "vault_zip": zip_path,
            "tier": tier,
            "auto_upload": auto_upload,
            "message": f"Vault package created for {project_name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== ON-CHAIN ANCHOR ENDPOINTS =====

@app.post("/api/anchor/batch")
async def anchor_batch(request: AnchorRequest, api_key: str = Depends(require_auth)):
    """Anchor glyph batch on-chain"""
    try:
        result = anchor.anchor_batch(request.glyph_ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/anchor/verify/{root}")
async def verify_anchor(root: str, api_key: str = Depends(require_auth)):
    """Check if root is anchored"""
    result = anchor.is_anchored(root)
    return result

@app.get("/api/anchor/proof")
async def get_merkle_proof(
    glyph_ids: str,
    glyph_id: str,
    api_key: str = Depends(require_auth)
):
    """Get Merkle proof for glyph"""
    glyph_list = glyph_ids.split(",")
    proof = anchor.get_proof(glyph_list, glyph_id)
    root = anchor.get_merkle_root(glyph_list)
    return {
        "glyph_id": glyph_id,
        "proof": proof,
        "root": root
    }

@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str, api_key: str = Depends(require_auth)):
    """Get job status"""
    job = get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/api/jobs")
async def list_jobs(api_key: str = Depends(require_auth)):
    """List all jobs"""
    return {"jobs": list(job_store.values()), "count": len(job_store)}

# ===== CALEON CHAT ENDPOINTS =====

class CaleonChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"
    context: Optional[Dict[str, Any]] = {}

class CaleonChatResponse(BaseModel):
    response: str
    context: Dict[str, Any]
    ucm_status: str

@app.post("/api/caleon/chat")
async def caleon_chat(request: CaleonChatRequest, api_key: str = Depends(require_auth)):
    """Caleon AI chat endpoint with UCM integration"""
    try:
        # Get UCM-powered response
        ucm_response = ucm_bridge.request_explanation(
            skill_id="general_assistance",
            user_level="intermediate"
        )

        # Enhance with context awareness
        context = request.context or {}
        panel = context.get("activePanel", "dashboard")
        bundle = context.get("activeBundle")

        # Generate context-aware response
        if panel == "vault":
            response_text = f"I see you're working in the Vault. {ucm_response[:100]}... Would you like help with glyph creation or vault management?"
        elif panel == "learn":
            response_text = f"In the learning panel, I can assist with your educational journey. {ucm_response[:100]}... Shall I generate a personalized quiz?"
        elif panel == "collect":
            response_text = f"The collection system is powerful. {ucm_response[:100]}... Need help ingesting NFTs or managing your collection?"
        else:
            response_text = f"Welcome to GOAT. {ucm_response[:100]}... I'm here to help you navigate the system."

        return CaleonChatResponse(
            response=response_text,
            context={
                "panel": panel,
                "bundle": bundle,
                "timestamp": datetime.utcnow().isoformat()
            },
            ucm_status="connected"
        )

    except Exception as e:
        # Fallback response if UCM fails
        return CaleonChatResponse(
            response="I'm here to help, though I'm having trouble connecting to the full UCM cognition right now. How can I assist you with the GOAT system?",
            context={"error": str(e)},
            ucm_status="fallback"
        )

# ===== VISIDATA INTEGRATION ENDPOINTS =====

class DataExploreRequest(BaseModel):
    data: List[Dict[str, Any]]  # List of rows, each row is a dict
    format: str = "json"  # json, csv, etc.

@app.post("/api/data/explore")
async def explore_data(request: DataExploreRequest, api_key: str = Depends(require_auth)):
    """Explore data using VisiData"""
    try:
        import visidata as vd
        from visidata import Sheet
        import io
        import json
        
        # Convert data to VisiData sheet
        if request.format == "json":
            # Create a temporary JSON file
            json_data = json.dumps(request.data)
            sheet = vd.openSource("json", io.StringIO(json_data))
        elif request.format == "csv":
            # Assume data is list of dicts, convert to CSV
            import csv
            output = io.StringIO()
            if request.data:
                writer = csv.DictWriter(output, fieldnames=request.data[0].keys())
                writer.writeheader()
                writer.writerows(request.data)
            sheet = vd.openSource("csv", io.StringIO(output.getvalue()))
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
        
        # Get basic stats
        stats = {
            "nRows": sheet.nRows,
            "nCols": sheet.nCols,
            "columns": [col.name for col in sheet.columns],
            "sample_rows": request.data[:5] if len(request.data) > 5 else request.data
        }
        
        return {
            "status": "success",
            "stats": stats,
            "visidata_ready": True
        }
        
    except ImportError:
        raise HTTPException(status_code=503, detail="VisiData not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data exploration failed: {str(e)}")

@app.post("/api/data/analyze")
async def analyze_data(request: DataExploreRequest, api_key: str = Depends(require_auth)):
    """Advanced data analysis using VisiData"""
    try:
        import visidata as vd
        import pandas as pd
        from io import StringIO
        
        # Convert to pandas for analysis
        df = pd.DataFrame(request.data)
        
        analysis = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "describe": df.describe().to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "unique_counts": df.nunique().to_dict()
        }
        
        # Try VisiData frequency analysis on first column
        if not df.empty and len(df.columns) > 0:
            first_col = df.columns[0]
            freq = df[first_col].value_counts().head(10).to_dict()
            analysis["frequency_first_col"] = freq
        
        return {
            "status": "success",
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# ===== LEGACY BUILDING ENDPOINTS =====

@app.post("/api/legacy/build")
async def build_legacy(request: LegacyBuildRequest, api_key: str = Depends(require_auth)):
    """Build a legacy product using VisiData analysis"""
    try:
        user_data = {
            "user_id": request.user_id,
            "author": request.author,
            "title": request.title,
            "data_files": request.data_files,
            "description": request.description
        }

        legacy = legacy_builder.build_legacy(user_data, request.product_type)

        return {
            "status": "success",
            "legacy": legacy,
            "export_path": str(legacy_builder.get_legacy_path(request.user_id, request.product_type))
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Legacy building failed: {str(e)}")

@app.post("/api/legacy/mint")
async def mint_legacy(request: MintRequest, api_key: str = Depends(require_auth)):
    """Mint legacy NFT using CertSig or TrueMark"""
    try:
        # Load legacy data
        user_id, product_type = request.legacy_id.split('_', 1)
        legacy_path = legacy_builder.get_legacy_path(user_id, product_type)
        legacy_file = legacy_path / "legacy.json"

        if not legacy_file.exists():
            raise HTTPException(status_code=404, detail="Legacy not found")

        with open(legacy_file, 'r') as f:
            legacy_data = json.load(f)

        # Prepare mint data
        mint_data = minting_manager.prepare_mint_data(legacy_data, request.mint_engine)

        # Here you would integrate with actual CertSig/TrueMark APIs
        # For now, return mock response
        mint_result = {
            "mint_engine": request.mint_engine,
            "engine_details": minting_manager.mint_engines.get(request.mint_engine, {}),
            "transaction_hash": f"mock_tx_{request.legacy_id}_{datetime.utcnow().timestamp()}",
            "token_id": f"mock_token_{request.legacy_id}",
            "contract_address": f"mock_contract_{request.mint_engine}",
            "metadata": mint_data["metadata"],
            "content_hash": mint_data["content_hash"],
            "timestamp": mint_data["timestamp"]
        }

        return {
            "status": "success",
            "mint_result": mint_result,
            "message": f"Legacy minted successfully on {minting_manager.mint_engines[request.mint_engine]['name']}",
            "caleon_message": minting_manager.get_caleon_seeds("post_mint")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Minting failed: {str(e)}")

@app.get("/api/legacy/{user_id}/{product_type}")
async def get_legacy(user_id: str, product_type: str, api_key: str = Depends(require_auth)):
    """Get legacy product details"""
    try:
        legacy_path = legacy_builder.get_legacy_path(user_id, product_type)
        legacy_file = legacy_path / "legacy.json"

        if not legacy_file.exists():
            raise HTTPException(status_code=404, detail="Legacy not found")

        with open(legacy_file, 'r') as f:
            legacy = json.load(f)

        return {
            "status": "success",
            "legacy": legacy
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve legacy: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,  # Pass app object directly instead of string
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        reload=False
    )
