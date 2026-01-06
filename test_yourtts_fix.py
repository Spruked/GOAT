import asyncio
from engines.voice_engine import VoiceEngine

async def test():
    engine = VoiceEngine(cpu_mode=True)

    # Create a test profile
    result = await engine.create_voice_profile(
        creation_method='parameter',
        name='test_yourtts_fixed2',
        description='Test YourTTS voice with correct speaker and array conversion',
        voice_type='narrator',
        param_config={'style': 'warm_fatherly', 'target_vowel': 'a'}
    )
    print('Profile created:', result['profile_id'])

    # Load and test synthesis
    profile = await engine.load_voice_profile(result['profile_id'])
    text = 'Hello, this is a test of the YourTTS voice synthesis system with the correct speaker and array conversion.'

    print('Testing audio synthesis...')
    audio_bytes = await engine.synthesize_with_character_voice(text, profile, 'neutral')

    print(f'Audio generated: {len(audio_bytes)} bytes')

    # Save for testing
    with open('./temp/test_yourtts_fixed2.wav', 'wb') as f:
        f.write(audio_bytes)
    print('Saved to ./temp/test_yourtts_fixed2.wav')

if __name__ == "__main__":
    asyncio.run(test())