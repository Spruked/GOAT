# ucm_bridge.py
"""
GOAT UCM Bridge - Connects GOAT to external UCM cognition service

ALIGNMENT DOCTRINE:
"DALS records truth. UCM learns from truth. GOAT produces behavior."

UCM is the only learning and decision-making system.

UCM consumes:
- DALS-observed GOAT behavior
- historical classifications
- emitted learning events

UCM learns about GOAT, not from GOAT instruction.
"""

import requests
import sys
import os
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path

class UCMBridge:
    """Bridge between GOAT and external UCM cognition service"""

    def __init__(self, ucm_endpoint: str = None):
        self.ucm_endpoint = ucm_endpoint or os.getenv("UCM_ENDPOINT", "http://localhost:8080")
        self.api_key = os.getenv("UCM_API_KEY")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def get_skill_inference(self, user_id: str) -> Dict[str, Any]:
        """Get skill inferences from external UCM service for user"""
        try:
            response = self.session.get(f"{self.ucm_endpoint}/api/cognition/skills/{user_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"UCM API error: {response.status_code}")
                return {}
        except Exception as e:
            print(f"UCM connection error: {e}")
            return {}

    def request_explanation(self, skill_id: str, user_level: str = "beginner") -> str:
        """Request explanation from external UCM service"""
        try:
            payload = {
                "content": f"Explain {skill_id} at {user_level} level",
                "priority": "teaching",
                "metadata": {"skill_id": skill_id, "user_level": user_level}
            }
            response = self.session.post(f"{self.ucm_endpoint}/reason", json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get("result", {}).get("response", "")
            else:
                print(f"UCM API error: {response.status_code}")
        except Exception as e:
            print(f"UCM connection error: {e}")

        # Fallback explanation
        return f"This skill covers {skill_id} concepts with practical applications."

    def get_user_cognition_history(self, user_id: str) -> Dict[str, Any]:
        """Get user's cognition history for difficulty scaling"""
        try:
            response = self.session.get(f"{self.ucm_endpoint}/api/cognition/history/{user_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"UCM API error: {response.status_code}")
                return {}
        except Exception as e:
            print(f"UCM connection error: {e}")
            return {}

    def submit_learning_event(self, user_id: str, event: Dict[str, Any]):
        """Submit learning event to external UCM service"""
        try:
            payload = {
                "user_id": user_id,
                "event": event,
                "timestamp": event.get("timestamp")
            }
            response = self.session.post(f"{self.ucm_endpoint}/api/events/learning", json=payload)
            if response.status_code not in [200, 201, 202]:
                print(f"UCM API error submitting event: {response.status_code}")
        except Exception as e:
            print(f"UCM connection error: {e}")
            pass  # Silent failure for now

    def generate_quiz(self, skill_id: str, difficulty: str = "medium", num_questions: int = 5, user_id: str = None) -> Dict[str, Any]:
        """Generate quiz using external UCM service"""
        try:
            payload = {
                "skill_id": skill_id,
                "difficulty": difficulty,
                "num_questions": num_questions,
                "user_id": user_id,
                "priority": "teaching"
            }
            response = self.session.post(f"{self.ucm_endpoint}/api/quiz/generate", json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"UCM API quiz error: {response.status_code}")
        except Exception as e:
            print(f"UCM connection error: {e}")

        # Fallback to basic quiz structure
        return self._generate_fallback_quiz(skill_id, difficulty, num_questions)

    def _parse_quiz_from_text(self, text: str, skill_id: str, difficulty: str, num_questions: int) -> Dict[str, Any]:
        """Parse quiz from UCM text output"""
        # Simple parsing - in production would use better NLP
        questions = []
        lines = text.split('\n')
        current_question = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q') and ':' in line:
                if current_question:
                    questions.append(current_question)
                q_text = line.split(':', 1)[1].strip()
                current_question = {
                    "id": f"q{len(questions)+1}",
                    "question": q_text,
                    "options": [],
                    "correct_answer": "A",
                    "explanation": "Generated by UCM"
                }
            elif line.startswith(('A)', 'B)', 'C)', 'D)')) and current_question:
                current_question["options"].append(line[2:].strip())
            elif line.startswith('Correct:') and current_question:
                current_question["correct_answer"] = line.split(':')[1].strip()
        
        if current_question:
            questions.append(current_question)
        
        # Ensure we have the right number of questions
        while len(questions) < num_questions:
            questions.append({
                "id": f"q{len(questions)+1}",
                "question": f"What is a key concept in {skill_id}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "A",
                "explanation": "Fallback question"
            })
        
        return {
            "skill_id": skill_id,
            "difficulty": difficulty,
            "questions": questions[:num_questions],
            "passing_score": 0.7,
            "time_limit_minutes": 10
        }

    def _generate_fallback_quiz(self, skill_id: str, difficulty: str, num_questions: int) -> Dict[str, Any]:
        """Generate basic fallback quiz"""
        import random
        questions = []
        
        for i in range(num_questions):
            questions.append({
                "id": f"q{i+1}",
                "question": f"Question {i+1} about {skill_id}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
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