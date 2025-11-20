# difficulty_engine.py
"""
GOAT Difficulty Engine - Adaptive difficulty scaling
"""

import math
from typing import Dict, Any, List
from datetime import datetime, timedelta

class DifficultyEngine:
    """Adaptive difficulty scaling using Elo + Bayesian methods"""

    def __init__(self):
        self.elo_base = 1200
        self.elo_k = 32

    def calculate_user_skill_level(self, user_history: List[Dict[str, Any]]) -> float:
        """Calculate user's current skill level using Elo rating"""
        rating = self.elo_base

        for quiz_result in user_history[-10:]:  # Last 10 quizzes
            expected_score = self._expected_score(rating, quiz_result.get("difficulty_rating", 1200))
            actual_score = quiz_result.get("score", 0)
            rating += self.elo_k * (actual_score - expected_score)

        return rating

    def _expected_score(self, user_rating: float, question_rating: float) -> float:
        """Calculate expected score using Elo formula"""
        return 1 / (1 + math.pow(10, (question_rating - user_rating) / 400))

    def recommend_difficulty(self, user_id: str, skill_id: str, user_history: List[Dict[str, Any]]) -> str:
        """Recommend quiz difficulty for user"""
        user_level = self.calculate_user_skill_level(user_history)

        # Simple difficulty mapping
        if user_level < 1000:
            return "beginner"
        elif user_level < 1400:
            return "intermediate"
        else:
            return "advanced"

    def scale_question_difficulty(self, base_difficulty: str, user_performance: float) -> str:
        """Scale question difficulty based on recent performance"""
        if user_performance > 0.8:
            # Increase difficulty
            levels = ["beginner", "intermediate", "advanced", "expert"]
            current_idx = levels.index(base_difficulty) if base_difficulty in levels else 1
            return levels[min(current_idx + 1, len(levels) - 1)]
        elif user_performance < 0.6:
            # Decrease difficulty
            levels = ["beginner", "intermediate", "advanced", "expert"]
            current_idx = levels.index(base_difficulty) if base_difficulty in levels else 1
            return levels[max(current_idx - 1, 0)]

        return base_difficulty

    def apply_spaced_repetition(self, skill_id: str, last_practiced: datetime, mastery_level: float) -> bool:
        """Determine if skill should be reviewed using spaced repetition"""
        if not last_practiced:
            return True

        days_since = (datetime.utcnow() - last_practiced).days

        # Spaced repetition intervals based on mastery
        if mastery_level >= 0.9:
            interval = 30  # Monthly review
        elif mastery_level >= 0.7:
            interval = 7   # Weekly review
        elif mastery_level >= 0.5:
            interval = 2   # Bi-daily review
        else:
            interval = 1   # Daily review

        return days_since >= interval

    def calculate_mastery_decay(self, current_mastery: float, days_since_practice: int) -> float:
        """Calculate mastery decay over time"""
        if days_since_practice <= 0:
            return current_mastery

        # Exponential decay: lose 5% per week
        decay_rate = 0.05 / 7  # 5% per week
        decay_factor = math.exp(-decay_rate * days_since_practice)

        return current_mastery * decay_factor

    def get_personalized_quiz_params(self, user_id: str, skill_id: str, user_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get personalized quiz parameters"""
        difficulty = self.recommend_difficulty(user_id, skill_id, user_history)

        # Adjust based on recent performance
        recent_performance = self._calculate_recent_performance(user_history)

        return {
            "difficulty": self.scale_question_difficulty(difficulty, recent_performance),
            "num_questions": self._calculate_optimal_questions(recent_performance),
            "time_limit": self._calculate_time_limit(difficulty, recent_performance)
        }

    def _calculate_recent_performance(self, user_history: List[Dict[str, Any]]) -> float:
        """Calculate recent performance average"""
        recent_quizzes = user_history[-5:]  # Last 5 quizzes
        if not recent_quizzes:
            return 0.5  # Default

        return sum(q.get("score", 0) for q in recent_quizzes) / len(recent_quizzes)

    def _calculate_optimal_questions(self, performance: float) -> int:
        """Calculate optimal number of questions based on performance"""
        if performance > 0.8:
            return 10  # More questions for advanced users
        elif performance > 0.6:
            return 7   # Standard
        else:
            return 5   # Fewer for struggling users

    def _calculate_time_limit(self, difficulty: str, performance: float) -> int:
        """Calculate time limit in minutes"""
        base_times = {
            "beginner": 15,
            "intermediate": 12,
            "advanced": 10,
            "expert": 8
        }

        base_time = base_times.get(difficulty, 12)

        # Adjust based on performance
        if performance > 0.8:
            return max(base_time - 2, 5)  # Faster for good performers
        elif performance < 0.6:
            return base_time + 3  # More time for struggling users

        return base_time