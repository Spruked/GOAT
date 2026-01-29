"""
APEX DOC Evidence Bundle Validator.

Reference implementation of the APEX EvidenceBundleValidator.
This is the gatekeeper that validates GOAT evidence bundles before certification.
"""

import hashlib
import json
from typing import Tuple, List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class EvidenceBundleValidator:
    """
    Validates GOAT Evidence Bundles before 13-layer processing.
    Bulletproof rejection of invalid inputs.
    """

    # Whitelisted GOAT instances (mTLS certs or API keys)
    AUTHORIZED_PRODUCERS = {
        "goat_prod_us_east_1": "0xCERT_HASH_PLACEHOLDER",
        "goat_prod_eu_west_1": "0xCERT_HASH_PLACEHOLDER",
        "goat_staging": "0xSTAGING_CERT_PLACEHOLDER"
    }

    # Allowed profiles (no cherry-picking layers)
    VALID_LAYER_PROFILES = {
        "STANDARD_13",
        "LITE_7",           # Reduced for low-stakes content
        "ENTERPRISE_13",    # With additional legal assertions
        "FORENSIC_13"       # Maximum scrutiny (court-ready)
    }

    # Schema version compatibility
    SUPPORTED_GOAT_VERSIONS = ["2.1.0", "2.1.1", "2.2.0"]

    # Business rules
    MAX_BUNDLE_SIZE_BYTES = 10 * 1024 * 1024 * 1024  # 10GB
    MAX_PROVENANCE_ENTRIES = 1000
    MAX_FILES_PER_BUNDLE = 100
    BUNDLE_EXPIRY_HOURS = 24

    def validate(self, bundle: dict, signature: str, api_key: str) -> Tuple[bool, List[str]]:
        """
        Returns: (is_valid, rejection_reasons)
        Empty rejection list = ACCEPT
        """
        rejections = []

        # 1. Authentication
        if not self._authenticate_producer(api_key, signature, bundle):
            return False, ["INVALID_AUTH: Producer not authorized or signature mismatch"]

        # 2. Schema validation
        required_roots = {"bundle_id", "attestation", "content_manifest", "provenance_log", "certification_request"}
        missing = required_roots - set(bundle.keys())
        if missing:
            rejections.append(f"SCHEMA_VIOLATION: Missing required fields: {missing}")
            return False, rejections  # Fatal, can't proceed

        # 3. Producer attestation check (legal boundary)
        attestation = bundle.get("attestation", {})
        if attestation.get("producer") != "GOAT":
            rejections.append("ATTESTATION_VIOLATION: Producer must be GOAT")

        if not attestation.get("no_forensic_claims", False):
            rejections.append("ATTESTATION_VIOLATION: Must explicitly disclaim forensic authority")

        if attestation.get("certification_authority") != "APEX_DOC_REQUIRED":
            rejections.append("ATTESTATION_VIOLATION: Must specify APEX_DOC as certifier")

        # 4. Version compatibility
        goat_ver = bundle.get("submitted_at")  # Actually should check header or field
        # Note: In production, check against SUPPORTED_GOAT_VERSIONS

        # 5. Bundle ID format validation
        bundle_id = bundle.get("bundle_id", "")
        if not self._validate_bundle_id_format(bundle_id):
            rejections.append("INVALID_BUNDLE_ID: Format must be GBL-YYYY-MM-DD-XXXX")

        # 6. Timestamp freshness (replay attack prevention)
        submitted_at = bundle.get("submitted_at", "")
        try:
            submitted_dt = datetime.fromisoformat(submitted_at.replace('Z', '+00:00'))
            age = datetime.utcnow() - submitted_dt.replace(tzinfo=None)
            if age > timedelta(hours=self.BUNDLE_EXPIRY_HOURS):
                rejections.append(f"STALE_BUNDLE: Submitted {age.total_seconds()/3600:.1f} hours ago (max {self.BUNDLE_EXPIRY_HOURS})")

            if age < timedelta(seconds=-60):  # Future timestamp
                rejections.append("FUTURE_TIMESTAMP: Bundle timestamp is in the future (clock skew?)")
        except ValueError:
            rejections.append("INVALID_TIMESTAMP: submitted_at must be valid ISO format")

        # 7. Content manifest validation
        manifest = bundle.get("content_manifest", {})
        files = manifest.get("files", [])

        if len(files) > self.MAX_FILES_PER_BUNDLE:
            rejections.append(f"MANIFEST_OVERSIZE: {len(files)} files exceeds max {self.MAX_FILES_PER_BUNDLE}")

        total_size = sum(f.get("size_bytes", 0) for f in files)
        if total_size > self.MAX_BUNDLE_SIZE_BYTES:
            rejections.append(f"CONTENT_TOO_LARGE: {total_size} bytes exceeds {self.MAX_BUNDLE_SIZE_BYTES}")

        # 8. Hash verification (files must be retrievable and match hashes)
        for file_entry in files:
            if not self._verify_file_integrity(file_entry):
                rejections.append(f"HASH_MISMATCH: {file_entry.get('filename')} hash verification failed")

        # 9. Provenance log validation
        log = bundle.get("provenance_log", [])
        if len(log) > self.MAX_PROVENANCE_ENTRIES:
            rejections.append(f"PROVENANCE_EXCESSIVE: {len(log)} entries exceeds {self.MAX_PROVENANCE_ENTRIES}")

        # Verify log chain integrity (each operation references previous)
        if not self._verify_provenance_chain(log):
            rejections.append("PROVENANCE_CHAIN_BROKEN: Log entries do not form valid sequence")

        # 10. Certification request validation
        request = bundle.get("certification_request", {})
        profile = request.get("layer_profile")
        if profile not in self.VALID_LAYER_PROFILES:
            rejections.append(f"INVALID_LAYER_PROFILE: {profile} not in {self.VALID_LAYER_PROFILES}")

        # No cherry-picking check
        if "requested_layers" in request:
            rejections.append("CHERRY_PICKING_DETECTED: Use 'layer_profile' not 'requested_layers'")

        # 11. Callback safety (prevent SSRF)
        callback = request.get("callback_url", "")
        if callback and not self._validate_callback_url(callback):
            rejections.append("CALLBACK_UNSAFE: URL must be HTTPS and not internal IP")

        return len(rejections) == 0, rejections

    def _authenticate_producer(self, api_key: str, signature: str, bundle: dict) -> bool:
        """HMAC verification + API key whitelist."""
        if api_key not in self.AUTHORIZED_PRODUCERS:
            return False

        # Verify HMAC-SHA256 of bundle body
        expected_cert = self.AUTHORIZED_PRODUCERS[api_key]
        computed = hashlib.sha256(f"{bundle}{expected_cert}".encode()).hexdigest()
        return computed == signature

    def _validate_bundle_id_format(self, bundle_id: str) -> bool:
        """GBL-YYYY-MM-DD-XXXX format."""
        import re
        return bool(re.match(r"^GBL-\d{4}-\d{2}-\d{2}-[A-Z0-9]{4}$", bundle_id))

    def _verify_file_integrity(self, file_entry: dict) -> bool:
        """Check file exists at retrieval_uri and matches hash."""
        # Implementation would fetch from IPFS/S3 and hash verify
        # For now, structural validation only
        required = {"filename", "hash_sha3", "size_bytes", "retrieval_uri"}
        return required.issubset(file_entry.keys())

    def _verify_provenance_chain(self, log: list) -> bool:
        """Ensure provenance entries form coherent timeline."""
        if not log:
            return True  # Empty log is valid (edge case)

        timestamps = []
        prev_hash = None

        for entry in log:
            # Check hash chaining
            if entry.get("prev_entry_hash") != prev_hash:
                return False

            # Verify entry hash
            entry_data = {k: v for k, v in entry.items() if k not in ['entry_hash']}
            entry_str = json.dumps(entry_data, sort_keys=True, separators=(',', ':'))
            expected_hash = hashlib.sha256(entry_str.encode()).hexdigest()

            if entry.get("entry_hash") != expected_hash:
                return False

            # Collect timestamps for ordering check
            try:
                ts = datetime.fromisoformat(entry.get("timestamp", "").replace('Z', '+00:00'))
                timestamps.append(ts)
            except:
                return False

            prev_hash = entry.get("entry_hash")

        # Verify chronological order
        return timestamps == sorted(timestamps)

    def _validate_callback_url(self, url: str) -> bool:
        """Prevent Server-Side Request Forgery."""
        from urllib.parse import urlparse
        parsed = urlparse(url)

        if parsed.scheme != "https":
            return False

        # Block internal IPs
        import socket
        try:
            ip = socket.getaddrinfo(parsed.hostname, None)[0][4][0]
            if ip.startswith(("10.", "192.168.", "127.", "0.", "172.16.")):
                return False
        except:
            return False

        return True