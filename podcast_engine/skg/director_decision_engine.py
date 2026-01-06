class DirectorDecisionEngine:
    """
    The Director's brain.
    One job: Take a line and decide EXACTLY how it must be performed.
    """

    def __init__(self):
        self.last_energy = 0.65   # Tracks emotional momentum
        self.last_intent = "neutral_statement"

    def analyze_intent(self, line: str) -> str:
        """Determine WHY the line exists — its purpose."""

        line_l = line.lower()

        if "?" in line:
            return "seeking_information"
        if "!" in line:
            return "impact_statement"
        if any(word in line_l for word in ["listen", "truth", "remember"]):
            return "drive_point_home"
        if any(word in line_l for word in ["but", "however"]):
            return "pivot"
        if any(word in line_l for word in ["love", "fear", "hurt"]):
            return "emotion_reveal"

        return "neutral_statement"

    def decide_delivery(self, intent: str, speaker: str) -> dict:
        """Turn intent into delivery style."""

        base_energy = {
            "neutral_statement": 0.55,
            "seeking_information": 0.62,
            "drive_point_home": 0.78,
            "pivot": 0.68,
            "impact_statement": 0.9,
            "emotion_reveal": 0.73,
        }.get(intent, 0.6)

        # Adjust for the actor
        if speaker == "phil_dandy":
            base_energy *= 0.95    # Phil is calm + precise
        elif speaker == "jim_dandy":
            base_energy *= 1.15    # Jim is more animated

        pitch_map = {
            "neutral_statement": "mid",
            "seeking_information": "rising",
            "drive_point_home": "low",
            "pivot": "mid-low",
            "impact_statement": "sharp",
            "emotion_reveal": "soft"
        }

        tone_map = {
            "neutral_statement": "natural",
            "seeking_information": "curious",
            "drive_point_home": "authoritative",
            "pivot": "thoughtful",
            "impact_statement": "intense",
            "emotion_reveal": "warm"
        }

        return {
            "energy": base_energy,
            "pitch": pitch_map[intent],
            "tone": tone_map[intent]
        }

    def decide_timing(self, intent: str) -> float:
        """How long to pause after the line."""

        pause_map = {
            "neutral_statement": 0.45,
            "seeking_information": 0.35,
            "drive_point_home": 0.9,
            "pivot": 0.6,
            "impact_statement": 1.1,
            "emotion_reveal": 0.8
        }

        return pause_map.get(intent, 0.5)

    def emphasize_words(self, line: str) -> list:
        """Mark key words for the POM to stress."""

        keywords = ["truth", "love", "fear", "listen", "remember", "power"]

        return [w for w in line.split() if w.lower().rstrip(",.!") in keywords]

    def build_directive(self, line: str, speaker: str) -> dict:
        """The FULL decision — the Director's verdict."""

        intent = self.analyze_intent(line)
        delivery = self.decide_delivery(intent, speaker)
        pause = self.decide_timing(intent)
        emphasis = self.emphasize_words(line)

        directive = {
            "intent": intent,
            "energy": delivery["energy"],
            "pitch": delivery["pitch"],
            "tone": delivery["tone"],
            "emphasis": emphasis,
            "pause_after": pause,
            "breath": True if intent in ["impact_statement", "emotion_reveal"] else False
        }

        # Update state
        self.last_energy = delivery["energy"]
        self.last_intent = intent

        return directive