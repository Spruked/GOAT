from podcast_builder.builder import PodcastBuilder
from podcast_builder.tts import generate_tts_voice

def generate_sample_podcast():
    topic = "The Future of Web3 Education"
    audience = "Educators and Web3 Enthusiasts"
    tone = "Professional"
    length = "long"

    builder = PodcastBuilder()
    script = builder.build(topic, audience, tone, length)

    print("Generated Podcast Script:\n")
    print(script)

    audio_path = generate_tts_voice(
        text=script,
        voice_id="en-US-JennyNeural",
        output_path="t:\\GOAT\\deliverables\\podcast_engine\\temp\\sample_podcast.mp3"
    )

    print(f"\nPodcast audio saved at: {audio_path}")

if __name__ == "__main__":
    generate_sample_podcast()