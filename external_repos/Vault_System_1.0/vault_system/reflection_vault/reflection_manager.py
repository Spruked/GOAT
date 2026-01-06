# reflection_manager.py

import json
import os
from typing import List, Dict, Any
from .reflection_schema import ReflectionEntry


class ReflectionVault:
    """
    Stores Caleon's reflections in an organized, structured way.
    Purpose:
        - Keep her mental space organized
        - Track insights from all modules
        - Allow retrieval for future cycles
        - Prevent mental drift or duplication
    """

    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.vault_file = os.path.join(vault_path, "reflection_vault.json")

        os.makedirs(self.vault_path, exist_ok=True)
        self._load()

    def _load(self):
        if not os.path.exists(self.vault_file):
            self.reflections: List[Dict[str, Any]] = []
            self._save()
        else:
            with open(self.vault_file, "r") as f:
                self.reflections = json.load(f)

    def _save(self):
        with open(self.vault_file, "w") as f:
            json.dump(self.reflections, f, indent=2)

    # -----------------------------------------
    # Add new reflection
    # -----------------------------------------
    def add_reflection(self, entry: ReflectionEntry):
        self.reflections.append(entry.__dict__)
        self._save()

    # -----------------------------------------
    # Retrieve reflections for organization
    # -----------------------------------------
    def get_by_module(self, module_name: str) -> List[Dict[str, Any]]:
        return [r for r in self.reflections if r["module"] == module_name]

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.reflections[-limit:]

    # -----------------------------------------
    # Cleanup / organization features
    # -----------------------------------------
    def purge_old(self, max_entries: int):
        """
        Prevent the vault from growing forever.
        This keeps Caleon's memory tidy.
        """
        if len(self.reflections) > max_entries:
            self.reflections = self.reflections[-max_entries:]
            self._save()

    def summary(self) -> Dict[str, Any]:
        """
        Gives Caleon a quick sense of what she has been learning.
        """
        by_module = {}
        for r in self.reflections:
            by_module.setdefault(r["module"], 0)
            by_module[r["module"]] += 1

        return {
            "total_reflections": len(self.reflections),
            "by_module": by_module
        }