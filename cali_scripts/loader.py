# cali_scripts/loader.py
"""
CaliScriptLoader - Loads and caches all scripted responses.
Provides fast, predictable access to Caleon's personality.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

class CaliScriptLoader:
    """
    Loads all script files into memory for fast access.
    Supports variable substitution and context injection.
    """

    def __init__(self):
        self.base_path = Path(__file__).parent / "scripts"
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.load_all()

    def load_all(self) -> None:
        """Load all JSON script files into memory cache."""
        if not self.base_path.exists():
            raise FileNotFoundError(f"Scripts directory not found: {self.base_path}")

        for script_file in self.base_path.glob("*.json"):
            category = script_file.stem
            try:
                with open(script_file, 'r', encoding='utf-8') as f:
                    self.cache[category] = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to load {script_file}: {e}")
            except Exception as e:
                print(f"Warning: Error loading {script_file}: {e}")

    def get(self, category: str, entry: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """
        Get a scripted response with optional variable substitution.

        Args:
            category: Script category (e.g., 'greetings')
            entry: Specific entry key (e.g., 'welcome_dashboard')
            variables: Dict of variables to substitute (e.g., {'name': 'Bryan'})

        Returns:
            The scripted response with variables substituted
        """
        # Get the category data
        category_data = self.cache.get(category, {})

        # Get the specific entry
        text = category_data.get(entry, f"[Script Missing: {category}.{entry}]")

        # Handle arrays (like personality.json)
        if isinstance(text, list):
            # For arrays, return a random item or first item
            text = text[0] if text else f"[Empty Array: {category}.{entry}]"

        # Variable substitution
        if variables:
            for key, value in variables.items():
                placeholder = "{{{ " + key + " }}}"
                text = text.replace(placeholder, str(value))

        return text

    def reload(self) -> None:
        """Reload all scripts from disk."""
        self.cache.clear()
        self.load_all()

    def get_categories(self) -> list[str]:
        """Get list of available script categories."""
        return list(self.cache.keys())

    def get_entries(self, category: str) -> list[str]:
        """Get list of entries in a category."""
        return list(self.cache.get(category, {}).keys())