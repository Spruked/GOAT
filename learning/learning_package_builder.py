# learning_package_builder.py
"""
Learning Package Builder for GOAT
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import LearningEngine, QuizGenerator

class LearningPackageBuilder:
    """Builds learning packages for skills"""

    def __init__(self, output_dir: str = "./deliverables/learning"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_package(self, skill_id: str, learning_engine: "LearningEngine", quiz_generator: "QuizGenerator") -> Dict[str, Any]:
        """Build a complete learning package"""
        package = {
            "skill_id": skill_id,
            "title": f"Mastering {skill_id.title()}",
            "content": {
                "overview": f"Complete guide to {skill_id}",
                "modules": [
                    {
                        "title": f"Introduction to {skill_id}",
                        "content": f"Learn the basics of {skill_id}",
                        "quizzes": []
                    }
                ]
            },
            "metadata": {
                "difficulty": "intermediate",
                "estimated_time": "2 hours",
                "prerequisites": []
            }
        }

        # Save package
        package_path = self.output_dir / skill_id / "package.json"
        package_path.parent.mkdir(parents=True, exist_ok=True)

        with open(package_path, 'w') as f:
            json.dump(package, f, indent=2)

        return package

    def get_package_path(self, skill_id: str) -> str:
        """Get the path to a teaching package"""
        return str(self.output_dir / skill_id)