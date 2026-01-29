# goat/core/field_reflection_service.py
"""
Reflection Service: Idle-time learning for GOAT.
Triggers when system load is low (<20%).
"""

import asyncio
import psutil
import os
from datetime import datetime
from typing import List, Dict
from goat.core.goat_field_skg import GOATSpaceField, FieldObservation
import logging

logger = logging.getLogger(__name__)

class FieldReflectionService:
    """
    Manages GOAT's self-improvement cycles.
    Conservative, bounded, interruptible.
    """

    def __init__(self):
        self.field = GOATSpaceField()
        self.running = False
        self.idle_threshold = 20.0  # CPU % below which we consider "idle"

    async def start_monitoring(self):
        """Background task watching for idle times."""
        self.running = True
        logger.info("GOAT Field Reflection Service started")

        while self.running:
            await asyncio.sleep(60)  # Check every minute

            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent

                if cpu_percent < self.idle_threshold and memory_percent < 70:
                    # System is idle enough for reflection
                    logger.debug(f"System idle (CPU: {cpu_percent}%, Mem: {memory_percent}%), triggering reflection")
                    await self.field.reflect(idle_threshold_seconds=0)

                elif cpu_percent > 80:
                    # High load: ensure reflection is paused
                    self.field.reflection_active = False
                    logger.debug(f"High load detected (CPU: {cpu_percent}%), pausing reflection")

            except Exception as e:
                logger.error(f"Error in reflection monitoring: {e}")

    async def stop_monitoring(self):
        """Stop the monitoring service."""
        self.running = False
        logger.info("GOAT Field Reflection Service stopped")

    async def record_distillation(self, distiller_id: str, files: List[str],
                                  signals: Dict, duration_ms: int, success: bool):
        """
        Wrapper for Distillers to record operations to Field.
        """
        obs = FieldObservation(
            sequence_id=self.field.sequence_counter,
            timestamp=datetime.utcnow().isoformat(),
            operation_type='distillation',
            inputs_hash=hashlib.sha256(str(files).encode()).hexdigest()[:16],
            outcome='success' if success else 'failure',
            metrics={
                'processing_time_ms': duration_ms,
                'files_count': len(files),
                'signals_extracted': len(signals.get('themes', [])),
                'distiller_id': distiller_id
            },
            context={
                'file_types': [f.split('.')[-1] for f in files if '.' in f],
                'total_size_mb': sum(os.path.getsize(f) for f in files if os.path.exists(f)) / (1024*1024),
                'distiller_id': distiller_id
            }
        )

        await self.field.observe(obs)
        self.field.sequence_counter += 1

        logger.debug(f"Recorded distillation observation: {obs.sequence_id}")

    async def record_worker_session(self, worker_id: str, session_metrics: Dict):
        """
        Wrapper for Workers to record sessions.
        """
        obs = FieldObservation(
            sequence_id=self.field.sequence_counter,
            timestamp=datetime.utcnow().isoformat(),
            operation_type='worker_session',
            inputs_hash=hashlib.sha256(str(session_metrics.get('user_id', '')).encode()).hexdigest()[:16],
            outcome=session_metrics.get('outcome', 'unknown'),
            metrics={
                'interaction_count': session_metrics.get('interactions', 0),
                'duration_seconds': session_metrics.get('duration', 0),
                'user_satisfaction': session_metrics.get('satisfaction', None)
            },
            context={
                'worker_id': worker_id,
                'product_type': session_metrics.get('product_type'),
                'complexity_score': session_metrics.get('complexity', 0.5)
            }
        )

        await self.field.observe(obs)
        self.field.sequence_counter += 1

        logger.debug(f"Recorded worker session observation: {obs.sequence_id}")

    async def record_error(self, component: str, error_type: str, context: Dict):
        """
        Record system errors for pattern analysis.
        """
        obs = FieldObservation(
            sequence_id=self.field.sequence_counter,
            timestamp=datetime.utcnow().isoformat(),
            operation_type='error',
            inputs_hash=hashlib.sha256(str(context).encode()).hexdigest()[:16],
            outcome='failure',
            metrics={
                'error_type': error_type,
                'component': component
            },
            context=context
        )

        await self.field.observe(obs)
        self.field.sequence_counter += 1

        logger.warning(f"Recorded error observation: {component} - {error_type}")

    def get_runtime_optimizations(self) -> Dict:
        """
        Distillers and Workers call this to get optimized configs.
        Safe, read-only, human-approved only.
        """
        return self.field.compile_insights()

    def get_field_stats(self) -> Dict:
        """
        Get statistics about the field's current state.
        """
        base_stats = {
            'total_observations': self.field.sequence_counter,
            'graph_nodes': self.field.graph.number_of_nodes() if self.field.graph else 0,
            'graph_edges': self.field.graph.number_of_edges() if self.field.graph else 0,
            'pending_proposals': len(self._get_pending_proposals()),
            'last_reflection': self.field.last_reflection.isoformat(),
            'reflection_active': self.field.reflection_active
        }

        # Add graph health if available
        if self.field.graph is not None:
            health = self.field.get_graph_health_report()
            base_stats.update({
                'graph_health': health,
                'clutter_stats': self.field.clutter_stats,
                'last_repair': self.field._get_last_repair_time(),
                'archived_nodes': self.field._count_archived_nodes()
            })

        return base_stats

    def _get_pending_proposals(self) -> List[Dict]:
        """Get list of pending improvement proposals."""
        if not self.field.proposal_queue.exists():
            return []
        queue = json.loads(self.field.proposal_queue.read_text())
        return [p for p in queue if p['status'] == 'pending_review']

# Global instance
field_reflection_service = FieldReflectionService()