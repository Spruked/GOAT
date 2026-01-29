"""
GOAT Evidence Bundle Generator.

Creates evidence bundles for APEX DOC certification.
Bundles contain content, provenance logs, and certification requests.
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import json
import hmac
import secrets
from pathlib import Path

class EvidenceBundleGenerator:
    """
    Generates evidence bundles for APEX DOC certification.

    Handles bundle creation, HMAC signing, provenance chaining,
    and submission preparation.
    """

    def __init__(self, goat_version: str = "2.1.0", instance_id: str = "goat-prod-us-east-1"):
        self.goat_version = goat_version
        self.instance_id = instance_id

    async def create_bundle(self, content_files: List[Dict[str, Any]],
                          provenance_log: List[Dict[str, Any]],
                          certification_request: Dict[str, Any],
                          context_hints: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a complete evidence bundle for APEX submission.

        Args:
            content_files: List of file manifests with hashes and URIs
            provenance_log: Chain of processing operations
            certification_request: APEX certification parameters
            context_hints: Optional advisory context

        Returns:
            Complete evidence bundle ready for signing and submission
        """
        bundle_id = self._generate_bundle_id()
        submitted_at = datetime.utcnow().isoformat() + "Z"

        # Chain the provenance log
        chained_provenance = self._chain_provenance_log(provenance_log)

        # Create content manifest
        content_manifest = {
            "files": content_files,
            "structure_map_hash": self._calculate_structure_hash(content_files)
        }

        bundle = {
            "bundle_id": bundle_id,
            "submitted_at": submitted_at,
            "goat_version": self.goat_version,

            "attestation": {
                "producer": "GOAT",
                "role": "evidence_preparation_only",
                "certification_authority": "APEX_DOC_REQUIRED",
                "no_forensic_claims": True,
                "goat_instance_id": self.instance_id
            },

            "content_manifest": content_manifest,

            "provenance_log": chained_provenance,

            "context_hints": {
                "type": "advisory_only",
                **(context_hints or {})
            },

            "certification_request": certification_request
        }

        return bundle

    def _generate_bundle_id(self) -> str:
        """Generate unique bundle ID in GBL-YYYY-MM-DD-XXXX format."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        random_suffix = secrets.token_hex(2).upper()
        return f"GBL-{today}-{random_suffix}"

    def _chain_provenance_log(self, log_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Chain provenance log entries with hash references.

        Each entry references the previous entry's hash for immutability.
        """
        chained = []
        prev_hash = None

        for entry in log_entries:
            # Create entry hash
            entry_data = {k: v for k, v in entry.items() if k != 'entry_hash'}
            entry_str = json.dumps(entry_data, sort_keys=True, separators=(',', ':'))
            entry_hash = hashlib.sha256(entry_str.encode()).hexdigest()

            # Add chaining
            chained_entry = {
                **entry_data,
                "prev_entry_hash": prev_hash,
                "entry_hash": entry_hash
            }

            chained.append(chained_entry)
            prev_hash = entry_hash

        return chained

    def _calculate_structure_hash(self, files: List[Dict[str, Any]]) -> str:
        """Calculate hash of content structure."""
        structure_data = {
            "file_count": len(files),
            "total_size": sum(f.get("size_bytes", 0) for f in files),
            "file_hashes": [f.get("hash_sha3", "") for f in files]
        }
        structure_str = json.dumps(structure_data, sort_keys=True)
        return hashlib.sha256(structure_str.encode()).hexdigest()

    def sign_bundle(self, bundle: Dict[str, Any], api_secret: bytes) -> Dict[str, Any]:
        """
        Sign bundle for APEX submission.

        Args:
            bundle: The evidence bundle
            api_secret: GOAT API secret for HMAC

        Returns:
            Signed bundle with HMAC signature
        """
        timestamp = bundle["submitted_at"]
        idempotency_key = bundle["bundle_id"]

        # Compute HMAC using canonical JSON
        signature = self._compute_hmac(api_secret, bundle, timestamp, idempotency_key)

        return {
            "bundle": bundle,
            "signature": signature,
            "timestamp": timestamp,
            "idempotency_key": idempotency_key
        }

    def _compute_hmac(self, secret: bytes, body: Dict[str, Any],
                     timestamp: str, idempotency_key: str) -> str:
        """
        Compute HMAC signature for APEX submission.

        Uses canonical JSON to ensure both sides produce identical signatures.
        """
        # Create canonical JSON (no whitespace, sorted keys)
        canonical = json.dumps(body, separators=(',', ':'), sort_keys=True)

        # Include timestamp and idempotency key
        message = f"{timestamp}.{idempotency_key}.{canonical}"

        return hmac.new(secret, message.encode(), hashlib.sha256).hexdigest()

    async def validate_bundle(self, bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate bundle before submission (client-side validation).

        Based on APEX EvidenceBundleValidator requirements.
        Returns (is_valid, error_messages)
        """
        errors = []

        # Required fields
        required_roots = {"bundle_id", "submitted_at", "attestation",
                         "content_manifest", "provenance_log", "certification_request"}
        missing = required_roots - set(bundle.keys())
        if missing:
            errors.append(f"SCHEMA_VIOLATION: Missing required fields: {missing}")
            return False, errors  # Fatal, can't proceed

        # Attestation validation (legal boundary)
        attestation = bundle.get("attestation", {})
        if attestation.get("producer") != "GOAT":
            errors.append("ATTESTATION_VIOLATION: Producer must be GOAT")
        if not attestation.get("no_forensic_claims", False):
            errors.append("ATTESTATION_VIOLATION: Must explicitly disclaim forensic authority")
        if attestation.get("certification_authority") != "APEX_DOC_REQUIRED":
            errors.append("ATTESTATION_VIOLATION: Must specify APEX_DOC as certifier")

        # Bundle ID format validation
        bundle_id = bundle.get("bundle_id", "")
        if not self._validate_bundle_id_format(bundle_id):
            errors.append("INVALID_BUNDLE_ID: Format must be GBL-YYYY-MM-DD-XXXX")

        # Timestamp freshness (replay attack prevention)
        submitted_at = bundle.get("submitted_at", "")
        try:
            submitted_dt = datetime.fromisoformat(submitted_at.replace('Z', '+00:00'))
            age = datetime.utcnow() - submitted_dt.replace(tzinfo=None)
            max_age = timedelta(hours=24)  # BUNDLE_EXPIRY_HOURS

            if age > max_age:
                errors.append(f"STALE_BUNDLE: Submitted {age.total_seconds()/3600:.1f} hours ago (max 24)")
            if age < timedelta(seconds=-60):  # Future timestamp
                errors.append("FUTURE_TIMESTAMP: Bundle timestamp is in the future (clock skew?)")
        except ValueError:
            errors.append("INVALID_TIMESTAMP: submitted_at must be ISO format")

        # Content manifest validation
        manifest = bundle.get("content_manifest", {})
        files = manifest.get("files", [])

        max_files = 100  # MAX_FILES_PER_BUNDLE
        if len(files) > max_files:
            errors.append(f"MANIFEST_OVERSIZE: {len(files)} files exceeds max {max_files}")

        max_size = 10 * 1024 * 1024 * 1024  # 10GB MAX_BUNDLE_SIZE_BYTES
        total_size = sum(f.get("size_bytes", 0) for f in files)
        if total_size > max_size:
            errors.append(f"CONTENT_TOO_LARGE: {total_size} bytes exceeds {max_size}")

        # File structure validation
        for i, file_entry in enumerate(files):
            required_file_fields = {"filename", "hash_sha3", "size_bytes", "retrieval_uri"}
            missing_fields = required_file_fields - set(file_entry.keys())
            if missing_fields:
                errors.append(f"FILE_{i}_INCOMPLETE: Missing {missing_fields}")

        # Provenance log validation
        log = bundle.get("provenance_log", [])
        max_entries = 1000  # MAX_PROVENANCE_ENTRIES
        if len(log) > max_entries:
            errors.append(f"PROVENANCE_EXCESSIVE: {len(log)} entries exceeds {max_entries}")

        # Verify log chain integrity
        if not self._validate_provenance_chain(log):
            errors.append("PROVENANCE_CHAIN_BROKEN: Log entries do not form valid sequence")

        # Certification request validation
        request = bundle.get("certification_request", {})
        valid_profiles = {"STANDARD_13", "LITE_7", "ENTERPRISE_13", "FORENSIC_13"}
        profile = request.get("layer_profile")
        if profile not in valid_profiles:
            errors.append(f"INVALID_LAYER_PROFILE: {profile} not in {valid_profiles}")

        # No cherry-picking check
        if "requested_layers" in request:
            errors.append("CHERRY_PICKING_DETECTED: Use 'layer_profile' not 'requested_layers'")

        # Callback safety (prevent SSRF)
        callback = request.get("callback_url", "")
        if callback and not self._validate_callback_url(callback):
            errors.append("CALLBACK_UNSAFE: URL must be HTTPS and not internal IP")

        # Version compatibility
        goat_version = bundle.get("goat_version", "")
        supported_versions = ["2.1.0", "2.1.1", "2.2.0"]
        if goat_version not in supported_versions:
            errors.append(f"VERSION_UNSUPPORTED: {goat_version} not in {supported_versions}")

        return len(errors) == 0, errors

    def _validate_bundle_id_format(self, bundle_id: str) -> bool:
        """Validate GBL-YYYY-MM-DD-XXXX format."""
        import re
        return bool(re.match(r"^GBL-\d{4}-\d{2}-\d{2}-[A-F0-9]{4}$", bundle_id))

    def _validate_callback_url(self, url: str) -> bool:
        """Prevent Server-Side Request Forgery."""
        from urllib.parse import urlparse
        parsed = urlparse(url)

        if parsed.scheme != "https":
            return False

        # Block internal IPs (simplified check)
        import socket
        try:
            # Only check if it's a valid hostname, don't resolve to avoid network calls
            if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
                return False
            # Check for private IP ranges in hostname (basic check)
            if parsed.hostname and any(parsed.hostname.startswith(prefix)
                                     for prefix in ['10.', '192.168.', '172.']):
                return False
        except:
            return False

        return True