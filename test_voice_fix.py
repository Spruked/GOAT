import asyncio
from engines.voice_engine import VoiceEngine

async def test():
    engine = VoiceEngine()
    result = await engine.create_voice_profile(
        creation_method='parameter',
        name='test_bryan',
        description='Test voice',
        voice_type='narrator',
        param_config={'style': 'warm_fatherly', 'emotional_range': ['loving'], 'pitch_modulation': 0.95, 'target_vowel': 'a'}
    )
    print('Profile created:', result['profile_id'])

    # Load the full profile
    profile = await engine.load_voice_profile(result['profile_id'])
    print('Profile loaded with keys:', list(profile.keys()))

    audio = await engine.synthesize_with_character_voice('Hello world', profile, 'neutral')
    print('Audio generated, size:', len(audio), 'bytes')

    with open('test_audio.wav', 'wb') as f:
        f.write(audio)
    print('Test audio saved')

if __name__ == "__main__":
    asyncio.run(test())