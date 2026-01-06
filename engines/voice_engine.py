# engines/voice_engine.py
"""
GOAT Voice Engine: Integrates POM 2.0 for professional audiobook creation
"""

import os
import json
import uuid
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import hashlib
import io
import numpy as np
import soundfile as sf
from functools import wraps

# CPU Sequential Lock Decorator
def cpu_sequential_lock(func):
    """Decorator to prevent concurrent execution on CPU"""
    lock = asyncio.Lock()

    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with lock:
            print(f"🔒 Sequential Lock: {func.__name__}")
            return await func(*args, **kwargs)

    return wrapper

# Real POM and Coqui TTS imports from local directories
try:
    import sys
    from pathlib import Path

    # Add Phonatory_Output_Module to path
    pom_path = Path(__file__).parent.parent / "Phonatory_Output_Module"
    sys.path.insert(0, str(pom_path))

    # Import POM modules
    from phonitory_output_module import PhonatoryOutputModule
    from larynx_sim import LarynxSimulator
    from formant_filter import FormantFilter
    from tongue_artic import TongueArticulator
    from lip_control import LipController
    from uvula_control import UvulaController

    # Import Coqui TTS from local directory
    coqui_path = pom_path / "Coqui_TTS"
    sys.path.insert(0, str(coqui_path))
    from TTS.api import TTS

    POM_AVAILABLE = True
    print("✅ Real POM 2.0 Phonatory Output Module loaded successfully")
    print("✅ Coqui TTS loaded from local directory")

except ImportError as e:
    print(f"⚠️  POM/Coqui TTS not available - {e}")
    # Fallback for development
    class PhonatoryOutputModule:
        def phonate(self, text, out_path=None, **kwargs):
            # Mock implementation
            if out_path:
                # Create a dummy WAV file
                import wave
                import struct
                with wave.open(out_path, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(22050)
                    # Generate 1 second of silence
                    for _ in range(22050):
                        wav_file.writeframes(struct.pack('<h', 0))
            return out_path or "mock_output.wav"

    class LarynxSimulator:
        pass

    class FormantFilter:
        pass

    class TongueArticulator:
        pass

    class LipController:
        pass

    class UvulaController:
        pass

    class TTS:
        def tts_to_file(self, text, file_path):
            # Create dummy file
            import wave
            import struct
            with wave.open(file_path, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(22050)
                for _ in range(22050):
                    wav_file.writeframes(struct.pack('<h', 0))

    POM_AVAILABLE = False

def debug_audio_pipeline(audio_data, stage_name, voice_profile_id):
    """
    Debug audio at each stage to identify corruption point
    """
    print(f"\n=== DEBUG: {stage_name} ===")
    print(f"Voice Profile: {voice_profile_id}")
    print(f"Shape: {audio_data.shape if hasattr(audio_data, 'shape') else 'N/A'}")
    print(f"Type: {type(audio_data)}")
    print(f"Min/Max: {np.min(audio_data) if isinstance(audio_data, np.ndarray) else 'N/A'} / {np.max(audio_data) if isinstance(audio_data, np.ndarray) else 'N/A'}")
    print(f"Mean: {np.mean(audio_data) if isinstance(audio_data, np.ndarray) else 'N/A'}")
    print(f"Contains NaN: {np.any(np.isnan(audio_data)) if isinstance(audio_data, np.ndarray) else 'N/A'}")

    # Check for clipping
    if isinstance(audio_data, np.ndarray):
        clipping = np.sum(np.abs(audio_data) > 0.95) / len(audio_data) * 100
        print(f"Clipping: {clipping:.2f}%")

    # Save debug audio
    debug_path = f"./temp/debug_{stage_name}_{voice_profile_id}.wav"
    if isinstance(audio_data, np.ndarray):
        sf.write(debug_path, audio_data, 22050)
        print(f"Saved debug audio to: {debug_path}")

    return audio_data

class VoiceVault:
    """Secure storage for voice profiles with glyph integration"""

    def __init__(self, vault_path: str = "./data/vault"):
        self.vault_path = Path(vault_path)
        self.voices_path = Path("./voices/profiles")
        self.voices_path.mkdir(exist_ok=True)

    async def secure_voice_profile(self, voice_profile: Dict) -> str:
        """Store voice profile and create vault glyph for provenance"""
        profile_id = voice_profile["profile_id"]

        # Save profile JSON
        profile_path = self.voices_path / f"{profile_id}.json"
        with open(profile_path, 'w') as f:
            json.dump(voice_profile, f, indent=2)

        # Create glyph hash for provenance
        glyph_data = json.dumps(voice_profile, sort_keys=True)
        glyph_id = hashlib.sha256(glyph_data.encode()).hexdigest()[:16]

        # Store glyph reference
        glyph_ref = {
            "glyph_id": f"voice_glyph_{glyph_id}",
            "profile_id": profile_id,
            "created_at": datetime.utcnow().isoformat(),
            "data_hash": hashlib.sha256(glyph_data.encode()).hexdigest()
        }

        glyph_path = self.vault_path / "voice_glyphs" / f"{glyph_id}.json"
        glyph_path.parent.mkdir(exist_ok=True)
        with open(glyph_path, 'w') as f:
            json.dump(glyph_ref, f, indent=2)

        return glyph_ref["glyph_id"]

class CPUMemoryManager:
    """Track and limit memory usage on CPU"""

    def __init__(self, max_memory_gb=24):  # Leave 8GB for OS/other processes
        self.max_memory_bytes = max_memory_gb * 1024**3
        self.current_usage = 0

    def check_memory(self):
        """Check if we have enough memory to load another model"""
        try:
            import psutil
            available = psutil.virtual_memory().available
            return available > 4 * 1024**3  # Need 4GB free
        except ImportError:
            # Fallback if psutil not available
            return True

    def estimate_model_size(self, model_type):
        """Estimate model memory footprint"""
        sizes = {
            "coqui_yourtts": 2.5 * 1024**3,
            "hifigan": 1.2 * 1024**3,
            "voice_profile": 0.5 * 1024**3
        }
        return sizes.get(model_type, 1 * 1024**3)

class VoiceEngine:
    """
    GOAT Voice Engine: Integrates POM 2.0 for professional audiobook creation
    """

    def __init__(self, cpu_mode=True):
        # CRITICAL: Force consistent sample rate
        self.SAMPLE_RATE = 22050  # Coqui TTS default - DO NOT CHANGE

        # CPU mode optimizations
        self.cpu_mode = cpu_mode
        self.memory_manager = CPUMemoryManager()

        # FOR CPU: Reduce model cache to prevent memory overflow
        self.model_cache = {}  # Only cache current model
        self.active_model = None
        self.CPU_TIMEOUT = 300  # 5 minutes vs 30 seconds for GPU

        # Initialize POM with correct config path
        pom_config_path = Path(__file__).parent.parent / "Phonatory_Output_Module" / "voice_config.json"
        self.pom = PhonatoryOutputModule(config_path=str(pom_config_path))
        self.vault = VoiceVault()

        # Initialize Coqui TTS - always try to load it
        try:
            from TTS.api import TTS as CoquiTTS
            self.coqui_tts = CoquiTTS(
                model_name="tts_models/multilingual/multi-dataset/your_tts",
                progress_bar=False,
                gpu=False  # Force CPU mode
            )
            # FORCE sample rate consistency
            self.coqui_tts.synthesizer.output_sample_rate = self.SAMPLE_RATE
            print("✅ Coqui TTS loaded successfully")
            print(f"✅ Sample rate locked to: {self.SAMPLE_RATE} Hz")
            print(f"✅ CPU mode: {self.cpu_mode}")
        except Exception as e:
            print(f"❌ Coqui TTS initialization failed: {e}")
            self.coqui_tts = None

        # Initialize POM if available
        if POM_AVAILABLE:
            try:
                pom_config_path = Path(__file__).parent.parent / "Phonatory_Output_Module" / "voice_config.json"
                self.pom = PhonatoryOutputModule(config_path=str(pom_config_path))
                print("✅ POM 2.0 Phonatory Output Module loaded successfully")
            except Exception as e:
                print(f"❌ POM initialization failed: {e}")
                self.pom = None
        else:
            print("⚠️  POM 2.0 not available - using basic TTS only")
            self.pom = None

    async def create_voice_profile(
        self,
        creation_method: str,  # "sample" or "parameter"
        name: str,
        description: str,
        voice_type: str,  # "character" or "narrator"
        sample_path: Optional[str] = None,
        param_config: Optional[Dict] = None
    ) -> Dict:
        """
        Create a voice profile using either sample cloning or parameter synthesis
        """
        profile_id = f"vp_{voice_type}_{hash(name) % 10000:04d}"

        if creation_method == "sample":
            # Path 1: Clone from audio sample
            speaker_embedding = await self._extract_speaker_embedding(sample_path)
            pom_config = self._map_sample_to_pom_params(sample_path)

        elif creation_method == "parameter":
            # Path 2: Create from descriptive parameters
            # For YourTTS, use speaker names instead of embeddings
            if "your_tts" in self.coqui_tts.model_name.lower():
                # YourTTS uses speaker names, not embeddings
                speaker_name = self._map_params_to_yourtts_speaker(param_config)
                speaker_embedding = None  # YourTTS doesn't use embeddings
                print(f"Using YourTTS speaker: {speaker_name}")
            else:
                # For other models, generate speaker embedding
                speaker_embedding = self._generate_default_speaker_embedding(param_config)
            
            pom_config = self._build_pom_from_description(param_config)

        # Store voice profile
        voice_profile = {
            "profile_id": profile_id,
            "name": name,
            "description": description,
            "voice_type": voice_type,
            "creation_method": creation_method,
            "coqui_model": {
                "speaker_embedding": speaker_embedding.tolist() if speaker_embedding is not None else None,
                "speaker_name": speaker_name if "your_tts" in self.coqui_tts.model_name.lower() and creation_method == "parameter" else None,
                "model_name": "tts_models/multilingual/multi-dataset/your_tts"
            },
            "pom_config": pom_config,
            "emotional_ranges": self._initialize_emotion_profiles(pom_config),
            "metadata": {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "created_by": "voice_engine",
                "usage_count": 0,
                "average_quality_score": 0.0
            }
        }

        # Save to vault with provenance
        glyph_id = await self.vault.secure_voice_profile(voice_profile)

        return {
            "profile_id": profile_id,
            "glyph_id": glyph_id,
            "status": "created",
            "pom_available": POM_AVAILABLE
        }

    async def load_voice_profile(self, profile_id: str) -> Dict:
        """Load a voice profile from storage"""
        profile_path = self.vault.voices_path / f"{profile_id}.json"
        if not profile_path.exists():
            raise FileNotFoundError(f"Voice profile {profile_id} not found")
        
        with open(profile_path, 'r') as f:
            return json.load(f)

    @cpu_sequential_lock
    async def synthesize_with_character_voice(
        self,
        text: str,
        voice_profile: Dict,
        character_emotion: str = "neutral",
        context: Optional[Dict] = None
    ) -> bytes:
        """
        Synthesize speech for fiction - applies character-specific phonatory processing
        CPU-optimized with sequential processing and memory management
        """
        try:
            print(f"\n🎤 Synthesizing: '{text[:50]}...'")
            print(f"Using profile: {voice_profile['profile_id']}")
            print(f"CPU mode: {self.cpu_mode}")

            # CPU: Check memory before proceeding
            if self.cpu_mode and not self.memory_manager.check_memory():
                print("⚠️ Low memory detected! Attempting cleanup...")
                await self._unload_inactive_models()
                if not self.memory_manager.check_memory():
                    raise MemoryError("Insufficient RAM for synthesis")

            # Clear previous model from cache to free RAM
            if (self.active_model and
                self.active_model != voice_profile['profile_id']):
                print(f"🧹 Clearing previous model: {self.active_model}")
                await self._unload_model(self.active_model)

            # Load required model
            await self._ensure_model_loaded(voice_profile['profile_id'])
            self.active_model = voice_profile['profile_id']

            # 1. Base Coqui TTS synthesis
            # Check if this is a YourTTS model with speaker name
            speaker_name = voice_profile["coqui_model"].get("speaker_name")
            speaker_embedding = voice_profile["coqui_model"]["speaker_embedding"]
            
            # Convert back to numpy array if it's stored as a list
            if isinstance(speaker_embedding, list):
                speaker_embedding = np.array(speaker_embedding)
            
            print(f"Speaker embedding shape: {speaker_embedding.shape if hasattr(speaker_embedding, 'shape') else 'INVALID'}")
            if speaker_name:
                print(f"Using YourTTS speaker: {speaker_name}")

            # Validate speaker parameters
            if speaker_name is None and (speaker_embedding is None or (hasattr(speaker_embedding, 'shape') and speaker_embedding.shape[0] == 0)):
                print("⚠️ No speaker parameters - using default voice")
                speaker_embedding = None

            # Try different TTS approaches based on model type
            try:
                # For YourTTS with speaker name, use speaker parameter
                if speaker_name is not None:
                    base_audio = self.coqui_tts.tts(
                        text=text,
                        speaker=speaker_name,
                        language="en"
                    )
                # For YourTTS, use a valid speaker
                elif "your_tts" in self.coqui_tts.model_name.lower():
                    base_audio = self.coqui_tts.tts(
                        text=text,
                        speaker="male-en-2",  # Use valid male speaker as fallback
                        language="en"
                    )
                else:
                    # For other models, use speaker_embedding
                    base_audio = self.coqui_tts.tts(
                        text=text,
                        speaker_embedding=speaker_embedding,
                        language="en"
                    )
            except Exception as tts_error:
                print(f"TTS call failed: {tts_error}")
                # Fallback: try without speaker parameters
                try:
                    base_audio = self.coqui_tts.tts(
                        text=text,
                        language="en"
                    )
                    print("✅ Used fallback TTS without speaker parameters")
                except Exception as fallback_error:
                    print(f"❌ Fallback TTS also failed: {fallback_error}")
                    raise tts_error

            base_audio = debug_audio_pipeline(base_audio, "1_after_tts", voice_profile['profile_id'])

            # Convert list to numpy array if needed
            if isinstance(base_audio, list):
                base_audio = np.array(base_audio, dtype=np.float32)
                print(f"✓ Converted list to numpy array: shape {base_audio.shape}")

            base_audio = debug_audio_pipeline(base_audio, "1_after_tts", voice_profile['profile_id'])

            # 2. Apply POM modules with validation (SKIP on CPU to prevent corruption)
            if self.cpu_mode:
                print("⚠️ CPU mode: Skipping POM modules to prevent memory corruption")
                # Still do final validation and normalization
                pass
            else:
                # GPU mode: Apply POM modules normally
                pom_config = voice_profile["pom_config"]

                # Sanitize POM parameters to safe ranges
                pom_config = self._sanitize_pom_config(pom_config)

                # Apply formant filter if enabled
                if pom_config["formant_filter"]["enabled"]:
                    shifts = pom_config["formant_filter"]["formant_shifts"]
                    bandwidths = pom_config["formant_filter"]["bandwidth_adjustments"]

                    print(f"Applying formant filter: shifts={shifts}, bandwidths={bandwidths}")

                    # Apply formant filtering
                    base_audio = self.pom.apply_formant_filter(
                        audio=base_audio,
                        shifts=shifts,
                        bandwidths=bandwidths
                    )

                    base_audio = debug_audio_pipeline(base_audio, "2_after_formant", voice_profile['profile_id'])

            # Apply other POM modules as needed...

            # 3. Final validation and normalization
            if isinstance(base_audio, np.ndarray):
                # Ensure correct dtype
                if base_audio.dtype != np.float32:
                    base_audio = base_audio.astype(np.float32)

                # Ensure correct range [-1, 1]
                if np.max(np.abs(base_audio)) > 1.0:
                    print("⚠️ Audio clipping detected - normalizing...")
                    base_audio = base_audio / np.max(np.abs(base_audio)) * 0.95

                # Ensure mono
                if len(base_audio.shape) > 1:
                    base_audio = np.mean(base_audio, axis=1)

            # Get the original sample rate from TTS output
            output_sample_rate = self.coqui_tts.synthesizer.output_sample_rate
            print(f"✓ TTS output sample rate: {output_sample_rate}Hz")

            # Convert to WAV bytes for return (use original sample rate)
            import io
            wav_buffer = io.BytesIO()
            sf.write(wav_buffer, base_audio, output_sample_rate, format='WAV')
            audio_bytes = wav_buffer.getvalue()

            print(f"✓ Generated audio: {len(audio_bytes)} bytes (WAV format at {output_sample_rate}Hz)")
            return audio_bytes

        except Exception as e:
            print(f"❌ SYNTHESIS FAILED: {e}")
            print(f"Text: {text}")
            print(f"Voice Profile: {voice_profile.get('profile_id', 'UNKNOWN')}")

            # Return silent audio instead of crashing
            output_sample_rate = self.coqui_tts.synthesizer.output_sample_rate if self.coqui_tts else 16000
            silent_audio = np.zeros((output_sample_rate,), dtype=np.float32)  # 1 second of silence
            import io
            wav_buffer = io.BytesIO()
            sf.write(wav_buffer, silent_audio, output_sample_rate, format='WAV')
            return wav_buffer.getvalue()

    def _sanitize_pom_config(self, config: Dict) -> Dict:
        """Clamp POM values to safe ranges to prevent audio corruption"""
        if "formant_filter" in config:
            # Formant shifts should be -0.3 to +0.3
            for key in ["f1", "f2", "f3"]:
                if key in config["formant_filter"]["formant_shifts"]:
                    original = config["formant_filter"]["formant_shifts"][key]
                    clamped = max(-0.3, min(0.3, original))
                    if original != clamped:
                        print(f"⚠️ Clamped formant shift {key}: {original} -> {clamped}")
                    config["formant_filter"]["formant_shifts"][key] = clamped

            # Bandwidth adjustments should be 0.5 to 2.0
            for key in ["f1", "f2", "f3"]:
                if key in config["formant_filter"]["bandwidth_adjustments"]:
                    original = config["formant_filter"]["bandwidth_adjustments"][key]
                    clamped = max(0.5, min(2.0, original))
                    if original != clamped:
                        print(f"⚠️ Clamped bandwidth {key}: {original} -> {clamped}")
                    config["formant_filter"]["bandwidth_adjustments"][key] = clamped

        if "larynx_sim" in config:
            # Vocal fold tension should be 0.0 to 1.0
            if "vocal_fold_tension" in config["larynx_sim"]:
                original = config["larynx_sim"]["vocal_fold_tension"]
                clamped = max(0.0, min(1.0, original))
                if original != clamped:
                    print(f"⚠️ Clamped vocal fold tension: {original} -> {clamped}")
                config["larynx_sim"]["vocal_fold_tension"] = clamped

            # Breathiness should be 0.0 to 1.0
            if "breathiness" in config["larynx_sim"]:
                original = config["larynx_sim"]["breathiness"]
                clamped = max(0.0, min(1.0, original))
                if original != clamped:
                    print(f"⚠️ Clamped breathiness: {original} -> {clamped}")
                config["larynx_sim"]["breathiness"] = clamped

        return config

    def _map_params_to_yourtts_speaker(self, param_config: Dict) -> str:
        """
        Map parameter configuration to YourTTS speaker name
        """
        style = param_config.get("style", "neutral").lower()
        
        # Map styles to available speakers for better variety
        if "female" in style or "bright" in style or "soft" in style:
            return "female-en-5"  # Female English speaker
        elif "male" in style or "deep" in style or "warm_fatherly" in style:
            return "male-en-2"  # Male English speaker
        elif "warm" in style or "gentle" in style:
            return "female-en-5"  # Female for warm styles
        else:
            # Default to female for neutral styles
            return "female-en-5"
        """
        Generate a default speaker embedding for parameter-based voice profiles.
        This creates a basic embedding that Coqui TTS can use.
        """
        try:
            # For parameter-based voices, we need to generate a speaker embedding
            # Since we don't have a reference sample, we'll use Coqui's default
            # and modify it slightly based on parameters

            # Get the base speaker embedding from Coqui TTS
            # This is a bit of a hack, but necessary for parameter-based voices
            if hasattr(self.coqui_tts, 'synthesizer') and hasattr(self.coqui_tts.synthesizer, 'speaker_manager'):
                # Try to get a default speaker embedding
                try:
                    # Use the default speaker (usually index 0)
                    default_embedding = self.coqui_tts.synthesizer.speaker_manager.get_speaker_embedding(0)
                    if default_embedding is not None:
                        # Convert to numpy array if needed
                        if not isinstance(default_embedding, np.ndarray):
                            default_embedding = np.array(default_embedding)

                        # Apply small modifications based on param_config to create variation
                        style = param_config.get("style", "neutral")
                        if "warm" in style.lower():
                            # Slightly modify for warmer sound
                            default_embedding = default_embedding * 0.98  # Slight reduction
                        elif "bright" in style.lower():
                            # Slightly modify for brighter sound
                            default_embedding = default_embedding * 1.02  # Slight increase

                        print(f"Generated default speaker embedding with shape: {default_embedding.shape}")
                        return default_embedding
                except Exception as e:
                    print(f"Could not get default speaker embedding: {e}")

            # Fallback: Create a random embedding in the expected range
            # Coqui TTS speaker embeddings are typically 512-dimensional
            print("Using fallback random speaker embedding")
            embedding = np.random.normal(0, 0.1, 512).astype(np.float32)

            # Normalize to unit length (L2 normalization)
            embedding = embedding / np.linalg.norm(embedding)

            return embedding

        except Exception as e:
            print(f"Error generating speaker embedding: {e}")
            # Ultimate fallback: return None and let Coqui use its default
            return None

    async def _ensure_model_loaded(self, model_id):
        """Ensure the required model is loaded (CPU memory management)"""
        if model_id not in self.model_cache:
            print(f"Loading model: {model_id}")
            # In CPU mode, we don't actually cache models to save memory
            # Just ensure Coqui TTS is ready
            if self.coqui_tts is None:
                raise RuntimeError("Coqui TTS not initialized")

    async def _unload_model(self, model_id):
        """Explicitly unload model to free RAM (CPU optimization)"""
        if model_id in self.model_cache:
            del self.model_cache[model_id]

        # Force garbage collection
        import gc
        gc.collect()

        # Clear any cached computations
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass

        print(f"🧹 Unloaded model: {model_id}")

    async def _unload_inactive_models(self):
        """Unload all models except the active one to free memory"""
        models_to_unload = [mid for mid in self.model_cache.keys() if mid != self.active_model]
        for model_id in models_to_unload:
            await self._unload_model(model_id)

        print(f"🧹 Unloaded {len(models_to_unload)} inactive models")

    async def synthesize_with_narrator_voice(
        self,
        text: str,
        narrator_profile: Dict,
        section_type: str = "main",
        technical_terms: Optional[List[str]] = None
    ) -> bytes:
        """
        Synthesize speech for nonfiction - optimized for clarity and comprehension
        """
        # Create temporary output path
        temp_path = f"./temp/voice_{uuid.uuid4()}.wav"

        # Build POM parameters from narrator profile
        pom_config = narrator_profile["pom_config"]

        # Pre-process text for technical terms (add pronunciation hints)
        if technical_terms:
            text = self._inject_pronunciation_hints(text, technical_terms)

        # Map section type to POM parameters
        pitch_factor = 1.0

        # Extract formant target for narrator (usually neutral)
        formant_target = pom_config.get("formant_filter", {}).get("target_vowel", None)

        # Get articulation and nasalization parameters
        articulation = pom_config.get("tongue_articulation", {})
        nasalization = pom_config.get("uvula_control", {})

        # Adjust parameters based on section type
        if section_type == "footnote":
            pitch_factor = 0.9  # Slightly lower pitch for footnotes
        elif section_type == "quote":
            pitch_factor = 1.1  # Slightly higher pitch for quotes

        # Use real POM phonate method
        output_path = self.pom.phonate(
            text=text,
            out_path=temp_path,
            pitch_factor=pitch_factor,
            articulation=articulation,
            nasalization=nasalization
        )

        # Read the generated audio file
        with open(output_path, 'rb') as f:
            audio_bytes = f.read()

        # Clean up temp file
        os.remove(output_path)

        return audio_bytes

    async def _extract_speaker_embedding(self, sample_path: str) -> Optional[str]:
        """Extract speaker embedding from audio sample"""
        if not POM_AVAILABLE:
            return f"mock_embedding_{hash(sample_path) % 1000}"

        # In real implementation, this would extract speaker embedding
        # For now, return mock path
        return f"./voices/models/speaker_{hash(sample_path) % 1000}.pth"

    def _map_sample_to_pom_params(self, sample_path: str) -> Dict:
        """
        Analyze audio sample and generate appropriate POM parameters
        """
        # Mock analysis - in real implementation, this would analyze the audio
        return {
            "formant_filter": {
                "enabled": True,
                "formant_shifts": {
                    "f1": -0.1,
                    "f2": 0.15,
                    "f3": 0.05
                },
                "bandwidth_adjustments": {
                    "f1": 1.2,
                    "f2": 1.1,
                    "f3": 1.0
                }
            },
            "larynx_sim": {
                "enabled": True,
                "vocal_fold_tension": 0.7,
                "breathiness": 0.3,
                "vibrato_rate": 4.5
            },
            "lip_control": {
                "enabled": True,
                "lip_rounding": 0.4,
                "articulation_precision": 0.8
            },
            "tongue_artic": {
                "enabled": True,
                "tongue_position": "retroflex",
                "articulation_sharpness": 0.6
            },
            "uvula_control": {
                "enabled": False,
                "nasalization": 0.0
            }
        }

    def _build_pom_from_description(self, param_config: Dict) -> Dict:
        """Build POM config from descriptive parameters"""
        # Map descriptive parameters to POM settings
        return {
            "formant_filter": {
                "enabled": True,
                "target_vowel": param_config.get("target_vowel", "a"),
                "formant_shifts": param_config.get("formant_shifts", {"f1": 0.0, "f2": 0.0, "f3": 0.0}),
                "bandwidth_adjustments": param_config.get("bandwidth_adjustments", {"f1": 1.0, "f2": 1.0, "f3": 1.0})
            },
            "larynx_sim": {
                "enabled": True,
                "vocal_fold_tension": param_config.get("tension", 0.6),
                "breathiness": param_config.get("breathiness", 0.2),
                "vibrato_rate": param_config.get("vibrato_rate", 4.0)
            },
            "lip_control": {
                "enabled": True,
                "lip_rounding": param_config.get("lip_rounding", 0.3),
                "articulation_precision": param_config.get("articulation_precision", 0.8)
            },
            "tongue_articulation": {
                "enabled": True,
                "tongue_position": param_config.get("tongue_position", "alveolar"),
                "articulation_sharpness": param_config.get("sharpness", 0.7)
            },
            "uvula_control": {
                "enabled": param_config.get("nasal", False),
                "nasalization": param_config.get("nasalization", 0.0)
            }
        }

    def _initialize_emotion_profiles(self, pom_config: Dict) -> Dict:
        """Initialize emotion-specific voice profiles"""
        return {
            "neutral": {
                "pitch_mean": 110,
                "pitch_std": 15,
                "speaking_rate": 1.0,
                "intensity": 0.7
            },
            "angry": {
                "pitch_mean": 120,
                "pitch_std": 25,
                "speaking_rate": 1.3,
                "intensity": 0.95
            },
            "weary": {
                "pitch_mean": 100,
                "pitch_std": 10,
                "speaking_rate": 0.85,
                "intensity": 0.5
            },
            "excited": {
                "pitch_mean": 125,
                "pitch_std": 20,
                "speaking_rate": 1.2,
                "intensity": 0.9
            },
            "calm": {
                "pitch_mean": 105,
                "pitch_std": 12,
                "speaking_rate": 0.9,
                "intensity": 0.6
            }
        }

    def _apply_emotion_modulation(self, audio: np.ndarray, emotion_profile: Dict, pom_config: Dict) -> np.ndarray:
        """Apply emotion-specific audio modulation"""
        # Mock emotion modulation - in real implementation, this would adjust audio
        return audio

    def _inject_pronunciation_hints(self, text: str, technical_terms: List[str]) -> str:
        """Inject pronunciation hints for technical terms"""
        # Mock implementation - in real implementation, this would add SSML
        return text

    def _reduce_intensity(self, audio: np.ndarray, factor: float) -> np.ndarray:
        """Reduce audio intensity"""
        return audio * factor

    def _add_formal_prosody(self, audio: np.ndarray) -> np.ndarray:
        """Add formal prosody patterns"""
        # Mock implementation
        return audio

    def _audio_to_wav_bytes(self, audio: np.ndarray) -> bytes:
        """Convert audio array to WAV bytes"""
        # Mock WAV conversion - in real implementation, use scipy or similar
        import wave
        import struct

        # Create a simple WAV file in memory
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(22050)
            # Convert float32 to int16
            audio_int16 = (audio * 32767).astype(np.int16)
            wav_file.writeframes(audio_int16.tobytes())

        return buffer.getvalue()

    async def get_profile(self, profile_id: str) -> Dict:
        """Get voice profile by ID"""
        profile_path = Path("./voices/profiles") / f"{profile_id}.json"
        if not profile_path.exists():
            raise FileNotFoundError(f"Voice profile {profile_id} not found")

        with open(profile_path, 'r') as f:
            return json.load(f)

    async def profile_exists(self, profile_id: str) -> bool:
        """Check if voice profile exists"""
        profile_path = Path("./voices/profiles") / f"{profile_id}.json"
        return profile_path.exists()

    async def preview_voice(self, profile_id: str, text: str, emotion: str) -> bytes:
        """Generate voice preview"""
        profile = await self.get_profile(profile_id)
        return await self.synthesize_with_character_voice(text, profile, emotion)