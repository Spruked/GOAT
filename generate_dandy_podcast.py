import asyncio
from dandy_skg_module import DandySKGModule
from dandy_skg_models import BuildReview
from datetime import datetime

async def generate_dandy_podcast():
    # Initialize module
    dandy_module = DandySKGModule()
    dandy_module.initialize({
        "dandy_vault_path": "./vaults/dandy_podcast",
        # Optionally add podcast_manifest for real ingestion
    })

    # Create a mock build review about the GOAT
    build_data = {
        "user_id": "goat_team",
        "project_name": "GOAT Orchestrator",
        "summary": "GOAT is a modular, multi-persona AI system for orchestrating autonomous teams and content creation. It features a host assistant bubble, SM-P1 plugin architecture, and seamless integration with social platforms.",
        "tech_stack": ["Python", "FastAPI", "React", "Docker"],
        "code_snippets": ["class GOATOrchestrator:", "def handle_message(self, ...):"],
        "preview_url": "https://goat.app/demo"
    }
    # Submit build for review
    submit_result = await dandy_module.handle({
        "action": "submit_build",
        "build_data": build_data
    }, context={})
    review_id = submit_result["review_id"]

    # Generate a 3-minute podcast (roughly 450-500 words)
    # We'll generate a long YouTube segment and print it
    content_result = await dandy_module.handle({
        "action": "generate_review",
        "build_id": review_id,
        "platforms": ["youtube"]
    }, context={})
    print("\n=== Phil & Jim Dandy Podcast: The GOAT Special ===\n")
    print(content_result["content"]["youtube"])

if __name__ == "__main__":
    asyncio.run(generate_dandy_podcast())
