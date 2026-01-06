# routes/graph_routes.py
"""
GOAT Graph API Routes - HTML Graph Generation
Provides endpoints for generating interactive graph visualizations
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from engines.graph_engine import GOATGraphEngine
from engines.graph_view_html import GraphViewHTML

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/graphs", tags=["graphs"])

# Initialize engines
graph_engine = GOATGraphEngine()
html_view = GraphViewHTML()

# Pydantic models
class GraphHTMLRequest(BaseModel):
    concepts: Optional[Dict[str, Any]] = None
    graph_type: str = "concepts"  # concepts, characters, themes, contradictions, story_flow
    title: Optional[str] = "GOAT Graph"
    options: Optional[Dict[str, Any]] = None

class GraphHTMLResponse(BaseModel):
    html_path: str
    graph_url: str  # Full URL for frontend
    success: bool
    message: str

@router.post("/html", response_model=GraphHTMLResponse)
async def generate_graph_html(request: GraphHTMLRequest):
    """
    Generate an interactive HTML graph visualization
    Returns the path to the HTML file for iframe embedding
    """
    try:
        logger.info(f"Generating HTML graph of type: {request.graph_type}")

        # Build the graph based on type
        if request.graph_type == "concepts" and request.concepts:
            graph = graph_engine.build_concept_graph(request.concepts)
        elif request.graph_type == "characters" and isinstance(request.concepts, dict):
            # Assume concepts contains character data
            graph = graph_engine.build_character_relationship_graph(request.concepts)
        elif request.graph_type == "themes" and isinstance(request.concepts, dict):
            # Assume concepts contains theme data
            graph = graph_engine.build_theme_cluster_graph(request.concepts)
        else:
            # Default to concept graph
            default_concepts = request.concepts or {"Example": ["Concept1", "Concept2"]}
            graph = graph_engine.build_concept_graph(default_concepts)

        # Render to HTML
        html_path = html_view.render(graph, request.title, request.options)

        # Create full URL (assuming served from /graphs/)
        graph_url = f"/graphs/{html_path.split('/')[-1]}"

        return GraphHTMLResponse(
            html_path=html_path,
            graph_url=graph_url,
            success=True,
            message=f"Interactive graph generated with {graph.number_of_nodes()} nodes"
        )

    except Exception as e:
        logger.error(f"Error generating graph HTML: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate graph: {str(e)}")

@router.post("/concept-html")
async def generate_concept_graph_html(request: Request):
    """
    Quick endpoint for concept graphs (legacy compatibility)
    """
    try:
        data = await request.json()
        concepts = data.get("concepts", {})

        graph = graph_engine.build_concept_graph(concepts)
        html_path = html_view.render(graph, "Concept Graph")

        graph_url = f"/graphs/{html_path.split('/')[-1]}"

        return {
            "html_path": html_path,
            "graph_url": graph_url,
            "success": True
        }

    except Exception as e:
        logger.error(f"Error generating concept graph HTML: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate concept graph: {str(e)}")

@router.get("/test")
async def test_graph_generation():
    """
    Test endpoint that generates a sample graph
    """
    try:
        # Create a test concept graph
        test_concepts = {
            "Abby": ["Love", "Loss", "Courage"],
            "Butch": ["Legacy", "Strength"],
            "Angela": ["Trauma", "Conflict"],
            "Marcus": ["Hope", "Redemption"]
        }

        graph = graph_engine.build_concept_graph(test_concepts)
        html_path = html_view.render(graph, "Test GOAT Graph")

        graph_url = f"/graphs/{html_path.split('/')[-1]}"

        return {
            "message": "Test graph generated successfully",
            "html_path": html_path,
            "graph_url": graph_url,
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges()
        }

    except Exception as e:
        logger.error(f"Error in graph test: {e}")
        raise HTTPException(status_code=500, detail=f"Graph test failed: {str(e)}")