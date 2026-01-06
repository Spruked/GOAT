"""
GOAT Learning Engine - Adaptive learning and recommendation system
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import sys
import json
import random

sys.path.append(str(Path(__file__).parent.parent))

from knowledge.graph import KnowledgeGraph
from learning.difficulty_engine import DifficultyEngine
from learning.ucm_bridge import UCMBridge
from learning.event_logger import EventLogger
from learning.learning_package_builder import LearningPackageBuilder
from learning.glyph_forge import GlyphForge
from learning.vault_bridge import VaultBridge


class LearningEngine:
    """Adaptive learning and recommendation engine"""
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.graph = knowledge_graph
        self.difficulty_engine = DifficultyEngine()
        self.ucm_bridge = UCMBridge()
        self.event_logger = EventLogger()
        self.package_builder = LearningPackageBuilder()
        self.glyph_forge = GlyphForge()
        self.vault_bridge = VaultBridge()
    
    def recommend_content(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Recommend next learning content for user using UCM cognition

        Args:
            user_id: User identifier
            category: Optional category filter

        Returns:
            Recommended skill and learning NFTs
        """
        # Get UCM-powered skill inference
        ucm_inference = self.ucm_bridge.get_skill_inference(user_id)

        # Use UCM recommendations if available
        if ucm_inference and ucm_inference.get("skill_levels"):
            # Find next skill based on UCM analysis
            next_skill = self._find_next_skill_from_ucm(ucm_inference, category)
        else:
            # Fallback to graph-based recommendation
            next_skill = self.graph.recommend_next_skill(user_id, category)

        if not next_skill:
            return None

        # Get full skill tree
        skill_tree = self.graph.get_skill_tree(next_skill["id"])

        return {
            "skill": next_skill,
            "learning_nfts": skill_tree.get("learning_nfts", []),
            "prerequisites": skill_tree.get("prerequisites", []),
            "recommended_order": self._create_learning_plan(skill_tree)
        }

    def _create_learning_plan(self, skill_tree: Dict[str, Any]) -> List[str]:
        """Create ordered learning plan from skill tree"""
        plan = []

        # Add prerequisites first
        for prereq in skill_tree.get("prerequisites", []):
            plan.append(f"Review: {prereq['name']}")

        # Add main skill NFTs ordered by confidence
        for nft in sorted(
            skill_tree.get("learning_nfts", []),
            key=lambda x: x.get("confidence", 0),
            reverse=True
        ):
            plan.append(f"Study: {nft['title']}")

        plan.append("Complete assessment")
        
        return plan
    
    def _find_next_skill_from_ucm(self, ucm_inference: Dict[str, Any], category: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Find next skill based on UCM inference"""
        skill_levels = ucm_inference.get("skill_levels", {})
        
        # Get all skills from graph
        all_skills = self.graph.export_graph().get("skills", {})
        
        # Find skills the user hasn't mastered yet
        candidate_skills = []
        for skill_id, skill_data in all_skills.items():
            if category and skill_data.get("category") != category:
                continue
            
            user_level = skill_levels.get(skill_id, 0)
            if user_level < 0.8:  # Not yet mastered
                candidate_skills.append((skill_id, skill_data, user_level))
        
        if not candidate_skills:
            return None
        
        # Sort by user level (lowest first) and prerequisites met
        candidate_skills.sort(key=lambda x: x[2])  # Sort by current level
        
        for skill_id, skill_data, level in candidate_skills:
            # Check if prerequisites are met
            if self._prerequisites_met(skill_id, skill_levels):
                return {
                    "id": skill_id,
                    "name": skill_data.get("name", skill_id),
                    "description": skill_data.get("description", ""),
                    "category": skill_data.get("category", ""),
                    "current_level": level
                }
        
        return None
    
    def _prerequisites_met(self, skill_id: str, skill_levels: Dict[str, float]) -> bool:
        """Check if skill prerequisites are met"""
        skill_tree = self.graph.get_skill_tree(skill_id)
        if not skill_tree:
            return True
        
        for prereq in skill_tree.get("prerequisites", []):
            prereq_id = prereq.get("id")
            if prereq_id and skill_levels.get(prereq_id, 0) < 0.6:
                return False
        
        return True
    
    def generate_explanation(
        self,
        glyph_id: str,
        user_level: str = "beginner",
        style: str = "concise"
    ) -> Dict[str, Any]:
        """
        Generate personalized explanation using UCM
        """
        # Try UCM first
        ucm_explanation = self.ucm_bridge.request_explanation(glyph_id, user_level)
        
        if ucm_explanation:
            explanation_text = ucm_explanation
        else:
            # Fallback explanations
            explanations = {
                "concise": "This NFT teaches storage patterns in Solidity using mappings and arrays for gas efficiency.",
                "detailed": "This comprehensive NFT lesson covers Solidity storage patterns...",
                "eli5": "Think of storage like boxes where you keep your toys..."
            }
            explanation_text = explanations.get(style, explanations["concise"])

        return {
            "glyph_id": glyph_id,
            "explanation": explanation_text,
            "user_level": user_level,
            "estimated_time": "15 minutes",
            "key_concepts": [
                "Storage vs Memory",
                "Gas optimization",
                "Data structures"
            ]
        }
    
    def track_progress(
        self,
        user_id: str,
        skill_id: str,
        quiz_score: float
    ) -> Dict[str, Any]:
        """
        Track user progress after quiz
        
        Args:
            user_id: User identifier
            skill_id: Skill completed
            quiz_score: Score (0.0 to 1.0)
        
        Returns:
            Updated progress and next recommendation
        """
        # Update mastery
        self.graph.update_user_mastery(user_id, skill_id, quiz_score)
        
        # Log event
        self.event_logger.log_quiz_completion(user_id, skill_id, {
            "score": quiz_score,
            "passed": quiz_score >= 0.7,
            "difficulty": "medium"  # Could be dynamic
        })
        
        # Get updated progress
        progress = self.graph.get_user_progress(user_id)
        
        # Get next recommendation
        next_lesson = self.recommend_lesson(user_id)
        
        return {
            "progress": progress,
            "next_lesson": next_lesson,
            "achievement": self._check_achievements(user_id)
        }
    
    def _check_achievements(self, user_id: str) -> Optional[Dict[str, str]]:
        """Check for unlocked achievements"""
        progress = self.graph.get_user_progress(user_id)
        
        total_skills = progress["total_skills"]
        avg_mastery = progress["average_mastery"]
        
        if total_skills >= 10 and avg_mastery >= 0.8:
            return {
                "title": "Master Learner",
                "description": "Mastered 10+ skills with 80%+ average"
            }
        elif total_skills >= 5:
            return {
                "title": "Rising Star",
                "description": "Completed 5 skills"
            }
        
        return None


class TeachingNFTGenerator:
    """Generates teaching NFTs from skills"""
    
    def __init__(self, teacher_engine: "TeacherEngine", quiz_generator: "QuizGenerator"):
        self.teacher = teacher_engine
        self.quiz_gen = quiz_generator
    
    def generate_teaching_nft(self, skill_id: str, user_id: str = "system") -> Dict[str, Any]:
        """Generate complete teaching NFT for a skill"""
        
        # Build teaching package
        teaching_package = self.teacher.package_builder.build_package(
            skill_id, self.teacher, self.quiz_gen
        )
        
        # Forge glyph
        glyph = self.teacher.glyph_forge.forge_teaching_glyph(skill_id, teaching_package)
        
        # Export glyph
        glyph_id = self.teacher.glyph_forge.export_glyph(glyph)
        
        # Create vault package
        vault_zip = self.teacher.vault_bridge.create_teaching_vault(
            skill_id, 
            self.teacher.package_builder.get_package_path(skill_id)
        )
        
        # Log NFT mint
        self.teacher.event_logger.log_nft_mint(user_id, glyph_id, {
            "type": "teaching",
            "skill_id": skill_id,
            "cert_sig_ready": True
        })
        
        return {
            "glyph_id": glyph_id,
            "teaching_package": teaching_package,
            "vault_package": vault_zip,
            "nft_metadata": glyph["metadata"]
        }


class QuizGenerator:
    """Generate quizzes from NFT content"""
    
    def __init__(self, difficulty_engine: DifficultyEngine = None, ucm_bridge: UCMBridge = None):
        self.difficulty_engine = difficulty_engine or DifficultyEngine()
        self.ucm_bridge = ucm_bridge or UCMBridge()
    
    def generate_quiz(
        self,
        skill_id: str,
        difficulty: str = "medium",
        num_questions: int = 5,
        user_id: str = None,
        user_history: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized quiz for skill using UCM
        
        Args:
            skill_id: Skill to quiz on
            difficulty: Base difficulty level
            num_questions: Number of questions
            user_id: User ID for personalization
            user_history: User's quiz history
        
        Returns:
            Generated quiz
        """
        # Get personalized parameters if user data available
        if user_id and user_history:
            params = self.difficulty_engine.get_personalized_quiz_params(
                user_id, skill_id, user_history
            )
            difficulty = params["difficulty"]
            num_questions = params["num_questions"]
        
        # Use UCM to generate the quiz
        return self.ucm_bridge.generate_quiz(skill_id, difficulty, num_questions, user_id)
    
    def grade_quiz(
        self,
        quiz: Dict[str, Any],
        answers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Grade quiz answers
        
        Args:
            quiz: Quiz object
            answers: User's answers {question_id: answer}
        
        Returns:
            Grading results
        """
        results = []
        correct_count = 0
        
        for question in quiz["questions"]:
            qid = question["id"]
            user_answer = answers.get(qid)
            correct_answer = question["correct_answer"]
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            results.append({
                "question_id": qid,
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "explanation": question["explanation"]
            })
        
        score = correct_count / len(quiz["questions"])
        passed = score >= quiz["passing_score"]
        
        return {
            "score": score,
            "passed": passed,
            "correct_count": correct_count,
            "total_questions": len(quiz["questions"]),
            "results": results
        }


# Example usage
if __name__ == "__main__":
    # Initialize with knowledge graph
    graph = KnowledgeGraph(Path("./data/knowledge/graph.db"))
    teacher = TeacherEngine(graph)
    quiz_gen = QuizGenerator()
    
    # Recommend lesson
    recommendation = teacher.recommend_lesson("user_123")
    print(f"Recommended: {recommendation}")
    
    # Generate quiz
    quiz = quiz_gen.generate_quiz("solidity_storage")
    print(f"Quiz generated: {len(quiz['questions'])} questions")
    
    # Grade quiz
    mock_answers = {"q1": "A", "q2": "B", "q3": "C", "q4": "D", "q5": "A"}
    result = quiz_gen.grade_quiz(quiz, mock_answers)
    print(f"Score: {result['score']:.0%}")
