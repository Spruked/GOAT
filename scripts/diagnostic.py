# diagnostic.py - Comprehensive diagnostic test for GOAT Voice System

import sys
import os
sys.path.append('./Phonatory_Output_Module')
sys.path.append('./engines')

import asyncio
import numpy as np
import soundfile as sf
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from engines.voice_engine import VoiceEngine

async def run_diagnostics():
    """Comprehensive diagnostic test"""

    print("🔍 GOAT Voice System Diagnostic\n")

    # Ensure temp directory exists
    Path("./temp").mkdir(exist_ok=True)

    engine = VoiceEngine()

    # Test 1: Basic TTS without POM
    print("=== Test 1: Pure Coqui TTS (No POM) ===")
    try:
        text = "Hello, this is a test of the basic text to speech system."
        print(f"Text: {text}")

        # Bypass POM entirely - direct Coqui TTS
        if engine.coqui_tts:
            audio = engine.coqui_tts.tts(
                text=text,
                speaker_embedding=None,  # Use default voice
                language="en"
            )

            print(f"✓ Audio generated: {len(audio)} samples")
            print(f"✓ Sample rate: {engine.SAMPLE_RATE} Hz")
            print(f"✓ Duration: {len(audio)/engine.SAMPLE_RATE:.2f} seconds")
            print(f"✓ Audio range: {np.min(audio):.3f} to {np.max(audio):.3f}")
            print(f"✓ Contains NaN: {np.any(np.isnan(audio))}")

            # Save
            sf.write("./temp/test1_pure_tts.wav", audio, engine.SAMPLE_RATE)
            print("✓ Saved to ./temp/test1_pure_tts.wav")
        else:
            print("❌ Coqui TTS not available")

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: With speaker embedding
    print("\n=== Test 2: Coqui TTS with Speaker Embedding ===")
    try:
        if engine.coqui_tts:
            # Create a simple voice profile
            result = await engine.create_voice_profile(
                creation_method="parameter",
                name="Diagnostic Test Voice",
                description="Test voice for diagnostics",
                voice_type="character",
                param_config={
                    "style": "neutral",
                    "pitch_modulation": 1.0,
                    "target_vowel": "a"
                }
            )

            print(f"Created profile: {result['profile_id']}")

            # Load the profile
            profile = await engine.load_voice_profile(result['profile_id'])

            # Check speaker embedding
            speaker_embedding = profile["coqui_model"]["speaker_embedding"]
            print(f"Speaker embedding shape: {speaker_embedding.shape if hasattr(speaker_embedding, 'shape') else 'None'}")
            print(f"Speaker embedding type: {type(speaker_embedding)}")

            if speaker_embedding is not None and hasattr(speaker_embedding, 'shape'):
                print(f"Embedding L2 norm: {np.linalg.norm(speaker_embedding):.3f}")
                print(f"Embedding range: {np.min(speaker_embedding):.3f} to {np.max(speaker_embedding):.3f}")
                print(f"Contains NaN: {np.any(np.isnan(speaker_embedding))}")
                print(f"Contains Inf: {np.any(np.isinf(speaker_embedding))}")

            audio = engine.coqui_tts.tts(
                text=text,
                speaker_embedding=speaker_embedding,
                language="en"
            )

            print(f"✓ Audio generated with speaker embedding")
            print(f"✓ Audio range: {np.min(audio):.3f} to {np.max(audio):.3f}")
            sf.write("./temp/test2_with_embedding.wav", audio, engine.SAMPLE_RATE)
            print("✓ Saved to ./temp/test2_with_embedding.wav")
        else:
            print("❌ Coqui TTS not available")

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()

    # Test 3: Full POM Pipeline
    print("\n=== Test 3: Full POM Pipeline ===")
    try:
        if 'profile' in locals():
            audio_bytes = await engine.synthesize_with_character_voice(
                text=text,
                voice_profile=profile,
                emotion="neutral"
            )

            print(f"✓ Full pipeline audio generated: {len(audio_bytes)} bytes")

            # Convert bytes back to numpy for analysis
            audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32767.0
            print(f"✓ Converted to float32, range: {np.min(audio_array):.3f} to {np.max(audio_array):.3f}")

            sf.write("./temp/test3_full_pom.wav", audio_array, engine.SAMPLE_RATE)
            print("✓ Saved to ./temp/test3_full_pom.wav")
        else:
            print("❌ No profile available from Test 2")

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()

    # Test 4: Check existing voice profiles
    print("\n=== Test 4: Voice Profile Analysis ===")
    try:
        # List all profiles
        profiles_dir = Path("./voices/profiles")
        if profiles_dir.exists():
            profile_files = list(profiles_dir.glob("*.json"))
            print(f"Found {len(profile_files)} voice profile files:")

            for profile_file in profile_files:
                print(f"\n--- Profile: {profile_file.name} ---")
                try:
                    with open(profile_file, 'r') as f:
                        profile_data = json.load(f)

                    print(f"Name: {profile_data.get('name', 'Unknown')}")
                    print(f"Type: {profile_data.get('voice_type', 'Unknown')}")
                    print(f"Creation method: {profile_data.get('creation_method', 'Unknown')}")

                    # Check speaker embedding
                    embedding = profile_data.get("coqui_model", {}).get("speaker_embedding")
                    if embedding:
                        if isinstance(embedding, list):
                            embedding = np.array(embedding)
                        print(f"Embedding shape: {embedding.shape if hasattr(embedding, 'shape') else 'Invalid'}")
                        print(f"Embedding norm: {np.linalg.norm(embedding):.3f}")
                        print(f"Has NaN: {np.any(np.isnan(embedding))}")
                        print(f"Has Inf: {np.any(np.isinf(embedding))}")
                    else:
                        print("No speaker embedding found")

                    # Check POM config
                    pom_config = profile_data.get("pom_config", {})
                    if pom_config:
                        print("POM config present")
                        if "formant_filter" in pom_config:
                            shifts = pom_config["formant_filter"].get("formant_shifts", {})
                            print(f"Formant shifts: {shifts}")
                    else:
                        print("No POM config found")

                except Exception as e:
                    print(f"Error reading profile: {e}")
        else:
            print("No voices/profiles directory found")

    except Exception as e:
        print(f"❌ Profile analysis failed: {e}")

    print("\n=== Diagnostic Complete ===")
    print("Audio files saved to ./temp/:")
    print("- test1_pure_tts.wav: Pure Coqui TTS")
    print("- test2_with_embedding.wav: With speaker embedding")
    print("- test3_full_pom.wav: Full POM pipeline")
    print("\nListen to these files to identify where the gurgling starts!")

if __name__ == "__main__":
    import json
    asyncio.run(run_diagnostics())