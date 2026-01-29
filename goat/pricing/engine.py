"""
GOAT Pricing Engine

Dynamic pricing engine for GOAT services based on usage patterns,
resource consumption, and value delivery metrics.
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PricingEngine:
    """
    GOAT Pricing Engine.

    Calculates dynamic pricing for GOAT services based on:
    - Resource usage (CPU, memory, storage)
    - Processing complexity
    - Output quality/value
    - User tier and history
    """

    def __init__(self, field_system=None):
        """
        Initialize pricing engine.

        Args:
            field_system: GOAT Field system for usage tracking
        """
        self.field_system = field_system

        # Base pricing rates (per operation)
        self.base_rates = {
            'distillation': 0.01,      # per file
            'certificate': 0.05,       # per certificate
            'encryption': 0.001,       # per KB
            'storage': 0.0001,         # per MB/day
            'api_call': 0.0001         # per API call
        }

        # Multipliers for complexity/quality
        self.complexity_multipliers = {
            'simple': 1.0,
            'medium': 1.5,
            'complex': 2.5,
            'enterprise': 4.0
        }

        # User tier discounts
        self.tier_discounts = {
            'free': 0.0,
            'basic': 0.1,
            'premium': 0.25,
            'enterprise': 0.4
        }

    async def calculate_price(self, operation: str, params: Dict[str, Any],
                            user_tier: str = "free") -> Dict[str, Any]:
        """
        Calculate price for an operation.

        Args:
            operation: Type of operation
            params: Operation parameters
            user_tier: User subscription tier

        Returns:
            Pricing calculation result
        """
        try:
            # Base price
            base_price = self.base_rates.get(operation, 0.01)

            # Complexity multiplier
            complexity = params.get('complexity', 'simple')
            complexity_mult = self.complexity_multipliers.get(complexity, 1.0)

            # Resource usage multiplier
            resource_mult = self._calculate_resource_multiplier(params)

            # Quality/value multiplier
            quality_mult = self._calculate_quality_multiplier(params)

            # Subtotal
            subtotal = base_price * complexity_mult * resource_mult * quality_mult

            # Tier discount
            tier_discount = self.tier_discounts.get(user_tier, 0.0)
            discount_amount = subtotal * tier_discount

            # Final price
            final_price = subtotal - discount_amount

            result = {
                'operation': operation,
                'base_price': base_price,
                'complexity_multiplier': complexity_mult,
                'resource_multiplier': resource_mult,
                'quality_multiplier': quality_mult,
                'subtotal': subtotal,
                'tier_discount': tier_discount,
                'discount_amount': discount_amount,
                'final_price': max(final_price, 0.001),  # Minimum price
                'currency': 'USD',
                'calculated_at': datetime.utcnow().isoformat() + "Z"
            }

            # Record pricing observation in GOAT Field
            if self.field_system:
                await self._record_pricing_observation(result, params)

            return result

        except Exception as e:
            logger.error(f"Pricing calculation failed: {e}")
            return {
                'operation': operation,
                'error': str(e),
                'fallback_price': 0.01,
                'currency': 'USD'
            }

    def _calculate_resource_multiplier(self, params: Dict[str, Any]) -> float:
        """Calculate multiplier based on resource usage."""
        multiplier = 1.0

        # File size multiplier
        file_size_mb = params.get('file_size_mb', 1)
        if file_size_mb > 100:
            multiplier *= 2.0
        elif file_size_mb > 10:
            multiplier *= 1.5

        # Processing time multiplier
        processing_time_sec = params.get('processing_time_sec', 1)
        if processing_time_sec > 300:  # 5 minutes
            multiplier *= 2.0
        elif processing_time_sec > 60:  # 1 minute
            multiplier *= 1.3

        return multiplier

    def _calculate_quality_multiplier(self, params: Dict[str, Any]) -> float:
        """Calculate multiplier based on output quality/value."""
        multiplier = 1.0

        # Output size multiplier
        output_size_mb = params.get('output_size_mb', 1)
        if output_size_mb > 50:
            multiplier *= 1.8
        elif output_size_mb > 10:
            multiplier *= 1.3

        # Accuracy/confidence multiplier
        confidence = params.get('confidence', 0.8)
        if confidence > 0.95:
            multiplier *= 1.5
        elif confidence < 0.7:
            multiplier *= 0.8

        return multiplier

    async def _record_pricing_observation(self, pricing_result: Dict[str, Any],
                                        params: Dict[str, Any]):
        """Record pricing calculation in GOAT Field."""
        if not self.field_system:
            return

        # Create field observation
        from goat.core.goat_field_skg import FieldObservation

        observation = FieldObservation(
            timestamp=pricing_result['calculated_at'],
            operation_type='pricing_calculation',
            inputs_hash=hash(str(params)),
            outcome='success',
            metrics={
                'final_price': pricing_result['final_price'],
                'base_price': pricing_result['base_price'],
                'total_multiplier': pricing_result['complexity_multiplier'] *
                                 pricing_result['resource_multiplier'] *
                                 pricing_result['quality_multiplier']
            },
            context={
                'operation': pricing_result['operation'],
                'user_tier': params.get('user_tier', 'unknown'),
                'complexity': params.get('complexity', 'simple')
            },
            sequence_id=self.field_system._load_sequence()
        )

        await self.field_system.observe(observation)

    async def get_pricing_history(self, operation: str = None,
                                limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get pricing calculation history.

        Args:
            operation: Filter by operation type
            limit: Maximum results to return

        Returns:
            List of pricing calculations
        """
        if not self.field_system:
            return []

        # Query field for pricing observations
        results = await self.field_system.query(
            operation_type='pricing_calculation',
            limit=limit
        )

        if operation:
            results = [r for r in results if r['context'].get('operation') == operation]

        return results

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on pricing engine.

        Returns:
            Health status information
        """
        return {
            'pricing_status': 'healthy',
            'field_system_available': self.field_system is not None,
            'base_rates_configured': len(self.base_rates) > 0,
            'tier_discounts_configured': len(self.tier_discounts) > 0,
            'complexity_multipliers_configured': len(self.complexity_multipliers) > 0
        }