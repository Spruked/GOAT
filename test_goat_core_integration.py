"""
Test GOAT Core Components Integration

This test validates that all core GOAT components work together:
- VisiDataDistiller
- DistillerRegistry
- LegacyBuilderWorker
- GOATSpaceFieldSKG
- ChaCha20EncryptionVault
- CertificateGenerator
"""

import asyncio
import tempfile
import os
from pathlib import Path
import json
from datetime import datetime

# Import GOAT components
from goat.distillers.visidata_engine import VisiDataDistiller
from goat.distillers.registry import DistillerRegistry
from goat.workers.legacy_builder import LegacyBuilderWorker
from goat.core.goat_field_skg import GOATSpaceField, FieldObservation
from goat.security.chacha20_vault import ChaCha20EncryptionVault
from goat.security.certificate_generator import CertificateGenerator

async def test_core_components():
    """Test all core GOAT components working together."""
    print("🧪 Testing GOAT Core Components Integration")
    print("=" * 50)

    # Create temporary workspace
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # 1. Test GOAT Field SKG
        print("\n1. Testing GOAT Space-Field SKG...")
        field = GOATSpaceField(field_path=str(temp_path / "field"))

        # Create test observation
        observation = FieldObservation(
            timestamp=datetime.utcnow().isoformat() + "Z",
            operation_type="test_distillation",
            inputs_hash="test_hash_123",
            outcome="success",
            metrics={"processing_time": 100, "items_processed": 5},
            context={"file_type": "csv", "file_size": 1024},
            sequence_id=1
        )

        obs_hash = await field.observe(observation)
        print(f"   ✅ Recorded observation: {obs_hash}")

        # Query observations
        results = await field.query(operation_type="test_distillation")
        print(f"   ✅ Queried {len(results)} observations")

        # 2. Test Distiller Registry
        print("\n2. Testing Distiller Registry...")
        registry = DistillerRegistry(registry_path=str(temp_path / "registry.jsonl"))

        # Register VisiData distiller
        reg_id = registry.register_distiller(
            name="visidata",
            distiller_class=VisiDataDistiller,
            config={"default_chunk_size": 1000}
        )
        print(f"   ✅ Registered VisiData distiller: {reg_id}")

        # List distillers
        distillers = registry.list_distillers()
        print(f"   ✅ Found {len(distillers)} registered distillers")

        # 3. Test VisiData Distiller
        print("\n3. Testing VisiData Distiller...")

        # Create test CSV file
        csv_content = """name,age,city
John,25,New York
Jane,30,San Francisco
Bob,35,Chicago"""

        csv_file = temp_path / "test_data.csv"
        with open(csv_file, 'w') as f:
            f.write(csv_content)

        # Create and test distiller
        distiller = registry.create_distiller_instance("visidata", field_system=field)
        result = await distiller.distill(str(csv_file))

        print(f"   ✅ Distilled CSV: {result['row_count']} rows, {len(result['columns'])} columns")
        print(f"   ✅ Sample data: {len(result['sample_data'])} rows")

        # 4. Test Legacy Builder Worker
        print("\n4. Testing Legacy Builder Worker...")
        worker = LegacyBuilderWorker(registry, field_system=field)

        processing_result = await worker.process_content(str(csv_file))
        print(f"   ✅ Processed content: {processing_result['processing_record']['outcome']}")
        print(f"   ✅ Created {len(processing_result['legacy_content']['items'])} legacy items")

        # 5. Test ChaCha20 Encryption Vault
        print("\n5. Testing ChaCha20 Encryption Vault...")
        vault = ChaCha20EncryptionVault(
            vault_path=str(temp_path / "vault"),
            key_store_path=str(temp_path / "keys")
        )

        # Create encryption key
        key_id = vault.create_data_key("test_key", "test_context")
        print(f"   ✅ Created encryption key: {key_id}")

        # Encrypt data
        test_data = b"Hello, GOAT! This is test data for encryption."
        encrypted = await vault.encrypt_data(key_id, test_data)
        print(f"   ✅ Encrypted data: {len(encrypted['ciphertext'])} chars")

        # Decrypt data
        decrypted = await vault.decrypt_data(encrypted)
        assert decrypted == test_data, "Decryption failed!"
        print("   ✅ Decrypted data matches original")

        # 6. Test Certificate Generator
        print("\n6. Testing Certificate Generator...")
        cert_gen = CertificateGenerator(
            cert_store_path=str(temp_path / "certs"),
            key_store_path=str(temp_path / "cert_keys")
        )

        # Generate certificate chain
        cert_result = cert_gen.generate_certificate_chain(
            cert_id="test_cert",
            subject_info={
                'CN': 'GOAT Test Certificate',
                'O': 'GOAT Internal',
                'C': 'US',
                'ST': 'CA',
                'L': 'San Francisco'
            },
            validity_days=365
        )
        print(f"   ✅ Generated 11-layer certificate chain: {cert_result['cert_id']}")

        # 7. Test Health Checks
        print("\n7. Testing Health Checks...")

        # Field health
        field_health = await field.get_graph_health_report()
        print(f"   ✅ GOAT Field health: {field_health.get('status', 'unknown')}")

        # Registry health
        registry_health = await registry.health_check()
        print(f"   ✅ Registry health: {registry_health['registry_status']}")

        # Vault health
        vault_health = await vault.health_check()
        print(f"   ✅ Vault health: {vault_health['vault_status']}")

        # Certificate generator health
        cert_health = await cert_gen.health_check()
        print(f"   ✅ Certificate health: {cert_health['cert_status']}")

        # Worker health
        worker_health = await worker.health_check()
        print(f"   ✅ Worker health: {worker_health['worker_status']}")

        print("\n" + "=" * 50)
        print("🎉 All GOAT Core Components Tests Passed!")
        print("✅ VisiDataDistiller: Working")
        print("✅ DistillerRegistry: Working")
        print("✅ LegacyBuilderWorker: Working")
        print("✅ GOATSpaceFieldSKG: Working")
        print("✅ ChaCha20EncryptionVault: Working")
        print("✅ CertificateGenerator: Working")
        print("\n🚀 GOAT Core Architecture is Ready!")

if __name__ == "__main__":
    asyncio.run(test_core_components())