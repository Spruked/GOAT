"""
Distiller Interface

Abstract base class for all GOAT distillers.
Defines the contract for data extraction engines.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

class DistillerInterface(ABC):
    """
    Abstract interface for GOAT data distillers.

    All distillers must implement this interface to ensure
    consistent behavior and integration with the registry.
    """

    def __init__(self, field_system=None):
        """
        Initialize distiller with optional GOAT Field system.

        Args:
            field_system: GOAT Field system for observation recording
        """
        self.field_system = field_system

    @abstractmethod
    async def distill(self, file_path: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extract structured data from file.

        Args:
            file_path: Path to file to process
            options: Processing options

        Returns:
            Distillation results with observations
        """
        pass

    @abstractmethod
    def supported_formats(self) -> list:
        """
        Return list of supported file formats.

        Returns:
            List of supported file extensions/formats
        """
        pass

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on distiller.

        Returns:
            Health status information
        """
        return {
            'status': 'unknown',
            'supported_formats': self.supported_formats()
        }