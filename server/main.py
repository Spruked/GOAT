"""
GOAT FastAPI Server - Main API backend
React + FastAPI full-stack architecture
"""

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
import os

# Import GOAT modules
from vault.core import Vault
from vault.glyph_svg import generate_svg, generate_badge_svg
from vault.ipfs_gateway import IPFSGateway
from vault.onchain_anchor import OnChainAnchor
from collector.orchestrator import NFTOrchestrator
from collector.glyph_generator import GlyphGenerator
from knowledge.graph import KnowledgeGraph
from teacher.engine import TeacherEngine, QuizGenerator
from licenser.verifier import Verifier

# Initialize FastAPI
app = FastAPI(
    title="GOAT API - Greatest Of All Teachers",
    description="NFT Knowledge Engine with Glyph + Vault Provenance",
    version="2.1.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
VAULT_PATH = Path(os.getenv("VAULT_PATH", "./data/vault"))
VAULT_KEY = os.getenv("VAULT_ENCRYPTION_KEY", "goat_default_key_change_in_production")
KNOWLEDGE_DB = Path(os.getenv("KNOWLEDGE_DB", "./data/knowledge/graph.db"))

vault = Vault(
    storage_path=VAULT_PATH,
    encryption_key=VAULT_KEY,
    private_key=os.getenv("PRIVATE_KEY")
)

knowledge_graph = KnowledgeGraph(KNOWLEDGE_DB)
teacher = TeacherEngine(knowledge_graph)
quiz_gen = QuizGenerator()
verifier = Verifier(vault)
ipfs_gateway = IPFSGateway()
orchestrator = NFTOrchestrator(vault, ipfs_gateway, GlyphGenerator())
anchor = OnChainAnchor()

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

# Health check
@app.get("/")
async def root():
    return {
        "message": "GOAT v2.1 - The Proven Teacher",
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
async def get_vault_stats():
    """Get vault statistics"""
    return vault.get_stats()

@app.get("/api/glyph/{glyph_id}")
async def get_glyph(glyph_id: str):
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
async def get_proof(glyph_id: str):
    """Get cryptographic proof for glyph"""
    proof = vault.get_proof(glyph_id)
    if "error" in proof:
        raise HTTPException(status_code=404, detail=proof["error"])
    return proof

@app.get("/api/vault/list")
async def list_glyphs(source: Optional[str] = None, limit: int = 100):
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
async def ingest_ipfs(request: IngestRequest):
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
async def ingest_onchain(request: IngestOnChainRequest):
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

@app.post("/api/collect/webhook")
async def webhook_handler(webhook_data: Dict[str, Any]):
    """Handle mint webhooks"""
    try:
        result = await orchestrator.webhook_handler(webhook_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== KNOWLEDGE GRAPH ENDPOINTS =====

@app.get("/api/knowledge/skills")
async def list_skills():
    """List all skills"""
    graph_data = knowledge_graph.export_graph()
    return graph_data["skills"]

@app.get("/api/knowledge/skill/{skill_id}")
async def get_skill_tree(skill_id: str):
    """Get skill tree with prerequisites"""
    tree = knowledge_graph.get_skill_tree(skill_id)
    if not tree:
        raise HTTPException(status_code=404, detail="Skill not found")
    return tree

@app.get("/api/knowledge/path/{skill_id}")
async def get_learning_path(skill_id: str, user_id: Optional[str] = None):
    """Get learning path to skill"""
    path = knowledge_graph.get_learning_path(skill_id, user_id)
    return {"path": path, "total_steps": len(path)}

@app.get("/api/knowledge/export")
async def export_graph():
    """Export complete knowledge graph"""
    return knowledge_graph.export_graph()

# ===== TEACHER ENDPOINTS =====

@app.get("/api/teach/recommend/{user_id}")
async def recommend_lesson(user_id: str, category: Optional[str] = None):
    """Get personalized lesson recommendation"""
    recommendation = teacher.recommend_lesson(user_id, category)
    if not recommendation:
        return {"message": "No recommendations available", "completed_all": True}
    return recommendation

@app.get("/api/teach/explain/{glyph_id}")
async def explain_nft(
    glyph_id: str,
    user_level: str = "beginner",
    style: str = "concise"
):
    """Get AI-generated explanation"""
    explanation = teacher.generate_explanation(glyph_id, user_level, style)
    return explanation

@app.get("/api/teach/quiz/{skill_id}")
async def generate_quiz(skill_id: str, difficulty: str = "medium", num_questions: int = 5):
    """Generate quiz for skill"""
    quiz = quiz_gen.generate_quiz(skill_id, difficulty, num_questions)
    return quiz

@app.post("/api/teach/submit-quiz")
async def submit_quiz(submission: QuizAnswers):
    """Submit quiz answers and get results"""
    # Get quiz (in production, retrieve from database)
    quiz = quiz_gen.generate_quiz(submission.quiz_id)
    result = quiz_gen.grade_quiz(quiz, submission.answers)
    return result

@app.get("/api/teach/progress/{user_id}")
async def get_progress(user_id: str):
    """Get user learning progress"""
    progress = knowledge_graph.get_user_progress(user_id)
    return progress

# ===== VERIFIER ENDPOINTS =====

@app.post("/api/verify/completion")
async def verify_completion(
    user_id: str,
    skill_id: str,
    quiz_score: float,
    glyph_ids: List[str]
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
    glyph_ids: List[str]
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
async def submit_feedback(feedback: FeedbackRequest):
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

# ===== ON-CHAIN ANCHOR ENDPOINTS =====

@app.post("/api/anchor/batch")
async def anchor_batch(request: AnchorRequest):
    """Anchor glyph batch on-chain"""
    try:
        result = anchor.anchor_batch(request.glyph_ids)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/anchor/verify/{root}")
async def verify_anchor(root: str):
    """Check if root is anchored"""
    result = anchor.is_anchored(root)
    return result

@app.get("/api/anchor/proof")
async def get_merkle_proof(glyph_ids: str, glyph_id: str):
    """Get Merkle proof for glyph"""
    glyph_list = glyph_ids.split(",")
    proof = anchor.get_proof(glyph_list, glyph_id)
    root = anchor.get_merkle_root(glyph_list)
    return {
        "glyph_id": glyph_id,
        "proof": proof,
        "root": root
    }

# Serve React frontend in production
# Uncomment when frontend is built
# app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        reload=True
    )
