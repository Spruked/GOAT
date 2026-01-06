from podcast_builder.expander import LongFormExpander
from podcast_builder.composer import NarrativeComposer

class PodcastBuilder:
    def build(self, topic, audience, tone, length):
        expanded = LongFormExpander().expand(
            topic=topic,
            tone=tone,
            audience=audience,
            length=length,
            mode="podcast"
        )

        narrative = NarrativeComposer().compose(
            content=expanded,
            mode="podcast",
            tone=tone,
            audience=audience
        )

        return narrative