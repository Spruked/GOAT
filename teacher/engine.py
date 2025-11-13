"""
GOAT Teacher - Adaptive learning engine
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import sys
import json
import random

sys.path.append(str(Path(__file__).parent.parent))

from knowledge.graph import KnowledgeGraph


class TeacherEngine:
    """Adaptive teaching and recommendation engine"""
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.graph = knowledge_graph
    
    def recommend_lesson(
        self,
        user_id: str,
        category: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Recommend next lesson for user
        
        Args:
            user_id: User identifier
            category: Optional category filter
        
        Returns:
            Recommended skill and teaching NFTs
        """
        # Get next skill recommendation
        next_skill = self.graph.recommend_next_skill(user_id, category)
        
        if not next_skill:
            return None
        
        # Get full skill tree
        skill_tree = self.graph.get_skill_tree(next_skill["id"])
        
        return {
            "skill": next_skill,
            "teaching_nfts": skill_tree.get("teaching_nfts", []),
            "prerequisites": skill_tree.get("prerequisites", []),
            "recommended_order": self._create_lesson_plan(skill_tree)
        }
    
    def _create_lesson_plan(self, skill_tree: Dict[str, Any]) -> List[str]:
        """Create ordered lesson plan from skill tree"""
        plan = []
        
        # Add prerequisites first
        for prereq in skill_tree.get("prerequisites", []):
            plan.append(f"Review: {prereq['name']}")
        
        # Add main skill NFTs ordered by confidence
        for nft in sorted(
            skill_tree.get("teaching_nfts", []),
            key=lambda x: x.get("confidence", 0),
            reverse=True
        ):
            plan.append(f"Study: {nft['title']}")
        
        plan.append("Complete quiz")
        
        return plan
    
    def generate_explanation(
        self,
        glyph_id: str,
        user_level: str = "beginner",
        style: str = "concise"
    ) -> Dict[str, Any]:
        """
        Generate personalized explanation
        (In production, this would call an LLM)
        
        Args:
            glyph_id: NFT glyph to explain
            user_level: User's skill level
            style: Explanation style (concise, detailed, eli5)
        
        Returns:
            Generated explanation
        """
        # Mock LLM explanation
        explanations = {
            "concise": "This NFT teaches storage patterns in Solidity using mappings and arrays for gas efficiency.",
            "detailed": "This comprehensive NFT lesson covers Solidity storage patterns...",
            "eli5": "Think of storage like boxes where you keep your toys..."
        }
        
        return {
            "glyph_id": glyph_id,
            "explanation": explanations.get(style, explanations["concise"]),
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


class QuizGenerator:
    """Generate quizzes from NFT content"""
    
    def __init__(self):
        pass
    
    def generate_quiz(
        self,
        skill_id: str,
        difficulty: str = "medium",
        num_questions: int = 5
    ) -> Dict[str, Any]:
        """
        Generate quiz for skill
        (In production, this would use LLM to generate from NFT content)
        
        Args:
            skill_id: Skill to quiz on
            difficulty: Quiz difficulty
            num_questions: Number of questions
        
        Returns:
            Generated quiz
        """
        # Mock quiz generation
        questions = []
        
        for i in range(num_questions):
            questions.append({
                "id": f"q{i+1}",
                "question": f"Question {i+1} about {skill_id}?",
                "options": [
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D"
                ],
                "correct_answer": random.choice(["A", "B", "C", "D"]),
                "explanation": f"Explanation for question {i+1}"
            })
        
        return {
            "skill_id": skill_id,
            "difficulty": difficulty,
            "questions": questions,
            "passing_score": 0.7,
            "time_limit_minutes": 10
        }
    
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
