# vault_lookup.py

import json
import hashlib
import os
from typing import Any, Dict, Optional

class VaultLookup:
    """
    Provides a unified lookup across:
        - a priori vault
        - a posteriori vault
        - prior verdict logs
    """

    def __init__(self, vault_root: str):
        self.vault_root = vault_root
        self.apriori_path = os.path.join(vault_root, "a_priori_vault.json")
        self.aposteriori_path = os.path.join(vault_root, "a_posteriori_vault.json")
        self.decision_log_path = os.path.join(vault_root, "prior_verdicts.json")

        self._load_vaults()

    def _load_vaults(self):
        self.apriori = self._load_json(self.apriori_path)
        self.aposteriori = self._load_json(self.aposteriori_path)
        self.decision_log = self._load_json(self.decision_log_path)

    def _load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return {}
        with open(path, "r") as f:
            return json.load(f)

    # -----------------------------------------
    # FAST LOOKUP FOR HARMONIZER
    # -----------------------------------------
    def lookup_prior_verdict(self, case_fingerprint: str) -> Optional[Dict[str, Any]]:
        """
        Direct match lookup for a previously resolved case.
        """
        return self.decision_log.get(case_fingerprint)

    def lookup_apriori(self, key: str) -> Optional[Any]:
        """
        Retrieves any apriori rule or prior resolutions.
        """
        return self.apriori.get(key)

    def lookup_aposteriori(self, key: str) -> Optional[Any]:
        """
        Retrieves evidence-based or empirical prior data.
        """
        return self.aposteriori.get(key)

    # -----------------------------------------
    # CASE FINGERPRINT (standardized)
    # -----------------------------------------
    def fingerprint_case(self, case: Dict[str, Any]) -> str:
        canonical = json.dumps(case, sort_keys=True).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()