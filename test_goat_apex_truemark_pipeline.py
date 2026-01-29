"""
Integration test for complete GOAT↔APEX↔TrueMark pipeline.

Tests the full certification and minting workflow with security validations.
"""

import asyncio
import json
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta

from goat.output.evidence_bundle import EvidenceBundleGenerator
from goat.integrations.apex_client import APEXClient
from goat.integrations.apex_callback_handler import APEXCallbackHandler
from goat.integrations.truemark_mint_connector import TrueMarkMintConnector
from goat.core.goat_field_skg import GOATFieldSKG

class TestGOATAPEXTrueMarkPipeline:
    """Test the complete GOAT→APEX→TrueMark certification pipeline."""

    @pytest.fixture
    def mock_apex_keys(self):
        """Mock APEX Ed25519 keypair."""
        import ed25519
        signing_key = ed25519.SigningKey.generate()
        return signing_key, signing_key.get_verifying_key()

    @pytest.fixture
    def mock_truemark_keys(self):
        """Mock TrueMark Ed25519 keypair."""
        import ed25519
        signing_key = ed25519.SigningKey.generate()
        return signing_key, signing_key.get_verifying_key()

    @pytest.fixture
    def field_system(self):
        """Mock GOAT Field system."""
        return Mock(spec=GOATFieldSKG)

    @pytest.fixture
    async def evidence_generator(self):
        """Create evidence bundle generator."""
        generator = EvidenceBundleGenerator()
        yield generator

    @pytest.fixture
    async def apex_client(self, mock_apex_keys):
        """Create APEX client with mock keys."""
        _, verify_key = mock_apex_keys
        client = APEXClient(
            apex_endpoint="http://mock-apex:8080",
            apex_public_key=verify_key.to_bytes()
        )
        yield client

    @pytest.fixture
    async def truemark_connector(self, mock_apex_keys, mock_truemark_keys):
        """Create TrueMark connector."""
        _, apex_verify = mock_apex_keys
        truemark_sign, _ = mock_truemark_keys

        connector = TrueMarkMintConnector(
            apex_public_key=apex_verify.to_bytes(),
            truemark_endpoint="http://mock-truemark:8080",
            mint_private_key=truemark_sign.to_bytes()
        )
        yield connector

    @pytest.fixture
    async def callback_handler(self, mock_apex_keys, field_system, truemark_connector):
        """Create APEX callback handler."""
        _, verify_key = mock_apex_keys

        handler = APEXCallbackHandler(
            apex_public_key=verify_key.to_bytes(),
            field_system=field_system,
            truemark_connector=truemark_connector
        )
        yield handler

    @pytest.mark.asyncio
    async def test_complete_pipeline(self, evidence_generator, apex_client,
                                  callback_handler, mock_apex_keys):
        """Test the complete GOAT→APEX→TrueMark pipeline."""

        # Step 1: Generate evidence bundle
        test_data = {
            "operation": "test_operation",
            "inputs": {"param1": "value1"},
            "outputs": {"result": "success"},
            "metrics": {"duration_ms": 100}
        }

        bundle = await evidence_generator.generate_bundle(
            operation_type="test_certification",
            inputs=test_data,
            outputs={"certified": True},
            metrics={"confidence": 0.95}
        )

        assert bundle["bundle_id"]
        assert bundle["hmac_signature"]
        assert len(bundle["provenance_log"]) > 0

        # Step 2: Submit to APEX (mock response)
        apex_sign, _ = mock_apex_keys

        mock_response = {
            "request_id": "apex_req_123",
            "status": "processing",
            "estimated_completion": (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z"
        }

        with patch.object(apex_client.session, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.status = 200
            mock_post.return_value.json = AsyncMock(return_value=mock_response)

            submit_result = await apex_client.submit_bundle(bundle)
            assert submit_result["request_id"] == "apex_req_123"

        # Step 3: Simulate APEX callback with certificate
        callback_payload = {
            "apex_request_id": "apex_req_123",
            "bundle_id": bundle["bundle_id"],
            "certificate": {
                "certificate_id": "cert_456",
                "layers": list(range(1, 14)),  # 13 layers
                "forensic_hash": "hash_789",
                "signatures": ["sig1", "sig2"]
            },
            "issued_at": datetime.utcnow().isoformat() + "Z",
            "expires_at": (datetime.utcnow() + timedelta(days=365)).isoformat() + "Z"
        }

        # Sign callback with APEX key
        canonical = json.dumps(callback_payload, separators=(',', ':'), sort_keys=True)
        signature = apex_sign.sign(canonical.encode()).hex()

        # Step 4: Process callback
        with patch.object(callback_handler.truemark_connector, 'initiate_mint', new_callable=AsyncMock) as mock_mint:
            mock_mint.return_value = {
                "mint_id": "mint_789",
                "asset_id": "asset_101",
                "blockchain_tx": "tx_202",
                "minted_at": datetime.utcnow().isoformat() + "Z",
                "status": "confirmed"
            }

            result = await callback_handler.handle_callback(
                callback_payload, signature, "apex_req_123"
            )

            assert result["status"] == "processed"
            assert result["certificate_id"] == "cert_456"

            # Verify TrueMark mint was triggered
            mock_mint.assert_called_once()

    @pytest.mark.asyncio
    async def test_invalid_signature_rejection(self, callback_handler):
        """Test that invalid signatures are rejected."""

        callback_payload = {
            "apex_request_id": "apex_req_123",
            "bundle_id": "bundle_456",
            "certificate": {
                "certificate_id": "cert_789",
                "layers": list(range(1, 14)),
                "forensic_hash": "hash_101",
                "signatures": ["sig1"]
            },
            "issued_at": datetime.utcnow().isoformat() + "Z",
            "expires_at": (datetime.utcnow() + timedelta(days=365)).isoformat() + "Z"
        }

        # Invalid signature
        invalid_signature = "deadbeef" * 16

        with pytest.raises(Exception) as exc_info:
            await callback_handler.handle_callback(
                callback_payload, invalid_signature, "apex_req_123"
            )

        assert "Invalid APEX signature" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_expired_certificate_rejection(self, callback_handler, mock_apex_keys):
        """Test that expired certificates are rejected."""

        apex_sign, _ = mock_apex_keys

        callback_payload = {
            "apex_request_id": "apex_req_123",
            "bundle_id": "bundle_456",
            "certificate": {
                "certificate_id": "cert_789",
                "layers": list(range(1, 14)),
                "forensic_hash": "hash_101",
                "signatures": ["sig1"]
            },
            "issued_at": (datetime.utcnow() - timedelta(days=400)).isoformat() + "Z",
            "expires_at": (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"  # Already expired
        }

        canonical = json.dumps(callback_payload, separators=(',', ':'), sort_keys=True)
        signature = apex_sign.sign(canonical.encode()).hex()

        with pytest.raises(Exception) as exc_info:
            await callback_handler.handle_callback(
                callback_payload, signature, "apex_req_123"
            )

        assert "Certificate is already expired" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_replay_protection(self, truemark_connector):
        """Test that mint replay attacks are prevented."""

        cert_record = {
            "certificate_id": "cert_123",
            "apex_request_id": "apex_456",
            "layers": list(range(1, 14)),
            "forensic_hash": "hash_789",
            "issued_at": datetime.utcnow().isoformat() + "Z",
            "expires_at": (datetime.utcnow() + timedelta(days=365)).isoformat() + "Z"
        }

        asset_metadata = {"type": "test_asset"}

        # First mint should succeed
        with patch.object(truemark_connector, '_submit_mint_request', new_callable=AsyncMock) as mock_submit:
            mock_submit.return_value = {"mint_id": "mint_123", "status": "confirmed"}

            result1 = await truemark_connector.initiate_mint(cert_record, asset_metadata)
            assert result1["mint_id"] == "mint_123"

        # Second mint with same certificate should fail
        with pytest.raises(Exception) as exc_info:
            await truemark_connector.initiate_mint(cert_record, asset_metadata)

        assert "Mint already processed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_health_checks(self, evidence_generator, apex_client,
                               callback_handler, truemark_connector):
        """Test health checks for all components."""

        # Evidence generator health
        gen_health = await evidence_generator.health_check()
        assert gen_health["status"] == "healthy"

        # APEX client health
        client_health = await apex_client.health_check()
        assert client_health["apex_client_status"] == "healthy"

        # Callback handler health
        handler_health = await callback_handler.health_check()
        assert handler_health["callback_handler_status"] == "healthy"
        assert handler_health["truemark_connector_available"] is True

        # TrueMark connector health
        connector_health = await truemark_connector.health_check()
        assert connector_health["truemark_connector_status"] == "healthy"