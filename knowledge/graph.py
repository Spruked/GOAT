"""
GOAT Knowledge Graph - Semantic skill tree and learning paths
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path
import sqlite3
from datetime import datetime


class KnowledgeGraph:
    """
    Manages semantic relationships between NFTs, skills, and learning paths
    Uses SQLite for simplicity (can upgrade to Neo4j)
    """
    
    def __init__(self, db_path: Path):
        """
        Initialize knowledge graph
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
    
    def _init_schema(self):
        """Initialize graph schema"""
        with sqlite3.connect(self.db_path) as conn:
            # Skills table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    difficulty TEXT,
                    category TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # NFTs table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS nfts (
                    glyph_id TEXT PRIMARY KEY,
                    title TEXT,
                    source TEXT,
                    content_hash TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # NFT teaches Skill relationship
            conn.execute("""
                CREATE TABLE IF NOT EXISTS nft_teaches_skill (
                    nft_glyph_id TEXT,
                    skill_id TEXT,
                    confidence REAL DEFAULT 1.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (nft_glyph_id) REFERENCES nfts(glyph_id),
                    FOREIGN KEY (skill_id) REFERENCES skills(id),
                    PRIMARY KEY (nft_glyph_id, skill_id)
                )
            """)
            
            # Skill prerequisites
            conn.execute("""
                CREATE TABLE IF NOT EXISTS skill_prerequisites (
                    skill_id TEXT,
                    prerequisite_id TEXT,
                    required BOOLEAN DEFAULT 1,
                    FOREIGN KEY (skill_id) REFERENCES skills(id),
                    FOREIGN KEY (prerequisite_id) REFERENCES skills(id),
                    PRIMARY KEY (skill_id, prerequisite_id)
                )
            """)
            
            # User mastery
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_mastery (
                    user_id TEXT,
                    skill_id TEXT,
                    mastery_level REAL DEFAULT 0.0,
                    last_practiced TEXT,
                    FOREIGN KEY (skill_id) REFERENCES skills(id),
                    PRIMARY KEY (user_id, skill_id)
                )
            """)

            # Quizzes table for persistence
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quizzes (
                    id TEXT PRIMARY KEY,
                    skill_id TEXT NOT NULL,
                    user_id TEXT,
                    difficulty TEXT,
                    questions TEXT,  -- JSON
                    answers_hash TEXT,  -- Hash of correct answers
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT,
                    score REAL
                )
            """)
            
            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_skill_category ON skills(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_nft_source ON nfts(source)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_user_mastery ON user_mastery(user_id)")
    
    def add_skill(
        self,
        skill_id: str,
        name: str,
        description: str = "",
        difficulty: str = "beginner",
        category: str = "general"
    ) -> Dict[str, Any]:
        """Add a skill to the graph"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO skills (id, name, description, difficulty, category)
                VALUES (?, ?, ?, ?, ?)
            """, (skill_id, name, description, difficulty, category))
        
        return {
            "id": skill_id,
            "name": name,
            "difficulty": difficulty,
            "category": category
        }
    
    def add_nft(self, glyph_id: str, title: str, source: str, content_hash: str):
        """Add NFT to graph"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO nfts (glyph_id, title, source, content_hash)
                VALUES (?, ?, ?, ?)
            """, (glyph_id, title, source, content_hash))
    
    def link_nft_to_skill(self, glyph_id: str, skill_id: str, confidence: float = 1.0):
        """Create TEACHES relationship"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO nft_teaches_skill (nft_glyph_id, skill_id, confidence)
                VALUES (?, ?, ?)
            """, (glyph_id, skill_id, confidence))
    
    def add_prerequisite(self, skill_id: str, prerequisite_id: str, required: bool = True):
        """Add skill prerequisite"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO skill_prerequisites (skill_id, prerequisite_id, required)
                VALUES (?, ?, ?)
            """, (skill_id, prerequisite_id, int(required)))
    
    def get_skill_tree(self, skill_id: str) -> Dict[str, Any]:
        """Get complete skill tree including prerequisites"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Get skill info
            skill = conn.execute(
                "SELECT * FROM skills WHERE id = ?", (skill_id,)
            ).fetchone()
            
            if not skill:
                return {}
            
            # Get prerequisites
            prereqs = conn.execute("""
                SELECT s.*, sp.required
                FROM skills s
                JOIN skill_prerequisites sp ON s.id = sp.prerequisite_id
                WHERE sp.skill_id = ?
            """, (skill_id,)).fetchall()
            
            # Get NFTs that teach this skill
            nfts = conn.execute("""
                SELECT n.*, nts.confidence
                FROM nfts n
                JOIN nft_teaches_skill nts ON n.glyph_id = nts.nft_glyph_id
                WHERE nts.skill_id = ?
                ORDER BY nts.confidence DESC
            """, (skill_id,)).fetchall()
            
            return {
                "skill": dict(skill),
                "prerequisites": [dict(p) for p in prereqs],
                "teaching_nfts": [dict(n) for n in nfts]
            }
    
    def get_learning_path(self, target_skill: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate optimal learning path to reach target skill
        
        Args:
            target_skill: Goal skill ID
            user_id: Optional user ID to consider mastery
        
        Returns:
            Ordered list of skills to learn
        """
        path = []
        visited = set()
        
        def build_path(skill_id: str):
            if skill_id in visited:
                return
            
            visited.add(skill_id)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                # Get prerequisites
                prereqs = conn.execute("""
                    SELECT prerequisite_id, required
                    FROM skill_prerequisites
                    WHERE skill_id = ?
                """, (skill_id,)).fetchall()
                
                # Recursively add prerequisites
                for prereq in prereqs:
                    build_path(prereq["prerequisite_id"])
                
                # Add current skill
                skill = conn.execute(
                    "SELECT * FROM skills WHERE id = ?", (skill_id,)
                ).fetchone()
                
                if skill:
                    path.append(dict(skill))
        
        build_path(target_skill)
        
        return path
    
    def update_user_mastery(self, user_id: str, skill_id: str, mastery_level: float):
        """Update user's mastery of a skill"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO user_mastery (user_id, skill_id, mastery_level, last_practiced)
                VALUES (?, ?, ?, ?)
            """, (user_id, skill_id, mastery_level, datetime.utcnow().isoformat()))
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user's learning progress"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            mastered = conn.execute("""
                SELECT s.*, um.mastery_level, um.last_practiced
                FROM skills s
                JOIN user_mastery um ON s.id = um.skill_id
                WHERE um.user_id = ?
                ORDER BY um.mastery_level DESC
            """, (user_id,)).fetchall()
            
        return {
            "user_id": user_id,
            "mastered_skills": [dict(m) for m in mastered],
            "total_skills": len(mastered),
            "average_mastery": sum(m["mastery_level"] for m in mastered) / len(mastered) if mastered else 0
        }
    
    def store_quiz(self, quiz_id: str, skill_id: str, user_id: str, quiz_data: Dict[str, Any]) -> str:
        """Store quiz for persistence"""
        answers = {q["id"]: q["correct_answer"] for q in quiz_data["questions"]}
        answers_json = json.dumps(answers)
        answers_hash = hashlib.sha256(answers_json.encode()).hexdigest()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO quizzes
                (id, skill_id, user_id, difficulty, questions, answers_hash, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                quiz_id,
                skill_id,
                user_id,
                quiz_data.get("difficulty", "medium"),
                json.dumps(quiz_data["questions"]),
                answers_hash,
                datetime.utcnow().isoformat()
            ))

        return quiz_id

    def get_quiz(self, quiz_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored quiz"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()

            if row:
                return {
                    "id": row["id"],
                    "skill_id": row["skill_id"],
                    "user_id": row["user_id"],
                    "difficulty": row["difficulty"],
                    "questions": json.loads(row["questions"]),
                    "answers_hash": row["answers_hash"],
                    "created_at": row["created_at"],
                    "completed_at": row["completed_at"],
                    "score": row["score"]
                }
        return None

    def submit_quiz_answers(self, quiz_id: str, answers: Dict[str, str]) -> Dict[str, Any]:
        """Submit quiz answers and calculate score"""
        quiz = self.get_quiz(quiz_id)
        if not quiz:
            raise ValueError("Quiz not found")

        # Verify answers against stored quiz
        correct_answers = {q["id"]: q["correct_answer"] for q in quiz["questions"]}
        results = []

        correct_count = 0
        for qid, user_answer in answers.items():
            correct_answer = correct_answers.get(qid)
            is_correct = user_answer == correct_answer
            if is_correct:
                correct_count += 1

            results.append({
                "question_id": qid,
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "explanation": next((q["explanation"] for q in quiz["questions"] if q["id"] == qid), "")
            })

        score = correct_count / len(quiz["questions"])
        passed = score >= 0.7

        # Update quiz record
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE quizzes
                SET completed_at = ?, score = ?
                WHERE id = ?
            """, (datetime.utcnow().isoformat(), score, quiz_id))

        return {
            "score": score,
            "passed": passed,
            "correct_count": correct_count,
            "total_questions": len(quiz["questions"]),
            "results": results
        }

    def recommend_next_skill(self, user_id: str, category: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Recommend next skill to learn based on user progress"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Get user's mastered skills
            mastered = set(
                row["skill_id"] for row in conn.execute(
                    "SELECT skill_id FROM user_mastery WHERE user_id = ? AND mastery_level >= 0.7",
                    (user_id,)
                ).fetchall()
            )
            
            # Find skills where prerequisites are met but not yet mastered
            query = """
                SELECT s.*, COUNT(sp.prerequisite_id) as prereq_count
                FROM skills s
                LEFT JOIN skill_prerequisites sp ON s.id = sp.skill_id
                WHERE s.id NOT IN (
                    SELECT skill_id FROM user_mastery WHERE user_id = ? AND mastery_level >= 0.7
                )
            """
            params = [user_id]
            
            if category:
                query += " AND s.category = ?"
                params.append(category)
            
            query += " GROUP BY s.id ORDER BY prereq_count ASC, s.difficulty ASC LIMIT 1"
            
            recommended = conn.execute(query, params).fetchone()
            
            return dict(recommended) if recommended else None
    
    def export_graph(self) -> Dict[str, Any]:
        """Export entire graph as JSON"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            skills = [dict(row) for row in conn.execute("SELECT * FROM skills").fetchall()]
            nfts = [dict(row) for row in conn.execute("SELECT * FROM nfts").fetchall()]
            relationships = [dict(row) for row in conn.execute("SELECT * FROM nft_teaches_skill").fetchall()]
            prerequisites = [dict(row) for row in conn.execute("SELECT * FROM skill_prerequisites").fetchall()]
            
            return {
                "skills": skills,
                "nfts": nfts,
                "teaches_relationships": relationships,
                "prerequisites": prerequisites
            }


# Example usage
if __name__ == "__main__":
    graph = KnowledgeGraph(Path("./data/knowledge/graph.db"))
    
    # Add skills
    graph.add_skill("solidity_basics", "Solidity Basics", difficulty="beginner", category="blockchain")
    graph.add_skill("solidity_storage", "Storage Patterns", difficulty="intermediate", category="blockchain")
    graph.add_skill("gas_optimization", "Gas Optimization", difficulty="advanced", category="blockchain")
    
    # Add prerequisites
    graph.add_prerequisite("solidity_storage", "solidity_basics")
    graph.add_prerequisite("gas_optimization", "solidity_storage")
    
    # Add NFT
    graph.add_nft(
        glyph_id="0xabc123",
        title="Learn Solidity Storage",
        source="ipfs://Qm...",
        content_hash="sha256..."
    )
    
    # Link NFT to skill
    graph.link_nft_to_skill("0xabc123", "solidity_storage", confidence=0.95)
    
    # Get learning path
    path = graph.get_learning_path("gas_optimization")
    print(f"Learning path: {[s['name'] for s in path]}")
    
    # Update user progress
    graph.update_user_mastery("user_123", "solidity_basics", 0.8)
    
    # Recommend next
    next_skill = graph.recommend_next_skill("user_123")
    print(f"Recommended: {next_skill['name'] if next_skill else 'None'}")
