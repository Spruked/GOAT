# goat_core/draft_engine/draft_pipeline.py
"""
GOAT Draft Engine - Main Pipeline
Orchestrates the complete content generation workflow
"""

import json
import time
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from .structure_interpreter import StructureInterpreter
from .content_generator import ContentGenerator
from .continuity_manager import ContinuityManager
from .tone_harmonizer import ToneHarmonizer
from .quality_validator import QualityValidator

class DraftPipeline:
    """Main pipeline for GOAT content generation"""

    def __init__(self, api_key: Optional[str] = None):
        self.structure_interpreter = StructureInterpreter()
        self.content_generator = ContentGenerator()  # Caleon-native - no API key needed
        self.continuity_manager = ContinuityManager()
        self.tone_harmonizer = ToneHarmonizer()
        self.quality_validator = QualityValidator()

    def generate_content(self, outline_text: str, content_type: str = "book",
                        project_title: str = "Untitled Project") -> Dict[str, Any]:
        """
        Generate complete content from outline

        Args:
            outline_text: User-provided outline
            content_type: Type of content (book, course, framework, archive)
            project_title: Title of the project

        Returns:
            Complete generation results
        """
        start_time = time.time()

        # Initialize results
        results = {
            "project_title": project_title,
            "content_type": content_type,
            "generation_start": datetime.now().isoformat(),
            "status": "in_progress",
            "blueprint": {},
            "sections": [],
            "metadata": {},
            "errors": []
        }

        try:
            # Step 1: Interpret structure
            print("📋 Interpreting outline structure...")
            blueprint = self.structure_interpreter.interpret_outline(outline_text, content_type)
            results["blueprint"] = blueprint

            # Step 2: Prepare context
            context = {
                "content_type": content_type,
                "title": project_title,
                "total_sections": len(blueprint["writing_plan"]),
                "estimated_word_count": blueprint["metadata"]["estimated_word_count"]
            }

            # Step 3: Generate content for each section
            print(f"✍️  Generating content for {len(blueprint['writing_plan'])} sections...")
            sections_content = []

            for i, section_plan in enumerate(blueprint["writing_plan"]):
                print(f"  Section {i+1}/{len(blueprint['writing_plan'])}: {section_plan['title']}")

                try:
                    # Generate section content
                    section_content = self._generate_section_content(section_plan, context)

                    # Validate section
                    validation = self.quality_validator.validate_content(
                        section_content["content"], section_plan
                    )

                    section_content["validation"] = validation
                    sections_content.append(section_content)

                    print(f"    ✓ Completed ({len(section_content['content'].split())} words, score: {validation['overall_score']:.1f})")

                except Exception as e:
                    error_msg = f"Failed to generate section {section_plan['title']}: {str(e)}"
                    results["errors"].append(error_msg)
                    print(f"    ✗ {error_msg}")

            results["sections"] = sections_content

            # Step 4: Assemble final content
            print("📚 Assembling final content...")
            final_content = self._assemble_final_content(results)

            # Step 5: Final validation
            print("✅ Running final quality checks...")
            final_validation = self._validate_final_content(final_content)

            # Update results
            results.update({
                "final_content": final_content,
                "final_validation": final_validation,
                "generation_time": time.time() - start_time,
                "status": "completed" if not results["errors"] else "completed_with_errors",
                "metadata": {
                    "total_sections": len(sections_content),
                    "total_words": len(final_content.split()),
                    "avg_quality_score": sum(s.get("validation", {}).get("overall_score", 0) for s in sections_content) / max(len(sections_content), 1),
                    "generation_duration": time.time() - start_time
                }
            })

        except Exception as e:
            results["status"] = "failed"
            results["errors"].append(f"Pipeline failed: {str(e)}")
            print(f"❌ Pipeline failed: {str(e)}")

        return results

    def _generate_section_content(self, section_plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content for a single section with full pipeline"""
        # Get continuity context
        continuity_data = self.continuity_manager.get_context_for_section(section_plan["title"])

        # Generate initial content
        section_content = self.content_generator.generate_section_content(
            section_plan, context, continuity_data
        )

        # Harmonize tone
        harmonized_content = self.tone_harmonizer.harmonize_content(
            section_content["content"],
            {"content_type": section_plan["content_type"], "title": section_plan["title"]}
        )

        section_content["content"] = harmonized_content

        # Update continuity with new content
        self.continuity_manager.update_from_content(section_content)

        return section_content

    def _assemble_final_content(self, results: Dict[str, Any]) -> str:
        """Assemble all sections into final content"""
        content_parts = []

        # Add title
        content_parts.append(f"# {results['project_title']}\n")

        # Add blueprint metadata
        blueprint = results.get("blueprint", {})
        if blueprint:
            content_parts.append(f"*Content Type:* {blueprint.get('content_type', 'Unknown')}")
            content_parts.append(f"*Estimated Words:* {blueprint.get('metadata', {}).get('estimated_word_count', 0)}")
            content_parts.append("")

        # Add sections
        for section in results.get("sections", []):
            section_title = section.get("section_plan", {}).get("title", "Untitled Section")
            section_content = section.get("content", "")

            content_parts.append(f"## {section_title}")
            content_parts.append("")
            content_parts.append(section_content)
            content_parts.append("")

        return "\n".join(content_parts).strip()

    def _validate_final_content(self, content: str) -> Dict[str, Any]:
        """Run final validation on assembled content"""
        # Create a mock section plan for validation
        mock_plan = {
            "title": "Complete Work",
            "word_target": len(content.split()),
            "content_type": "complete"
        }

        return self.quality_validator.validate_content(content, mock_plan)

    def save_results(self, results: Dict[str, Any], output_path: str):
        """Save generation results to file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Create a clean version for saving (remove large content if needed)
        save_results = results.copy()

        # Optionally truncate very long content for the summary
        if len(save_results.get("final_content", "")) > 10000:
            save_results["final_content_preview"] = save_results["final_content"][:5000] + "...[truncated]"
            del save_results["final_content"]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(save_results, f, indent=2, ensure_ascii=False, default=str)

    def export_to_markdown(self, results: Dict[str, Any], output_path: str):
        """Export final content to Markdown file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        content = results.get("final_content", "")

        # Add metadata header
        metadata = results.get("metadata", {})
        header = f"""---
title: {results.get('project_title', 'Untitled')}
content_type: {results.get('content_type', 'unknown')}
generated_at: {results.get('generation_start', datetime.now().isoformat())}
total_sections: {metadata.get('total_sections', 0)}
total_words: {metadata.get('total_words', 0)}
avg_quality_score: {metadata.get('avg_quality_score', 0):.1f}
generation_time: {metadata.get('generation_duration', 0):.1f}s
---

"""

        final_content = header + content

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)

    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status and capabilities"""
        return {
            "status": "ready",
            "components": {
                "structure_interpreter": "active",
                "content_generator": "active",
                "continuity_manager": "active",
                "tone_harmonizer": "active",
                "quality_validator": "active"
            },
            "supported_content_types": ["book", "course", "framework", "archive"],
            "capabilities": [
                "Multi-section content generation",
                "Continuity management",
                "Tone harmonization",
                "Quality validation",
                "Markdown export"
            ]
        }

    def reset_pipeline(self):
        """Reset pipeline state for new project"""
        self.continuity_manager.reset_continuity()
        print("🔄 Pipeline reset - ready for new project")

# Convenience function for quick generation
def generate_goat_content(outline_text: str, content_type: str = "book",
                         project_title: str = "GOAT Generated Content") -> Dict[str, Any]:
    """
    Quick function to generate GOAT content

    Args:
        outline_text: The outline to generate from
        content_type: Type of content to generate
        project_title: Title for the project

    Returns:
        Generation results
    """
    pipeline = DraftPipeline()
    return pipeline.generate_content(outline_text, content_type, project_title)