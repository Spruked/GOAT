"""
Distiller Registry - Sovereign registry for instrumental components.

Core Principles:
- Registry owns all distillers
- No external control over registration
- Immutable registration records
- Audit trail for all operations
"""

import asyncio
from typing import Dict, List, Any, Optional, Type
from datetime import datetime
import hashlib
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DistillerRegistry:
    """
    Sovereign registry for GOAT's instrumental components.
    Manages distiller lifecycle and maintains audit trail.
    """

    def __init__(self, registry_path: str = "goat/distillers/registry.jsonl"):
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        # In-memory registry
        self._distillers: Dict[str, Dict[str, Any]] = {}
        self._audit_log: List[Dict[str, Any]] = []

        # Load existing registry
        self._load_registry()

    def register_distiller(self, name: str, distiller_class: Type, config: Dict[str, Any] = None) -> str:
        """
        Register a new distiller in the sovereign registry.

        Args:
            name: Unique distiller name
            distiller_class: The distiller class
            config: Optional configuration

        Returns:
            Registration ID
        """
        if name in self._distillers:
            raise ValueError(f"Distiller '{name}' already registered")

        registration_id = hashlib.sha256(
            f"{name}:{distiller_class.__name__}:{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]

        registration = {
            'id': registration_id,
            'name': name,
            'class_name': distiller_class.__name__,
            'module': distiller_class.__module__,
            'config': config or {},
            'registered_at': datetime.utcnow().isoformat() + "Z",
            'status': 'active',
            'version': getattr(distiller_class, '__version__', '1.0.0')
        }

        self._distillers[name] = registration
        self._audit_log.append({
            'timestamp': datetime.utcnow().isoformat() + "Z",
            'action': 'register',
            'distiller_name': name,
            'registration_id': registration_id,
            'details': registration
        })

        self._save_registry()
        logger.info(f"Registered distiller: {name} ({registration_id})")

        return registration_id

    def unregister_distiller(self, name: str) -> bool:
        """
        Remove a distiller from the registry.

        Args:
            name: Distiller name to remove

        Returns:
            True if removed, False if not found
        """
        if name not in self._distillers:
            return False

        registration = self._distillers[name]
        registration_id = registration['id']

        # Mark as inactive rather than delete (audit trail)
        registration['status'] = 'inactive'
        registration['unregistered_at'] = datetime.utcnow().isoformat() + "Z"

        self._audit_log.append({
            'timestamp': datetime.utcnow().isoformat() + "Z",
            'action': 'unregister',
            'distiller_name': name,
            'registration_id': registration_id
        })

        self._save_registry()
        logger.info(f"Unregistered distiller: {name}")

        return True

    def get_distiller_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get information about a registered distiller."""
        return self._distillers.get(name)

    def list_distillers(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """List all registered distillers."""
        distillers = list(self._distillers.values())
        if active_only:
            distillers = [d for d in distillers if d['status'] == 'active']
        return distillers

    def create_distiller_instance(self, name: str, field_system=None) -> Any:
        """
        Create an instance of a registered distiller.

        Args:
            name: Distiller name
            field_system: GOAT Field system instance

        Returns:
            Distiller instance
        """
        if name not in self._distillers:
            raise ValueError(f"Distiller '{name}' not registered")

        registration = self._distillers[name]
        if registration['status'] != 'active':
            raise ValueError(f"Distiller '{name}' is not active")

        # Import the class dynamically
        try:
            import importlib
            module = importlib.import_module(registration['module'])
            distiller_class = getattr(module, registration['class_name'])
        except (ImportError, AttributeError) as e:
            raise RuntimeError(f"Cannot import distiller class: {e}")

        # Create instance with field system
        instance = distiller_class(field_system=field_system)

        # Apply configuration if provided
        config = registration.get('config', {})
        if hasattr(instance, 'configure') and config:
            instance.configure(config)

        self._audit_log.append({
            'timestamp': datetime.utcnow().isoformat() + "Z",
            'action': 'instantiate',
            'distiller_name': name,
            'registration_id': registration['id']
        })

        return instance

    def get_audit_log(self, distiller_name: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit log entries, optionally filtered by distiller."""
        log = self._audit_log
        if distiller_name:
            log = [entry for entry in log if entry.get('distiller_name') == distiller_name]

        return log[-limit:] if limit else log

    def _load_registry(self):
        """Load registry from persistent storage."""
        if not self.registry_path.exists():
            return

        try:
            with open(self.registry_path, 'r') as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        if entry['action'] == 'register':
                            self._distillers[entry['distiller_name']] = entry['details']
                        elif entry['action'] == 'unregister':
                            if entry['distiller_name'] in self._distillers:
                                self._distillers[entry['distiller_name']]['status'] = 'inactive'
                        self._audit_log.append(entry)
        except Exception as e:
            logger.error(f"Failed to load registry: {e}")

    def _save_registry(self):
        """Save registry to persistent storage."""
        try:
            with open(self.registry_path, 'w') as f:
                for entry in self._audit_log:
                    f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on registry and distillers."""
        health = {
            'registry_status': 'healthy',
            'total_distillers': len(self._distillers),
            'active_distillers': len([d for d in self._distillers.values() if d['status'] == 'active']),
            'inactive_distillers': len([d for d in self._distillers.values() if d['status'] == 'inactive']),
            'audit_entries': len(self._audit_log),
            'distiller_health': {}
        }

        # Check each active distiller
        for name, info in self._distillers.items():
            if info['status'] != 'active':
                continue

            try:
                instance = self.create_distiller_instance(name)
                # Basic health check - distiller should have distill method
                has_distill = hasattr(instance, 'distill')
                health['distiller_health'][name] = {
                    'status': 'healthy' if has_distill else 'degraded',
                    'has_distill_method': has_distill
                }
            except Exception as e:
                health['distiller_health'][name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }

        return health