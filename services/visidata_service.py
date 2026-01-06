# services/visidata_service.py
"""
VisiData Service for GOAT
Provides data analysis capabilities for legacy building
"""

import subprocess
import tempfile
import json
import os
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class VisiDataService:
    """Service for analyzing data files with VisiData"""

    @staticmethod
    def analyze_file(file_path: str) -> Dict[str, Any]:
        """
        Runs VisiData in batch mode to extract columns, types, stats.
        Returns structured analysis of the data.
        """
        try:
            # Load file with pandas first for basic analysis
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                # Try CSV as fallback
                df = pd.read_csv(file_path)

            # Basic analysis
            analysis = {
                "filename": Path(file_path).name,
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "null_counts": df.isnull().sum().to_dict(),
                "unique_counts": df.nunique().to_dict(),
                "sample_rows": df.head(5).to_dict('records'),
                "summary_stats": {}
            }

            # Add numeric summary stats
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                analysis["summary_stats"] = df[numeric_cols].describe().to_dict()

            # Add text analysis for object columns
            text_cols = df.select_dtypes(include=['object']).columns
            if len(text_cols) > 0:
                analysis["text_analysis"] = {}
                for col in text_cols:
                    text_data = df[col].dropna().astype(str)
                    analysis["text_analysis"][col] = {
                        "unique_values": int(text_data.nunique()),
                        "avg_length": float(text_data.str.len().mean()),
                        "total_words": int(text_data.str.split().str.len().sum()),
                        "sample_values": text_data.head(3).tolist()
                    }

            # Extract potential themes/topics from text
            analysis["extracted_themes"] = VisiDataService._extract_themes_from_data(df)

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return {
                "error": str(e),
                "filename": Path(file_path).name,
                "shape": None,
                "columns": [],
                "extracted_themes": []
            }

    @staticmethod
    def _extract_themes_from_data(df: pd.DataFrame) -> List[str]:
        """Extract potential themes/topics from dataframe content"""
        themes = []

        # Look for common content indicators in column names
        content_indicators = [
            'topic', 'chapter', 'section', 'title', 'name', 'subject',
            'category', 'theme', 'concept', 'idea', 'principle', 'lesson'
        ]

        for col in df.columns:
            col_lower = col.lower()
            if any(indicator in col_lower for indicator in content_indicators):
                # Get unique values from this column
                unique_vals = df[col].dropna().unique()[:10]  # Limit to 10
                themes.extend([str(val).title() for val in unique_vals if len(str(val)) > 3])

        # Also check text content for keywords
        text_content = ""
        for col in df.select_dtypes(include=['object']).columns:
            sample_text = ' '.join(df[col].dropna().astype(str).head(50))
            text_content += sample_text + ' '

        # Extract keywords from text (simple approach)
        words = text_content.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Only meaningful words
                word_freq[word] = word_freq.get(word, 0) + 1

        # Get top keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        themes.extend([word.title() for word, freq in top_keywords])

        # Remove duplicates and clean
        themes = list(set(themes))
        themes = [theme for theme in themes if len(theme) > 3][:8]  # Limit to 8 themes

        return themes if themes else ["Introduction", "Core Concepts", "Key Principles", "Applications"]

    @staticmethod
    def suggest_structure(analysis: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Suggest content structure based on data analysis"""

        suggestions = {
            "book": {
                "structure": ["Introduction", "Background", "Core Concepts", "Applications", "Case Studies", "Conclusion"],
                "chapter_count": max(6, len(analysis.get("extracted_themes", [])) + 2),
                "estimated_pages": max(50, len(analysis.get("columns", [])) * 8)
            },
            "course": {
                "structure": ["Overview", "Fundamentals", "Advanced Topics", "Practice", "Projects", "Assessment"],
                "module_count": max(4, len(analysis.get("extracted_themes", []))),
                "estimated_hours": max(8, len(analysis.get("columns", [])) * 2)
            },
            "masterclass": {
                "structure": ["Welcome", "Deep Dive", "Techniques", "Live Demo", "Q&A", "Resources"],
                "session_count": max(3, len(analysis.get("extracted_themes", []))),
                "estimated_hours": max(6, len(analysis.get("columns", [])) * 1.5)
            }
        }

        base_suggestion = suggestions.get(content_type, suggestions["book"])

        # Customize based on data
        if analysis.get("extracted_themes"):
            base_suggestion["themes"] = analysis["extracted_themes"]
            base_suggestion["data_driven_sections"] = [
                f"Exploring {theme}" for theme in analysis["extracted_themes"][:4]
            ]

        return base_suggestion

    @staticmethod
    def convert_to_knowledge_graph(analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Convert analyzed data into knowledge graph structure"""

        nodes = []
        edges = []

        # Create nodes from columns
        for i, col in enumerate(analysis.get("columns", [])):
            nodes.append({
                "id": f"col_{i}",
                "label": col,
                "type": "data_column",
                "properties": {
                    "data_type": analysis.get("dtypes", {}).get(col, "unknown"),
                    "unique_count": analysis.get("unique_counts", {}).get(col, 0),
                    "null_count": analysis.get("null_counts", {}).get(col, 0)
                }
            })

        # Create nodes from themes
        for i, theme in enumerate(analysis.get("extracted_themes", [])):
            nodes.append({
                "id": f"theme_{i}",
                "label": theme,
                "type": "content_theme",
                "properties": {"relevance_score": 1.0}
            })

            # Connect themes to relevant columns
            for j, col in enumerate(analysis.get("columns", [])):
                if theme.lower() in col.lower() or any(theme.lower() in str(val).lower() for val in analysis.get("sample_rows", [])):
                    edges.append({
                        "source": f"theme_{i}",
                        "target": f"col_{j}",
                        "type": "related_to",
                        "weight": 0.8
                    })

        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "data_source": analysis.get("filename", "unknown")
            }
        }

# Global instance
visidata_service = VisiDataService()