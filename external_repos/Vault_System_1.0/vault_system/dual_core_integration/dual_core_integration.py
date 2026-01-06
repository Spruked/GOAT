# dual_core_integration.py

from typing import Dict, Any, Optional, List, Tuple
import time
import threading
from enum import Enum
from dataclasses import dataclass, field
import hashlib
import json

class Hemisphere(Enum):
    LEFT = "left"
    RIGHT = "right"

class SynchronizationMode(Enum):
    MIRROR = "mirror"           # Exact duplication
    COMPLEMENTARY = "complementary"  # Different but compatible
    SPECIALIZED = "specialized" # Each handles different aspects
    REDUNDANT = "redundant"     # Backup for each other

@dataclass
class HemisphereMapping:
    component_name: str
    left_instance: Any = None
    right_instance: Any = None
    sync_mode: SynchronizationMode = SynchronizationMode.MIRROR
    last_sync: float = 0.0
    sync_interval: float = 60.0  # seconds
    conflict_resolution: str = "left_priority"  # left_priority, right_priority, merge, consensus
    is_active: bool = True

@dataclass
class SyncOperation:
    operation_id: str
    component_name: str
    hemisphere: Hemisphere
    operation_type: str  # read, write, update, delete
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    checksum: str = ""

class DualCoreIntegration:
    """
    Maps vault subsystems across both hemispheres for never-shutdown resilience.
    Each hemisphere maintains its own reflection vault + glyph trace, synchronized through ISS bridge.
    """

    def __init__(self, iss_connector, lifecycle_controller):
        self.iss_connector = iss_connector
        self.lifecycle_controller = lifecycle_controller

        self.hemisphere_mappings: Dict[str, HemisphereMapping] = {}
        self.sync_queue: List[SyncOperation] = []
        self.sync_history: List[Dict[str, Any]] = []

        self._sync_lock = threading.RLock()
        self._sync_thread = None
        self._sync_active = False

        # Hemisphere-specific data
        self.left_state: Dict[str, Any] = {}
        self.right_state: Dict[str, Any] = {}

        # Conflict resolution strategies
        self.conflict_resolvers = {
            'left_priority': self._resolve_left_priority,
            'right_priority': self._resolve_right_priority,
            'merge': self._resolve_merge,
            'consensus': self._resolve_consensus
        }

    def register_hemisphere_mapping(self,
                                   component_name: str,
                                   left_instance: Any,
                                   right_instance: Any,
                                   sync_mode: SynchronizationMode = SynchronizationMode.MIRROR,
                                   sync_interval: float = 60.0,
                                   conflict_resolution: str = "left_priority"):
        """Register a component mapping across hemispheres"""

        mapping = HemisphereMapping(
            component_name=component_name,
            left_instance=left_instance,
            right_instance=right_instance,
            sync_mode=sync_mode,
            sync_interval=sync_interval,
            conflict_resolution=conflict_resolution
        )

        self.hemisphere_mappings[component_name] = mapping

        # Initialize hemisphere states
        self.left_state[component_name] = {'last_update': 0.0, 'data': {}}
        self.right_state[component_name] = {'last_update': 0.0, 'data': {}}

    def start_dual_core_sync(self):
        """Start dual-core synchronization"""
        if self._sync_active:
            return

        self._sync_active = True
        self._sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self._sync_thread.start()

        # Set up ISS message handlers for cross-hemisphere communication
        self._setup_iss_handlers()

    def stop_dual_core_sync(self):
        """Stop dual-core synchronization"""
        self._sync_active = False
        if self._sync_thread:
            self._sync_thread.join(timeout=10)

    def _setup_iss_handlers(self):
        """Set up ISS handlers for hemisphere communication"""

        def handle_hemisphere_sync(message):
            """Handle sync messages from other hemisphere"""
            payload = message.payload
            source_hemisphere = payload.get('hemisphere')
            component_name = payload.get('component')
            operation = payload.get('operation')

            if source_hemisphere == 'left':
                self._process_sync_operation(Hemisphere.LEFT, component_name, operation)
            elif source_hemisphere == 'right':
                self._process_sync_operation(Hemisphere.RIGHT, component_name, operation)

        def handle_hemisphere_heartbeat(message):
            """Handle heartbeat from other hemisphere"""
            payload = message.payload
            hemisphere = payload.get('hemisphere')
            status = payload.get('status')

            # Update hemisphere health status
            if hemisphere == 'left':
                self.left_state['heartbeat'] = time.time()
                self.left_state['status'] = status
            elif hemisphere == 'right':
                self.right_state['heartbeat'] = time.time()
                self.right_state['status'] = status

        # Register handlers
        self.iss_connector.register_handler('hemisphere_sync', handle_hemisphere_sync)
        self.iss_connector.register_handler('hemisphere_heartbeat', handle_hemisphere_heartbeat)

    def _sync_loop(self):
        """Main synchronization loop"""
        while self._sync_active:
            try:
                self._perform_sync_cycle()
                time.sleep(30)  # Sync check every 30 seconds
            except Exception as e:
                print(f"Dual-core sync error: {e}")
                time.sleep(60)

    def _perform_sync_cycle(self):
        """Perform one cycle of synchronization"""
        current_time = time.time()

        for component_name, mapping in self.hemisphere_mappings.items():
            if not mapping.is_active:
                continue

            # Check if sync is due
            if current_time - mapping.last_sync >= mapping.sync_interval:
                self._sync_component(component_name)
                mapping.last_sync = current_time

        # Process queued operations
        self._process_sync_queue()

        # Send heartbeat
        self._send_heartbeat()

    def _sync_component(self, component_name: str):
        """Synchronize a specific component across hemispheres"""
        mapping = self.hemisphere_mappings[component_name]

        try:
            # Get current state from both hemispheres
            left_data = self._get_component_state(mapping.left_instance, component_name)
            right_data = self._get_component_state(mapping.right_instance, component_name)

            # Check for conflicts
            if self._detect_conflict(left_data, right_data):
                resolved_data = self._resolve_conflict(component_name, left_data, right_data)
            else:
                resolved_data = self._merge_states(left_data, right_data, mapping.sync_mode)

            # Apply synchronized state to both hemispheres
            self._apply_component_state(mapping.left_instance, component_name, resolved_data)
            self._apply_component_state(mapping.right_instance, component_name, resolved_data)

            # Record sync operation
            self._record_sync_operation(component_name, 'sync', resolved_data)

        except Exception as e:
            print(f"Sync failed for component {component_name}: {e}")
            self._record_sync_operation(component_name, 'sync_failed', {'error': str(e)})

    def _get_component_state(self, instance: Any, component_name: str) -> Dict[str, Any]:
        """Get current state from a component instance"""
        try:
            # This would need component-specific logic
            # For now, return a mock state
            if hasattr(instance, 'get_state'):
                return instance.get_state()
            else:
                return {'timestamp': time.time(), 'data': {}}
        except Exception as e:
            return {'error': str(e), 'timestamp': time.time()}

    def _apply_component_state(self, instance: Any, component_name: str, state: Dict[str, Any]):
        """Apply state to a component instance"""
        try:
            if hasattr(instance, 'set_state'):
                instance.set_state(state)
        except Exception as e:
            print(f"Failed to apply state to {component_name}: {e}")

    def _detect_conflict(self, left_data: Dict[str, Any], right_data: Dict[str, Any]) -> bool:
        """Detect if there's a conflict between hemisphere states"""
        # Simple conflict detection based on timestamps and checksums
        left_time = left_data.get('timestamp', 0)
        right_time = right_data.get('timestamp', 0)

        # If both have been updated recently and differently, potential conflict
        time_diff = abs(left_time - right_time)
        if time_diff > 300:  # 5 minutes
            return True

        # Check checksums if available
        left_checksum = left_data.get('checksum', '')
        right_checksum = right_data.get('checksum', '')

        if left_checksum and right_checksum and left_checksum != right_checksum:
            return True

        return False

    def _resolve_conflict(self, component_name: str, left_data: Dict[str, Any], right_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflicts between hemispheres"""
        mapping = self.hemisphere_mappings[component_name]
        resolver = self.conflict_resolvers.get(mapping.conflict_resolution, self._resolve_left_priority)

        return resolver(component_name, left_data, right_data)

    def _resolve_left_priority(self, component_name: str, left_data: Dict[str, Any], right_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflict by prioritizing left hemisphere"""
        return left_data

    def _resolve_right_priority(self, component_name: str, left_data: Dict[str, Any], right_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflict by prioritizing right hemisphere"""
        return right_data

    def _resolve_merge(self, component_name: str, left_data: Dict[str, Any], right_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflict by merging data"""
        merged = left_data.copy()

        # Simple merge strategy - right data takes precedence for conflicts
        for key, value in right_data.items():
            if key not in merged or merged[key] != value:
                merged[key] = value

        merged['merged_from_conflict'] = True
        merged['merge_timestamp'] = time.time()

        return merged

    def _resolve_consensus(self, component_name: str, left_data: Dict[str, Any], right_data: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflict through consensus (voting/similarity)"""
        # For now, use merge strategy
        return self._resolve_merge(component_name, left_data, right_data)

    def _merge_states(self, left_data: Dict[str, Any], right_data: Dict[str, Any], sync_mode: SynchronizationMode) -> Dict[str, Any]:
        """Merge states based on synchronization mode"""
        if sync_mode == SynchronizationMode.MIRROR:
            # Exact duplication - use most recent
            left_time = left_data.get('timestamp', 0)
            right_time = right_data.get('timestamp', 0)
            return left_data if left_time >= right_time else right_data

        elif sync_mode == SynchronizationMode.COMPLEMENTARY:
            # Merge complementary data
            merged = left_data.copy()
            for key, value in right_data.items():
                if key not in merged:
                    merged[key] = value
            return merged

        elif sync_mode == SynchronizationMode.SPECIALIZED:
            # Keep specialized data separate but synchronized
            return {
                'left_specialization': left_data,
                'right_specialization': right_data,
                'sync_timestamp': time.time()
            }

        elif sync_mode == SynchronizationMode.REDUNDANT:
            # Redundant backup - use primary, keep backup
            return left_data  # Assume left is primary

        return left_data  # Default fallback

    def _process_sync_queue(self):
        """Process queued synchronization operations"""
        with self._sync_lock:
            operations_to_process = self.sync_queue[:10]  # Process up to 10 at a time
            self.sync_queue = self.sync_queue[10:]

        for operation in operations_to_process:
            try:
                self._execute_sync_operation(operation)
            except Exception as e:
                print(f"Failed to process sync operation {operation.operation_id}: {e}")

    def _execute_sync_operation(self, operation: SyncOperation):
        """Execute a synchronization operation"""
        mapping = self.hemisphere_mappings.get(operation.component_name)
        if not mapping:
            return

        # Route to appropriate hemisphere
        if operation.hemisphere == Hemisphere.LEFT:
            target_instance = mapping.left_instance
        else:
            target_instance = mapping.right_instance

        # Apply operation (this would need component-specific logic)
        try:
            if hasattr(target_instance, 'apply_operation'):
                target_instance.apply_operation(operation.operation_type, operation.data)
        except Exception as e:
            print(f"Failed to apply operation to {operation.component_name}: {e}")

    def _send_heartbeat(self):
        """Send heartbeat to other hemisphere"""
        heartbeat_message = {
            'hemisphere': 'left',  # This instance is left hemisphere
            'status': self.lifecycle_controller.get_system_status(),
            'timestamp': time.time()
        }

        self.iss_connector.send_message('hemisphere_heartbeat', heartbeat_message)

    def queue_sync_operation(self, component_name: str, hemisphere: Hemisphere,
                           operation_type: str, data: Dict[str, Any]):
        """Queue a synchronization operation"""
        operation = SyncOperation(
            operation_id=f"sync_{component_name}_{int(time.time())}_{len(self.sync_queue)}",
            component_name=component_name,
            hemisphere=hemisphere,
            operation_type=operation_type,
            data=data,
            checksum=self._calculate_checksum(data)
        )

        with self._sync_lock:
            self.sync_queue.append(operation)

    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate checksum for data integrity"""
        canonical = json.dumps(data, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()

    def _record_sync_operation(self, component_name: str, operation_type: str, data: Dict[str, Any]):
        """Record synchronization operation for audit"""
        record = {
            'component_name': component_name,
            'operation_type': operation_type,
            'timestamp': time.time(),
            'data_summary': str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
        }

        self.sync_history.append(record)

        # Keep history manageable
        if len(self.sync_history) > 1000:
            self.sync_history = self.sync_history[-500:]

    def get_hemisphere_status(self) -> Dict[str, Any]:
        """Get status of both hemispheres"""
        current_time = time.time()

        left_heartbeat_age = current_time - self.left_state.get('heartbeat', 0)
        right_heartbeat_age = current_time - self.right_state.get('heartbeat', 0)

        return {
            'left_hemisphere': {
                'status': self.left_state.get('status', 'unknown'),
                'last_heartbeat': self.left_state.get('heartbeat', 0),
                'heartbeat_age_seconds': left_heartbeat_age,
                'is_alive': left_heartbeat_age < 300  # 5 minutes
            },
            'right_hemisphere': {
                'status': self.right_state.get('status', 'unknown'),
                'last_heartbeat': self.right_state.get('heartbeat', 0),
                'heartbeat_age_seconds': right_heartbeat_age,
                'is_alive': right_heartbeat_age < 300  # 5 minutes
            },
            'sync_queue_length': len(self.sync_queue),
            'mappings_active': sum(1 for m in self.hemisphere_mappings.values() if m.is_active),
            'last_sync_operations': self.sync_history[-5:] if self.sync_history else []
        }

    def failover_to_hemisphere(self, target_hemisphere: Hemisphere):
        """Failover all operations to specified hemisphere"""
        print(f"Initiating failover to {target_hemisphere.value} hemisphere")

        # This would implement failover logic
        # For now, just log the operation
        self._record_sync_operation('system', 'failover', {'target': target_hemisphere.value})

    def get_sync_statistics(self) -> Dict[str, Any]:
        """Get synchronization statistics"""
        if not self.sync_history:
            return {}

        # Analyze sync history
        component_syncs = {}
        operation_types = {}

        for record in self.sync_history:
            comp = record['component_name']
            op_type = record['operation_type']

            component_syncs[comp] = component_syncs.get(comp, 0) + 1
            operation_types[op_type] = operation_types.get(op_type, 0) + 1

        return {
            'total_sync_operations': len(self.sync_history),
            'component_sync_frequency': component_syncs,
            'operation_type_frequency': operation_types,
            'average_sync_interval': 30.0,  # From sync loop
            'queue_length': len(self.sync_queue)
        }