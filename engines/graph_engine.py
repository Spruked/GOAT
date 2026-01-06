# engines/graph_engine.py
"""
GOAT Graph Engine - Interactive Knowledge Visualization
Creates concept maps, character relationships, theme clusters, and SKG predicate graphs
"""

import networkx as nx
from pyvis.network import Network
import uuid
import os
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
import json

class GOATGraphEngine:
    """
    GOAT's graph visualization engine using NetworkX + PyVis
    Creates interactive HTML graphs for concepts, characters, themes, and knowledge
    """

    def __init__(self, output_dir: str = "static/graphs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # Default visualization settings
        self.default_options = {
            "height": "650px",
            "width": "100%",
            "bgcolor": "#222222",
            "font_color": "white",
            "notebook": False,
            "cdn_resources": "remote"
        }

    def build_concept_graph(self, concepts: Dict[str, List[str]]) -> nx.Graph:
        """
        Build a concept relationship graph

        Args:
            concepts: Dict mapping nodes to their connected concepts
                     e.g., {"Abby": ["Love", "Loss", "Protection"]}

        Returns:
            NetworkX graph object
        """
        G = nx.Graph()

        # Add nodes and edges
        for node, links in concepts.items():
            # Add main node
            G.add_node(node, size=25, color="#00ff88", title=f"Concept: {node}")

            # Add connected concepts
            for linked in links:
                if not G.has_node(linked):
                    G.add_node(linked, size=20, color="#0088ff", title=f"Linked: {linked}")
                G.add_edge(node, linked, weight=1, title=f"{node} → {linked}")

        return G

    def build_character_relationship_graph(self, characters: Dict[str, Dict[str, Any]]) -> nx.Graph:
        """
        Build character relationship graph

        Args:
            characters: Dict with character data including relationships
                       e.g., {"John": {"relationships": ["loves": "Sarah", "friends": "Mike"]}}
        """
        G = nx.Graph()

        # Add character nodes
        for char_name, char_data in characters.items():
            G.add_node(char_name, size=30, color="#ff6b6b",
                      title=f"Character: {char_name}")

            # Add relationship edges
            relationships = char_data.get('relationships', [])
            for rel in relationships:
                if isinstance(rel, dict):
                    for rel_type, target in rel.items():
                        if target in characters:
                            G.add_edge(char_name, target, weight=2,
                                     title=f"{rel_type}", color="#ff4757")

        return G

    def build_theme_cluster_graph(self, themes: Dict[str, List[str]]) -> nx.Graph:
        """
        Build theme clustering graph

        Args:
            themes: Dict mapping themes to related elements
                   e.g., {"Love": ["Romance", "Heartbreak", "Passion"]}
        """
        G = nx.Graph()

        # Create theme clusters
        for theme, elements in themes.items():
            # Add theme node
            G.add_node(theme, size=35, color="#ffd93d",
                      title=f"Theme: {theme}", shape="diamond")

            # Add element nodes and connect
            for element in elements:
                if not G.has_node(element):
                    G.add_node(element, size=20, color="#6bcf7f",
                              title=f"Element: {element}")
                G.add_edge(theme, element, weight=1, color="#ffd93d")

        return G

    def build_contradiction_network(self, contradictions: List[Dict[str, Any]]) -> nx.Graph:
        """
        Build contradiction network graph

        Args:
            contradictions: List of contradiction dictionaries
        """
        G = nx.Graph()

        for i, contra in enumerate(contradictions):
            contra_node = f"Contradiction_{i}"
            G.add_node(contra_node, size=25, color="#ff3838",
                      title=f"{contra.get('description', 'Contradiction')}",
                      shape="triangle")

            # Connect to related elements
            evidence = contra.get('evidence', [])
            for evidence_item in evidence:
                if not G.has_node(evidence_item):
                    G.add_node(evidence_item, size=15, color="#ff9f43",
                              title=f"Evidence: {evidence_item[:50]}...")
                G.add_edge(contra_node, evidence_item, color="#ff3838")

        return G

    def build_story_flow_graph(self, chapters: List[Dict[str, Any]]) -> nx.Graph:
        """
        Build story flow visualization

        Args:
            chapters: List of chapter dictionaries with content and metadata
        """
        G = nx.DiGraph()  # Directed graph for story flow

        for i, chapter in enumerate(chapters):
            chapter_node = f"Chapter {chapter.get('number', i+1)}"
            title = chapter.get('title', f'Chapter {i+1}')

            G.add_node(chapter_node, size=30, color="#4ecdc4",
                      title=f"{title}: {chapter.get('summary', '')[:100]}...",
                      shape="box")

            # Connect to next chapter
            if i < len(chapters) - 1:
                next_chapter = f"Chapter {chapters[i+1].get('number', i+2)}"
                G.add_edge(chapter_node, next_chapter, color="#4ecdc4", arrows="to")

        return G

    def visualize(self, graph: nx.Graph, title: str = "GOAT Graph",
                  options: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate interactive HTML visualization

        Args:
            graph: NetworkX graph to visualize
            title: Title for the visualization
            options: Additional PyVis options

        Returns:
            Path to generated HTML file
        """
        # Merge options
        vis_options = {**self.default_options}
        if options:
            vis_options.update(options)

        # Create network
        net = Network(**vis_options)
        net.from_nx(graph)

        # Generate unique filename
        file_id = str(uuid.uuid4())
        output_path = os.path.join(self.output_dir, f"{file_id}.html")

        # Save graph
        net.save_graph(output_path)

        return output_path

    def save_graph_data(self, graph: nx.Graph, filename: str) -> str:
        """
        Save graph as JSON for later loading

        Args:
            graph: NetworkX graph to save
            filename: Base filename (will add .json)

        Returns:
            Path to saved JSON file
        """
        # Convert to node-link format
        data = nx.node_link_data(graph)

        json_path = os.path.join(self.output_dir, f"{filename}.json")
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)

        return json_path

    def load_graph_data(self, filename: str) -> nx.Graph:
        """
        Load graph from JSON file

        Args:
            filename: JSON filename (without .json extension)

        Returns:
            NetworkX graph object
        """
        json_path = os.path.join(self.output_dir, f"{filename}.json")

        with open(json_path, 'r') as f:
            data = json.load(f)

        return nx.node_link_graph(data)

    def get_graph_stats(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Get statistics about the graph

        Args:
            graph: NetworkX graph to analyze

        Returns:
            Dictionary with graph statistics
        """
        return {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "density": nx.density(graph),
            "average_clustering": nx.average_clustering(graph),
            "connected_components": nx.number_connected_components(graph) if not graph.is_directed() else "N/A",
            "is_directed": graph.is_directed()
        }

# Convenience functions for quick graph creation
def create_concept_graph(concepts: Dict[str, List[str]], title: str = "Concept Graph") -> str:
    """Quick function to create and visualize a concept graph"""
    engine = GOATGraphEngine()
    graph = engine.build_concept_graph(concepts)
    return engine.visualize(graph, title)

def create_character_graph(characters: Dict[str, Dict[str, Any]], title: str = "Character Relationships") -> str:
    """Quick function to create and visualize character relationships"""
    engine = GOATGraphEngine()
    graph = engine.build_character_relationship_graph(characters)
    return engine.visualize(graph, title)