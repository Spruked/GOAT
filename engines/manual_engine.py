# engines/manual_engine.py
"""
Manual Generation Engine - Creates user manuals, owner's manuals, training manuals, etc.
Separate from book generation with specialized formatting and structure
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import json

from engines.deep_parser import DeepParser
from engines.summarization_engine import SummarizationEngine

logger = logging.getLogger(__name__)

class ManualEngine:
    """Engine for generating various types of manuals"""

    def __init__(self):
        self.deep_parser = DeepParser()
        self.summarizer = SummarizationEngine()

    def generate_user_manual(self, product_name: str, features: List[str], instructions: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a user manual for a product"""
        try:
            # Parse and structure the content
            instructions_text = json.dumps(instructions)
            parsed_content = self.deep_parser.parse(instructions_text)

            # Create manual structure
            manual = {
                "title": f"{product_name} User Manual",
                "type": "user_manual",
                "generated_at": datetime.utcnow().isoformat(),
                "sections": [
                    {
                        "title": "Introduction",
                        "content": f"Welcome to the {product_name} User Manual. This guide will help you understand and use {product_name} effectively."
                    },
                    {
                        "title": "Features",
                        "content": self._format_features(features)
                    },
                    {
                        "title": "Getting Started",
                        "content": instructions.get("getting_started", "Basic setup instructions not provided.")
                    },
                    {
                        "title": "Usage Instructions",
                        "content": self._format_instructions(instructions)
                    },
                    {
                        "title": "Troubleshooting",
                        "content": instructions.get("troubleshooting", "Common issues and solutions not provided.")
                    },
                    {
                        "title": "Safety Information",
                        "content": instructions.get("safety", "Please follow all applicable safety guidelines.")
                    }
                ]
            }

            return manual

        except Exception as e:
            logger.error(f"Failed to generate user manual: {str(e)}")
            raise

    def generate_owner_manual(self, product_name: str, specifications: Dict[str, Any], maintenance: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an owner's manual for equipment/products"""
        try:
            manual = {
                "title": f"{product_name} Owner's Manual",
                "type": "owner_manual",
                "generated_at": datetime.utcnow().isoformat(),
                "sections": [
                    {
                        "title": "Product Overview",
                        "content": f"This owner's manual contains important information about your {product_name}."
                    },
                    {
                        "title": "Specifications",
                        "content": self._format_specifications(specifications)
                    },
                    {
                        "title": "Installation",
                        "content": specifications.get("installation", "Installation instructions not provided.")
                    },
                    {
                        "title": "Operation",
                        "content": specifications.get("operation", "Operation instructions not provided.")
                    },
                    {
                        "title": "Maintenance",
                        "content": self._format_maintenance(maintenance)
                    },
                    {
                        "title": "Warranty Information",
                        "content": specifications.get("warranty", "Warranty information not provided.")
                    }
                ]
            }

            return manual

        except Exception as e:
            logger.error(f"Failed to generate owner's manual: {str(e)}")
            raise

    def generate_training_manual(self, topic: str, objectives: List[str], content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a training manual for educational purposes"""
        try:
            manual = {
                "title": f"{topic} Training Manual",
                "type": "training_manual",
                "generated_at": datetime.utcnow().isoformat(),
                "sections": [
                    {
                        "title": "Course Overview",
                        "content": f"This training manual covers {topic} and is designed to help you achieve the following objectives: {', '.join(objectives)}."
                    },
                    {
                        "title": "Learning Objectives",
                        "content": self._format_objectives(objectives)
                    },
                    {
                        "title": "Prerequisites",
                        "content": content.get("prerequisites", "No prerequisites specified.")
                    },
                    {
                        "title": "Course Content",
                        "content": self._format_training_content(content)
                    },
                    {
                        "title": "Exercises and Activities",
                        "content": content.get("exercises", "No exercises provided.")
                    },
                    {
                        "title": "Assessment",
                        "content": content.get("assessment", "Assessment methods not specified.")
                    }
                ]
            }

            return manual

        except Exception as e:
            logger.error(f"Failed to generate training manual: {str(e)}")
            raise

    def _format_features(self, features: List[str]) -> str:
        """Format feature list for manual"""
        if not features:
            return "Features not specified."
        return "\n".join(f"• {feature}" for feature in features)

    def _format_instructions(self, instructions: Dict[str, Any]) -> str:
        """Format usage instructions"""
        content = ""
        for section, text in instructions.items():
            if section not in ["getting_started", "troubleshooting", "safety"]:
                content += f"\n\n{section.replace('_', ' ').title()}:\n{text}"
        return content or "Detailed instructions not provided."

    def _format_specifications(self, specs: Dict[str, Any]) -> str:
        """Format product specifications"""
        if not specs:
            return "Specifications not provided."
        return "\n".join(f"• {key.replace('_', ' ').title()}: {value}" for key, value in specs.items())

    def _format_maintenance(self, maintenance: Dict[str, Any]) -> str:
        """Format maintenance instructions"""
        if not maintenance:
            return "Maintenance instructions not provided."
        content = ""
        for task, instructions in maintenance.items():
            content += f"\n\n{task.replace('_', ' ').title()}:\n{instructions}"
        return content

    def _format_objectives(self, objectives: List[str]) -> str:
        """Format learning objectives"""
        if not objectives:
            return "Objectives not specified."
        return "\n".join(f"• {obj}" for obj in objectives)

    def _format_training_content(self, content: Dict[str, Any]) -> str:
        """Format training content"""
        formatted = ""
        for module, details in content.items():
            if module not in ["prerequisites", "exercises", "assessment"]:
                formatted += f"\n\n{module.replace('_', ' ').title()}:\n{details}"
        return formatted or "Training content not provided."