# goat_core/draft_engine/quality_validator.py
"""
GOAT Draft Engine - Quality Validator
Validates and improves content quality through multi-pass critique
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from collections import Counter

try:
    import textstat
    TEXTSTAT_AVAILABLE = True
except ImportError:
    textstat = None
    TEXTSTAT_AVAILABLE = False

class QualityValidator:
    """Validates and improves content quality"""

    def __init__(self):
        self.quality_criteria = {
            "readability": {
                "min_flesch_score": 60,
                "max_flesch_score": 80,
                "target_grade_level": "8-12"
            },
            "structure": {
                "min_paragraphs": 3,
                "max_paragraph_length": 300,  # words
                "header_ratio": 0.1  # headers per 100 words
            },
            "engagement": {
                "question_ratio": 0.02,  # questions per 100 words
                "personal_pronoun_ratio": 0.01,
                "active_voice_percentage": 70
            },
            "content_quality": {
                "unique_words_ratio": 0.4,
                "avg_sentence_length_min": 15,
                "avg_sentence_length_max": 25,
                "filler_words_max": 0.05  # percentage
            }
        }

    def validate_content(self, content: str, section_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive quality validation of content

        Args:
            content: The content to validate
            section_plan: The plan for this section

        Returns:
            Validation results with score and issues
        """
        results = {
            "overall_score": 0,
            "readability_score": 0,
            "structure_score": 0,
            "engagement_score": 0,
            "content_score": 0,
            "issues": [],
            "recommendations": [],
            "passed": False
        }

        # Readability validation
        readability = self._validate_readability(content)
        results["readability_score"] = readability["score"]
        results["issues"].extend(readability["issues"])

        # Structure validation
        structure = self._validate_structure(content)
        results["structure_score"] = structure["score"]
        results["issues"].extend(structure["issues"])

        # Engagement validation
        engagement = self._validate_engagement(content)
        results["engagement_score"] = engagement["score"]
        results["issues"].extend(engagement["issues"])

        # Content quality validation
        content_quality = self._validate_content_quality(content)
        results["content_score"] = content_quality["score"]
        results["issues"].extend(content_quality["issues"])

        # Calculate overall score
        results["overall_score"] = (
            readability["score"] +
            structure["score"] +
            engagement["score"] +
            content_quality["score"]
        ) / 4

        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results["issues"])

        # Determine if content passes
        results["passed"] = results["overall_score"] >= 7.0 and len(results["issues"]) <= 3

        return results

    def _validate_readability(self, content: str) -> Dict[str, Any]:
        """Validate readability metrics"""
        if TEXTSTAT_AVAILABLE and textstat:
            flesch_score = textstat.flesch_reading_ease(content)
            grade_level = textstat.flesch_kincaid_grade(content)
        else:
            # Fallback readability calculation
            flesch_score = 65  # Neutral score
            grade_level = 9

        score = 10
        issues = []

        criteria = self.quality_criteria["readability"]

        if flesch_score < criteria["min_flesch_score"]:
            score -= 2
            issues.append(f"Content too complex (Flesch score: {flesch_score:.1f}, target: {criteria['min_flesch_score']}+)")

        if flesch_score > criteria["max_flesch_score"]:
            score -= 1
            issues.append(f"Content too simple (Flesch score: {flesch_score:.1f}, target: <{criteria['max_flesch_score']})")

        if not (8 <= grade_level <= 12):
            score -= 1
            issues.append(f"Grade level {grade_level:.1f} outside target range 8-12")

        return {
            "score": max(0, score),
            "flesch_score": flesch_score,
            "grade_level": grade_level,
            "issues": issues
        }

    def _validate_structure(self, content: str) -> Dict[str, Any]:
        """Validate content structure"""
        score = 10
        issues = []

        criteria = self.quality_criteria["structure"]

        # Check paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if len(paragraphs) < criteria["min_paragraphs"]:
            score -= 2
            issues.append(f"Too few paragraphs ({len(paragraphs)}, minimum: {criteria['min_paragraphs']})")

        # Check paragraph lengths
        word_counts = [len(p.split()) for p in paragraphs]
        long_paragraphs = [wc for wc in word_counts if wc > criteria["max_paragraph_length"]]
        if long_paragraphs:
            score -= 1
            issues.append(f"Some paragraphs too long (max {max(long_paragraphs)} words, limit: {criteria['max_paragraph_length']})")

        # Check headers
        headers = re.findall(r'^#{1,3}\s+', content, re.MULTILINE)
        total_words = len(content.split())
        header_ratio = len(headers) / max(total_words, 1) * 100

        if header_ratio < criteria["header_ratio"] * 100:
            score -= 1
            issues.append(f"Insufficient section headers (ratio: {header_ratio:.2f}%, target: {criteria['header_ratio']*100:.1f}%)")

        return {
            "score": max(0, score),
            "paragraph_count": len(paragraphs),
            "avg_paragraph_length": sum(word_counts) / max(len(word_counts), 1),
            "header_count": len(headers),
            "issues": issues
        }

    def _validate_engagement(self, content: str) -> Dict[str, Any]:
        """Validate engagement elements"""
        score = 10
        issues = []

        criteria = self.quality_criteria["engagement"]
        total_words = len(content.split())

        # Check questions
        questions = re.findall(r'\?', content)
        question_ratio = len(questions) / max(total_words, 1) * 100

        if question_ratio < criteria["question_ratio"] * 100:
            score -= 1
            issues.append(f"Low engagement - few questions (ratio: {question_ratio:.2f}%, target: {criteria['question_ratio']*100:.1f}%)")

        # Check personal pronouns
        personal_pronouns = ['I', 'you', 'we', 'us']
        pronoun_count = sum(content.upper().count(pronoun.upper()) for pronoun in personal_pronouns)
        pronoun_ratio = pronoun_count / max(total_words, 1) * 100

        if pronoun_ratio < criteria["personal_pronoun_ratio"] * 100:
            score -= 1
            issues.append(f"Too impersonal - low personal pronoun usage (ratio: {pronoun_ratio:.2f}%)")

        # Check active voice (simplified)
        passive_indicators = ['was', 'were', 'is being', 'are being', 'has been', 'have been']
        passive_count = sum(content.lower().count(indicator) for indicator in passive_indicators)
        active_percentage = 100 - (passive_count / max(total_words, 1) * 100)

        if active_percentage < criteria["active_voice_percentage"]:
            score -= 1
            issues.append(f"Too much passive voice ({active_percentage:.1f}%, target: {criteria['active_voice_percentage']}%)")

        return {
            "score": max(0, score),
            "question_count": len(questions),
            "personal_pronoun_count": pronoun_count,
            "active_voice_percentage": active_percentage,
            "issues": issues
        }

    def _validate_content_quality(self, content: str) -> Dict[str, Any]:
        """Validate content quality metrics"""
        score = 10
        issues = []

        criteria = self.quality_criteria["content_quality"]
        words = content.split()
        total_words = len(words)

        # Check unique words ratio
        unique_words = len(set(word.lower() for word in words))
        unique_ratio = unique_words / max(total_words, 1)

        if unique_ratio < criteria["unique_words_ratio"]:
            score -= 2
            issues.append(f"Low vocabulary diversity (unique ratio: {unique_ratio:.2f}, target: {criteria['unique_words_ratio']})")

        # Check sentence length
        sentences = re.split(r'[.!?]+', content)
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        avg_sentence_length = sum(sentence_lengths) / max(len(sentence_lengths), 1)

        if not (criteria["avg_sentence_length_min"] <= avg_sentence_length <= criteria["avg_sentence_length_max"]):
            score -= 1
            issues.append(f"Average sentence length {avg_sentence_length:.1f} outside target range {criteria['avg_sentence_length_min']}-{criteria['avg_sentence_length_max']} words")

        # Check filler words
        filler_words = ['very', 'really', 'quite', 'actually', 'basically', 'literally', 'just', 'so', 'well']
        filler_count = sum(content.lower().count(word) for word in filler_words)
        filler_ratio = filler_count / max(total_words, 1)

        if filler_ratio > criteria["filler_words_max"]:
            score -= 1
            issues.append(f"Too many filler words (ratio: {filler_ratio:.2f}%, max: {criteria['filler_words_max']})")

        return {
            "score": max(0, score),
            "unique_words_ratio": unique_ratio,
            "avg_sentence_length": avg_sentence_length,
            "filler_words_ratio": filler_ratio,
            "issues": issues
        }

    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate improvement recommendations based on issues"""
        recommendations = []

        for issue in issues:
            if "complex" in issue.lower():
                recommendations.append("Simplify language and use shorter sentences")
            elif "simple" in issue.lower():
                recommendations.append("Add more sophisticated vocabulary and concepts")
            elif "paragraph" in issue.lower():
                recommendations.append("Break up long paragraphs and improve structure")
            elif "header" in issue.lower():
                recommendations.append("Add more section headers to organize content")
            elif "question" in issue.lower():
                recommendations.append("Add rhetorical questions to increase engagement")
            elif "impersonal" in issue.lower():
                recommendations.append("Use more personal pronouns (you, I, we) to connect with reader")
            elif "passive" in issue.lower():
                recommendations.append("Convert passive voice to active voice")
            elif "vocabulary" in issue.lower():
                recommendations.append("Use more varied vocabulary and avoid repetition")
            elif "sentence length" in issue.lower():
                recommendations.append("Vary sentence length for better rhythm")
            elif "filler" in issue.lower():
                recommendations.append("Remove unnecessary filler words")

        return list(set(recommendations))  # Remove duplicates

    def auto_improve_content(self, content: str, validation_results: Dict[str, Any]) -> str:
        """Automatically improve content based on validation results"""
        improved = content

        issues = validation_results.get("issues", [])

        for issue in issues:
            if "filler" in issue.lower():
                # Remove common filler words
                filler_words = ['very', 'really', 'quite', 'actually', 'basically', 'literally']
                for filler in filler_words:
                    improved = re.sub(r'\b' + filler + r'\b', '', improved, flags=re.IGNORECASE)

            elif "passive" in issue.lower():
                # Simple passive to active conversion
                improved = re.sub(r'(\w+) was (\w+ed)', r'\1 \2', improved)
                improved = re.sub(r'(\w+) were (\w+ed)', r'\1 \2', improved)

        # Clean up extra spaces
        improved = re.sub(r'\s+', ' ', improved)
        improved = re.sub(r'\s*\n\s*', '\n', improved)

        return improved.strip()

    def get_quality_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate a human-readable quality report"""
        results = validation_results

        report = f"""CONTENT QUALITY REPORT
======================

Overall Score: {results['overall_score']:.1f}/10
Status: {'PASSED' if results['passed'] else 'NEEDS IMPROVEMENT'}

SCORES:
• Readability: {results['readability_score']}/10
• Structure: {results['structure_score']}/10
• Engagement: {results['engagement_score']}/10
• Content Quality: {results['content_score']}/10

ISSUES FOUND ({len(results['issues'])}):
{chr(10).join(f'• {issue}' for issue in results['issues'])}

RECOMMENDATIONS:
{chr(10).join(f'• {rec}' for rec in results['recommendations'])}
"""

        return report