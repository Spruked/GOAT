# lifecycle_control.py

from typing import Dict, Any, Optional, Callable
from enum import Enum
import time
import threading
from dataclasses import dataclass, field

class LifecycleState(Enum):
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    REPAIRING = "repairing"

@dataclass
class ComponentStatus:
    name: str
    state: LifecycleState
    last_transition: float = field(default_factory=time.time)
    health_score: float = 1.0
    error_count: int = 0
    dependencies: list = field(default_factory=list)
    dependents: list = field(default_factory=list)

class LifecycleController:
    """
    Manages the lifecycle of all vault subsystems.
    Provides dynamic start/stop/repair/replace capabilities.
    """

    def __init__(self):
        self.components: Dict[str, ComponentStatus] = {}
        self.component_instances: Dict[str, Any] = {}
        self.lifecycle_hooks: Dict[str, Dict[str, Callable]] = {}
        self._lock = threading.RLock()

    def register_component(self,
                          name: str,
                          instance: Any,
                          dependencies: list = None,
                          start_hook: Callable = None,
                          stop_hook: Callable = None,
                          repair_hook: Callable = None,
                          replace_hook: Callable = None):
        """Register a component with its lifecycle hooks"""

        with self._lock:
            self.components[name] = ComponentStatus(
                name=name,
                state=LifecycleState.UNINITIALIZED,
                dependencies=dependencies or []
            )
            self.component_instances[name] = instance

            self.lifecycle_hooks[name] = {
                'start': start_hook,
                'stop': stop_hook,
                'repair': repair_hook,
                'replace': replace_hook
            }

            # Update dependents
            for dep in self.components[name].dependencies:
                if dep in self.components:
                    self.components[dep].dependents.append(name)

    def start_component(self, name: str) -> bool:
        """Start a specific component"""
        with self._lock:
            if name not in self.components:
                return False

            component = self.components[name]

            # Check dependencies
            for dep in component.dependencies:
                if dep not in self.components or self.components[dep].state != LifecycleState.ACTIVE:
                    component.state = LifecycleState.ERROR
                    component.error_count += 1
                    return False

            # Start component
            component.state = LifecycleState.INITIALIZING

            try:
                if self.lifecycle_hooks[name]['start']:
                    self.lifecycle_hooks[name]['start'](self.component_instances[name])

                component.state = LifecycleState.ACTIVE
                component.last_transition = time.time()
                component.health_score = 1.0

                # Start dependents if they were waiting
                self._cascade_start_dependents(name)

                return True

            except Exception as e:
                component.state = LifecycleState.ERROR
                component.error_count += 1
                print(f"Failed to start component {name}: {e}")
                return False

    def stop_component(self, name: str, graceful: bool = True) -> bool:
        """Stop a specific component"""
        with self._lock:
            if name not in self.components:
                return False

            component = self.components[name]

            # Stop dependents first
            for dependent in component.dependents:
                if self.components[dependent].state == LifecycleState.ACTIVE:
                    self.stop_component(dependent, graceful)

            component.state = LifecycleState.STOPPING

            try:
                if self.lifecycle_hooks[name]['stop']:
                    self.lifecycle_hooks[name]['stop'](self.component_instances[name], graceful)

                component.state = LifecycleState.STOPPED
                component.last_transition = time.time()

                return True

            except Exception as e:
                component.state = LifecycleState.ERROR
                component.error_count += 1
                print(f"Failed to stop component {name}: {e}")
                return False

    def suspend_component(self, name: str) -> bool:
        """Suspend a component temporarily"""
        with self._lock:
            if name not in self.components:
                return False

            component = self.components[name]

            if component.state != LifecycleState.ACTIVE:
                return False

            # Stop dependents first
            for dependent in component.dependents:
                if self.components[dependent].state == LifecycleState.ACTIVE:
                    self.suspend_component(dependent)

            component.state = LifecycleState.SUSPENDED
            component.last_transition = time.time()

            return True

    def resume_component(self, name: str) -> bool:
        """Resume a suspended component"""
        with self._lock:
            if name not in self.components:
                return False

            component = self.components[name]

            if component.state != LifecycleState.SUSPENDED:
                return False

            component.state = LifecycleState.ACTIVE
            component.last_transition = time.time()

            # Resume dependents
            self._cascade_start_dependents(name)

            return True

    def repair_component(self, name: str) -> bool:
        """Repair a faulty component"""
        with self._lock:
            if name not in self.components:
                return False

            component = self.components[name]

            if component.state not in [LifecycleState.ERROR, LifecycleState.STOPPED]:
                return False

            component.state = LifecycleState.REPAIRING

            try:
                if self.lifecycle_hooks[name]['repair']:
                    self.lifecycle_hooks[name]['repair'](self.component_instances[name])

                component.state = LifecycleState.STOPPED  # Ready to restart
                component.health_score = 0.8  # Slightly degraded after repair
                component.last_transition = time.time()

                return True

            except Exception as e:
                component.state = LifecycleState.ERROR
                component.error_count += 1
                print(f"Failed to repair component {name}: {e}")
                return False

    def replace_component(self, name: str, new_instance: Any) -> bool:
        """Replace a component instance"""
        with self._lock:
            if name not in self.components:
                return False

            component = self.components[name]

            # Stop the old component
            if component.state == LifecycleState.ACTIVE:
                self.stop_component(name)

            try:
                if self.lifecycle_hooks[name]['replace']:
                    self.lifecycle_hooks[name]['replace'](self.component_instances[name], new_instance)

                self.component_instances[name] = new_instance
                component.state = LifecycleState.STOPPED  # Ready to restart
                component.last_transition = time.time()
                component.error_count = 0  # Reset error count

                return True

            except Exception as e:
                component.state = LifecycleState.ERROR
                component.error_count += 1
                print(f"Failed to replace component {name}: {e}")
                return False

    def _cascade_start_dependents(self, name: str):
        """Start dependent components that were waiting"""
        component = self.components[name]

        for dependent in component.dependents:
            dep_component = self.components[dependent]
            if dep_component.state == LifecycleState.STOPPED:
                # Check if all dependencies are now active
                all_deps_active = all(
                    self.components[dep].state == LifecycleState.ACTIVE
                    for dep in dep_component.dependencies
                )
                if all_deps_active:
                    self.start_component(dependent)

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        with self._lock:
            total_components = len(self.components)
            active_components = sum(1 for c in self.components.values() if c.state == LifecycleState.ACTIVE)
            error_components = sum(1 for c in self.components.values() if c.state == LifecycleState.ERROR)

            avg_health = sum(c.health_score for c in self.components.values()) / total_components if total_components > 0 else 0

            return {
                'total_components': total_components,
                'active_components': active_components,
                'error_components': error_components,
                'system_health': avg_health,
                'components': {
                    name: {
                        'state': status.state.value,
                        'health_score': status.health_score,
                        'error_count': status.error_count,
                        'last_transition': status.last_transition
                    }
                    for name, status in self.components.items()
                }
            }

    def graceful_shutdown(self):
        """Shutdown all components gracefully"""
        with self._lock:
            # Stop in reverse dependency order
            to_stop = [name for name, comp in self.components.items()
                      if comp.state == LifecycleState.ACTIVE]

            for name in reversed(to_stop):
                self.stop_component(name, graceful=True)