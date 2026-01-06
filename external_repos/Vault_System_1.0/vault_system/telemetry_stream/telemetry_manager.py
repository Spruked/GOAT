from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import time
import json
from datetime import datetime, timedelta
from collections import defaultdict, deque
from enum import Enum
import numpy as np

class TelemetryEventType(Enum):
    VAULT_ACCESS = "vault_access"
    GATE_DECISION = "gate_decision"
    MEMORY_OPERATION = "memory_operation"
    DECISION_ENGINE = "decision_engine"
    APRIORI_MINING = "apriori_mining"
    GLYPH_GENERATION = "glyph_generation"
    SECURITY_EVENT = "security_event"
    SYSTEM_HEALTH = "system_health"

@dataclass
class TelemetryEvent:
    event_id: str
    event_type: TelemetryEventType
    timestamp: float
    component: str
    operation: str
    duration: float
    success: bool
    metrics: Dict[str, Any]
    metadata: Dict[str, Any]

class TelemetryManager:
    def __init__(self, retention_days: int = 30, max_events: int = 10000):
        self.retention_days = retention_days
        self.max_events = max_events
        self.event_stream = deque(maxlen=max_events)
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))
        self.performance_metrics = {}
        self.alert_thresholds = {
            'error_rate': 0.05,  # 5% error rate
            'response_time': 5.0,  # 5 seconds
            'memory_usage': 0.8,   # 80% memory usage
        }
        
    def record_event(self, event_type: TelemetryEventType, component: str, 
                    operation: str, duration: float, success: bool,
                    metrics: Dict[str, Any] = None, metadata: Dict[str, Any] = None) -> str:
        """Record a telemetry event"""
        event_id = f"telem_{int(time.time())}_{len(self.event_stream):06d}"
        
        event = TelemetryEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=time.time(),
            component=component,
            operation=operation,
            duration=duration,
            success=success,
            metrics=metrics or {},
            metadata=metadata or {}
        )
        
        self.event_stream.append(event)
        self._update_metrics(event)
        
        # Check for alerts
        self._check_alerts(event)
        
        return event_id
    
    def _update_metrics(self, event: TelemetryEvent):
        """Update performance metrics based on event"""
        component = event.component
        
        # Initialize component metrics if needed
        if component not in self.performance_metrics:
            self.performance_metrics[component] = {
                'total_operations': 0,
                'successful_operations': 0,
                'total_duration': 0.0,
                'last_operation': event.timestamp
            }
        
        metrics = self.performance_metrics[component]
        metrics['total_operations'] += 1
        metrics['total_duration'] += event.duration
        metrics['last_operation'] = event.timestamp
        
        if event.success:
            metrics['successful_operations'] += 1
            
        # Store historical metrics
        self.metrics_history[component].append({
            'timestamp': event.timestamp,
            'duration': event.duration,
            'success': event.success,
            'operation': event.operation
        })
    
    def _check_alerts(self, event: TelemetryEvent):
        """Check if event triggers any alerts"""
        # Check for high error rates
        error_rate = self.get_error_rate(event.component)
        if error_rate > self.alert_thresholds['error_rate']:
            self._trigger_alert(
                f"High error rate in {event.component}: {error_rate:.1%}",
                "ERROR_RATE_HIGH",
                event
            )
        
        # Check for slow operations
        if event.duration > self.alert_thresholds['response_time']:
            self._trigger_alert(
                f"Slow operation in {event.component}: {event.duration:.2f}s",
                "RESPONSE_TIME_HIGH",
                event
            )
    
    def _trigger_alert(self, message: str, alert_type: str, event: TelemetryEvent):
        """Trigger an alert"""
        alert_event = TelemetryEvent(
            event_id=f"alert_{int(time.time())}",
            event_type=TelemetryEventType.SECURITY_EVENT,
            timestamp=time.time(),
            component="TelemetryManager",
            operation="alert_triggered",
            duration=0.0,
            success=True,
            metrics={'alert_message': message, 'alert_type': alert_type},
            metadata={'trigger_event': asdict(event)}
        )
        
        self.event_stream.append(alert_event)
        print(f"ALERT: {message}")  # In production, this would go to monitoring system
    
    def get_component_metrics(self, component: str, hours: int = 24) -> Dict[str, Any]:
        """Get metrics for specific component"""
        if component not in self.performance_metrics:
            return {}
            
        metrics = self.performance_metrics[component]
        total_ops = metrics['total_operations']
        successful_ops = metrics['successful_operations']
        
        # Calculate rates
        success_rate = successful_ops / total_ops if total_ops > 0 else 0
        avg_duration = metrics['total_duration'] / total_ops if total_ops > 0 else 0
        
        # Get recent events for trend analysis
        recent_events = self.get_recent_events(component, hours)
        recent_success_rate = self._calculate_recent_success_rate(recent_events)
        
        return {
            'total_operations': total_ops,
            'successful_operations': successful_ops,
            'success_rate': success_rate,
            'recent_success_rate': recent_success_rate,
            'average_duration': avg_duration,
            'last_operation': metrics['last_operation'],
            'uptime': self._calculate_uptime(component)
        }
    
    def get_recent_events(self, component: Optional[str] = None, 
                         hours: int = 24) -> List[TelemetryEvent]:
        """Get recent events, optionally filtered by component"""
        cutoff_time = time.time() - (hours * 3600)
        
        if component:
            return [
                event for event in self.event_stream
                if event.timestamp >= cutoff_time and event.component == component
            ]
        else:
            return [
                event for event in self.event_stream
                if event.timestamp >= cutoff_time
            ]
    
    def get_error_rate(self, component: str, hours: int = 1) -> float:
        """Calculate error rate for component"""
        recent_events = self.get_recent_events(component, hours)
        if not recent_events:
            return 0.0
            
        error_count = sum(1 for event in recent_events if not event.success)
        return error_count / len(recent_events)
    
    def _calculate_recent_success_rate(self, events: List[TelemetryEvent]) -> float:
        """Calculate success rate from events list"""
        if not events:
            return 1.0
            
        success_count = sum(1 for event in events if event.success)
        return success_count / len(events)
    
    def _calculate_uptime(self, component: str) -> float:
        """Calculate component uptime based on recent operations"""
        recent_events = self.get_recent_events(component, 24)  # Last 24 hours
        if not recent_events:
            return 1.0
            
        success_rate = self._calculate_recent_success_rate(recent_events)
        return success_rate
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health assessment"""
        components = set(event.component for event in self.event_stream)
        health_scores = {}
        
        for component in components:
            metrics = self.get_component_metrics(component, 1)  # Last hour
            if metrics:
                # Health score based on success rate and performance
                success_score = metrics.get('recent_success_rate', 1.0)
                perf_score = 1.0 - min(1.0, metrics.get('average_duration', 0) / 10.0)  # Normalize
                health_scores[component] = (success_score + perf_score) / 2
        
        overall_health = np.mean(list(health_scores.values())) if health_scores else 1.0
        
        return {
            'overall_health': overall_health,
            'component_health': health_scores,
            'total_events': len(self.event_stream),
            'active_components': len(components),
            'system_uptime': min(health_scores.values()) if health_scores else 1.0
        }
    
    def export_telemetry(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Export telemetry data for time range"""
        events = [
            asdict(event) for event in self.event_stream
            if start_time <= event.timestamp <= end_time
        ]
        return events
    
    def clear_old_events(self):
        """Clear events older than retention period"""
        cutoff_time = time.time() - (self.retention_days * 24 * 3600)
        
        # Since we're using deque with maxlen, old events are automatically removed
        # This method is for explicit cleanup if needed
        self.event_stream = deque(
            [event for event in self.event_stream if event.timestamp >= cutoff_time],
            maxlen=self.max_events
        )