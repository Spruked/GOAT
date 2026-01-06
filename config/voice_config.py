# config/voice_config.py
"""
Voice Synthesis Configuration for GOAT Audiobook System
"""

import os
from pathlib import Path

# Voice Engine Configuration
VOICE_CONFIG = {
    "engine": {
        "name": "GOAT Voice Engine",
        "version": "2.0.0",
        "pom_integration": True,
        "coqui_tts_model": "tts_models/multilingual/multi-dataset/your_tts",
        "sample_rate": 22050,
        "channels": 1,
        "bit_depth": 16
    },

    "directories": {
        "voices": "./voices",
        "profiles": "./voices/profiles",
        "models": "./voices/models",
        "temp": "./voices/temp",
        "vault": "./data/vault",
        "glyphs": "./data/vault/voice_glyphs"
    },

    "voice_profiles": {
        "character_defaults": {
            "gender": {
                "male": {
                    "tension": 0.7,
                    "breathiness": 0.15,
                    "vibrato_rate": 4.0,
                    "pitch_range": (85, 180)
                },
                "female": {
                    "tension": 0.5,
                    "breathiness": 0.25,
                    "vibrato_rate": 4.5,
                    "pitch_range": (165, 255)
                }
            },
            "age_ranges": {
                "child": {"pitch_multiplier": 1.3, "tension": 0.4},
                "young_adult": {"pitch_multiplier": 1.1, "tension": 0.6},
                "adult": {"pitch_multiplier": 1.0, "tension": 0.7},
                "elderly": {"pitch_multiplier": 0.9, "tension": 0.8}
            },
            "personality_modifiers": {
                "aggressive": {"tension": 1.2, "breathiness": 0.8},
                "calm": {"tension": 0.7, "breathiness": 0.3},
                "excitable": {"vibrato_rate": 1.3, "breathiness": 1.2},
                "weary": {"tension": 0.5, "breathiness": 1.4}
            }
        },

        "narrator_defaults": {
            "content_types": {
                "fiction": {
                    "clarity_boost": 0.8,
                    "engagement_boost": 0.9,
                    "prosody_variation": 0.8
                },
                "nonfiction": {
                    "clarity_boost": 1.0,
                    "engagement_boost": 0.6,
                    "prosody_variation": 0.5
                },
                "poetry": {
                    "clarity_boost": 0.9,
                    "engagement_boost": 1.0,
                    "prosody_variation": 1.0
                },
                "technical": {
                    "clarity_boost": 1.2,
                    "engagement_boost": 0.4,
                    "prosody_variation": 0.3
                }
            }
        }
    },

    "pom_modules": {
        "formant_filter": {
            "enabled": True,
            "formant_ranges": {
                "f1": (200, 800),  # Vowel formants
                "f2": (800, 2500),
                "f3": (2500, 3500)
            },
            "bandwidth_defaults": {
                "f1": 80,
                "f2": 120,
                "f3": 160
            }
        },

        "larynx_simulation": {
            "enabled": True,
            "tension_range": (0.3, 0.9),
            "breathiness_range": (0.1, 0.5),
            "vibrato_range": (3.0, 6.0)
        },

        "lip_control": {
            "enabled": True,
            "rounding_range": (0.2, 0.6),
            "articulation_precision_range": (0.6, 1.0)
        },

        "tongue_articulation": {
            "enabled": True,
            "positions": ["alveolar", "retroflex", "dental", "velar"],
            "sharpness_range": (0.4, 0.9)
        },

        "uvula_control": {
            "enabled": False,  # Enable for specific languages/ethnicities
            "nasalization_range": (0.0, 0.3)
        }
    },

    "emotional_profiles": {
        "neutral": {
            "pitch_variation": 0.1,
            "speaking_rate": 1.0,
            "intensity": 0.7,
            "pause_frequency": 0.5
        },
        "angry": {
            "pitch_variation": 0.3,
            "speaking_rate": 1.3,
            "intensity": 0.95,
            "pause_frequency": 0.3
        },
        "weary": {
            "pitch_variation": 0.05,
            "speaking_rate": 0.85,
            "intensity": 0.5,
            "pause_frequency": 0.8
        },
        "excited": {
            "pitch_variation": 0.25,
            "speaking_rate": 1.2,
            "intensity": 0.9,
            "pause_frequency": 0.4
        },
        "calm": {
            "pitch_variation": 0.08,
            "speaking_rate": 0.9,
            "intensity": 0.6,
            "pause_frequency": 0.7
        }
    },

    "audiobook_settings": {
        "chapter_pauses": {
            "between_chapters": 2.0,  # seconds
            "after_title": 1.0,
            "between_segments": 0.5
        },

        "export_formats": {
            "wav": {
                "sample_rate": 22050,
                "bit_depth": 16,
                "channels": 1
            },
            "mp3": {
                "bitrate": 128,
                "quality": "high"
            },
            "m4b": {
                "bitrate": 128,
                "chapters": True,
                "metadata": True
            }
        },

        "quality_presets": {
            "draft": {
                "sample_rate": 16000,
                "model_size": "small",
                "pom_enabled": False
            },
            "standard": {
                "sample_rate": 22050,
                "model_size": "medium",
                "pom_enabled": True
            },
            "professional": {
                "sample_rate": 44100,
                "model_size": "large",
                "pom_enabled": True,
                "post_processing": True
            }
        }
    },

    "character_voice_matching": {
        "similarity_threshold": 0.8,
        "reuse_existing_profiles": True,
        "auto_generate_missing": True,

        "voice_characteristics_map": {
            "age": {
                "child": ["high_pitch", "fast_pace", "clear_articulation"],
                "teen": ["variable_pitch", "moderate_pace", "casual_articulation"],
                "adult": ["stable_pitch", "normal_pace", "precise_articulation"],
                "elderly": ["lower_pitch", "slower_pace", "deliberate_articulation"]
            },
            "personality": {
                "confident": ["strong_projection", "steady_rhythm"],
                "shy": ["soft_volume", "hesitant_pauses"],
                "aggressive": ["loud_volume", "fast_pace", "sharp_articulation"],
                "calm": ["moderate_volume", "slow_pace", "smooth_rhythm"]
            }
        }
    },

    "narrator_optimization": {
        "content_analysis": {
            "complexity_thresholds": {
                "simple": 0.3,
                "moderate": 0.6,
                "complex": 0.8
            },
            "technical_term_boost": 0.1,
            "sentence_length_penalty": 0.05
        },

        "pacing_rules": {
            "max_speed": 1.5,
            "min_speed": 0.5,
            "default_speed": 1.0,
            "complexity_speed_reduction": 0.2
        },

        "clarity_enhancements": {
            "articulation_boost_max": 1.5,
            "pause_insertion_threshold": 0.7,
            "emphasis_detection": True
        }
    },

    "performance_settings": {
        "max_concurrent_synthesis": 3,
        "cache_enabled": True,
        "cache_ttl_hours": 24,
        "temp_file_cleanup": True,
        "memory_limit_mb": 2048
    },

    "fallback_settings": {
        "mock_pom_enabled": True,
        "basic_tts_fallback": True,
        "error_handling": {
            "max_retries": 3,
            "retry_delay_seconds": 1,
            "graceful_degradation": True
        }
    }
}

# Environment-specific overrides
def get_config():
    """Get configuration with environment overrides"""
    config = VOICE_CONFIG.copy()

    # Override from environment variables
    if os.getenv("VOICE_SAMPLE_RATE"):
        config["engine"]["sample_rate"] = int(os.getenv("VOICE_SAMPLE_RATE"))

    if os.getenv("VOICE_POM_ENABLED", "").lower() == "false":
        config["engine"]["pom_integration"] = False

    if os.getenv("VOICE_QUALITY_PRESET"):
        preset = os.getenv("VOICE_QUALITY_PRESET")
        if preset in config["audiobook_settings"]["quality_presets"]:
            config["current_quality_preset"] = preset

    return config

# Export configuration
voice_config = get_config()