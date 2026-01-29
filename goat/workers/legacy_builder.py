"""
Legacy Builder Worker - GOAT's primary content processing persona.

Core Principles:
- Uses distillers for data extraction
- Builds legacy content from observations
- No autonomous decisions (reports to GOAT Field)
- Maintains processing audit trail
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class LegacyBuilderWorker:
    """
    GOAT's primary content processing worker.
    Builds legacy content using distillers, reports observations.
    """

    def __init__(self, distiller_registry, field_system=None):
        self.registry = distiller_registry
        self.field_system = field_system
        self.processing_history: List[Dict[str, Any]] = []

    async def process_content(self, content_path: str, content_type: str = None,
                            options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process content using appropriate distillers.

        Args:
            content_path: Path to content file
            content_type: Override content type detection
            options: Processing options

        Returns:
            Processing results with observations
        """
        start_time = datetime.utcnow()
        content_path = Path(content_path)

        if not content_path.exists():
            raise FileNotFoundError(f"Content not found: {content_path}")

        # Detect content type if not provided
        if not content_type:
            content_type = self._detect_content_type(content_path)

        # Select appropriate distiller
        distiller_name = self._select_distiller(content_type)
        if not distiller_name:
            raise ValueError(f"No distiller available for content type: {content_type}")

        try:
            # Create distiller instance
            distiller = self.registry.create_distiller_instance(distiller_name, self.field_system)

            # Process content
            options = options or {}
            result = await distiller.distill(str(content_path), options)

            # Build legacy content from observations
            legacy_content = await self._build_legacy_content(result, content_type)

            # Record processing observation
            processing_record = {
                'timestamp': datetime.utcnow().isoformat() + "Z",
                'content_path': str(content_path),
                'content_type': content_type,
                'distiller_used': distiller_name,
                'processing_time_ms': (datetime.utcnow() - start_time).total_seconds() * 1000,
                'result_summary': {
                    'rows_processed': result.get('row_count', 0),
                    'columns_found': len(result.get('columns', [])),
                    'legacy_items_created': len(legacy_content.get('items', []))
                },
                'outcome': 'success'
            }

            self.processing_history.append(processing_record)

            # Report to GOAT Field
            if self.field_system:
                await self._record_field_observation(processing_record, result)

            return {
                'processing_record': processing_record,
                'distillation_result': result,
                'legacy_content': legacy_content
            }

        except Exception as e:
            # Record failure
            failure_record = {
                'timestamp': datetime.utcnow().isoformat() + "Z",
                'content_path': str(content_path),
                'content_type': content_type,
                'distiller_used': distiller_name if 'distiller_name' in locals() else None,
                'error': str(e),
                'outcome': 'failure'
            }

            self.processing_history.append(failure_record)

            if self.field_system:
                await self._record_field_observation(failure_record, {})

            raise

    def _detect_content_type(self, file_path: Path) -> str:
        """Detect content type from file extension."""
        extension_map = {
            '.csv': 'csv',
            '.tsv': 'tsv',
            '.json': 'json',
            '.xlsx': 'xlsx',
            '.xls': 'xlsx',
            '.ods': 'ods',
            '.html': 'html',
            '.xml': 'xml',
            '.txt': 'text',
            '.md': 'markdown'
        }

        ext = file_path.suffix.lower()
        return extension_map.get(ext, 'unknown')

    def _select_distiller(self, content_type: str) -> Optional[str]:
        """Select appropriate distiller for content type."""
        # Map content types to distillers
        distiller_map = {
            'csv': 'visidata',
            'tsv': 'visidata',
            'json': 'visidata',
            'xlsx': 'visidata',
            'xls': 'visidata',
            'ods': 'visidata',
            'html': 'visidata',
            'xml': 'visidata'
        }

        distiller_name = distiller_map.get(content_type)
        if distiller_name:
            # Check if distiller is registered and active
            info = self.registry.get_distiller_info(distiller_name)
            if info and info['status'] == 'active':
                return distiller_name

        return None

    async def _build_legacy_content(self, distillation_result: Dict[str, Any],
                                  content_type: str) -> Dict[str, Any]:
        """
        Build legacy content from distillation observations.
        Creates structured content for GOAT's knowledge base.
        """
        legacy_items = []

        # Extract columns and sample data
        columns = distillation_result.get('columns', [])
        sample_data = distillation_result.get('sample_data', [])
        row_count = distillation_result.get('row_count', 0)

        # Create legacy item for structure
        structure_item = {
            'type': 'data_structure',
            'content_type': content_type,
            'columns': columns,
            'row_count': row_count,
            'column_types': distillation_result.get('structure', {}).get('column_types', {}),
            'created_at': datetime.utcnow().isoformat() + "Z"
        }
        legacy_items.append(structure_item)

        # Create legacy items for sample data (first few rows)
        for i, row in enumerate(sample_data[:5]):  # Limit to 5 sample rows
            data_item = {
                'type': 'data_sample',
                'row_index': i,
                'data': row,
                'content_type': content_type,
                'created_at': datetime.utcnow().isoformat() + "Z"
            }
            legacy_items.append(data_item)

        # Create summary item
        summary_item = {
            'type': 'processing_summary',
            'content_type': content_type,
            'total_rows': row_count,
            'columns_count': len(columns),
            'has_headers': distillation_result.get('structure', {}).get('has_headers', False),
            'sample_rows_processed': len(sample_data),
            'created_at': datetime.utcnow().isoformat() + "Z"
        }
        legacy_items.append(summary_item)

        return {
            'items': legacy_items,
            'summary': {
                'total_items': len(legacy_items),
                'content_types': list(set(item['type'] for item in legacy_items)),
                'processing_timestamp': datetime.utcnow().isoformat() + "Z"
            }
        }

    async def _record_field_observation(self, processing_record: Dict[str, Any],
                                      distillation_result: Dict[str, Any]):
        """Record processing observation in GOAT Field."""
        if not self.field_system:
            return

        # Create field observation
        from goat.core.goat_field_skg import FieldObservation

        observation = FieldObservation(
            timestamp=processing_record['timestamp'],
            operation_type='content_processing',
            inputs_hash=hashlib.sha256(
                f"{processing_record['content_path']}:{processing_record['content_type']}".encode()
            ).hexdigest(),
            outcome=processing_record['outcome'],
            metrics={
                'processing_time_ms': processing_record.get('processing_time_ms', 0),
                'rows_processed': processing_record.get('result_summary', {}).get('rows_processed', 0),
                'columns_found': processing_record.get('result_summary', {}).get('columns_found', 0),
                'legacy_items_created': processing_record.get('result_summary', {}).get('legacy_items_created', 0)
            },
            context={
                'content_path': processing_record['content_path'],
                'content_type': processing_record['content_type'],
                'distiller_used': processing_record.get('distiller_used'),
                'file_size': Path(processing_record['content_path']).stat().st_size if Path(processing_record['content_path']).exists() else 0
            },
            sequence_id=self.field_system._load_sequence()
        )

        await self.field_system.observe(observation)

    def get_processing_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent processing history."""
        return self.processing_history[-limit:] if limit else self.processing_history

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on worker and dependencies."""
        health = {
            'worker_status': 'healthy',
            'registry_available': self.registry is not None,
            'field_system_available': self.field_system is not None,
            'processing_history_count': len(self.processing_history),
            'available_distillers': []
        }

        # Check available distillers
        if self.registry:
            try:
                distillers = self.registry.list_distillers(active_only=True)
                health['available_distillers'] = [d['name'] for d in distillers]
            except Exception as e:
                health['registry_error'] = str(e)
                health['worker_status'] = 'degraded'

        return health