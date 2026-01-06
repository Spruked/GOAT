# audiobook_engine/config.py
"""
GOAT Audiobook Engine Configuration
Voice profiles, default settings, and system paths
"""

import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass

# Base paths
AUDIOBOOK_BASE_PATH = Path(os.getenv("AUDIOBOOK_BASE_PATH", "./deliverables/audiobooks"))
TEMP_AUDIO_PATH = Path(os.getenv("TEMP_AUDIO_PATH", "./temp/audio"))
VAULT_AUDIO_PATH = Path(os.getenv("VAULT_AUDIO_PATH", "./data/vault/audio"))

# Ensure directories exist
AUDIOBOOK_BASE_PATH.mkdir(parents=True, exist_ok=True)
TEMP_AUDIO_PATH.mkdir(parents=True, exist_ok=True)
VAULT_AUDIO_PATH.mkdir(parents=True, exist_ok=True)

@dataclass
class VoiceProfile:
    """Voice profile configuration"""
    name: str
    provider: str  # "coqui", "xtts", "azure", "elevenlabs"
    voice_id: str
    language: str = "en"
    gender: str = "neutral"
    age: str = "adult"
    style: str = "narrative"
    speed: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0
    sample_rate: int = 22050
    emotion: str = "neutral"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "provider": self.provider,
            "voice_id": self.voice_id,
            "language": self.language,
            "gender": self.gender,
            "age": self.age,
            "style": self.style,
            "speed": self.speed,
            "pitch": self.pitch,
            "volume": self.volume,
            "sample_rate": self.sample_rate,
            "emotion": self.emotion
        }

# Default voice profiles
DEFAULT_VOICES = {
    "narrative_male": VoiceProfile(
        name="Professional Male Narrator",
        provider="coqui",
        voice_id="tts_models/en/ljspeech/tacotron2-DDC_ph",
        language="en",
        gender="male",
        age="adult",
        style="narrative",
        speed=0.9,
        emotion="neutral"
    ),

    "narrative_female": VoiceProfile(
        name="Professional Female Narrator",
        provider="coqui",
        voice_id="tts_models/en/ljspeech/tacotron2-DDC_ph",
        language="en",
        gender="female",
        age="adult",
        style="narrative",
        speed=0.95,
        emotion="neutral"
    ),

    "conversational_male": VoiceProfile(
        name="Conversational Male",
        provider="coqui",
        voice_id="tts_models/en/ljspeech/tacotron2-DDC_ph",
        language="en",
        gender="male",
        age="adult",
        style="conversational",
        speed=1.0,
        emotion="friendly"
    ),

    "conversational_female": VoiceProfile(
        name="Conversational Female",
        provider="coqui",
        voice_id="tts_models/en/ljspeech/tacotron2-DDC_ph",
        language="en",
        gender="female",
        age="adult",
        style="conversational",
        speed=1.05,
        emotion="friendly"
    ),

    "dramatic_male": VoiceProfile(
        name="Dramatic Male",
        provider="coqui",
        voice_id="tts_models/en/ljspeech/tacotron2-DDC_ph",
        language="en",
        gender="male",
        age="adult",
        style="dramatic",
        speed=0.85,
        pitch=0.1,
        emotion="intense"
    )
}

# Audio processing settings
AUDIO_CONFIG = {
    "sample_rate": 22050,
    "channels": 1,  # mono for audiobooks
    "bit_depth": 16,
    "format": "wav",  # intermediate format
    "final_format": "m4b",  # final output format

    # Normalization settings (EBU R128)
    "target_loudness": -16.0,  # LUFS
    "loudness_range": 11.0,    # LU
    "true_peak": -1.0,         # dBTP

    # Silence trimming
    "silence_threshold": -40.0,  # dBFS
    "min_silence_duration": 0.5,  # seconds

    # Chapter markers
    "chapter_marker_silence": 2.0,  # seconds between chapters
    "chapter_marker_tone": False,   # add subtle tone between chapters

    # Quality settings
    "compression_quality": "high",  # low, medium, high
    "noise_reduction": True,
    "de_essing": True,
    "dynamic_range_compression": False
}

# Worker settings
WORKER_CONFIG = {
    "max_concurrent_jobs": int(os.getenv("AUDIOBOOK_MAX_JOBS", "3")),
    "job_timeout_seconds": int(os.getenv("AUDIOBOOK_JOB_TIMEOUT", "3600")),  # 1 hour
    "retry_attempts": 3,
    "retry_delay_seconds": 60,

    # Queue settings
    "queue_name": "audiobook_generation",
    "priority_levels": ["low", "normal", "high", "urgent"],

    # Resource limits
    "max_memory_gb": 8.0,
    "max_cpu_percent": 80.0
}

# TTS Engine settings
TTS_CONFIG = {
    "coqui": {
        "model_cache_dir": "./models/tts",
        "use_cuda": os.getenv("USE_CUDA", "false").lower() == "true",
        "use_gpu": os.getenv("USE_GPU", "false").lower() == "true",
        "gpu_device": int(os.getenv("GPU_DEVICE", "0")),
        "batch_size": 1,  # single sentence for quality
        "length_scale": 1.0,
        "noise_scale": 0.667,
        "noise_w": 0.8
    },

    "xtts": {
        "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
        "model_cache_dir": "./models/xtts",
        "use_cuda": os.getenv("USE_CUDA", "false").lower() == "true",
        "temperature": 0.85,
        "length_penalty": 1.0,
        "repetition_penalty": 2.0,
        "top_k": 50,
        "top_p": 0.85,
        "speed": 1.0
    }
}

# SSML processing settings
SSML_CONFIG = {
    "default_language": "en-US",
    "default_voice": "narrative_male",
    "prosody_defaults": {
        "rate": "medium",
        "pitch": "medium",
        "volume": "medium"
    },

    # Dialogue detection patterns
    "dialogue_markers": [
        '"', "'", "''", """, """,
        "said", "asked", "replied", "whispered", "shouted",
        ":", "—", "–"
    ],

    # Emphasis patterns
    "emphasis_words": [
        "important", "crucial", "vital", "essential", "key",
        "amazing", "incredible", "extraordinary", "remarkable",
        "dramatic", "intense", "powerful", "significant"
    ],

    # Pause insertion
    "sentence_pause_ms": 300,
    "paragraph_pause_ms": 800,
    "chapter_pause_ms": 2000
}

# Export and manifest settings
EXPORT_CONFIG = {
    "manifest_version": "goat-audiobook-v1",
    "checksum_algorithm": "sha256",
    "compression_format": "aac",  # for M4B
    "bitrate_kbps": 128,

    # Metadata tags
    "id3_version": 4,
    "include_cover_art": True,
    "include_chapter_marks": True,

    # Vault integration
    "auto_commit_to_vault": True,
    "vault_retention_days": 365 * 10,  # 10 years

    # CDN settings (if using external storage)
    "use_cdn": False,
    "cdn_base_url": "",
    "signed_url_expiry_hours": 24
}

def get_voice_profile(profile_name: str) -> VoiceProfile:
    """Get a voice profile by name"""
    return DEFAULT_VOICES.get(profile_name, DEFAULT_VOICES["narrative_male"])

def get_all_voice_profiles() -> Dict[str, Dict[str, Any]]:
    """Get all available voice profiles as dict"""
    return {name: profile.to_dict() for name, profile in DEFAULT_VOICES.items()}

def validate_config():
    """Validate configuration settings"""
    # Check required directories
    required_dirs = [AUDIOBOOK_BASE_PATH, TEMP_AUDIO_PATH, VAULT_AUDIO_PATH]
    for dir_path in required_dirs:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    # Validate voice profiles
    for name, profile in DEFAULT_VOICES.items():
        if not profile.voice_id:
            raise ValueError(f"Voice profile {name} missing voice_id")

    # Validate audio settings
    if AUDIO_CONFIG["sample_rate"] not in [16000, 22050, 44100, 48000]:
        raise ValueError("Invalid sample rate")

    print("✅ Audiobook Engine configuration validated")

# API Configuration
API_CONFIG = {
    'host': os.getenv('API_HOST', '0.0.0.0'),
    'port': int(os.getenv('API_PORT', '8000')),
    'debug': os.getenv('API_DEBUG', 'false').lower() == 'true',
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    'cors_origins': os.getenv('CORS_ORIGINS', '*').split(',') if os.getenv('CORS_ORIGINS') else ['*'],
    'workers': int(os.getenv('API_WORKERS', '2')),
    'timeout': int(os.getenv('API_TIMEOUT', '300')),
}

# Export Manager Configuration
EXPORT_CONFIG = {
    'format': os.getenv('EXPORT_FORMAT', 'm4b'),
    'include_chapters': os.getenv('INCLUDE_CHAPTERS', 'true').lower() == 'true',
    'output_dir': os.getenv('EXPORT_OUTPUT_DIR', './exports'),
}

# Worker Configuration
WORKER_CONFIG = {
    'audio_workers': int(os.getenv('AUDIO_WORKERS', '2')),
    'project_workers': int(os.getenv('PROJECT_WORKERS', '1')),
    'queue_timeout': int(os.getenv('QUEUE_TIMEOUT', '3600')),
    'retry_attempts': int(os.getenv('RETRY_ATTEMPTS', '3')),
    'retry_delay': int(os.getenv('RETRY_DELAY', '5')),
}

# Initialize on import
validate_config()