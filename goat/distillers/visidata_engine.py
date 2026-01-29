"""
VisiData Distiller - Non-agentic data extraction engine for GOAT.

Core Principles:
- Streaming processing (no pandas, minimal memory)
- Pattern detection without interpretation
- Immutable observations for GOAT Field
- No decision-making (pure instrumentation)
"""

import visidata
from visidata import vd, Sheet, Column, Progress
import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Iterator
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class VisiDataDistiller:
    """
    Non-agentic data extraction engine.
    Observes, extracts, reports. Never decides.
    """

    def __init__(self, field_system=None):
        self.field_system = field_system
        self.supported_formats = {
            'csv': self._process_csv,
            'tsv': self._process_tsv,
            'json': self._process_json,
            'xlsx': self._process_xlsx,
            'xls': self._process_xlsx,
            'ods': self._process_ods,
            'html': self._process_html,
            'xml': self._process_xml
        }

    async def distill(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extract structured data from file using VisiData.
        Returns observations, not interpretations.
        """
        start_time = datetime.utcnow()
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = file_path.suffix.lower().lstrip('.')
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")

        options = options or {}
        chunk_size = options.get('chunk_size', 1000)
        pre_filter = options.get('pre_filter')

        try:
            # Process file with VisiData
            processor = self.supported_formats[file_ext]
            result = await processor(file_path, chunk_size, pre_filter)

            # Record observation in GOAT Field
            if self.field_system:
                await self._record_observation(
                    operation_type='distillation',
                    file_path=str(file_path),
                    file_type=file_ext,
                    metrics={
                        'processing_time_ms': (datetime.utcnow() - start_time).total_seconds() * 1000,
                        'rows_processed': result.get('row_count', 0),
                        'columns_detected': len(result.get('columns', [])),
                        'chunk_size_used': chunk_size
                    },
                    context={
                        'file_size': file_path.stat().st_size,
                        'file_type': file_ext,
                        'options': options
                    },
                    outcome='success'
                )

            return result

        except Exception as e:
            # Record failure observation
            if self.field_system:
                await self._record_observation(
                    operation_type='distillation',
                    file_path=str(file_path),
                    file_type=file_ext,
                    metrics={'error': str(e)},
                    context={'file_size': file_path.stat().st_size},
                    outcome='failure'
                )
            raise

    async def _process_csv(self, file_path: Path, chunk_size: int, pre_filter: str = None) -> Dict[str, Any]:
        """Process CSV files with streaming."""
        vd.options.delimiter = ','  # Ensure CSV detection

        # Load with VisiData
        sheet = vd.openSource(str(file_path))

        # Apply pre-filter if specified
        if pre_filter == 'drop_empty_rows':
            sheet = sheet.filter(lambda r: any(str(v).strip() for v in r.values()))

        # Extract structure
        columns = [col.name for col in sheet.columns]
        sample_rows = []

        # Get sample data (streaming)
        for i, row in enumerate(sheet.iterrows()):
            if i >= 10:  # Sample first 10 rows
                break
            sample_rows.append(dict(row))

        return {
            'file_type': 'csv',
            'columns': columns,
            'row_count': sheet.nRows,
            'sample_data': sample_rows,
            'structure': {
                'has_headers': self._detect_headers(sheet),
                'column_types': self._infer_column_types(sheet),
                'encoding': 'utf-8'  # VisiData handles encoding
            }
        }

    async def _process_tsv(self, file_path: Path, chunk_size: int, pre_filter: str = None) -> Dict[str, Any]:
        """Process TSV files."""
        vd.options.delimiter = '\t'
        return await self._process_csv(file_path, chunk_size, pre_filter)  # Reuse CSV logic

    async def _process_json(self, file_path: Path, chunk_size: int, pre_filter: str = None) -> Dict[str, Any]:
        """Process JSON files."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            # JSON array of objects
            if data:
                columns = list(data[0].keys()) if isinstance(data[0], dict) else ['value']
                sample_rows = data[:10]
                row_count = len(data)
            else:
                columns = []
                sample_rows = []
                row_count = 0
        elif isinstance(data, dict):
            # Single JSON object - flatten
            columns = list(data.keys())
            sample_rows = [data]
            row_count = 1
        else:
            raise ValueError("Unsupported JSON structure")

        return {
            'file_type': 'json',
            'columns': columns,
            'row_count': row_count,
            'sample_data': sample_rows,
            'structure': {
                'is_array': isinstance(data, list),
                'column_types': {col: type(data[0][col]).__name__ if data else 'unknown' for col in columns}
            }
        }

    async def _process_xlsx(self, file_path: Path, chunk_size: int, pre_filter: str = None) -> Dict[str, Any]:
        """Process Excel files."""
        try:
            sheet = vd.openSource(str(file_path))

            columns = [col.name for col in sheet.columns]
            sample_rows = []

            for i, row in enumerate(sheet.iterrows()):
                if i >= 10:
                    break
                sample_rows.append(dict(row))

            return {
                'file_type': 'xlsx',
                'columns': columns,
                'row_count': sheet.nRows,
                'sample_data': sample_rows,
                'structure': {
                    'has_headers': self._detect_headers(sheet),
                    'column_types': self._infer_column_types(sheet),
                    'sheets': [sheet.name] if hasattr(sheet, 'name') else ['Sheet1']
                }
            }
        except Exception as e:
            # Fallback for complex Excel files
            logger.warning(f"VisiData Excel processing failed: {e}, using basic detection")
            return await self._fallback_excel_processing(file_path)

    async def _process_ods(self, file_path: Path, chunk_size: int, pre_filter: str = None) -> Dict[str, Any]:
        """Process OpenDocument spreadsheets."""
        # Similar to Excel but with ODS-specific handling
        return await self._process_xlsx(file_path, chunk_size, pre_filter)

    async def _process_html(self, file_path: Path, chunk_size: int, pre_filter: str = None) -> Dict[str, Any]:
        """Process HTML tables."""
        try:
            sheet = vd.openSource(str(file_path))

            columns = [col.name for col in sheet.columns]
            sample_rows = []

            for i, row in enumerate(sheet.iterrows()):
                if i >= 10:
                    break
                sample_rows.append(dict(row))

            return {
                'file_type': 'html',
                'columns': columns,
                'row_count': sheet.nRows,
                'sample_data': sample_rows,
                'structure': {
                    'tables_found': 1,  # VisiData extracts first table
                    'has_headers': self._detect_headers(sheet)
                }
            }
        except Exception:
            return await self._fallback_html_processing(file_path)

    async def _process_xml(self, file_path: Path, chunk_size: int, pre_filter: str = None) -> Dict[str, Any]:
        """Process XML files."""
        # Basic XML structure detection
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Extract element structure
            elements = []
            for child in root[:10]:  # Sample first 10 elements
                if child.attrib or child.text:
                    elements.append({
                        'tag': child.tag,
                        'attributes': child.attrib,
                        'text': child.text.strip() if child.text else None
                    })

            return {
                'file_type': 'xml',
                'columns': ['tag', 'attributes', 'text'],
                'row_count': len(elements),
                'sample_data': elements,
                'structure': {
                    'root_tag': root.tag,
                    'namespaces': dict(root.nsmap) if hasattr(root, 'nsmap') else {}
                }
            }
        except Exception:
            return await self._fallback_text_processing(file_path, 'xml')

    async def _fallback_excel_processing(self, file_path: Path) -> Dict[str, Any]:
        """Fallback for complex Excel files."""
        return {
            'file_type': 'xlsx',
            'columns': ['raw_content'],
            'row_count': 1,
            'sample_data': [{'raw_content': 'Complex Excel file detected - manual processing required'}],
            'structure': {'fallback': True}
        }

    async def _fallback_html_processing(self, file_path: Path) -> Dict[str, Any]:
        """Fallback for complex HTML files."""
        return {
            'file_type': 'html',
            'columns': ['raw_content'],
            'row_count': 1,
            'sample_data': [{'raw_content': 'Complex HTML detected - table extraction required'}],
            'structure': {'fallback': True}
        }

    async def _fallback_text_processing(self, file_path: Path, file_type: str) -> Dict[str, Any]:
        """Fallback for text-based files."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(1000)  # First 1000 chars

        return {
            'file_type': file_type,
            'columns': ['content'],
            'row_count': 1,
            'sample_data': [{'content': content}],
            'structure': {'fallback': True}
        }

    def _detect_headers(self, sheet) -> bool:
        """Detect if first row contains headers."""
        if not sheet.columns or sheet.nRows < 2:
            return False

        # Simple heuristic: check if first row values look like headers
        first_row = next(sheet.iterrows())
        header_score = 0

        for value in first_row.values():
            val_str = str(value).strip()
            if val_str and not val_str.isdigit() and len(val_str) < 50:
                header_score += 1

        return header_score > len(first_row) * 0.7

    def _infer_column_types(self, sheet) -> Dict[str, str]:
        """Infer column data types."""
        types = {}
        sample_size = min(100, sheet.nRows)

        for col in sheet.columns:
            col_name = col.name
            values = []

            # Sample values from column
            for i, row in enumerate(sheet.iterrows()):
                if i >= sample_size:
                    break
                val = row.get(col_name)
                if val is not None:
                    values.append(val)

            # Infer type
            if not values:
                types[col_name] = 'empty'
            elif all(isinstance(v, (int, float)) or (isinstance(v, str) and v.replace('.', '').replace('-', '').isdigit()) for v in values):
                types[col_name] = 'numeric'
            elif all(isinstance(v, str) and len(v) < 10 for v in values):
                types[col_name] = 'categorical'
            else:
                types[col_name] = 'text'

        return types

    async def _record_observation(self, operation_type: str, file_path: str, file_type: str,
                                metrics: Dict, context: Dict, outcome: str):
        """Record processing observation in GOAT Field."""
        if not self.field_system:
            return

        # Create field observation
        from goat.core.goat_field_skg import FieldObservation

        observation = FieldObservation(
            timestamp=datetime.utcnow().isoformat() + "Z",
            operation_type=operation_type,
            inputs_hash=hashlib.sha256(f"{file_path}:{file_type}".encode()).hexdigest(),
            outcome=outcome,
            metrics=metrics,
            context=context,
            sequence_id=self.field_system._load_sequence()
        )

        await self.field_system.observe(observation)