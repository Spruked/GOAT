# engines/graph_view_html.py
"""
GOAT Graph View HTML Layer - PyVis HTML Rendering
Converts NetworkX graphs to interactive HTML visualizations
"""

import os
import uuid
from pyvis.network import Network
from typing import Optional

class GraphViewHTML:
    """
    PyVis-based HTML graph renderer for GOAT
    Clean separation: only handles HTML output, no graph logic
    """

    def __init__(self, output_dir: str = "static/graphs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # Default PyVis options for GOAT theme
        self.default_options = {
            "height": "650px",
            "width": "100%",
            "bgcolor": "#111111",
            "font_color": "white",
            "notebook": False,
            "cdn_resources": "remote"
        }

    def render(self, graph, title: str = "GOAT Graph", options: Optional[dict] = None) -> str:
        """
        Takes a NetworkX graph and renders an interactive HTML file via PyVis.
        Returns: the HTML file path.

        Args:
            graph: NetworkX graph object
            title: Title for the visualization
            options: Additional PyVis options (optional)

        Returns:
            Path to the generated HTML file
        """
        # Merge options
        vis_options = {**self.default_options}
        if options:
            vis_options.update(options)

        # Create network
        net = Network(**vis_options)

        # Enable smooth physics
        net.barnes_hut()

        # Convert NetworkX to PyVis
        net.from_nx(graph)

        # Enable physics for interactivity
        net.toggle_physics(True)

        # Generate unique filename
        file_id = f"{uuid.uuid4().hex}.html"
        path = os.path.join(self.output_dir, file_id)

        # Save the interactive graph
        net.save_graph(path)

        return path

    def render_with_custom_options(self, graph, title: str = "GOAT Graph",
                                 height: str = "650px", width: str = "100%",
                                 bgcolor: str = "#111111", font_color: str = "white") -> str:
        """
        Render with custom visual options
        """
        custom_options = {
            "height": height,
            "width": width,
            "bgcolor": bgcolor,
            "font_color": font_color,
            "notebook": False,
            "cdn_resources": "remote"
        }

        return self.render(graph, title, custom_options)