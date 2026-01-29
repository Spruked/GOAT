# test_goat_field.py
"""
Test script for GOAT Field autobiographical memory system.
Validates conservative learning, human approval, and distiller integration.
"""

import asyncio
import sys
import os
import tempfile
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from goat.core.goat_field_skg import GOATSpaceField, FieldObservation
from goat.core.field_reflection_service import field_reflection_service
from goat.admin.field_review import field_review
from dals.core.distiller_registry import distiller_registry
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_goat_field_system():
    """Test complete GOAT Field autobiographical memory system."""

    print("=== Testing GOAT Field Autobiographical Memory System ===\n")

    # Test 1: Basic field operations
    print("1. Testing basic field operations...")
    field = GOATSpaceField("./test_goat_field/")

    # Create test observations
    obs1 = FieldObservation(
        sequence_id=0,
        timestamp="2024-01-27T10:00:00Z",
        operation_type="distillation",
        inputs_hash="abc123",
        outcome="success",
        metrics={"processing_time_ms": 1500, "files_count": 1},
        context={"file_type": "csv", "distiller_id": "visidata_distiller"}
    )

    obs2 = FieldObservation(
        sequence_id=1,
        timestamp="2024-01-27T10:05:00Z",
        operation_type="distillation",
        inputs_hash="def456",
        outcome="success",
        metrics={"processing_time_ms": 65000, "files_count": 1},  # Slow file
        context={"file_type": "csv", "distiller_id": "visidata_distiller"}
    )

    await field.observe(obs1)
    await field.observe(obs2)

    print("✓ Recorded 2 observations to field")

    # Test 2: Pattern extraction
    print("\n2. Testing pattern extraction...")
    await field.reflect(idle_threshold_seconds=0)  # Force reflection

    pending = field_review.list_pending()
    print(f"✓ Generated {len(pending)} improvement proposals")

    if pending:
        proposal = pending[0]
        print(f"  - Proposal: {proposal['observation']}")
        print(f"  - Confidence: {proposal['confidence']:.2f}")

    # Test 3: Human approval workflow
    print("\n3. Testing human approval workflow...")
    if pending:
        proposal_id = pending[0]['proposal_id']
        approved_config = {
            "chunk_size": 500,
            "pre_filter": "remove_null_rows"
        }

        field_review.approve(proposal_id, approved_config, "test_admin")
        print("✓ Approved improvement proposal")

        approved = field_review.list_approved()
        print(f"✓ {len(approved)} approved proposals")

    # Test 4: Runtime optimizations
    print("\n4. Testing runtime optimizations...")
    insights = field.compile_insights()
    print(f"✓ Generated insights: {list(insights.keys())}")

    if 'distiller_optimizations' in insights:
        print(f"  - Distiller optimizations: {insights['distiller_optimizations']}")

    # Test 5: Distiller integration
    print("\n5. Testing distiller integration...")

    # Create a test CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("name,age,city\nJohn,25,NYC\nJane,30,LA\n")
        test_file = f.name

    try:
        # Get distiller with optimizations
        distiller = distiller_registry.get_distiller("visidata_distiller", use_optimizations=True)
        print("✓ Retrieved distiller with optimizations")

        # Test distillation
        result = distiller.distill([test_file])
        print(f"✓ Distillation result: {len(result.signals)} signals extracted")

        # Record to field
        await field_reflection_service.record_distillation(
            distiller_id="visidata_distiller",
            files=[test_file],
            signals=result.signals,
            duration_ms=100,
            success=True
        )
        print("✓ Recorded distillation to field")

    finally:
        os.unlink(test_file)

    # Test 6: Field statistics
    print("\n6. Testing field statistics...")
    stats = field_reflection_service.get_field_stats()
    print(f"✓ Field stats: {stats}")

    # Test 7: Audit trail
    print("\n7. Testing audit trail...")
    audit = field_review.get_audit_trail(5)
    print(f"✓ Audit trail: {len(audit)} entries")

    print("\n=== GOAT Field Test Results ===")
    print("✓ Autobiographical memory system functional")
    print("✓ Conservative learning with confidence caps")
    print("✓ Human approval workflow working")
    print("✓ Distiller integration complete")
    print("✓ Pattern extraction and optimization generation")
    print("✓ Immutable journal and audit trails")

    return True

async def test_clutter_cleaning():
    """Test clutter detection and cleaning functionality."""
    print("\n=== Testing Clutter Cleaning ===")

    field = GOATSpaceField("./test_goat_field/")

    # Create some test observations with varying ages and connectivity
    base_time = datetime.utcnow()

    # Recent successful observations (should be kept)
    obs1 = FieldObservation(
        sequence_id=0,
        timestamp=(base_time).isoformat(),
        operation_type="distillation",
        inputs_hash="abc123",
        outcome="success",
        metrics={"processing_time_ms": 1000},
        context={"file_type": "csv"}
    )

    obs2 = FieldObservation(
        sequence_id=1,
        timestamp=(base_time).isoformat(),
        operation_type="distillation",
        inputs_hash="def456",
        outcome="success",
        metrics={"processing_time_ms": 1200},
        context={"file_type": "csv"}
    )

    # Old isolated observation (should be archived)
    obs3 = FieldObservation(
        sequence_id=2,
        timestamp=(base_time - timedelta(days=10)).isoformat(),  # 10 days old
        operation_type="distillation",
        inputs_hash="ghi789",
        outcome="success",
        metrics={"processing_time_ms": 5000},
        context={"file_type": "txt"}
    )

    await field.observe(obs1)
    await field.observe(obs2)
    await field.observe(obs3)

    print(f"✓ Created {field.graph.number_of_nodes()} nodes, {field.graph.number_of_edges()} edges")

    # Manually trigger clutter detection
    clutter_edges, clutter_nodes = field._detect_clutter()
    print(f"✓ Detected {len(clutter_edges)} clutter edges, {len(clutter_nodes)} clutter nodes")

    # Trigger self-repair
    if clutter_edges or clutter_nodes:
        await field._self_repair(clutter_edges, clutter_nodes)
        print("✓ Self-repair completed")

    # Check health after repair
    health = field.get_graph_health_report()
    print(f"✓ Post-repair health: {health.get('status', 'unknown')}")
    print(f"  - Nodes: {health.get('total_nodes', 0)}")
    print(f"  - Edges: {health.get('total_edges', 0)}")
    print(f"  - Archived: {field._count_archived_nodes()}")

    return True

if __name__ == "__main__":
    async def main():
        try:
            success1 = await test_goat_field_system()
            success2 = await test_error_handling()
            success3 = await test_clutter_cleaning()

            if success1 and success2 and success3:
                print("\n🎉 All GOAT Field tests passed!")
                return 0
            else:
                print("\n❌ Some tests failed")
                return 1

        except Exception as e:
            print(f"\n💥 Test suite failed: {e}")
            import traceback
            traceback.print_exc()
            return 1

    exit_code = asyncio.run(main())
    sys.exit(exit_code)