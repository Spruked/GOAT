"""
GOAT Field Health Dashboard

Administrative interface for monitoring GOAT Field health,
performance metrics, and system status.
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class FieldHealthDashboard:
    """
    GOAT Field Health Dashboard.

    Provides comprehensive monitoring and health checks for:
    - GOAT Field system
    - Distiller registry
    - Worker operations
    - Encryption vault
    - Certificate generator
    - Overall system performance
    """

    def __init__(self, field_system, distiller_registry=None,
                 encryption_vault=None, cert_generator=None):
        """
        Initialize health dashboard.

        Args:
            field_system: GOAT Field system instance
            distiller_registry: Distiller registry instance
            encryption_vault: Encryption vault instance
            cert_generator: Certificate generator instance
        """
        self.field_system = field_system
        self.distiller_registry = distiller_registry
        self.encryption_vault = encryption_vault
        self.cert_generator = cert_generator

    async def get_system_health(self) -> Dict[str, Any]:
        """
        Get comprehensive system health status.

        Returns:
            Complete health report for all GOAT components
        """
        health_report = {
            'timestamp': datetime.utcnow().isoformat() + "Z",
            'overall_status': 'healthy',
            'components': {},
            'alerts': [],
            'metrics': {}
        }

        # Check each component
        components_to_check = [
            ('field_system', self.field_system, 'health_check'),
            ('distiller_registry', self.distiller_registry, 'health_check'),
            ('encryption_vault', self.encryption_vault, 'health_check'),
            ('cert_generator', self.cert_generator, 'health_check')
        ]

        for component_name, component, check_method in components_to_check:
            if component and hasattr(component, check_method):
                try:
                    health = await getattr(component, check_method)()
                    health_report['components'][component_name] = health

                    # Check for unhealthy status
                    status_key = f'{component_name}_status'
                    if status_key in health and health[status_key] != 'healthy':
                        health_report['overall_status'] = 'degraded'
                        health_report['alerts'].append({
                            'component': component_name,
                            'severity': 'warning',
                            'message': f'{component_name} is {health[status_key]}'
                        })

                except Exception as e:
                    health_report['components'][component_name] = {'status': 'error', 'error': str(e)}
                    health_report['overall_status'] = 'unhealthy'
                    health_report['alerts'].append({
                        'component': component_name,
                        'severity': 'error',
                        'message': f'Health check failed: {str(e)}'
                    })

        # Gather system metrics
        health_report['metrics'] = await self._gather_system_metrics()

        # Generate recommendations
        health_report['recommendations'] = self._generate_recommendations(health_report)

        return health_report

    async def _gather_system_metrics(self) -> Dict[str, Any]:
        """Gather system-wide performance metrics."""
        metrics = {
            'total_observations': 0,
            'active_distillers': 0,
            'total_certificates': 0,
            'encryption_operations': 0,
            'uptime_hours': 0  # Would need system start time
        }

        # Get metrics from components
        if self.field_system:
            field_health = await self.field_system.health_check()
            metrics['total_observations'] = field_health.get('total_observations', 0)

        if self.distiller_registry:
            registry_health = await self.distiller_registry.health_check()
            metrics['active_distillers'] = registry_health.get('active_distillers', 0)

        if self.cert_generator:
            cert_health = await self.cert_generator.health_check()
            metrics['total_certificates'] = cert_health.get('total_certificates', 0)

        if self.encryption_vault:
            vault_health = await self.encryption_vault.health_check()
            metrics['encryption_operations'] = vault_health.get('audit_entries', 0)

        return metrics

    def _generate_recommendations(self, health_report: Dict[str, Any]) -> List[str]:
        """Generate health improvement recommendations."""
        recommendations = []

        # Check component health
        for component_name, health in health_report['components'].items():
            status = health.get(f'{component_name}_status', health.get('status', 'unknown'))

            if status == 'unhealthy':
                recommendations.append(f"Critical: {component_name} requires immediate attention")
            elif status == 'degraded':
                recommendations.append(f"Warning: {component_name} performance is degraded")

        # Check metrics for recommendations
        metrics = health_report['metrics']

        if metrics['total_observations'] > 10000:
            recommendations.append("Consider field compaction - observation count is high")

        if metrics['active_distillers'] == 0:
            recommendations.append("No active distillers - content processing unavailable")

        if metrics['total_certificates'] > 100:
            recommendations.append("High certificate count - consider cleanup")

        return recommendations

    async def get_performance_report(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """
        Generate performance report for specified time range.

        Args:
            time_range_hours: Hours to look back for performance data

        Returns:
            Performance metrics report
        """
        start_time = datetime.utcnow() - timedelta(hours=time_range_hours)

        report = {
            'time_range_hours': time_range_hours,
            'start_time': start_time.isoformat() + "Z",
            'end_time': datetime.utcnow().isoformat() + "Z",
            'operation_counts': {},
            'performance_metrics': {},
            'error_rates': {}
        }

        # Query field for performance data
        if self.field_system:
            observations = await self.field_system.query(
                time_range=(start_time, datetime.utcnow())
            )

            # Analyze observations
            for obs in observations:
                op_type = obs['operation_type']

                # Count operations
                report['operation_counts'][op_type] = report['operation_counts'].get(op_type, 0) + 1

                # Track performance metrics
                if 'processing_time_ms' in obs['metrics']:
                    if op_type not in report['performance_metrics']:
                        report['performance_metrics'][op_type] = []
                    report['performance_metrics'][op_type].append(obs['metrics']['processing_time_ms'])

                # Track errors
                if obs['outcome'] == 'failure':
                    report['error_rates'][op_type] = report['error_rates'].get(op_type, 0) + 1

        # Calculate averages and rates
        for op_type, times in report['performance_metrics'].items():
            if times:
                report['performance_metrics'][op_type] = {
                    'avg_time_ms': sum(times) / len(times),
                    'min_time_ms': min(times),
                    'max_time_ms': max(times),
                    'count': len(times)
                }

        for op_type, error_count in report['error_rates'].items():
            total_ops = report['operation_counts'].get(op_type, 0)
            if total_ops > 0:
                report['error_rates'][op_type] = error_count / total_ops

        return report

    async def get_alert_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent system alerts.

        Args:
            limit: Maximum alerts to return

        Returns:
            List of recent alerts
        """
        # This would query an alerts log
        # For now, return empty list as alerts are generated on-demand
        return []

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on the dashboard itself.

        Returns:
            Dashboard health status
        """
        return {
            'dashboard_status': 'healthy',
            'field_system_connected': self.field_system is not None,
            'registry_connected': self.distiller_registry is not None,
            'vault_connected': self.encryption_vault is not None,
            'cert_generator_connected': self.cert_generator is not None
        }