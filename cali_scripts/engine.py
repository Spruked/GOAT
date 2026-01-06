# cali_scripts/engine.py
"""
CaliScripts Engine - Simple interface to Caleon's scripted responses.
Provides consistent personality across the entire GOAT platform.
"""

from .loader import CaliScriptLoader

class CaliScripts:
    """
    Main interface for Caleon's scripted response system.
    Use CaliScripts.say() for all platform responses.
    """

    _loader = CaliScriptLoader()

    @staticmethod
    def say(category: str, entry: str, **variables) -> str:
        """
        Get a scripted response from Caleon.

        Args:
            category: Script category (e.g., 'greetings')
            entry: Specific entry key (e.g., 'welcome_dashboard')
            **variables: Keyword arguments for variable substitution

        Returns:
            Caleon's scripted response

        Example:
            CaliScripts.say("greetings", "welcome_dashboard", name="Bryan")
            # Returns: "Welcome back, Bryan. Let's build something worth remembering."
        """
        return CaliScripts._loader.get(category, entry, variables=variables if variables else None)

    @staticmethod
    def reload() -> None:
        """Reload all scripts from disk (useful for development)."""
        CaliScripts._loader.reload()

    @staticmethod
    def get_categories() -> list[str]:
        """Get list of available script categories."""
        return CaliScripts._loader.get_categories()

    @staticmethod
    def get_entries(category: str) -> list[str]:
        """Get list of entries in a category."""
        return CaliScripts._loader.get_entries(category)

    # Convenience methods for common categories
    @staticmethod
    def greet(entry: str, **variables) -> str:
        """Greeting responses."""
        return CaliScripts.say("greetings", entry, **variables)

    @staticmethod
    def onboard(entry: str, **variables) -> str:
        """Onboarding responses."""
        return CaliScripts.say("onboarding", entry, **variables)

    @staticmethod
    def navigate(entry: str, **variables) -> str:
        """Navigation responses."""
        return CaliScripts.say("navigation", entry, **variables)

    @staticmethod
    def error(entry: str, **variables) -> str:
        """Error responses."""
        return CaliScripts.say("errors", entry, **variables)

    @staticmethod
    def confirm(entry: str, **variables) -> str:
        """Confirmation responses."""
        return CaliScripts.say("confirmations", entry, **variables)

    @staticmethod
    def draft(entry: str, **variables) -> str:
        """Draft engine responses."""
        return CaliScripts.say("drafts", entry, **variables)