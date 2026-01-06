# legacy_builder.py
"""
GOAT Legacy Builder
Creates masterpieces from user data using VisiData analysis
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import visidata as vd

class LegacyBuilder:
    """Builds complete legacies from user data using VisiData analysis"""

    def __init__(self, output_dir: str = "./deliverables/legacy"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_legacy(self, user_data: Dict[str, Any], product_type: str = "book") -> Dict[str, Any]:
        """Build complete legacy product using VisiData analysis"""

        # Analyze user data with VisiData
        data_insights = self._analyze_data_with_visidata(user_data)

        # Generate content based on product type
        if product_type == "book":
            content = self._generate_book_content(user_data, data_insights)
        elif product_type == "course":
            content = self._generate_course_content(user_data, data_insights)
        elif product_type == "masterclass":
            content = self._generate_masterclass_content(user_data, data_insights)
        else:
            content = self._generate_general_content(user_data, data_insights, product_type)

        # Generate NFT metadata
        nft_metadata = self._generate_nft_metadata(user_data, content, product_type)

        legacy = {
            "user_id": user_data.get("user_id", "anonymous"),
            "product_type": product_type,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version": "1.0",
            "data_insights": data_insights,
            "content": content,
            "nft_metadata": nft_metadata
        }

        # Export files
        self._export_legacy_files(legacy)

        return legacy

    def _analyze_data_with_visidata(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user data using VisiData for insights"""
        insights = {}

        # Convert user data to DataFrame for analysis
        if "data_files" in user_data:
            for file_path in user_data["data_files"]:
                if os.path.exists(file_path):
                    try:
                        # Load data with VisiData
                        vd_sheet = vd.openSource(file_path)
                        df = vd_sheet.to_pandas()

                        # Basic analysis
                        insights[file_path] = {
                            "row_count": len(df),
                            "column_count": len(df.columns),
                            "columns": list(df.columns),
                            "data_types": df.dtypes.to_dict(),
                            "summary_stats": df.describe().to_dict() if df.select_dtypes(include=[int, float]).shape[1] > 0 else {},
                            "null_counts": df.isnull().sum().to_dict()
                        }

                        # Text analysis if text columns exist
                        text_cols = df.select_dtypes(include=['object']).columns
                        if len(text_cols) > 0:
                            insights[file_path]["text_analysis"] = {}
                            for col in text_cols:
                                text_data = df[col].dropna().astype(str)
                                insights[file_path]["text_analysis"][col] = {
                                    "unique_values": text_data.nunique(),
                                    "avg_length": text_data.str.len().mean(),
                                    "word_count": text_data.str.split().str.len().sum()
                                }

                    except Exception as e:
                        insights[file_path] = {"error": str(e)}

        return insights

    def _generate_book_content(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate book content structure"""
        return {
            "title": user_data.get("title", "Untitled Book"),
            "chapters": self._structure_chapters(user_data, insights),
            "foreword": f"This book represents the greatest work of {user_data.get('author', 'the author')}.",
            "estimated_pages": len(insights) * 10 + 50,  # Rough estimate
            "key_themes": self._extract_themes(insights)
        }

    def _generate_course_content(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate course content structure"""
        return {
            "title": user_data.get("title", "Untitled Course"),
            "modules": self._structure_modules(user_data, insights),
            "duration_hours": len(insights) * 2,
            "learning_objectives": self._extract_objectives(insights),
            "prerequisites": user_data.get("prerequisites", [])
        }

    def _generate_masterclass_content(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate masterclass content structure"""
        return {
            "title": user_data.get("title", "Untitled Masterclass"),
            "sessions": self._structure_sessions(user_data, insights),
            "duration_hours": len(insights) * 3,
            "expertise_level": "Advanced",
            "key_takeaways": self._extract_takeaways(insights)
        }

    def _generate_general_content(self, user_data: Dict[str, Any], insights: Dict[str, Any], product_type: str) -> Dict[str, Any]:
        """Generate general content structure"""
        return {
            "title": user_data.get("title", f"Untitled {product_type.title()}"),
            "sections": self._structure_sections(user_data, insights, product_type),
            "content_type": product_type,
            "insights_summary": self._summarize_insights(insights)
        }

    def _structure_chapters(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Structure book chapters based on data insights"""
        chapters = []
        themes = self._extract_themes(insights)

        for i, theme in enumerate(themes[:10]):  # Limit to 10 chapters
            chapters.append({
                "number": i + 1,
                "title": f"Chapter {i+1}: {theme.title()}",
                "content_outline": f"Exploring {theme} based on data analysis",
                "estimated_pages": 15
            })

        return chapters

    def _structure_modules(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Structure course modules"""
        modules = []
        objectives = self._extract_objectives(insights)

        for i, objective in enumerate(objectives[:8]):
            modules.append({
                "number": i + 1,
                "title": f"Module {i+1}: {objective}",
                "lessons": ["Introduction", "Core Concepts", "Practice", "Assessment"],
                "duration_hours": 2
            })

        return modules

    def _structure_sessions(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Structure masterclass sessions"""
        sessions = []
        takeaways = self._extract_takeaways(insights)

        for i, takeaway in enumerate(takeaways[:6]):
            sessions.append({
                "number": i + 1,
                "title": f"Session {i+1}: {takeaway}",
                "duration_hours": 1.5,
                "format": "Interactive Workshop"
            })

        return sessions

    def _structure_sections(self, user_data: Dict[str, Any], insights: Dict[str, Any], product_type: str) -> List[Dict[str, Any]]:
        """Structure general sections"""
        sections = []
        summary = self._summarize_insights(insights)

        for i, key_point in enumerate(summary.get("key_points", [])[:5]):
            sections.append({
                "number": i + 1,
                "title": f"Section {i+1}: {key_point}",
                "content_type": product_type
            })

        return sections

    def _extract_themes(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key themes from insights"""
        themes = []
        for file_insights in insights.values():
            if isinstance(file_insights, dict) and "columns" in file_insights:
                themes.extend([col.replace("_", " ").title() for col in file_insights["columns"][:3]])

        # Remove duplicates and limit
        return list(set(themes))[:5] if themes else ["Introduction", "Core Concepts", "Advanced Topics", "Conclusion", "Appendices"]

    def _extract_objectives(self, insights: Dict[str, Any]) -> List[str]:
        """Extract learning objectives"""
        return ["Understand core concepts", "Apply knowledge practically", "Master advanced techniques", "Create original work", "Teach others"]

    def _extract_takeaways(self, insights: Dict[str, Any]) -> List[str]:
        """Extract key takeaways"""
        return ["Master the fundamentals", "Develop expert techniques", "Build practical skills", "Create lasting value", "Inspire others"]

    def _summarize_insights(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize data insights"""
        total_files = len(insights)
        total_rows = sum([f.get("row_count", 0) for f in insights.values() if isinstance(f, dict)])

        return {
            "total_files_analyzed": total_files,
            "total_data_points": total_rows,
            "key_points": ["Data-driven insights", "Structured knowledge", "Actionable intelligence"],
            "recommendations": ["Focus on quality over quantity", "Structure content logically", "Include practical examples"]
        }

    def _generate_nft_metadata(self, user_data: Dict[str, Any], content: Dict[str, Any], product_type: str) -> Dict[str, Any]:
        """Generate CertSig-ready NFT metadata"""
        return {
            "name": f"GOAT Legacy NFT: {content.get('title', 'Untitled')}",
            "description": f"Permanent proof of authorship for {product_type}: {content.get('title', 'Untitled')} - created through GOAT's legacy building system",
            "external_url": f"https://goat.gg/legacy/{user_data.get('user_id', 'anonymous')}",
            "attributes": [
                {"trait_type": "Product Type", "value": product_type},
                {"trait_type": "Author", "value": user_data.get('author', 'Anonymous')},
                {"trait_type": "Creation Date", "value": datetime.utcnow().date().isoformat()},
                {"trait_type": "Data Sources", "value": len(user_data.get('data_files', []))},
                {"trait_type": "Content Sections", "value": len(content.get('chapters', content.get('modules', content.get('sections', []))))},
                {"trait_type": "Creator", "value": "GOAT AI"}
            ],
            "properties": {
                "product_type": product_type,
                "content_structure": {
                    "title": content.get('title'),
                    "sections": len(content.get('chapters', content.get('modules', content.get('sections', []))))
                },
                "authorship_proof": {
                    "author": user_data.get('author'),
                    "creation_timestamp": datetime.utcnow().isoformat(),
                    "data_integrity_hash": "placeholder_hash"  # Would be actual hash
                }
            }
        }

    def _export_legacy_files(self, legacy: Dict[str, Any]):
        """Export legacy as individual files"""
        base_path = self.output_dir / f"{legacy['user_id']}_{legacy['product_type']}"
        base_path.mkdir(exist_ok=True)

        # Export each component
        files_to_export = [
            ("content.json", legacy["content"]),
            ("data_insights.json", legacy["data_insights"]),
            ("nft_metadata.json", legacy["nft_metadata"]),
            ("legacy.json", legacy)
        ]

        for filename, data in files_to_export:
            with open(base_path / filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)

        # Export content as markdown if it's a book
        if legacy["product_type"] == "book" and "chapters" in legacy["content"]:
            with open(base_path / "book_outline.md", 'w') as f:
                f.write(f"# {legacy['content']['title']}\n\n")
                f.write(f"**Author:** {legacy.get('user_data', {}).get('author', 'Anonymous')}\n\n")
                f.write("## Table of Contents\n\n")
                for chapter in legacy["content"]["chapters"]:
                    f.write(f"{chapter['number']}. {chapter['title']}\n")

    def get_legacy_path(self, user_id: str, product_type: str) -> Path:
        """Get path to exported legacy"""
        return self.output_dir / f"{user_id}_{product_type}"