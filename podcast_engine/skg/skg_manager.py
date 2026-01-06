import json
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class SpeakerKnowledgeGraph:
    def __init__(self, skg_path: str = "skg/skg_core.json"):
        self.skg_path = Path(__file__).parent / skg_path
        self.data = self._load_skg()
        self._initialize_voices()

    def _load_skg(self):
        if self.skg_path.exists():
            with open(self.skg_path, 'r') as f:
                return json.load(f)
        return self._create_default_skg()

    def _create_default_skg(self):
        """Create minimal SKG if file doesn't exist"""
        default_skg = {
            "show_metadata": {
                "show_name": "The Phil and Jim Dandy Show",
                "episode_format": "interview_discussion",
                "target_duration_seconds": 1800
            },
            "personas": {},
            "standby_personas": {},
            "episode_state": {
                "current_topic": None,
                "active_personas": [],
                "conversation_history": []
            }
        }
        with open(self.skg_path, 'w') as f:
            json.dump(default_skg, f, indent=2)
        return default_skg

    def _initialize_voices(self):
        """Pre-cache all cloned voices using Coqui's caching"""
        try:
            # Import here to avoid circular imports
            sys.path.append(str(Path(__file__).parent.parent.parent / "Phonatory_Output_Module"))
            from phonitory_output_module import PhonatoryOutputModule
            self.emitter = PhonatoryOutputModule()

            for persona_id, persona in self.data["personas"].items():
                if persona["voice_profile"]["type"] == "cloned":
                    speaker_id = persona["voice_profile"]["speaker_id"]
                    reference_wavs = persona["voice_profile"]["reference_wavs"]

                    # Check if reference files exist
                    existing_refs = [wav for wav in reference_wavs if Path(wav).exists()]
                    if existing_refs:
                        # Clone and cache (Coqui stores in ~/.local/share/tts/voices/)
                        self.emitter.clone_voice(
                            speaker_wav=existing_refs,
                            speaker=speaker_id
                        )
                        print(f"✅ Voice cached: {persona_id} as {speaker_id}")
                    else:
                        print(f"⚠️  Reference audio not found for {persona_id}, using preset fallback")
        except ImportError:
            print("⚠️  Phonatory Output Module not available, voice caching skipped")
            self.emitter = None

    def synthesize_as_persona(self, text: str, persona_id: str, performance_directives: Dict = None) -> str:
        """Generate speech with persona-specific voice modifications and performance directives"""
        if not self.emitter:
            raise RuntimeError("Phonatory Output Module not initialized")

        persona = self._get_persona(persona_id)
        voice_profile = persona["voice_profile"]

        # Apply performance directives to modify voice parameters
        pitch_shift = voice_profile.get("base_pitch", 1.0)
        speed = voice_profile.get("speaking_rate", 1.0)

        if performance_directives:
            # Apply emotional pitch adjustments
            if "base_pitch" in performance_directives:
                pitch_shift *= performance_directives["base_pitch"]

            # Apply speaking rate adjustments
            if "speaking_rate" in performance_directives:
                speed *= performance_directives["speaking_rate"]

            # Apply stress markers to text
            if "stress_words" in performance_directives:
                text = self._inject_stress_markers(text, performance_directives["stress_words"])

            # Add emotional prompts
            if "emotion" in performance_directives:
                emotion = performance_directives["emotion"]
                emotion_prompts = {
                    "terrified": "[terrified voice] ",
                    "affectionate": "[warm, affectionate tone] ",
                    "horrified": "[horrified] ",
                    "excited": "[excited] ",
                    "sad": "[sad tone] "
                }
                if emotion in emotion_prompts:
                    text = emotion_prompts[emotion] + text

        # Create output directory
        output_dir = Path(__file__).parent / "output" / "segments"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{persona_id}_{abs(hash(text))}.wav"

        # Use cached voice if cloned, otherwise use preset
        self.emitter.phonate(
            text=text,
            speaker=voice_profile["speaker_id"],
            language="en",
            pitch_shift=pitch_shift,
            speed=speed,
            output_path=str(output_path)
        )

        return str(output_path)

    def _inject_stress_markers(self, text: str, stress_words: List[Tuple[str, float]]) -> str:
        """Add emphasis markers for Coqui to stress"""
        modified_text = text

        for word, level in stress_words:
            if level > 0.8:
                # High stress: add emphasis markers
                modified_text = modified_text.replace(word, f"[{word.upper()}]")
            elif level > 0.6:
                # Medium stress: add emphasis marker
                modified_text = modified_text.replace(word, f"*{word}*")

        return modified_text

    def activate_standby_persona(self, topic_keywords: List[str]) -> Optional[str]:
        """Intelligently activate standby persona based on topic keywords"""
        topic_text = " ".join(topic_keywords).lower()

        for persona_id, persona in self.data["standby_personas"].items():
            activation_keywords = persona["persona_traits"].get("activation_keywords", [])

            if any(keyword.lower() in topic_text for keyword in activation_keywords):
                if persona_id not in self.data["episode_state"]["active_personas"]:
                    self.data["episode_state"]["active_personas"].append(persona_id)
                    self._save_skg()
                    print(f"🎭 Activated guest persona: {persona['name']}")
                    return persona_id
        return None

    def get_persona(self, persona_id: str) -> Optional[Dict]:
        """Get persona data by ID from any registry"""
        if persona_id in self.data["personas"]:
            return self.data["personas"][persona_id]
        elif persona_id in self.data["standby_personas"]:
            return self.data["standby_personas"][persona_id]
        elif persona_id in self.data.get("narrator_pool", {}):
            return self.data["narrator_pool"][persona_id]
        elif persona_id in self.data.get("character_voice_registry", {}):
            return self.data["character_voice_registry"][persona_id]
        return None

    def synthesize_as_character(self, text: str, character_id: str, base_narrator_id: str, emotion: str = None) -> str:
        """Generate character voice based on narrator + modifications"""
        character = self.data.get("character_voice_registry", {}).get(character_id)
        if not character:
            raise ValueError(f"Character {character_id} not found")

        base_persona = self.get_persona(character["base_persona"])
        if not base_persona:
            raise ValueError(f"Base persona {character['base_persona']} not found")

        # Start with base modifications
        mods = character["voice_modifications"].copy()

        # Apply emotional variants if specified
        if emotion and "emotional_variants" in character:
            emotion_mods = character["emotional_variants"].get(emotion, {})
            for key, value in emotion_mods.items():
                if key in mods:
                    mods[key] += value  # Additive modification
                else:
                    mods[key] = value

        # Create output directory
        output_dir = Path(__file__).parent / "output" / "segments"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"char_{character_id}_{emotion or 'neutral'}_{abs(hash(text))}.wav"

        # Use emitter if available
        if self.emitter:
            self.emitter.phonate(
                text=text,
                speaker=base_persona["voice_profile"]["speaker_id"],
                pitch_shift=mods.get("pitch_shift", 0),
                speed=mods.get("speaking_rate", 1.0),
                output_path=str(output_path)
            )

            # Add post-processing effects
            if "reverb" in mods:
                self._apply_reverb(str(output_path), mods["reverb"])
        else:
            # Create silent placeholder if no emitter
            try:
                from pydub import AudioSegment
                placeholder = AudioSegment.silent(duration=1000)  # 1 second
                placeholder.export(str(output_path), format="wav")
            except ImportError:
                raise RuntimeError("Neither Phonatory Output Module nor pydub available")

        return str(output_path)

    def set_mode(self, persona_id: str, mode: str):
        """Switch persona between podcast/audiobook modes"""
        persona = self.get_persona(persona_id)
        if not persona:
            raise ValueError(f"Persona {persona_id} not found")

        if "mode_specific_traits" in persona and mode in persona["mode_specific_traits"]:
            persona["active_traits"] = persona["mode_specific_traits"][mode]
            print(f"🎬 {persona_id} switched to {mode} mode")
            self._save_skg()
        else:
            print(f"⚠️  Mode {mode} not available for {persona_id}")

    def concatenate_audio_segments(self, paths: List[str], crossfade: int = 150) -> str:
        """Join segments with smooth crossfades"""
        try:
            from pydub import AudioSegment
        except ImportError:
            raise RuntimeError("pydub required for audio concatenation")

        if not paths:
            return ""

        # Filter out empty paths
        valid_paths = [p for p in paths if p and Path(p).exists()]

        if not valid_paths:
            raise ValueError("No valid audio paths to concatenate")

        # Load first segment
        combined = AudioSegment.from_wav(valid_paths[0])

        # Add remaining segments with crossfade
        for path in valid_paths[1:]:
            segment = AudioSegment.from_wav(path)
            combined = combined.append(segment, crossfade=crossfade)

        # Create output path
        output_dir = Path(__file__).parent / "output" / "temp"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"combined_{abs(hash(''.join(valid_paths)))}.wav"
        combined.export(str(output_path), format="wav")

        return str(output_path)

    def _apply_reverb(self, audio_path: str, reverb_config: Dict):
        """Apply reverb effect to audio file"""
        try:
            from pydub import AudioSegment
            from pydub.effects import reverb

            audio = AudioSegment.from_wav(audio_path)

            # Apply reverb effect
            reverbed = reverb(
                audio,
                room_size=reverb_config.get("room_size", 0.5),
                wet_level=reverb_config.get("wet_level", 0.3)
            )

            # Overwrite original file
            reverbed.export(audio_path, format="wav")

        except ImportError:
            print("⚠️  pydub effects not available for reverb")
        except Exception as e:
            print(f"⚠️  Reverb application failed: {e}")

    def _get_persona(self, persona_id: str) -> Dict:
        """Internal method to get persona, raises error if not found"""
        persona = self.get_persona(persona_id)
        if not persona:
            raise ValueError(f"Persona {persona_id} not found")
        return persona

    def _save_skg(self):
        """Save current SKG state"""
        with open(self.skg_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def update_episode_state(self, topic: str, active_personas: List[str]):
        """Update current episode state"""
        self.data["episode_state"]["current_topic"] = topic
        self.data["episode_state"]["active_personas"] = active_personas
        self._save_skg()