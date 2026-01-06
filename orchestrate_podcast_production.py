# Orchestrate Podcast Production

from podcast_engine import PodcastEngine, LegacyInput

def orchestrate_podcast():
    """Orchestrates the production of a podcast using the PodcastEngine."""
    # Initialize the PodcastEngine
    engine = PodcastEngine()

    # Collect user input for podcast details
    topic = input("Enter the podcast topic: ")
    notes = input("Enter any additional notes: ")
    intent = input("Enter the intent (e.g., 'educational', 'entertainment'): ")
    audience = input("Enter the target audience: ")
    tone = input("Enter the tone (e.g., 'professional', 'casual'): ")
    length_estimate = input("Enter the length estimate (e.g., 'short', 'medium', 'long'): ")
    create_audiobook = True  # Default to 'yes'
    audio_type = input("Select audio type (podcast/audiobook): ").strip().lower()
    if audio_type not in ['podcast', 'audiobook']:
        print("Invalid audio type. Defaulting to 'podcast'.")
        audio_type = 'podcast'

    # Create the LegacyInput object
    user_input = LegacyInput(
        topic=topic,
        notes=notes,
        source_materials=[],  # No source materials provided in this example
        intent=intent,
        audience=audience,
        tone=tone,
        length_estimate=length_estimate,
        create_audiobook=create_audiobook,
        voice=None,  # Use default voice
        output_format=audio_type  # Pass audio type to the engine
    )

    # Run the podcast engine to create the legacy
    result = engine.create_legacy(user_input)

    # Display the result
    print("\nPodcast production completed!")
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Audio File: {result.get('audiobook_path', 'N/A')}")
    print(f"Details: {result}")

if __name__ == "__main__":
    orchestrate_podcast()