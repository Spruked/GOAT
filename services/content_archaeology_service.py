# services/content_archaeology_service.py
"""
GOAT Content Archaeology Engine - PREMIUM
Multi-file intelligence: Cross-references 50+ scattered files to find hidden narratives
Premium feature for Legacy tier users
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from core.distiller_interface import distiller_registry
from collections import Counter, defaultdict
import math
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import networkx as nx

# Try to import NLTK data, download if needed
try:
    nltk.data.find('vader_lexicon')
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('stopwords', quiet=True)

class PremiumContentArchaeologyService:
    """
    PREMIUM Content Archaeology Engine - Multi-file intelligence.
    Cross-references scattered files to discover hidden narratives and connections.
    """

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))

        # Enhanced content patterns for multi-file analysis
        self.content_patterns = {
            'unfinished_paragraphs': [
                r'\b(however|therefore|thus|consequently|furthermore|moreover|additionally)\b.*[^\.]$',
                r'^[A-Z][^.!?]*$',
                r'.*\([^)]*$',
                r'.*\[[^\]]*$'
            ],
            'story_triggers': [
                r'\b(suddenly|unexpectedly|surprisingly|amazingly|shockingly)\b',
                r'\b(discovered|found|uncovered|revealed|realized)\b',
                r'\b(what if|imagine|picture this|let me tell you)\b'
            ],
            'data_anomalies': [
                r'\b(\d{1,3}(?:,\d{3})*(?:\.\d+)?%)\b',  # Percentages
                r'\b\d+x\b',  # Multipliers (2x, 3x, etc.)
                r'\b(from \d+ to \d+)\b'  # Changes/ranges
            ],
            'cross_file_references': [
                r'\b(see|refer to|as mentioned in|according to)\b.*\b(file|document|note|entry)\b',
                r'\b(in \d{4}|last year|previously|earlier)\b.*\b(I|we|the team)\b',
                r'\b(this connects to|this relates to|this builds on)\b'
            ],
            'themes_keywords': [
                'chapter', 'section', 'topic', 'theme', 'concept', 'principle',
                'lesson', 'insight', 'discovery', 'breakthrough', 'revelation'
            ]
        }

        # Multi-file relationship patterns
        self.relationship_patterns = {
            'chronological': r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2}|january|february|march|april|may|june|july|august|september|october|november|december)\b',
            'causal': r'\b(because|therefore|thus|consequently|as a result|due to|leads to|causes)\b',
            'contradictory': r'\b(but|however|although|despite|contrary to|unlike|versus|on the other hand)\b',
            'evolutionary': r'\b(evolved|changed|transformed|shifted|moved from|progressed|developed)\b'
        }

    async def analyze_multi_file_intelligence(self,
                                            file_paths: List[str],
                                            user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        PREMIUM: Multi-file intelligence analysis.
        Cross-references all files to find hidden narratives and connections.

        Args:
            file_paths: List of file paths to analyze (up to 50+ files)
            user_context: Optional user context (intent, domain, etc.)

        Returns:
            Comprehensive multi-file analysis with hidden connections
        """
        print(f"🔍 Starting multi-file intelligence analysis of {len(file_paths)} files...")

        analysis_start = datetime.utcnow()

        # Phase 1: Individual file analysis
        individual_analyses = {}
        for i, file_path in enumerate(file_paths):
            if os.path.exists(file_path):
                try:
                    print(f"  📄 Analyzing file {i+1}/{len(file_paths)}: {Path(file_path).name}")
                    file_analysis = await self._analyze_single_file_premium(file_path)
                    individual_analyses[file_path] = file_analysis
                except Exception as e:
                    print(f"  ❌ Error analyzing {file_path}: {e}")
                    individual_analyses[file_path] = {"error": str(e)}

        # Phase 2: Cross-file relationship analysis
        print("  🔗 Analyzing cross-file relationships...")
        cross_file_analysis = self._analyze_cross_file_relationships(individual_analyses, file_paths)

        # Phase 3: Narrative reconstruction
        print("  📖 Reconstructing hidden narratives...")
        narrative_reconstruction = self._reconstruct_multi_file_narratives(
            individual_analyses, cross_file_analysis, user_context
        )

        # Phase 4: Generate archaeology report
        print("  📋 Generating archaeology report...")
        archaeology_report = self._generate_archaeology_report(
            individual_analyses, cross_file_analysis, narrative_reconstruction
        )

        analysis_time = (datetime.utcnow() - analysis_start).total_seconds()

        return {
            "analysis_type": "premium_multi_file_intelligence",
            "files_analyzed": len(file_paths),
            "analysis_time_seconds": analysis_time,
            "individual_analyses": individual_analyses,
            "cross_file_analysis": cross_file_analysis,
            "narrative_reconstruction": narrative_reconstruction,
            "archaeology_report": archaeology_report,
            "premium_features_used": [
                "multi_file_cross_referencing",
                "hidden_narrative_discovery",
                "relationship_mapping",
                "confidence_scoring",
                "narrative_reconstruction"
            ]
        }

    async def _analyze_single_file_premium(self, file_path: str) -> Dict[str, Any]:
        """
        Enhanced single file analysis for multi-file context
        """
        analysis = {
            "filename": Path(file_path).name,
            "file_path": file_path,
            "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            "content_summary": {},
            "entities_extracted": [],
            "themes_identified": [],
            "sentiment_analysis": {},
            "temporal_references": [],
            "cross_references": []
        }

        try:
            # Use VisiData Distiller for structured analysis
            visidata_distiller = distiller_registry.get_distiller("visidata_distiller")
            if visidata_distiller:
                distiller_result = visidata_distiller.distill(file_path)
                data_signals = distiller_result.signals

                # Extract structured information from distiller signals
                column_info = list(data_signals.get("columns", []))
                sample_rows = data_signals.get("sample_rows", [])
                text_content = []

                # Extract text content from sample rows
                for row in sample_rows:
                    if isinstance(row, dict):
                        row_text = ' '.join(str(val) for val in row.values() if val)
                    else:
                        row_text = ' '.join(str(cell) for cell in row)
                    if len(row_text.strip()) > 20:
                        text_content.append(row_text)

                # Also extract from any text columns
                text_analysis = data_signals.get("text_analysis", {})
                for col_name, col_stats in text_analysis.items():
                    sample_values = col_stats.get("sample_values", [])
                    text_content.extend([str(val) for val in sample_values if val])

                # Store distiller metadata
                analysis["data_signals"] = data_signals
                analysis["distiller_confidence"] = distiller_result.metadata.get("confidence", 0.0)
            else:
                # Fallback if distiller not available
                column_info = []
                text_content = []
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    text_content = [content[i:i+1000] for i in range(0, len(content), 500)][:10]

            # Enhanced content analysis
            analysis["content_summary"] = self._extract_content_summary(text_content)
            analysis["entities_extracted"] = self._extract_entities(text_content)
            analysis["themes_identified"] = self._identify_themes(text_content)
            analysis["sentiment_analysis"] = self._analyze_sentiment(text_content)
            analysis["temporal_references"] = self._extract_temporal_references(text_content)
            analysis["cross_references"] = self._identify_cross_references(text_content)

            # Data pattern analysis
            analysis["data_patterns"] = self._analyze_data_patterns(sample_rows, column_info)

        except Exception as e:
            analysis["error"] = str(e)
            # Fallback text analysis
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    text_content = [content]
                    analysis["content_summary"] = self._extract_content_summary(text_content)
                    analysis["themes_identified"] = self._identify_themes(text_content)
            except:
                pass

        return analysis

    def _extract_content_summary(self, text_content: List[str]) -> Dict[str, Any]:
        """Extract comprehensive content summary"""
        if not text_content:
            return {"total_text": 0, "avg_length": 0, "language": "unknown"}

        total_text = ' '.join(text_content)
        total_length = len(total_text)
        avg_length = total_length / len(text_content)

        # Simple language detection (English vs other)
        english_words = len(re.findall(r'\b(the|and|or|but|in|on|at|to|for|of|with|by)\b', total_text.lower()))
        language = "english" if english_words > len(text_content) * 0.1 else "other"

        return {
            "total_text_length": total_length,
            "avg_paragraph_length": avg_length,
            "paragraph_count": len(text_content),
            "language": language,
            "estimated_reading_time": total_length / 200  # words per minute
        }

    def _extract_entities(self, text_content: List[str]) -> List[Dict[str, Any]]:
        """Extract named entities and important terms"""
        entities = []

        # Simple entity extraction (in production, use spaCy or similar)
        all_text = ' '.join(text_content).upper()

        # Look for capitalized terms that might be names/concepts
        potential_entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', all_text)

        entity_counts = Counter(potential_entities)

        for entity, count in entity_counts.most_common(20):
            if len(entity) > 3 and count > 1:  # Appears multiple times
                entities.append({
                    "entity": entity.title(),
                    "frequency": count,
                    "type": "named_entity"  # Could be enhanced with proper NER
                })

        return entities

    def _identify_themes(self, text_content: List[str]) -> List[Dict[str, Any]]:
        """Identify content themes and topics"""
        all_text = ' '.join(text_content).lower()

        # Remove stop words and tokenize
        words = re.findall(r'\b\w+\b', all_text)
        filtered_words = [word for word in words if word not in self.stop_words and len(word) > 3]

        word_freq = Counter(filtered_words)

        themes = []
        for word, freq in word_freq.most_common(15):
            if freq > 2:  # Appears multiple times
                themes.append({
                    "theme": word,
                    "frequency": freq,
                    "relevance_score": freq / len(filtered_words)
                })

        return themes

    def _analyze_sentiment(self, text_content: List[str]) -> Dict[str, Any]:
        """Analyze sentiment across content"""
        if not text_content:
            return {"overall": "neutral", "scores": []}

        sentiments = []
        for text in text_content[:50]:  # Limit for performance
            if len(text) > 10:
                sentiment = self.sia.polarity_scores(text)
                sentiments.append(sentiment)

        if not sentiments:
            return {"overall": "neutral", "scores": []}

        # Average sentiments
        avg_sentiment = {
            "neg": sum(s["neg"] for s in sentiments) / len(sentiments),
            "neu": sum(s["neu"] for s in sentiments) / len(sentiments),
            "pos": sum(s["pos"] for s in sentiments) / len(sentiments),
            "compound": sum(s["compound"] for s in sentiments) / len(sentiments)
        }

        # Determine overall sentiment
        if avg_sentiment["compound"] > 0.05:
            overall = "positive"
        elif avg_sentiment["compound"] < -0.05:
            overall = "negative"
        else:
            overall = "neutral"

        return {
            "overall": overall,
            "average_scores": avg_sentiment,
            "sample_count": len(sentiments)
        }

    def _extract_temporal_references(self, text_content: List[str]) -> List[Dict[str, Any]]:
        """Extract temporal references and timeline data"""
        temporal_refs = []

        for text in text_content:
            # Find date patterns
            dates = re.findall(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b', text)
            months = re.findall(r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b', text, re.IGNORECASE)

            if dates or months:
                temporal_refs.append({
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "dates_found": dates,
                    "months_found": months,
                    "temporal_context": "date_reference"
                })

        return temporal_refs

    def _identify_cross_references(self, text_content: List[str]) -> List[Dict[str, Any]]:
        """Identify cross-references to other documents"""
        cross_refs = []

        for text in text_content:
            for pattern in self.content_patterns['cross_file_references']:
                if re.search(pattern, text, re.IGNORECASE):
                    cross_refs.append({
                        "text": text[:150] + "..." if len(text) > 150 else text,
                        "pattern": pattern,
                        "reference_type": "document_cross_reference"
                    })

        return cross_refs

    def _analyze_data_patterns(self, sample_data: List[List[str]], column_info: List[str]) -> Dict[str, Any]:
        """Analyze data patterns for structure insights"""
        patterns = {
            "column_count": len(column_info),
            "row_count": len(sample_data),
            "data_types": {},
            "patterns_detected": []
        }

        # Analyze column patterns
        for i, col_name in enumerate(column_info):
            col_values = []
            for row in sample_data:
                if i < len(row):
                    col_values.append(row[i])

            # Detect data type patterns
            if col_values:
                numeric_count = sum(1 for v in col_values if v.replace('.', '').replace('-', '').isdigit())
                text_count = sum(1 for v in col_values if len(v) > 2 and not v.replace('.', '').replace('-', '').isdigit())

                if numeric_count > len(col_values) * 0.8:
                    patterns["data_types"][col_name] = "numeric"
                elif text_count > len(col_values) * 0.8:
                    patterns["data_types"][col_name] = "text"
                else:
                    patterns["data_types"][col_name] = "mixed"

        return patterns

    def _analyze_cross_file_relationships(self, individual_analyses: Dict[str, Any], file_paths: List[str]) -> Dict[str, Any]:
        """
        Analyze relationships between files
        """
        relationships = {
            "file_connections": [],
            "shared_themes": [],
            "temporal_links": [],
            "contradictions": [],
            "evolutionary_threads": []
        }

        # Build theme intersection matrix
        file_themes = {}
        for file_path, analysis in individual_analyses.items():
            if "themes_identified" in analysis:
                themes = [theme["theme"] for theme in analysis["themes_identified"]]
                file_themes[file_path] = set(themes)

        # Find shared themes between files
        for i, file1 in enumerate(file_paths):
            for j, file2 in enumerate(file_paths):
                if i < j:  # Avoid duplicate comparisons
                    themes1 = file_themes.get(file1, set())
                    themes2 = file_themes.get(file2, set())

                    shared = themes1.intersection(themes2)
                    if shared:
                        relationships["shared_themes"].append({
                            "file1": Path(file1).name,
                            "file2": Path(file2).name,
                            "shared_themes": list(shared),
                            "overlap_score": len(shared) / max(len(themes1), len(themes2), 1)
                        })

        # Analyze temporal relationships
        temporal_data = {}
        for file_path, analysis in individual_analyses.items():
            if "temporal_references" in analysis and analysis["temporal_references"]:
                temporal_data[file_path] = analysis["temporal_references"]

        # Sort files by temporal references (simple chronological ordering)
        if temporal_data:
            relationships["temporal_links"] = self._analyze_temporal_links(temporal_data)

        return relationships

    def _analyze_temporal_links(self, temporal_data: Dict[str, List]) -> List[Dict[str, Any]]:
        """Analyze temporal connections between files"""
        temporal_links = []

        # Simple temporal ordering based on date mentions
        file_dates = {}
        for file_path, refs in temporal_data.items():
            dates = []
            for ref in refs:
                dates.extend(ref.get("dates_found", []))
            if dates:
                file_dates[file_path] = dates

        # Create timeline suggestions
        if len(file_dates) > 1:
            temporal_links.append({
                "type": "chronological_suggestion",
                "description": f"Found temporal references across {len(file_dates)} files",
                "timeline_files": [Path(f).name for f in file_dates.keys()],
                "suggested_order": "chronological_based_on_dates"
            })

        return temporal_links

    def _reconstruct_multi_file_narratives(self,
                                         individual_analyses: Dict[str, Any],
                                         cross_file_analysis: Dict[str, Any],
                                         user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Reconstruct narratives from multi-file analysis
        """
        reconstruction = {
            "primary_narratives": [],
            "hidden_connections": [],
            "contradictory_elements": [],
            "evolutionary_arcs": [],
            "confidence_scores": {}
        }

        # Extract primary narratives from shared themes
        shared_themes = cross_file_analysis.get("shared_themes", [])
        if shared_themes:
            # Group by shared themes to find narrative threads
            theme_groups = defaultdict(list)
            for connection in shared_themes:
                for theme in connection["shared_themes"]:
                    theme_groups[theme].append(connection)

            # Create narrative threads from theme groups
            for theme, connections in theme_groups.items():
                if len(connections) > 2:  # Theme appears in 3+ file pairs
                    reconstruction["primary_narratives"].append({
                        "theme": theme,
                        "files_involved": len(set([c["file1"] for c in connections] + [c["file2"] for c in connections])),
                        "connections": len(connections),
                        "narrative_potential": f"Strong narrative thread around '{theme}' across multiple files"
                    })

        # Identify hidden connections
        all_entities = []
        for analysis in individual_analyses.values():
            all_entities.extend(analysis.get("entities_extracted", []))

        entity_counts = Counter([e["entity"] for e in all_entities])
        hidden_connections = [entity for entity, count in entity_counts.items() if count > 2]

        if hidden_connections:
            reconstruction["hidden_connections"] = [{
                "entity": entity,
                "mentions_across_files": count,
                "connection_type": "entity_cross_reference"
            } for entity, count in entity_counts.items() if count > 2]

        # Calculate confidence scores
        reconstruction["confidence_scores"] = {
            "narrative_coherence": min(0.95, len(reconstruction["primary_narratives"]) * 0.2),
            "connection_strength": min(0.9, len(reconstruction["hidden_connections"]) * 0.15),
            "temporal_consistency": 0.8 if cross_file_analysis.get("temporal_links") else 0.3,
            "overall_confidence": 0
        }

        # Calculate overall confidence
        scores = reconstruction["confidence_scores"]
        scores["overall_confidence"] = (
            scores["narrative_coherence"] * 0.4 +
            scores["connection_strength"] * 0.3 +
            scores["temporal_consistency"] * 0.3
        )

        return reconstruction

    def _generate_archaeology_report(self,
                                   individual_analyses: Dict[str, Any],
                                   cross_file_analysis: Dict[str, Any],
                                   narrative_reconstruction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive archaeology report
        """
        total_files = len(individual_analyses)
        successful_analyses = sum(1 for a in individual_analyses.values() if "error" not in a)

        report = {
            "executive_summary": {
                "total_files_analyzed": total_files,
                "successful_analyses": successful_analyses,
                "success_rate": successful_analyses / total_files if total_files > 0 else 0,
                "narratives_discovered": len(narrative_reconstruction.get("primary_narratives", [])),
                "hidden_connections_found": len(narrative_reconstruction.get("hidden_connections", [])),
                "confidence_score": narrative_reconstruction.get("confidence_scores", {}).get("overall_confidence", 0)
            },
            "key_findings": [],
            "recommendations": [],
            "content_opportunities": []
        }

        # Generate key findings
        if narrative_reconstruction["primary_narratives"]:
            report["key_findings"].append({
                "type": "narrative_discovery",
                "title": f"Found {len(narrative_reconstruction['primary_narratives'])} strong narrative threads",
                "description": "Multi-file analysis revealed coherent story arcs that span your documents"
            })

        if narrative_reconstruction["hidden_connections"]:
            report["key_findings"].append({
                "type": "connection_discovery",
                "title": f"Identified {len(narrative_reconstruction['hidden_connections'])} cross-file connections",
                "description": "Entities and themes that connect your files in unexpected ways"
            })

        # Generate recommendations
        confidence = narrative_reconstruction.get("confidence_scores", {}).get("overall_confidence", 0)

        if confidence > 0.8:
            report["recommendations"].append({
                "priority": "high",
                "action": "Proceed with narrative reconstruction",
                "reason": ".1%"
            })
        elif confidence > 0.6:
            report["recommendations"].append({
                "priority": "medium",
                "action": "Review cross-file connections manually",
                "reason": ".1%"
            })
        else:
            report["recommendations"].append({
                "priority": "low",
                "action": "Consider additional context or files",
                "reason": "Limited connections found - may need more source material"
            })

        # Content opportunities
        if narrative_reconstruction["primary_narratives"]:
            report["content_opportunities"].append({
                "type": "book_chapters",
                "description": f"Extract {len(narrative_reconstruction['primary_narratives'])} chapters from discovered narratives",
                "estimated_value": f"${len(narrative_reconstruction['primary_narratives']) * 500} in content value"
            })

        return report

# Global instance
premium_content_archaeology_service = PremiumContentArchaeologyService()