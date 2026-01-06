# routes/graph_visualization.py
"""
GOAT Graph Visualization API Endpoints
Provides interactive graph generation for concepts, characters, themes, and knowledge
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import os
import logging

from engines.graph_engine import GOATGraphEngine
from engines.deep_parser import DeepParser
from engines.contradiction_detector import ContradictionDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
graph_engine = GOATGraphEngine()

# Pydantic models for request/response
class ConceptGraphRequest(BaseModel):
    concepts: Dict[str, List[str]]
    title: Optional[str] = "Concept Graph"

class CharacterGraphRequest(BaseModel):
    characters: Dict[str, Dict[str, Any]]
    title: Optional[str] = "Character Relationships"

class ThemeGraphRequest(BaseModel):
    themes: Dict[str, List[str]]
    title: Optional[str] = "Theme Clusters"

class StoryGraphRequest(BaseModel):
    text: str
    graph_type: str = "concepts"  # concepts, characters, themes, contradictions, story_flow

class GraphResponse(BaseModel):
    graph_url: str
    graph_stats: Dict[str, Any]
    success: bool
    message: str

@router.post("/concept-graph", response_model=GraphResponse)
async def create_concept_graph(request: ConceptGraphRequest, background_tasks: BackgroundTasks):
    """
    Generate an interactive concept relationship graph
    """
    try:
        logger.info(f"Creating concept graph with {len(request.concepts)} concepts")

        # Build graph
        graph = graph_engine.build_concept_graph(request.concepts)

        # Generate visualization
        graph_url = graph_engine.visualize(graph, request.title)

        # Get statistics
        stats = graph_engine.get_graph_stats(graph)

        # Clean up old graphs in background (keep last 50)
        background_tasks.add_task(cleanup_old_graphs, keep_last=50)

        return GraphResponse(
            graph_url=graph_url,
            graph_stats=stats,
            success=True,
            message=f"Concept graph created with {stats['nodes']} nodes and {stats['edges']} edges"
        )

    except Exception as e:
        logger.error(f"Error creating concept graph: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create concept graph: {str(e)}")

@router.post("/character-graph", response_model=GraphResponse)
async def create_character_graph(request: CharacterGraphRequest, background_tasks: BackgroundTasks):
    """
    Generate character relationship visualization
    """
    try:
        logger.info(f"Creating character graph with {len(request.characters)} characters")

        graph = graph_engine.build_character_relationship_graph(request.characters)
        graph_url = graph_engine.visualize(graph, request.title)
        stats = graph_engine.get_graph_stats(graph)

        background_tasks.add_task(cleanup_old_graphs, keep_last=50)

        return GraphResponse(
            graph_url=graph_url,
            graph_stats=stats,
            success=True,
            message=f"Character relationship graph created with {stats['nodes']} nodes"
        )

    except Exception as e:
        logger.error(f"Error creating character graph: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create character graph: {str(e)}")

@router.post("/theme-graph", response_model=GraphResponse)
async def create_theme_graph(request: ThemeGraphRequest, background_tasks: BackgroundTasks):
    """
    Generate theme cluster visualization
    """
    try:
        logger.info(f"Creating theme graph with {len(request.themes)} themes")

        graph = graph_engine.build_theme_cluster_graph(request.themes)
        graph_url = graph_engine.visualize(graph, request.title)
        stats = graph_engine.get_graph_stats(graph)

        background_tasks.add_task(cleanup_old_graphs, keep_last=50)

        return GraphResponse(
            graph_url=graph_url,
            graph_stats=stats,
            success=True,
            message=f"Theme cluster graph created with {stats['nodes']} nodes"
        )

    except Exception as e:
        logger.error(f"Error creating theme graph: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create theme graph: {str(e)}")

@router.post("/story-graph", response_model=GraphResponse)
async def create_story_graph(request: StoryGraphRequest, background_tasks: BackgroundTasks):
    """
    Generate story analysis graphs from text
    """
    try:
        logger.info(f"Creating story graph of type: {request.graph_type}")

        # Parse the text
        deep_parser = DeepParser()
        parsed = deep_parser.parse(request.text)

        # Create appropriate graph based on type
        if request.graph_type == "concepts":
            # Build concept graph from parsed text
            concepts = {}
            for char in parsed.characters:
                concepts[char] = parsed.themes[:3]  # Connect characters to main themes
            for theme in parsed.themes:
                concepts[theme] = [theme]  # Self-reference for themes
            graph = graph_engine.build_concept_graph(concepts)
            title = "Story Concepts"

        elif request.graph_type == "characters":
            # Build character relationships (simplified)
            characters = {}
            for char in parsed.characters:
                characters[char] = {"relationships": []}
            graph = graph_engine.build_character_relationship_graph(characters)
            title = "Story Characters"

        elif request.graph_type == "themes":
            # Build theme clusters
            themes = {}
            for theme in parsed.themes:
                themes[theme] = [theme]  # Simplified theme clustering
            graph = graph_engine.build_theme_cluster_graph(themes)
            title = "Story Themes"

        elif request.graph_type == "contradictions":
            # Build contradiction network
            detector = ContradictionDetector()
            report = detector.analyze_consistency(request.text)
            contradictions = [
                {
                    "description": c.description,
                    "evidence": c.evidence
                } for c in report.contradictions
            ]
            graph = graph_engine.build_contradiction_network(contradictions)
            title = "Story Contradictions"

        elif request.graph_type == "story_flow":
            # Build story flow
            chapters = []
            for i, chapter in enumerate(parsed.chapters):
                chapters.append({
                    "number": chapter.get("number", i+1),
                    "title": chapter.get("title", f"Chapter {i+1}"),
                    "summary": chapter["content"][:200] + "..."
                })
            graph = graph_engine.build_story_flow_graph(chapters)
            title = "Story Flow"

        else:
            raise HTTPException(status_code=400, detail=f"Unknown graph type: {request.graph_type}")

        # Generate visualization
        graph_url = graph_engine.visualize(graph, title)
        stats = graph_engine.get_graph_stats(graph)

        background_tasks.add_task(cleanup_old_graphs, keep_last=50)

        return GraphResponse(
            graph_url=graph_url,
            graph_stats=stats,
            success=True,
            message=f"Story {request.graph_type} graph created with {stats['nodes']} nodes"
        )

    except Exception as e:
        logger.error(f"Error creating story graph: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create story graph: {str(e)}")

@router.get("/graph-stats")
async def get_graph_storage_stats():
    """
    Get statistics about stored graphs
    """
    try:
        graphs_dir = "static/graphs"
        if not os.path.exists(graphs_dir):
            return {"total_graphs": 0, "total_size_mb": 0, "files": []}

        files = []
        total_size = 0

        for filename in os.listdir(graphs_dir):
            filepath = os.path.join(graphs_dir, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                total_size += size
                files.append({
                    "name": filename,
                    "size_bytes": size,
                    "modified": os.path.getmtime(filepath)
                })

        return {
            "total_graphs": len([f for f in files if f["name"].endswith(".html")]),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "files": sorted(files, key=lambda x: x["modified"], reverse=True)[:10]  # Last 10
        }

    except Exception as e:
        logger.error(f"Error getting graph stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get graph stats: {str(e)}")

def cleanup_old_graphs(keep_last: int = 50):
    """
    Clean up old graph files, keeping only the most recent ones
    """
    try:
        graphs_dir = "static/graphs"
        if not os.path.exists(graphs_dir):
            return

        # Get all HTML files with modification times
        html_files = []
        for filename in os.listdir(graphs_dir):
            if filename.endswith(".html"):
                filepath = os.path.join(graphs_dir, filename)
                html_files.append((filepath, os.path.getmtime(filepath)))

        # Sort by modification time (newest first)
        html_files.sort(key=lambda x: x[1], reverse=True)

        # Remove old files
        for filepath, _ in html_files[keep_last:]:
            try:
                os.remove(filepath)
                logger.info(f"Cleaned up old graph: {filepath}")
            except Exception as e:
                logger.warning(f"Failed to remove {filepath}: {e}")

    except Exception as e:
        logger.error(f"Error during graph cleanup: {e}")

# Export the router
graph_router = router