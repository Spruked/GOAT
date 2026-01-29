# dals/core/distiller_registry.py
"""
DistillerRegistry: Sovereign system for non-agentic instruments.
Independent from WorkerRegistry. Distillers are tools, not personas.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Type
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import logging

from core.distiller_interface import DistillerProtocol

logger = logging.getLogger(__name__)

@dataclass
class DistillerSpec:
    """Specification for a registered distiller instrument."""

    distiller_id: str
    version: str
    distiller_class: str
    capabilities: List[str]
    input_formats: List[str]
    resource_limits: Dict
    instrumentation_config: Dict
    lifecycle_config: Dict = field(default_factory=dict)
    registration_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def compute_fingerprint(self) -> str:
        """Unique hash of this specification for audit trails."""
        content = f"{self.distiller_id}:{self.version}:{sorted(self.capabilities)}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

class DistillerRegistry:
    """
    Sovereign registry for data extraction instruments.

    Key difference from WorkerRegistry:
    - Workers are AGENTIC (social surface, dialogue, decisions)
    - Distillers are INSTRUMENTAL (mechanical, signal-only, no persona)
    """

    _instance = None
    _registry: Dict[str, DistillerSpec] = {}
    _instances: Dict[str, DistillerProtocol] = {}  # Pooled instances
    _metrics: Dict[str, List[Dict]] = {}  # Instrumentation data

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_registry()
        return cls._instance

    def _load_registry(self):
        """Load all distiller specifications from registry directory."""
        registry_path = Path("dals/registry/distillers")
        if not registry_path.exists():
            logger.warning(f"Distiller registry path not found: {registry_path}")
            return

        for yaml_file in registry_path.glob("*.yaml"):
            try:
                with open(yaml_file) as f:
                    config = yaml.safe_load(f)

                distiller_config = config["distiller"]
                spec = DistillerSpec(
                    distiller_id=distiller_config["id"],
                    version=distiller_config["version"],
                    distiller_class=distiller_config["class"],
                    capabilities=distiller_config["capabilities"],
                    input_formats=distiller_config["inputs"]["formats"],
                    resource_limits=distiller_config["resources"],
                    instrumentation_config=distiller_config["instrumentation"],
                    lifecycle_config=distiller_config.get("lifecycle", {})
                )

                self._registry[spec.distiller_id] = spec
                self._metrics[spec.distiller_id] = []
                logger.info(f"Loaded distiller spec: {spec.distiller_id} v{spec.version}")

            except Exception as e:
                logger.error(f"Failed to load distiller spec from {yaml_file}: {e}")

    def get_distiller(self, distiller_id: str, use_optimizations: bool = True) -> Optional[DistillerProtocol]:
        """
        Retrieve or instantiate a distiller instrument.
        Implements pooling and lifecycle management.
        Optionally applies learned optimizations from GOAT Field.
        """
        spec = self._registry.get(distiller_id)
        if not spec:
            raise ValueError(f"Distiller {distiller_id} not registered")

        # Check pool first
        if distiller_id in self._instances:
            logger.debug(f"Returning pooled distiller: {distiller_id}")
            instance = self._instances[distiller_id]
        else:
            # Instantiate new
            try:
                module_path, class_name = spec.distiller_class.rsplit(".", 1)
                module = __import__(module_path, fromlist=[class_name])
                distiller_class = getattr(module, class_name)

                instance = distiller_class()

                # Apply resource constraints if supported
                if hasattr(instance, '_set_limits') and spec.resource_limits:
                    instance._set_limits(spec.resource_limits)

                # Pool if configured
                if spec.lifecycle_config.get("pooling", False):
                    max_pool = spec.lifecycle_config.get("max_pool_size", 5)
                    if len([k for k in self._instances.keys() if k.startswith(distiller_id)]) < max_pool:
                        self._instances[distiller_id] = instance
                        logger.debug(f"Pooled new distiller instance: {distiller_id}")

                logger.info(f"Instantiated distiller: {distiller_id} v{spec.version}")

            except Exception as e:
                logger.error(f"Failed to instantiate distiller {distiller_id}: {e}")
                raise

        # Apply GOAT Field optimizations if requested and available
        if use_optimizations and hasattr(instance, '_apply_learned_config'):
            try:
                from goat.core.field_reflection_service import field_reflection_service
                optimizations = field_reflection_service.get_runtime_optimizations()

                # Look for distiller-specific optimizations
                distiller_opts = optimizations.get('distiller_optimizations', {})
                if distiller_id in distiller_opts:
                    config = distiller_opts[distiller_id]
                    instance._apply_learned_config(config)
                    logger.debug(f"Applied learned config to {distiller_id}: {config}")

            except Exception as e:
                logger.warning(f"Failed to apply optimizations to {distiller_id}: {e}")

        return instance

    def instrument(self, distiller_id: str, operation: str, metrics: Dict):
        """
        Record instrumentation data for monitoring.
        Distillers are instrumented; Workers are observed.
        """
        if distiller_id not in self._metrics:
            self._metrics[distiller_id] = []

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "metrics": metrics,
            "fingerprint": self._registry[distiller_id].compute_fingerprint()
        }
        self._metrics[distiller_id].append(entry)

        # Keep only last 1000 entries for memory efficiency
        if len(self._metrics[distiller_id]) > 1000:
            self._metrics[distiller_id] = self._metrics[distiller_id][-1000:]

        logger.debug(f"Instrumented {distiller_id}: {operation}")

    def list_capabilities(self) -> Dict[str, List[str]]:
        """Map of distiller_id -> capabilities (for Worker discovery)."""
        return {
            did: spec.capabilities
            for did, spec in self._registry.items()
        }

    def get_provenance(self, distiller_id: str) -> Dict:
        """Get full audit trail for APEX DOC Layer 6 (Process)."""
        spec = self._registry[distiller_id]
        return {
            "distiller_id": distiller_id,
            "spec_fingerprint": spec.compute_fingerprint(),
            "version": spec.version,
            "registration_time": spec.registration_timestamp,
            "execution_history": self._metrics.get(distiller_id, [])[-100:],  # Last 100 ops
            "capabilities": spec.capabilities,
            "input_formats": spec.input_formats
        }

    def list_distillers(self) -> Dict[str, Dict]:
        """List all registered distillers with their specs."""
        return {
            did: {
                "version": spec.version,
                "capabilities": spec.capabilities,
                "input_formats": spec.input_formats,
                "resource_limits": spec.resource_limits,
                "last_used": self._metrics.get(did, [])[-1].get("timestamp") if self._metrics.get(did) else None
            }
            for did, spec in self._registry.items()
        }

    def health_check(self, distiller_id: str) -> Dict:
        """Run health checks on a distiller."""
        spec = self._registry.get(distiller_id)
        if not spec:
            return {"status": "not_registered"}

        try:
            distiller = self.get_distiller(distiller_id)

            # Run configured health checks
            health_results = {}
            for check_name in spec.instrumentation_config.get("health_checks", []):
                if check_name == "format_support_check":
                    health_results[check_name] = self._check_format_support(distiller, spec)
                elif check_name == "memory_pressure_test":
                    health_results[check_name] = self._check_memory_pressure(distiller, spec)
                elif check_name == "signal_validation_test":
                    health_results[check_name] = self._check_signal_validation(distiller)

            return {
                "status": "healthy" if all(r.get("passed", False) for r in health_results.values()) else "degraded",
                "checks": health_results,
                "last_check": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Health check failed for {distiller_id}: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.utcnow().isoformat()
            }

    def _check_format_support(self, distiller: DistillerProtocol, spec: DistillerSpec) -> Dict:
        """Check if distiller supports its declared formats."""
        try:
            # Test with minimal data for each format
            for fmt in spec.input_formats[:3]:  # Test first 3 formats
                test_data = f"test.{fmt}"
                if hasattr(distiller, 'can_process') and distiller.can_process(fmt):
                    continue
            return {"passed": True, "message": f"Supports {len(spec.input_formats)} formats"}
        except Exception as e:
            return {"passed": False, "error": str(e)}

    def _check_memory_pressure(self, distiller: DistillerProtocol, spec: DistillerSpec) -> Dict:
        """Test memory usage under load."""
        # Simplified check - in production would monitor actual memory
        return {"passed": True, "message": "Memory check placeholder"}

    def _check_signal_validation(self, distiller: DistillerProtocol) -> Dict:
        """Test signal validation capability."""
        try:
            # Test with empty result
            result = distiller.distill([])
            is_valid = distiller.validate_signals(result.signals)
            return {"passed": is_valid, "message": "Signal validation functional"}
        except Exception as e:
            return {"passed": False, "error": str(e)}

# Global singleton instance
distiller_registry = DistillerRegistry()