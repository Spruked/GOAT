# self_repair_protocols.py

from typing import Dict, Any, Optional, List, Callable
import time
import threading
from enum import Enum
from dataclasses import dataclass, field
import traceback

class RepairStrategy(Enum):
    ISOLATE_AND_RESTART = "isolate_and_restart"
    ROLLBACK_TO_BACKUP = "rollback_to_backup"
    REINITIALIZE_FROM_BLUEPRINT = "reinitialize_from_blueprint"
    REPLACE_WITH_REDUNDANT = "replace_with_redundant"
    EMERGENCY_SHUTDOWN = "emergency_shutdown"

@dataclass
class RepairAction:
    action_id: str
    component_name: str
    strategy: RepairStrategy
    timestamp: float = field(default_factory=time.time)
    success: bool = False
    error_message: str = ""
    recovery_time: float = 0.0
    backup_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ComponentHealth:
    name: str
    health_score: float = 1.0
    last_check: float = field(default_factory=time.time)
    consecutive_failures: int = 0
    total_failures: int = 0
    last_error: str = ""
    is_critical: bool = False
    repair_attempts: int = 0

class SelfRepairProtocols:
    """
    Automatic fault recovery system for vault subsystems.
    Can isolate faulty modules, reload from blueprints, and reinstate without downtime.
    """

    def __init__(self, blueprint_manager, lifecycle_controller):
        self.blueprint_manager = blueprint_manager
        self.lifecycle_controller = lifecycle_controller

        self.component_health: Dict[str, ComponentHealth] = {}
        self.repair_history: List[RepairAction] = []
        self.backups: Dict[str, Dict[str, Any]] = {}
        self.redundant_instances: Dict[str, Any] = {}

        self._repair_lock = threading.RLock()
        self._monitor_thread = None
        self._monitoring_active = False

        # Repair thresholds
        self.health_threshold = 0.7
        self.max_consecutive_failures = 3
        self.max_repair_attempts = 5

    def register_component(self, name: str, is_critical: bool = False):
        """Register a component for health monitoring"""
        self.component_health[name] = ComponentHealth(
            name=name,
            is_critical=is_critical
        )

    def start_health_monitoring(self):
        """Start automatic health monitoring"""
        if self._monitoring_active:
            return

        self._monitoring_active = True
        self._monitor_thread = threading.Thread(target=self._health_monitor_loop, daemon=True)
        self._monitor_thread.start()

    def stop_health_monitoring(self):
        """Stop health monitoring"""
        self._monitoring_active = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)

    def _health_monitor_loop(self):
        """Continuous health monitoring loop"""
        while self._monitoring_active:
            try:
                self._check_all_components()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Health monitor error: {e}")
                time.sleep(60)  # Wait longer on error

    def _check_all_components(self):
        """Check health of all registered components"""
        for name, health in self.component_health.items():
            try:
                self._check_component_health(name)
            except Exception as e:
                print(f"Error checking component {name}: {e}")
                self._record_failure(name, str(e))

    def _check_component_health(self, name: str):
        """Check health of a specific component"""
        health = self.component_health[name]

        # Get component status from lifecycle controller
        system_status = self.lifecycle_controller.get_system_status()
        component_status = system_status['components'].get(name)

        if not component_status:
            self._record_failure(name, "Component not found in system status")
            return

        # Assess health based on various metrics
        health_score = self._calculate_health_score(name, component_status)
        health.health_score = health_score
        health.last_check = time.time()

        # Check for critical failures
        if health_score < self.health_threshold:
            health.consecutive_failures += 1
            health.total_failures += 1

            if health.consecutive_failures >= self.max_consecutive_failures:
                self._trigger_repair(name)
        else:
            # Reset consecutive failures on good health
            health.consecutive_failures = 0

    def _calculate_health_score(self, name: str, status: Dict[str, Any]) -> float:
        """Calculate health score for a component"""
        score = 1.0

        # State-based scoring
        state = status.get('state', 'unknown')
        if state == 'error':
            score -= 0.5
        elif state == 'stopped':
            score -= 0.3
        elif state == 'repairing':
            score -= 0.2

        # Error count penalty
        error_count = status.get('error_count', 0)
        score -= min(error_count * 0.1, 0.3)

        # Age penalty (older checks are less reliable)
        last_check = status.get('last_transition', time.time())
        age_hours = (time.time() - last_check) / 3600
        if age_hours > 1:
            score -= min(age_hours * 0.05, 0.2)

        return max(0.0, min(1.0, score))

    def _record_failure(self, name: str, error: str):
        """Record a component failure"""
        health = self.component_health[name]
        health.consecutive_failures += 1
        health.total_failures += 1
        health.last_error = error
        health.last_check = time.time()

        if health.consecutive_failures >= self.max_consecutive_failures:
            self._trigger_repair(name)

    def _trigger_repair(self, name: str):
        """Trigger automatic repair for a component"""
        with self._repair_lock:
            health = self.component_health[name]

            if health.repair_attempts >= self.max_repair_attempts:
                print(f"Component {name} has exceeded max repair attempts")
                if health.is_critical:
                    self._emergency_shutdown(name)
                return

            health.repair_attempts += 1

            # Choose repair strategy
            strategy = self._select_repair_strategy(name)

            # Execute repair
            success = self._execute_repair(name, strategy)

            # Record repair action
            action = RepairAction(
                action_id=f"repair_{name}_{int(time.time())}",
                component_name=name,
                strategy=strategy,
                success=success
            )

            if success:
                health.consecutive_failures = 0
                health.repair_attempts = 0
                health.health_score = 0.8  # Slightly degraded after repair
            else:
                action.error_message = "Repair failed"

            self.repair_history.append(action)

    def _select_repair_strategy(self, name: str) -> RepairStrategy:
        """Select appropriate repair strategy"""
        health = self.component_health[name]

        # Critical components get more aggressive repair
        if health.is_critical:
            if health.repair_attempts == 0:
                return RepairStrategy.ISOLATE_AND_RESTART
            elif health.repair_attempts == 1:
                return RepairStrategy.REINITIALIZE_FROM_BLUEPRINT
            else:
                return RepairStrategy.REPLACE_WITH_REDUNDANT

        # Non-critical components
        if health.repair_attempts == 0:
            return RepairStrategy.ISOLATE_AND_RESTART
        elif health.repair_attempts < 3:
            return RepairStrategy.REINITIALIZE_FROM_BLUEPRINT
        else:
            return RepairStrategy.ROLLBACK_TO_BACKUP

    def _execute_repair(self, name: str, strategy: RepairStrategy) -> bool:
        """Execute the selected repair strategy"""
        try:
            if strategy == RepairStrategy.ISOLATE_AND_RESTART:
                return self._repair_isolate_and_restart(name)
            elif strategy == RepairStrategy.ROLLBACK_TO_BACKUP:
                return self._repair_rollback_to_backup(name)
            elif strategy == RepairStrategy.REINITIALIZE_FROM_BLUEPRINT:
                return self._repair_reinitialize_from_blueprint(name)
            elif strategy == RepairStrategy.REPLACE_WITH_REDUNDANT:
                return self._repair_replace_with_redundant(name)
            elif strategy == RepairStrategy.EMERGENCY_SHUTDOWN:
                return self._repair_emergency_shutdown(name)
            else:
                return False

        except Exception as e:
            print(f"Repair execution failed for {name}: {e}")
            return False

    def _repair_isolate_and_restart(self, name: str) -> bool:
        """Isolate component and restart it"""
        print(f"Isolating and restarting component: {name}")

        # Stop the component
        if not self.lifecycle_controller.stop_component(name, graceful=True):
            return False

        # Brief pause for cleanup
        time.sleep(1)

        # Restart the component
        if not self.lifecycle_controller.start_component(name):
            return False

        print(f"Successfully restarted component: {name}")
        return True

    def _repair_rollback_to_backup(self, name: str) -> bool:
        """Rollback component to backup state"""
        print(f"Rolling back component {name} to backup")

        if name not in self.backups:
            print(f"No backup available for component {name}")
            return False

        backup_data = self.backups[name]

        # Stop component
        self.lifecycle_controller.stop_component(name, graceful=False)

        # Restore from backup (this would need component-specific logic)
        # For now, just restart
        return self.lifecycle_controller.start_component(name)

    def _repair_reinitialize_from_blueprint(self, name: str) -> bool:
        """Reinitialize component from blueprint"""
        print(f"Reinitializing component {name} from blueprint")

        # Get blueprint
        blueprint = self.blueprint_manager.get_blueprint(name)
        if not blueprint:
            print(f"No blueprint found for component {name}")
            return False

        # Stop component
        self.lifecycle_controller.stop_component(name, graceful=False)

        # Reinitialize (this would need component-specific logic)
        # For now, just restart
        return self.lifecycle_controller.start_component(name)

    def _repair_replace_with_redundant(self, name: str) -> bool:
        """Replace with redundant instance"""
        print(f"Replacing component {name} with redundant instance")

        if name not in self.redundant_instances:
            print(f"No redundant instance available for component {name}")
            return False

        # Replace instance
        return self.lifecycle_controller.replace_component(name, self.redundant_instances[name])

    def _repair_emergency_shutdown(self, name: str) -> bool:
        """Emergency shutdown for critical component"""
        print(f"EMERGENCY: Shutting down critical component {name}")

        # Stop the component
        success = self.lifecycle_controller.stop_component(name, graceful=False)

        # Notify system of critical failure
        print(f"CRITICAL FAILURE: Component {name} has failed and been shut down")

        return success

    def create_backup(self, name: str, backup_data: Dict[str, Any]):
        """Create a backup of component state"""
        self.backups[name] = {
            'data': backup_data,
            'timestamp': time.time()
        }

    def register_redundant_instance(self, name: str, instance: Any):
        """Register a redundant instance for failover"""
        self.redundant_instances[name] = instance

    def get_repair_history(self, component_name: str = None) -> List[Dict[str, Any]]:
        """Get repair history"""
        if component_name:
            actions = [a for a in self.repair_history if a.component_name == component_name]
        else:
            actions = self.repair_history

        return [
            {
                'action_id': a.action_id,
                'component_name': a.component_name,
                'strategy': a.strategy.value,
                'timestamp': a.timestamp,
                'success': a.success,
                'error_message': a.error_message,
                'recovery_time': a.recovery_time
            }
            for a in actions
        ]

    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status"""
        total_components = len(self.component_health)
        healthy_components = sum(1 for h in self.component_health.values() if h.health_score >= self.health_threshold)
        critical_components = sum(1 for h in self.component_health.values() if h.is_critical)

        failing_components = [
            name for name, health in self.component_health.items()
            if health.consecutive_failures >= self.max_consecutive_failures
        ]

        return {
            'total_components': total_components,
            'healthy_components': healthy_components,
            'failing_components': failing_components,
            'critical_components': critical_components,
            'overall_health': healthy_components / total_components if total_components > 0 else 0,
            'components': {
                name: {
                    'health_score': health.health_score,
                    'consecutive_failures': health.consecutive_failures,
                    'total_failures': health.total_failures,
                    'repair_attempts': health.repair_attempts,
                    'last_error': health.last_error,
                    'is_critical': health.is_critical
                }
                for name, health in self.component_health.items()
            }
        }