from podcast_builder.templates import PODCAST_EXPANSION_TEMPLATE, FRAMEWORK_TEMPLATE

def ai_generate(prompt):
    """Placeholder for AI generation logic."""
    return f"Generated content based on prompt: {prompt}"

class LongFormExpander:
    def expand(self, topic, tone, audience, length, mode="podcast"):
        base_multiplier = {
            "short": 1.0,
            "medium": 2.0,
            "long": 3.5
        }.get(length, 2.0)

        template = {
            "podcast": PODCAST_EXPANSION_TEMPLATE,
            "framework": FRAMEWORK_TEMPLATE
        }[mode]

        content = ai_generate(
            f"Expand into a detailed {mode} script:\n"
            f"Topic: {topic}\nAudience: {audience}\nTone: {tone}\n"
            f"Length multiplier: {base_multiplier}\n"
            f"Template: {template}\n"
        )

        return content