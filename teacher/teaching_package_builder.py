# teaching_package_builder.py
"""
GOAT Teaching Package Builder
Exports complete teaching packages for Vault Forge
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class TeachingPackageBuilder:
    """Builds complete teaching packages for GOAT Vault"""

    def __init__(self, output_dir: str = "./deliverables/teaching"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_package(self, skill_id: str, teacher_engine, quiz_generator) -> Dict[str, Any]:
        """Build complete teaching package for a skill"""

        # Generate lesson plan
        lesson_plan = teacher_engine._create_lesson_plan(
            teacher_engine.graph.get_skill_tree(skill_id)
        )

        # Generate explanation
        explanation = teacher_engine.generate_explanation(skill_id)

        # Generate quiz
        quiz = quiz_generator.generate_quiz(skill_id)

        # Generate achievement
        achievement = teacher_engine._check_achievements("current_user")  # Placeholder

        # Generate NFT metadata
        nft_metadata = self._generate_nft_metadata(skill_id, lesson_plan, quiz)

        package = {
            "skill_id": skill_id,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "version": "1.0",
            "lesson_plan": lesson_plan,
            "explanation": explanation,
            "quiz": quiz,
            "achievement": achievement,
            "nft_metadata": nft_metadata
        }

        # Export files
        self._export_package_files(package)

        return package

    def _generate_nft_metadata(self, skill_id: str, lesson_plan: List[str], quiz: Dict[str, Any]) -> Dict[str, Any]:
        """Generate CertSig-ready NFT metadata"""
        return {
            "name": f"GOAT Teaching NFT: {skill_id}",
            "description": f"AI-generated teaching content for {skill_id} with adaptive lessons and quizzes",
            "external_url": f"https://goat.gg/teach/{skill_id}",
            "attributes": [
                {"trait_type": "Skill", "value": skill_id},
                {"trait_type": "Lessons", "value": len(lesson_plan)},
                {"trait_type": "Quiz Questions", "value": len(quiz.get('questions', []))},
                {"trait_type": "Difficulty", "value": quiz.get('difficulty', 'medium')},
                {"trait_type": "Creator", "value": "GOAT AI"}
            ],
            "properties": {
                "lesson_plan": lesson_plan,
                "quiz_structure": {
                    "questions": len(quiz.get('questions', [])),
                    "passing_score": quiz.get('passing_score', 0.7)
                }
            }
        }

    def _export_package_files(self, package: Dict[str, Any]):
        """Export package as individual files"""
        base_path = self.output_dir / package["skill_id"]
        base_path.mkdir(exist_ok=True)

        # Export each component
        files_to_export = [
            ("lesson_plan.json", {"lesson_plan": package["lesson_plan"]}),
            ("explanation.json", package["explanation"]),
            ("quiz.json", package["quiz"]),
            ("achievement.json", {"achievement": package["achievement"]}),
            ("nft_metadata.json", package["nft_metadata"]),
            ("package.json", package)
        ]

        for filename, data in files_to_export:
            with open(base_path / filename, 'w') as f:
                json.dump(data, f, indent=2)

        # Export explanation as markdown
        if "explanation" in package:
            with open(base_path / "explanation.md", 'w') as f:
                f.write(f"# {package['skill_id']} - Teaching Explanation\n\n")
                f.write(package["explanation"]["explanation"])
                f.write(f"\n\n**Estimated Time:** {package['explanation']['estimated_time']}")
                f.write(f"\n**Key Concepts:** {', '.join(package['explanation']['key_concepts'])}")

    def get_package_path(self, skill_id: str) -> Path:
        """Get path to exported package"""
        return self.output_dir / skill_id