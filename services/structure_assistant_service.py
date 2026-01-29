# services/structure_assistant_service.py
"""
GOAT Structure Assistant - PREMIUM
Intelligent content structuring and organization
Premium feature for Professional and Legacy tier users
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from collections import Counter, defaultdict
import math
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import networkx as nx

# Try to import NLTK data, download if needed
try:
    nltk.data.find('punkt')
    nltk.data.find('stopwords')
    nltk.data.find('wordnet')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)

class PremiumStructureAssistantService:
    """
    PREMIUM Structure Assistant - Intelligent content organization.
    Automatically structures scattered content into coherent frameworks.
    """

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

        # Enhanced structural patterns for content organization
        self.structural_patterns = {
            'headings': [
                r'^#{1,6}\s+.+$',  # Markdown headings
                r'^[A-Z][^.!?]*$',  # Title case lines
                r'^\d+\.?\s+[A-Z]',  # Numbered sections
                r'^[A-Z]{2,}:',  # ALL CAPS labels
            ],
            'transitions': [
                r'\b(however|therefore|thus|consequently|furthermore|moreover|additionally)\b',
                r'\b(first|second|third|next|then|finally|lastly)\b',
                r'\b(on the other hand|in contrast|similarly|likewise)\b',
                r'\b(for example|such as|including|specifically)\b'
            ],
            'conclusions': [
                r'\b(in conclusion|to summarize|in summary|overall|finally)\b',
                r'\b(the key point|the main idea|the bottom line)\b',
                r'\b(what this means|the implication|the result)\b'
            ],
            'questions': [
                r'\b(what|how|why|when|where|who)\b.*\?',
                r'\b(is it|are we|do you|can we)\b.*\?',
                r'\b(should|could|would)\b.*\?'
            ]
        }

        # Enhanced content frameworks
        self.content_frameworks = {
            'problem_solution': {
                'sections': ['Problem Statement', 'Current Challenges', 'Proposed Solution', 'Implementation Steps', 'Expected Results'],
                'transitions': ['The problem is', 'The solution involves', 'This leads to', 'The result will be']
            },
            'how_to_guide': {
                'sections': ['Introduction', 'Prerequisites', 'Step-by-Step Instructions', 'Tips & Tricks', 'Troubleshooting', 'Conclusion'],
                'transitions': ['First', 'Next', 'Then', 'After that', 'Finally']
            },
            'case_study': {
                'sections': ['Background', 'Challenge', 'Approach', 'Implementation', 'Results', 'Lessons Learned'],
                'transitions': ['The situation was', 'We decided to', 'This resulted in', 'The key lesson']
            },
            'comparison_analysis': {
                'sections': ['Introduction', 'Option A Overview', 'Option B Overview', 'Comparison Criteria', 'Analysis', 'Recommendation'],
                'transitions': ['Compared to', 'In contrast', 'Similarly', 'However', 'Therefore']
            },
            'story_narrative': {
                'sections': ['Setup', 'Conflict', 'Rising Action', 'Climax', 'Falling Action', 'Resolution'],
                'transitions': ['It began when', 'But then', 'As things progressed', 'The turning point', 'Afterward', 'In the end']
            },
            'memoir_timeline': {
                'sections': ['Early Life', 'Turning Points', 'Major Challenges', 'Breakthrough Moments', 'Current Chapter', 'Future Vision'],
                'transitions': ['In the beginning', 'Then came', 'The challenge was', 'The breakthrough', 'Now', 'Looking ahead']
            },
            'encyclopedia_az': {
                'sections': ['A-C Fundamentals', 'D-F Core Concepts', 'G-I Advanced Topics', 'J-L Applications', 'M-O Case Studies', 'P-R Future Trends', 'S-Z Reference'],
                'transitions': ['Starting with', 'Moving to', 'Building on', 'Applying this to', 'Considering', 'Finally']
            },
            'course_modular': {
                'sections': ['Foundation', 'Core Skills', 'Practice & Application', 'Advanced Topics', 'Integration', 'Final Project', 'Certification'],
                'transitions': ['We begin with', 'Now that you know', 'Let\'s apply this', 'Taking it further', 'Putting it together', 'To complete your journey']
            },
            'business_case_study': {
                'sections': ['The Challenge', 'Market Analysis', 'Strategy Development', 'Implementation', 'Results & Metrics', 'Lessons Learned', 'Future Applications'],
                'transitions': ['The situation demanded', 'Analysis showed', 'We developed', 'Implementation brought', 'The results were', 'We learned', 'This applies to']
            },
            'research_compilation': {
                'sections': ['Research Overview', 'Key Findings', 'Methodology Deep Dive', 'Data Analysis', 'Implications', 'Future Research', 'Practical Applications'],
                'transitions': ['Research indicates', 'The findings show', 'Methodology revealed', 'Analysis demonstrates', 'This implies', 'Future studies should', 'Practically speaking']
            }
        }

    async def analyze_content_structure(self,
                                      content: str,
                                      content_type: str = "mixed",
                                      user_intent: Optional[str] = None) -> Dict[str, Any]:
        """
        PREMIUM: Analyze and suggest optimal content structure.

        Args:
            content: Raw content to analyze
            content_type: Type of content (article, guide, story, etc.)
            user_intent: User's intended purpose or audience

        Returns:
            Structural analysis with recommendations
        """
        print(f"🔧 Starting premium structure analysis for {content_type} content...")

        analysis_start = datetime.utcnow()

        # Phase 1: Content segmentation
        segments = self._segment_content(content)

        # Phase 2: Structural pattern analysis
        structural_patterns = self._analyze_structural_patterns(segments)

        # Phase 3: Content flow analysis
        content_flow = self._analyze_content_flow(segments)

        # Phase 4: Framework recommendation
        framework_recommendation = self._recommend_content_framework(
            structural_patterns, content_flow, content_type, user_intent
        )

        # Phase 5: Generate restructuring suggestions
        restructuring_plan = self._generate_restructuring_plan(
            segments, structural_patterns, framework_recommendation
        )

        analysis_time = (datetime.utcnow() - analysis_start).total_seconds()

        return {
            "analysis_type": "premium_structure_assistant",
            "content_type": content_type,
            "user_intent": user_intent,
            "analysis_time_seconds": analysis_time,
            "segments_analyzed": len(segments),
            "structural_patterns": structural_patterns,
            "content_flow": content_flow,
            "framework_recommendation": framework_recommendation,
            "restructuring_plan": restructuring_plan,
            "premium_features_used": [
                "content_segmentation",
                "structural_pattern_analysis",
                "content_flow_mapping",
                "framework_recommendation",
                "restructuring_plan"
            ]
        }

    def _segment_content(self, content: str) -> List[Dict[str, Any]]:
        """
        Segment content into logical units
        """
        segments = []

        # Split by paragraphs first
        paragraphs = content.split('\n\n')

        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue

            # Further split by sentences if paragraph is too long
            if len(para) > 500:
                sentences = sent_tokenize(para)
                for j, sentence in enumerate(sentences):
                    segments.append({
                        "id": f"p{i}_s{j}",
                        "content": sentence.strip(),
                        "type": "sentence",
                        "length": len(sentence),
                        "position": len(segments)
                    })
            else:
                segments.append({
                    "id": f"p{i}",
                    "content": para,
                    "type": "paragraph",
                    "length": len(para),
                    "position": len(segments)
                })

        return segments

    def _analyze_structural_patterns(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze structural patterns in content
        """
        patterns = {
            "headings_found": [],
            "transitions_found": [],
            "questions_found": [],
            "conclusions_found": [],
            "structural_score": 0,
            "organization_level": "low"
        }

        for segment in segments:
            content = segment["content"]

            # Check for headings
            for pattern in self.structural_patterns['headings']:
                if re.search(pattern, content, re.MULTILINE):
                    patterns["headings_found"].append({
                        "content": content[:100] + "..." if len(content) > 100 else content,
                        "segment_id": segment["id"],
                        "pattern": pattern
                    })
                    break

            # Check for transitions
            for pattern in self.structural_patterns['transitions']:
                if re.search(pattern, content, re.IGNORECASE):
                    patterns["transitions_found"].append({
                        "content": content[:100] + "..." if len(content) > 100 else content,
                        "segment_id": segment["id"],
                        "transition_type": pattern
                    })
                    break

            # Check for questions
            for pattern in self.structural_patterns['questions']:
                if re.search(pattern, content, re.IGNORECASE):
                    patterns["questions_found"].append({
                        "content": content[:100] + "..." if len(content) > 100 else content,
                        "segment_id": segment["id"]
                    })
                    break

            # Check for conclusions
            for pattern in self.structural_patterns['conclusions']:
                if re.search(pattern, content, re.IGNORECASE):
                    patterns["conclusions_found"].append({
                        "content": content[:100] + "..." if len(content) > 100 else content,
                        "segment_id": segment["id"]
                    })
                    break

        # Calculate structural score
        total_segments = len(segments)
        heading_ratio = len(patterns["headings_found"]) / total_segments if total_segments > 0 else 0
        transition_ratio = len(patterns["transitions_found"]) / total_segments if total_segments > 0 else 0

        patterns["structural_score"] = (heading_ratio * 0.6) + (transition_ratio * 0.4)

        # Determine organization level
        if patterns["structural_score"] > 0.8:
            patterns["organization_level"] = "excellent"
        elif patterns["structural_score"] > 0.6:
            patterns["organization_level"] = "good"
        elif patterns["structural_score"] > 0.4:
            patterns["organization_level"] = "moderate"
        elif patterns["structural_score"] > 0.2:
            patterns["organization_level"] = "basic"
        else:
            patterns["organization_level"] = "low"

        return patterns

    def _analyze_content_flow(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the logical flow of content
        """
        flow_analysis = {
            "topic_progression": [],
            "logical_connections": [],
            "flow_score": 0,
            "flow_issues": [],
            "suggested_improvements": []
        }

        # Extract topics from each segment
        segment_topics = []
        for segment in segments:
            topics = self._extract_segment_topics(segment["content"])
            segment_topics.append({
                "segment_id": segment["id"],
                "topics": topics,
                "position": segment["position"]
            })

        # Analyze topic progression
        if len(segment_topics) > 1:
            for i in range(len(segment_topics) - 1):
                current_topics = set(segment_topics[i]["topics"])
                next_topics = set(segment_topics[i + 1]["topics"])

                overlap = len(current_topics.intersection(next_topics))
                total_unique = len(current_topics.union(next_topics))

                if total_unique > 0:
                    similarity = overlap / total_unique
                    flow_analysis["topic_progression"].append({
                        "from_segment": segment_topics[i]["segment_id"],
                        "to_segment": segment_topics[i + 1]["segment_id"],
                        "topic_similarity": similarity,
                        "shared_topics": list(current_topics.intersection(next_topics))
                    })

        # Calculate flow score based on topic consistency
        if flow_analysis["topic_progression"]:
            avg_similarity = sum(p["topic_similarity"] for p in flow_analysis["topic_progression"]) / len(flow_analysis["topic_progression"])
            flow_analysis["flow_score"] = avg_similarity

            # Identify flow issues
            for progression in flow_analysis["topic_progression"]:
                if progression["topic_similarity"] < 0.1:
                    flow_analysis["flow_issues"].append({
                        "type": "topic_jump",
                        "description": f"Abrupt topic change between segments {progression['from_segment']} and {progression['to_segment']}",
                        "severity": "high"
                    })

        # Suggest improvements
        if flow_analysis["flow_score"] < 0.5:
            flow_analysis["suggested_improvements"].append({
                "type": "add_transitions",
                "description": "Add transition sentences between sections with different topics",
                "priority": "high"
            })

        if len(flow_analysis["flow_issues"]) > 2:
            flow_analysis["suggested_improvements"].append({
                "type": "reorganize_sections",
                "description": "Consider reorganizing content sections for better logical flow",
                "priority": "medium"
            })

        return flow_analysis

    def _extract_segment_topics(self, content: str) -> List[str]:
        """
        Extract key topics from a content segment
        """
        # Tokenize and clean
        words = word_tokenize(content.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words and len(w) > 3]

        # Lemmatize
        lemmatized = [self.lemmatizer.lemmatize(word) for word in words]

        # Get most common words as topics
        word_freq = Counter(lemmatized)
        topics = [word for word, freq in word_freq.most_common(5) if freq > 1]

        return topics

    def _recommend_content_framework(self,
                                   structural_patterns: Dict[str, Any],
                                   content_flow: Dict[str, Any],
                                   content_type: str,
                                   user_intent: Optional[str]) -> Dict[str, Any]:
        """
        Recommend the best content framework
        """
        framework_scores = {}

        # Score each framework based on content characteristics
        for framework_name, framework in self.content_frameworks.items():
            score = 0
            reasons = []

            # Check if content has questions (good for guides)
            if framework_name == "how_to_guide" and structural_patterns["questions_found"]:
                score += 0.3
                reasons.append("Content contains questions, suitable for guide format")

            # Check for problem/solution indicators
            if framework_name == "problem_solution":
                problem_indicators = len([t for t in structural_patterns["transitions_found"]
                                        if "however" in t["transition_type"] or "but" in t["transition_type"]])
                if problem_indicators > 0:
                    score += 0.25
                    reasons.append("Content shows problem-solution patterns")

            # Check for narrative elements
            if framework_name == "story_narrative" and content_flow["flow_score"] > 0.6:
                score += 0.2
                reasons.append("Strong narrative flow detected")

            # Check for comparison elements
            if framework_name == "comparison_analysis":
                contrast_transitions = len([t for t in structural_patterns["transitions_found"]
                                          if "contrast" in t["transition_type"] or "however" in t["transition_type"]])
                if contrast_transitions > 1:
                    score += 0.25
                    reasons.append("Content contains comparison/contrast elements")

            # Check for case study indicators
            if framework_name == "case_study":
                result_indicators = len([c for c in structural_patterns["conclusions_found"]
                                       if "result" in c["content"].lower()])
                if result_indicators > 0:
                    score += 0.2
                    reasons.append("Content appears to describe results/outcomes")

            # Content type hints
            if content_type == "guide" and framework_name == "how_to_guide":
                score += 0.2
            elif content_type == "story" and framework_name == "story_narrative":
                score += 0.2
            elif content_type == "analysis" and framework_name == "comparison_analysis":
                score += 0.2

            framework_scores[framework_name] = {
                "score": score,
                "reasons": reasons,
                "framework_details": framework
            }

        # Get best framework
        best_framework = max(framework_scores.items(), key=lambda x: x[1]["score"])

        return {
            "recommended_framework": best_framework[0],
            "confidence_score": best_framework[1]["score"],
            "recommendation_reasons": best_framework[1]["reasons"],
            "framework_details": best_framework[1]["framework_details"],
            "all_scores": {k: v["score"] for k, v in framework_scores.items()}
        }

    def _generate_restructuring_plan(self,
                                   segments: List[Dict[str, Any]],
                                   structural_patterns: Dict[str, Any],
                                   framework_recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a detailed restructuring plan
        """
        plan = {
            "current_structure": {
                "total_segments": len(segments),
                "headings_count": len(structural_patterns["headings_found"]),
                "transitions_count": len(structural_patterns["transitions_found"]),
                "organization_level": structural_patterns["organization_level"]
            },
            "proposed_structure": {},
            "restructuring_steps": [],
            "estimated_effort": "low",
            "expected_improvement": 0
        }

        framework = framework_recommendation["framework_details"]
        recommended_sections = framework["sections"]

        # Create proposed structure
        plan["proposed_structure"] = {
            "framework": framework_recommendation["recommended_framework"],
            "sections": recommended_sections,
            "section_count": len(recommended_sections),
            "estimated_word_count": len(segments) * 50  # Rough estimate
        }

        # Generate restructuring steps
        plan["restructuring_steps"] = [
            {
                "step": 1,
                "action": "Identify main sections",
                "description": f"Map content to {len(recommended_sections)} framework sections: {', '.join(recommended_sections[:3])}...",
                "effort": "medium"
            },
            {
                "step": 2,
                "action": "Add section headings",
                "description": f"Add clear headings for each of the {len(recommended_sections)} sections",
                "effort": "low"
            },
            {
                "step": 3,
                "action": "Insert transitions",
                "description": "Add transition sentences between sections for better flow",
                "effort": "medium"
            },
            {
                "step": 4,
                "action": "Reorganize content",
                "description": "Move content segments to appropriate sections",
                "effort": "high"
            },
            {
                "step": 5,
                "action": "Add introduction/conclusion",
                "description": "Ensure content has proper opening and closing sections",
                "effort": "low"
            }
        ]

        # Estimate effort and improvement
        current_score = structural_patterns["structural_score"]
        target_score = min(0.9, current_score + 0.3)  # Assume 30% improvement

        plan["estimated_effort"] = "high" if len(segments) > 20 else "medium" if len(segments) > 10 else "low"
        plan["expected_improvement"] = target_score - current_score

        return plan

    async def apply_structural_recommendations(self,
                                             content: str,
                                             restructuring_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        PREMIUM: Apply structural recommendations to content
        """
        print("🔧 Applying structural recommendations...")

        # This would implement the actual restructuring
        # For now, return a preview of what would be done

        return {
            "operation": "structure_application",
            "status": "preview",
            "changes_applied": len(restructuring_plan.get("restructuring_steps", [])),
            "estimated_new_structure_score": restructuring_plan.get("expected_improvement", 0),
            "preview_sections": restructuring_plan.get("proposed_structure", {}).get("sections", [])
        }

    # Legacy compatibility methods for existing functionality
    async def analyze_and_suggest_structure(self,
                                          file_paths: List[str],
                                          user_intent: Optional[str] = None) -> Dict[str, Any]:
        """
        Legacy method for backward compatibility
        """
        # This would call the new premium method with file content
        return await self.analyze_content_structure("Sample content", "mixed", user_intent)

# Global instance
premium_structure_assistant_service = PremiumStructureAssistantService()