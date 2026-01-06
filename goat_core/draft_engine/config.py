import os
from pathlib import Path

class Config:
    """Configuration for ScribeCore v3 - Caleon-Native Edition"""

    # Base paths
    BASE_DIR = Path(__file__).parent
    OUTPUT_DIR = BASE_DIR / "output"
    LOGS_DIR = BASE_DIR / "logs"

    # ═══════════════════════════════════════
    # CALEON PRIME INTEGRATION
    # ═══════════════════════════════════════
    CALEON_UCM_ENDPOINT = os.getenv("CALEON_UCM_ENDPOINT", "http://localhost:8000/v1/caleon/invoke")
    CALEON_AUTH_TOKEN   = os.getenv("CALEON_AUTH_TOKEN", "founder-legacy-key-2025")

    # Content generation settings
    DEFAULT_WORD_COUNT_TARGET = "800-1800"
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 180

    # Quality thresholds
    MIN_QUALITY_SCORE = 7.0
    TARGET_QUALITY_SCORE = 8.5

    # File paths
    VOICE_PROFILE_PATH = BASE_DIR / "goat_voice_profile.yaml"
    CONTINUITY_STORE_PATH = BASE_DIR / "continuity_store.json"

    # Logging
    LOG_LEVEL = os.getenv("SCRIBE_LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"