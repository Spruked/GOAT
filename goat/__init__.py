"""
GOAT - Generative Operational AI Toolkit

A comprehensive framework for building AI systems with:
- Non-agentic data distillation
- Autobiographical memory (GOAT Field)
- Sovereign component registry
- Pre-storage encryption
- Internal certificate generation
- Human-controlled self-improvement

Core Principles:
1. OBSERVE, don't mutate
2. SUGGEST, don't change
3. WAIT for idle, don't interrupt
4. HUMAN approves, never auto-deploy
"""

__version__ = "0.1.0"
__author__ = "GOAT Development Team"

# Core imports for easy access
from .core.goat_field_skg import GOATSpaceField, FieldObservation
from .core.field_reflection_service import FieldReflectionService
from .distillers.registry import DistillerRegistry
from .workers.legacy_builder import LegacyBuilderWorker
from .encryption.vault import EncryptionVault
from .certificate.internal_generator import InternalCertificateGenerator
from .pricing.engine import PricingEngine
from .admin.field_health_dashboard import FieldHealthDashboard

__all__ = [
    'GOATSpaceField',
    'FieldObservation',
    'FieldReflectionService',
    'DistillerRegistry',
    'LegacyBuilderWorker',
    'EncryptionVault',
    'InternalCertificateGenerator',
    'PricingEngine',
    'FieldHealthDashboard'
]