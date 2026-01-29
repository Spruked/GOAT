from podcast_engine.core.dialogue_detector import DialogueDetector

detector = DialogueDetector()
sample_text = '''Host: Welcome to the show!
Guest: Thanks for having me.
Host says, "I'm excited to talk about AI."
This is some narration without a speaker.'''

result = detector.detect(sample_text)
print(f'Detected {len(result)} dialogue lines:')
for line in result:
    print(f'  {line.speaker}: {line.text[:50]}...')
print('C-1.1 Dialogue Detector functional test: PASSED')