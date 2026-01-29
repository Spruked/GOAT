# core/distiller_interface.py
"""
GOAT Distiller Protocol
Interface for all non-agentic data extraction instruments in GOAT

Distillers are PURE INSTRUMENTS:
- No persona, no dialogue, no decisions
- Extract signals from raw data sources
- Return structured facts for workers to interpret
- Mechanical extraction, not social interaction
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Protocol
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DistillerResult:
    """Standardized result format from all distillers"""

    def __init__(self, signals: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None):
        self.signals = signals  # Raw patterns, facts, structures (no narrative)
        self.metadata = metadata or {}  # Processing metadata (timing, confidence, etc.)
        self.timestamp = metadata.get('timestamp') if metadata else None
        self.confidence = metadata.get('confidence', 1.0) if metadata else 1.0
        self.validated = metadata.get('validated', False) if metadata else False

class DistillerProtocol(ABC):
    """
    Interface for ALL non-agentic data extraction instruments.
    Distillers are tools. They extract. They do not interpret.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this distiller"""
        pass

    @property
    @abstractmethod
    def supported_sources(self) -> List[str]:
        """List of input source types this distiller can process (e.g., ['csv', 'json', 'folder'])"""
        pass

    @property
    @abstractmethod
    def signal_types(self) -> List[str]:
        """List of signal types this distiller produces (e.g., ['frequencies', 'anomalies', 'correlations'])"""
        pass

    @abstractmethod
    def distill(self, sources: List[str], **kwargs) -> DistillerResult:
        """
        Extract signals from data sources.

        Args:
            sources: File paths or data source identifiers
            **kwargs: Distiller-specific parameters

        Returns:
            DistillerResult: Raw signals and metadata (no interpretation)
        """
        pass

    @abstractmethod
    def validate_signals(self, signals: Dict[str, Any]) -> bool:
        """
        Validate signal integrity and consistency.

        Args:
            signals: Signals to validate

        Returns:
            bool: True if signals are valid and consistent
        """
        pass

class DistillerRegistry:
    """
    Registry for all distillation engines in GOAT.
    Separate from WorkerRegistry - instruments are not agents.

    Distillers are loaded, versioned, and instrumented independently
    of agentic workers that wield them.
    """

    def __init__(self):
        self._distillers: Dict[str, DistillerProtocol] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def register(self, distiller: DistillerProtocol, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Register a distiller in the global registry"""
        name = distiller.name
        self._distillers[name] = distiller
        self._metadata[name] = metadata or {
            'registered_at': None,  # Could add timestamp
            'version': '1.0',
            'description': f'Distiller for {name}'
        }
        logger.info(f"Registered distiller: {name}")

    def get_distiller(self, name: str) -> Optional[DistillerProtocol]:
        """Get a distiller by name"""
        return self._distillers.get(name)

    def find_distillers_for_source(self, source_type: str) -> List[DistillerProtocol]:
        """Find all distillers that can process a given source type"""
        return [d for d in self._distillers.values() if source_type in d.supported_sources]

    def list_distillers(self) -> Dict[str, Dict[str, Any]]:
        """List all registered distillers with their capabilities and metadata"""
        return {
            name: {
                'supported_sources': distiller.supported_sources,
                'signal_types': distiller.signal_types,
                'metadata': self._metadata.get(name, {})
            }
            for name, distiller in self._distillers.items()
        }

    def validate_distiller(self, name: str) -> bool:
        """Validate that a distiller is properly registered and functional"""
        distiller = self.get_distiller(name)
        if not distiller:
            return False

        # Test with minimal input
        try:
            # This is a basic validation - real distillers should override
            result = distiller.distill([])
            return distiller.validate_signals(result.signals)
        except Exception as e:
            logger.error(f"Distiller validation failed for {name}: {e}")
            return False

# Global registry instance - separate from worker registry
distiller_registry = DistillerRegistry()