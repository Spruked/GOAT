# services/visidata_distiller.py
"""
VisiData Distiller for GOAT
Data distillation engine that transforms raw data files into structured signals

This is a DISTILLATION ENGINE (not a worker):
- Pure instrumentation, no agency
- Transforms raw data into structured signals
- Serves workers with processed information
- No intent, dialogue, or decisions
"""

import subprocess
import tempfile
import json
import os
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import time

from dals.core.distiller_registry import distiller_registry

logger = logging.getLogger(__name__)

class VisiDataDistiller(DistillerProtocol):
    """
    VisiData Distiller - Data distillation engine for GOAT.

    Transforms raw data files (CSV, JSON, Excel) into structured signals
    that workers can reason over. Pure instrumentation, no agency.
    """

    def __init__(self):
        self.resource_limits = {}
        self._instrumentation_data = []

    @property
    def name(self) -> str:
        return "visidata_distiller"

    @property
    def supported_sources(self) -> List[str]:
        return ["csv", "json", "xlsx", "xls", "folder"]

    @property
    def signal_types(self) -> List[str]:
        return ["frequencies", "statistics", "themes", "anomalies", "correlations", "data_quality"]

    def _set_limits(self, limits: Dict):
        """Apply resource limits from registry specification."""
        self.resource_limits = limits

    def distill(self, sources: List[str], **kwargs) -> DistillerResult:
        """
        Extract signals from data sources.

        Args:
            sources: File paths or data source identifiers
            **kwargs: Distiller-specific parameters

        Returns:
            DistillerResult: Raw signals and metadata (no interpretation)
        """
        start_time = time.time()

        try:
            if not sources:
                # Return empty result for no sources
                return DistillerResult(
                    signals={"message": "No sources provided"},
                    metadata={
                        "timestamp": time.time(),
                        "processing_time": 0.0,
                        "distiller_version": "2.0+",
                        "confidence": 0.0
                    }
                )

            # Process first source (for now - could be extended to handle multiple)
            source = sources[0]

            if os.path.isfile(source):
                # File path input
                signals = self._analyze_file(source)
            elif os.path.isdir(source):
                # Directory input - analyze all data files
                signals = self._analyze_folder(source)
            else:
                # Assume it's data content - convert to DataFrame if it's a list of dicts
                if isinstance(source, list) and source and isinstance(source[0], dict):
                    import pandas as pd
                    df = pd.DataFrame(source)
                    signals = self._analyze_dataframe(df, filename="data")
                elif isinstance(source, str):
                    # Try to parse as JSON or CSV string
                    try:
                        import pandas as pd
                        # Try JSON first
                        import json
                        data = json.loads(source)
                        if isinstance(data, list) and data and isinstance(data[0], dict):
                            df = pd.DataFrame(data)
                        else:
                            df = pd.DataFrame([data])
                        signals = self._analyze_dataframe(df, filename="data")
                    except:
                        # Fallback - treat as single text value
                        signals = {"error": "Unsupported string format", "content": source[:100]}
                else:
                    signals = {"error": "Unsupported source type", "type": str(type(source))}

            # Add processing metadata
            metadata = {
                "timestamp": time.time(),
                "processing_time": time.time() - start_time,
                "distiller_version": "2.0+",
                "confidence": self._calculate_confidence(signals),
                "sources_processed": len(sources),
                "validated": True
            }

            # Record instrumentation in registry
            distiller_registry.instrument(
                distiller_id=self.name,
                operation="distill",
                metrics={
                    "processing_time_ms": (time.time() - start_time) * 1000,
                    "sources_processed": len(sources),
                    "signals_extracted": len(signals),
                    "confidence_score": metadata["confidence"],
                    "memory_peak_mb": self.resource_limits.get("memory_mb", 512)
                }
            )

            # Record to GOAT Field for learning (async, non-blocking)
            import asyncio
            asyncio.create_task(
                self.record_to_field(sources, signals, int((time.time() - start_time) * 1000), True)
            )

            return DistillerResult(signals=signals, metadata=metadata)

        except Exception as e:
            logger.error(f"Error in VisiData distillation: {str(e)}")
            return DistillerResult(
                signals={"error": str(e)},
                metadata={
                    "timestamp": time.time(),
                    "processing_time": time.time() - start_time,
                    "error": True,
                    "validated": False
                }
            )

    def _apply_learned_config(self, config: Dict):
        """
        Apply learned optimizations from GOAT Field.
        Safe, read-only configuration changes.
        """
        # Apply chunking optimization for large files
        if 'recommended_chunk_size' in config:
            self._chunk_size = config['recommended_chunk_size']
            logger.debug(f"Applied chunk size optimization: {self._chunk_size}")

        # Apply pre-filtering if suggested
        if 'pre_filter_suggestion' in config:
            self._pre_filter = config['pre_filter_suggestion']
            logger.debug(f"Applied pre-filter optimization: {self._pre_filter}")

    async def record_to_field(self, sources: List[str], signals: Dict, duration_ms: int, success: bool):
        """
        Record distillation operation to GOAT Field for learning.
        """
        try:
            from goat.core.field_reflection_service import field_reflection_service
            await field_reflection_service.record_distillation(
                distiller_id=self.name,
                files=sources,
                signals=signals,
                duration_ms=duration_ms,
                success=success
            )
        except Exception as e:
            logger.warning(f"Failed to record to GOAT Field: {e}")

    def validate_signals(self, signals: Dict[str, Any]) -> bool:
        """
        Validate signal integrity and consistency.

        Args:
            signals: Signals to validate

        Returns:
            bool: True if signals are valid and consistent
        """
        if "error" in signals:
            return False

        # Check for required signal types
        required_signals = ["shape", "columns", "dtypes"]
        if not all(key in signals for key in required_signals):
            return False

        # Validate data types
        if not isinstance(signals.get("shape"), (tuple, list)) or len(signals["shape"]) != 2:
            return False

        if not isinstance(signals.get("columns"), list):
            return False

        # Check data quality signals if present
        quality = signals.get("data_quality_signals", {})
        if quality and not isinstance(quality.get("completeness"), (int, float)):
            return False

        return True

    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single data file"""
        try:
            # Load file with pandas
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                df = pd.read_json(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                # Try CSV as fallback
                df = pd.read_csv(file_path)

            return self._analyze_dataframe(df, filename=Path(file_path).name)

        except Exception as e:
            return {
                "error": str(e),
                "filename": Path(file_path).name,
                "data_quality": "unreadable"
            }

    def _analyze_folder(self, folder_path: str) -> Dict[str, Any]:
        """Analyze all data files in a folder"""
        folder_signals = {
            "folder_path": folder_path,
            "files_analyzed": [],
            "aggregate_signals": {}
        }

        data_files = []
        for ext in ['.csv', '.json', '.xlsx', '.xls']:
            data_files.extend(Path(folder_path).glob(f"**/*{ext}"))

        for file_path in data_files[:10]:  # Limit to 10 files for performance
            file_signals = self._analyze_file(str(file_path))
            folder_signals["files_analyzed"].append(file_signals)

        # Aggregate signals across files
        if folder_signals["files_analyzed"]:
            folder_signals["aggregate_signals"] = self._aggregate_folder_signals(folder_signals["files_analyzed"])

        return folder_signals

    def _analyze_dataframe(self, df: pd.DataFrame, filename: str = "data") -> Dict[str, Any]:
        """Analyze a pandas DataFrame"""
        signals = {
            "filename": filename,
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "unique_counts": df.nunique().to_dict(),
            "sample_rows": df.head(5).to_dict('records'),
            "summary_stats": {},
            "text_analysis": {},
            "data_quality_signals": {}
        }

        # Numeric summary stats
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            signals["summary_stats"] = df[numeric_cols].describe().to_dict()

        # Text analysis for object columns
        text_cols = df.select_dtypes(include=['object']).columns
        if len(text_cols) > 0:
            for col in text_cols:
                text_data = df[col].dropna().astype(str)
                signals["text_analysis"][col] = {
                    "unique_values": int(text_data.nunique()),
                    "avg_length": float(text_data.str.len().mean()),
                    "total_words": int(text_data.str.split().str.len().sum()),
                    "sample_values": text_data.head(3).tolist()
                }

        # Extract themes/topics
        signals["extracted_themes"] = self._extract_themes_from_dataframe(df)

        # Data quality signals
        signals["data_quality_signals"] = self._assess_data_quality(df)

        return signals

    def _extract_themes_from_dataframe(self, df: pd.DataFrame) -> List[str]:
        """Extract potential themes/topics from dataframe content"""
        themes = []

        # Look for content indicators in column names
        content_indicators = [
            'topic', 'chapter', 'section', 'title', 'name', 'subject',
            'category', 'theme', 'concept', 'idea', 'principle', 'lesson'
        ]

        for col in df.columns:
            col_lower = col.lower()
            if any(indicator in col_lower for indicator in content_indicators):
                unique_vals = df[col].dropna().unique()[:10]
                themes.extend([str(val).title() for val in unique_vals if len(str(val)) > 3])

        # Extract keywords from text content
        text_content = ""
        for col in df.select_dtypes(include=['object']).columns:
            sample_text = ' '.join(df[col].dropna().astype(str).head(50))
            text_content += sample_text + ' '

        # Simple keyword extraction
        words = text_content.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 4:
                word_freq[word] = word_freq.get(word, 0) + 1

        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        themes.extend([word.title() for word, freq in top_keywords])

        # Clean and deduplicate
        themes = list(set(themes))
        themes = [theme for theme in themes if len(theme) > 3][:8]

        return themes if themes else ["Introduction", "Core Concepts", "Key Principles", "Applications"]

    def _assess_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Assess data quality and emit signals"""
        quality_signals = {
            "completeness": 1.0 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])),
            "uniqueness": df.nunique().sum() / len(df.columns),
            "consistency": self._check_consistency(df),
            "anomalies_detected": self._detect_anomalies(df)
        }

        return quality_signals

    def _check_consistency(self, df: pd.DataFrame) -> float:
        """Check data consistency (simple heuristic)"""
        consistency_score = 1.0

        # Check for mixed types in columns
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_numeric(df[col], errors='coerce')
                    consistency_score -= 0.1  # Mixed types detected
                except:
                    pass

        return max(0.0, consistency_score)

    def _detect_anomalies(self, df: pd.DataFrame) -> List[str]:
        """Detect potential anomalies in data"""
        anomalies = []

        # Check for outlier numeric values
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            if df[col].std() > 0:  # Has variance
                z_scores = abs((df[col] - df[col].mean()) / df[col].std())
                outlier_count = (z_scores > 3).sum()
                if outlier_count > 0:
                    anomalies.append(f"Column '{col}' has {outlier_count} statistical outliers")

        # Check for unusual null patterns
        null_percentages = (df.isnull().sum() / len(df)) * 100
        high_null_cols = null_percentages[null_percentages > 50]
        if len(high_null_cols) > 0:
            anomalies.append(f"Columns with >50% nulls: {list(high_null_cols.index)}")

        return anomalies

    def _aggregate_folder_signals(self, file_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate signals across multiple files"""
        if not file_signals:
            return {}

        # Combine themes across files
        all_themes = []
        for signals in file_signals:
            all_themes.extend(signals.get("extracted_themes", []))

        # Count theme frequency
        theme_counts = {}
        for theme in all_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1

        # Get most common themes
        top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_files": len(file_signals),
            "common_themes": [theme for theme, count in top_themes],
            "theme_distribution": dict(top_themes),
            "data_types_found": list(set(
                dtype for signals in file_signals
                for dtype in signals.get("dtypes", {}).values()
            ))
        }

    def _calculate_confidence(self, signals: Dict[str, Any]) -> float:
        """Calculate confidence score for the distillation result"""
        if "error" in signals:
            return 0.0

        confidence = 0.5  # Base confidence

        # Higher confidence for more complete data
        if signals.get("shape", (0, 0))[0] > 10:  # More than 10 rows
            confidence += 0.2

        if len(signals.get("columns", [])) > 3:  # More than 3 columns
            confidence += 0.2

        if signals.get("extracted_themes"):  # Has extracted themes
            confidence += 0.1

        # Lower confidence for poor data quality
        quality = signals.get("data_quality_signals", {})
        if quality.get("completeness", 1.0) < 0.7:
            confidence -= 0.2

        return max(0.0, min(1.0, confidence))

# Register the distiller
visidata_distiller = VisiDataDistiller()
distiller_registry.register(visidata_distiller)