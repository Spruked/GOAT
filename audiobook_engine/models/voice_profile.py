from typing import Optional

class VoiceProfile:
    def __init__(
        self,
        profile_id: str,
        name: str,
        speed: float = 1.0,
        pitch: float = 1.0,
        emotion: str = "neutral",
        model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2",
        model_path: Optional[str] = None,
        config_path: Optional[str] = None,
        speaker_name: Optional[str] = None,
        language: str = "en",
        speed_multiplier: float = 1.0,
        warmup_text: str = "Hello, this is a test.",
    ):
        self.profile_id = profile_id
        self.name = name
        self.speed = speed
        self.pitch = pitch
        self.emotion = emotion
        self.model_name = model_name
        self.model_path = model_path
        self.config_path = config_path
        self.speaker_name = speaker_name
        self.language = language
        self.speed_multiplier = speed_multiplier
        self.warmup_text = warmup_text

    @property
    def cache_key(self) -> str:
        """Cache key for TTS instance."""
        return f"{self.model_name}_{self.speaker_name or 'default'}_{self.language}"

    @property
    def voice_id(self) -> str:
        """Alias for profile_id."""
        return self.profile_id