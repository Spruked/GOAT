from typing import Dict, List, Optional, Tuple
import random
import time
from dataclasses import dataclass
from podcast_engine.skg.director_decision_engine import DirectorDecisionEngine

@dataclass
class ConversationState:
    """Real-time conversation dynamics"""
    energy_level: float  # 0.0-1.0 (calm to hyper)
    last_speaker: str
    interruption_counter: int
    topic_engagement: float  # How engaged the "audience" would be
    banter_mode: bool  # Are we in riffing mode?
    pause_buffer: float  # Current pause duration before next line

class PodcastDirector:
    def __init__(self, skg):
        self.skg = skg
        self.dde = DirectorDecisionEngine()  # The Director's brain
        self.state = ConversationState(
            energy_level=0.7,
            last_speaker="phil_dandy",
            interruption_counter=0,
            topic_engagement=0.5,
            banter_mode=False,
            pause_buffer=0.5
        )

        self.director_config = self._load_director_config()
        self.banter_engine = BanterEngine(skg, self.director_config)
        self.pacing_engine = PacingEngine(self.director_config, self.dde)
        self.transition_engine = TransitionEngine(skg, self.director_config)

    def _load_director_config(self) -> Dict:
        """Director's creative choices and patterns"""
        return {
            "phil_and_jim_chemistry": {
                "interrupt_probability": 0.15,  # Jim interrupts Phil sometimes
                "finishing_sentences": 0.08,   # They complete each other's thoughts
                "laugh_tracks": ["light_chuckle", "genuine_laugh", "snort_laugh"],
                "energy_symmetry": 0.6  # How much they mirror each other's energy
            },
            "pacing_rules": {
                "topic_energy_boost": {
                    "AI/ML": 0.3,
                    "startup_funding": 0.25,
                    "creative_process": 0.15
                },
                "pause_durations": {
                    "standard": 0.4,
                    "punchline": 0.8,
                    "topic_transition": 1.2,
                    "dramatic_reveal": 1.5
                },
                "sentence_rate_words_per_minute": {
                    "phil_dandy": 145,
                    "jim_dandy": 165
                }
            },
            "banter_library": {
                "warm_up_seeds": [
                    "Jim, you've got to hear this...",
                    "Phil, I'm curious what you think about...",
                    "So I was thinking about this the other day..."
                ],
                "agreement_phrases": [
                    "Exactly! And also...",
                    "That reminds me of...",
                    "You're hitting on something huge here..."
                ],
                "challenge_phrases": [
                    "But hold on, what about...",
                    "I see it differently—what if...",
                    "I'm going to push back on that..."
                ],
                "recap_seeds": [
                    "So to recap for our listeners...",
                    "If I'm hearing you right, you're saying..."
                ]
            },
            "transition_patterns": {
                "ad_breaks": ["Let's take a quick pause...", "Quick word from our friends at..."],
                "topic_pivots": ["Speaking of which...", "That actually leads perfectly into..."],
                "listener_questions": ["We got a great question from...", "One of our listeners wrote in..."]
            }
        }

    def direct_conversation_segment(self, topic: Dict) -> List[Dict]:
        """
        Main entry: Take raw topic, return performance-directed segments
        """
        print(f"🎬 Podcast Director: Directing segment on '{topic['title']}'")

        segments = []
        raw_script = self._generate_raw_script(topic)

        # 1. Apply conversational flow
        script_with_flow = self._apply_conversational_flow(raw_script)

        # 2. Inject banter & chemistry
        script_with_banter = self.banter_engine.inject_banter(script_with_flow)

        # 3. Calculate precise timing & pauses
        final_script = self.pacing_engine.calculate_pacing(script_with_banter)

        # 4. Generate audio with performance direction
        for line in final_script:
            # Add performance metadata to synthesis
            audio_path = self.skg.synthesize_as_persona(
                text=line["text"],
                persona_id=line["speaker"],
                performance_directives=line.get("directives", {})
            )

            segments.append({
                "speaker": line["speaker"],
                "text": line["text"],
                "audio_path": audio_path,
                "pause_after": line.get("pause_after", 0.5),
                "energy": line.get("energy_level", 0.7),
                "banter_mode": line.get("banter_mode", False)
            })

            # Update conversation state
            self._update_state(line)

        return segments

    def _generate_raw_script(self, topic: Dict) -> List[Dict]:
        """Generate basic conversational structure from topic"""
        # This would integrate with existing podcast generation
        # For now, return a simple alternating structure
        script = []
        speakers = ["phil_dandy", "jim_dandy"]

        # Opening
        script.append({
            "speaker": "phil_dandy",
            "text": f"Welcome back to the show, Jim. Today we're talking about {topic['title']}.",
            "type": "opening"
        })

        # Main discussion (alternating)
        for i in range(3):
            speaker = speakers[i % 2]
            script.append({
                "speaker": speaker,
                "text": f"This is point number {i+1} about {topic['title']}.",
                "type": "discussion"
            })

        # Closing
        script.append({
            "speaker": "jim_dandy",
            "text": f"That's all for today on {topic['title']}. Thanks for listening!",
            "type": "closing"
        })

        return script

    def _apply_conversational_flow(self, raw_script: List[Dict]) -> List[Dict]:
        """Add interruption patterns and back-and-forth energy"""

        flow_enhanced = []
        chem = self.director_config["phil_and_jim_chemistry"]

        for i, line in enumerate(raw_script):
            # Add interruption markers between Phil → Jim
            if line["speaker"] == "phil_dandy" and i < len(raw_script) - 1:
                next_line = raw_script[i + 1]

                # Random interruption chance
                if random.random() < chem["interrupt_probability"]:
                    # Jim interrupts with a short interjection
                    interruption = self.banter_engine.generate_interruption(
                        based_on=line["text"],
                        from_speaker="jim_dandy",
                        interrupting_speaker="phil_dandy"
                    )
                    flow_enhanced.append(interruption)

                    # Mark original line as interrupted
                    line["was_interrupted"] = True
                    self.state.interruption_counter += 1

            # Add finishing-each-other's-sentences
            if random.random() < chem["finishing_sentences"] and i > 0:
                prev_line = raw_script[i - 1]
                if prev_line["speaker"] != line["speaker"]:
                    line["text"] = self.banter_engine.complete_sentence(prev_line, line)

            flow_enhanced.append(line)

        return flow_enhanced

    def _update_state(self, line: Dict):
        """Dynamic conversation state management"""
        self.state.last_speaker = line["speaker"]
        self.state.banter_mode = line.get("banter_mode", False)
        self.state.pause_buffer = line.get("pause_after", 0.5)

        # Energy decay/growth
        if "energy_level" in line:
            target_energy = line["energy_level"]
            current_energy = self.state.energy_level
            self.state.energy_level = current_energy * 0.7 + target_energy * 0.3  # Smooth transition

        print(f"   → State: Energy={self.state.energy_level:.2f}, Banter={self.state.banter_mode}")


class BanterEngine:
    """Generates organic interjections, callbacks, and chemistry"""

    def __init__(self, skg, config: Dict):
        self.skg = skg
        self.config = config

    def inject_banter(self, script: List[Dict]) -> List[Dict]:
        """Scan script for banter opportunities and inject them"""

        banter_enhanced = []

        for i, line in enumerate(script):
            banter_enhanced.append(line)

            # After 2-3 lines, inject a callback or agreement
            if i > 0 and i % 3 == 0 and random.random() < 0.4:
                callback = self.generate_callback(
                    referecing_line=script[i-1],
                    current_speaker=line["speaker"]
                )
                if callback:
                    banter_enhanced.append(callback)

            # Add laughter after punchlines
            if line.get("is_punchline", False):
                laugh = self.generate_laughter(for_line=line)
                banter_enhanced.append(laugh)

        return banter_enhanced

    def generate_interruption(self, based_on: str, from_speaker: str, interrupting_speaker: str) -> Dict:
        """Create a natural interruption"""

        # Extract key phrase from original line
        key_phrase = self._extract_key_phrase(based_on)

        interruption_templates = {
            "phil_dandy": [
                f"Wait, Jim—{key_phrase}—that reminds me!",
                f"Hold that thought, {key_phrase} is huge...",
                f"Jim! {key_phrase} actually connects to..."
            ],
            "jim_dandy": [
                f"Oh! {key_phrase}—I have to jump in!",
                f"Wait wait, {key_phrase} is exactly...",
                f"Hold up, {key_phrase} makes me think of..."
            ]
        }

        text = random.choice(interruption_templates[from_speaker])

        return {
            "speaker": from_speaker,
            "text": text,
            "interrupts": interrupting_speaker,
            "pause_after": 0.1,  # Quick pause
            "energy_level": 0.85,
            "banter_mode": True,
            "directives": {
                "interrupt_tone": True,
                "urgency": 0.7
            }
        }

    def generate_callback(self, referecing_line: Dict, current_speaker: str) -> Optional[Dict]:
        """Create a "That reminds me" or "Going back to..." moment"""

        if self.skg.state.interruption_counter > 2:
            return None  # Too many interruptions, let it breathe

        callback_templates = {
            "phil_dandy": [
                f"That actually ties back to what Jim said about...",
                f"Jim's point about {self._extract_keyword(referecing_line['text'])} is key...",
                f"You know, that reminds me of something..."
            ],
            "jim_dandy": [
                f"I love that, and it makes me think...",
                f"That's exactly what I was getting at with...",
                f"So Phil, you're saying..."
            ]
        }

        text = random.choice(callback_templates[current_speaker])

        return {
            "speaker": current_speaker,
            "text": text,
            "pause_before": 0.3,  # Brief pause for reflection
            "energy_level": 0.65,
            "banter_mode": True,
            "directives": {
                "reflective_tone": True
            }
        }

    def generate_laughter(self, for_line: Dict) -> Dict:
        """Add appropriate laugh track"""

        laugh_intensity = "genuine_laugh" if "[laughs]" in for_line.get("text", "") else "light_chuckle"

        # Use a pre-recorded laugh or synthesize
        laugh_audio = f"assets/laughs/{laugh_intensity}.wav"

        return {
            "speaker": "sound_effect",
            "text": f"[{laugh_intensity}]",
            "audio_path": laugh_audio,
            "pause_after": 0.3,
            "banter_mode": False
        }

    def complete_sentence(self, prev_line: Dict, current_line: Dict) -> str:
        """Complete the previous speaker's thought"""
        prev_text = prev_line["text"]
        current_text = current_line["text"]

        # Simple completion: append current to previous with connector
        connectors = ["and", "but", "so", "because"]
        connector = random.choice(connectors)

        return f"{prev_text} {connector} {current_text}"

    def _extract_key_phrase(self, text: str, max_len: int = 4) -> str:
        """Extract important noun phrase for interruption reference"""

        words = text.split()
        if len(words) <= max_len:
            return text

        # Take first 3-4 words
        return " ".join(words[:max_len])

    def _extract_keyword(self, text: str) -> str:
        """Extract a key noun or topic word"""
        words = text.split()
        # Simple: return first noun-like word
        for word in words:
            if len(word) > 3 and word[0].isupper():
                return word.lower()
        return "that"


class PacingEngine:
    """Calculates precise timing, WPM, and rhythmic flow"""

    def __init__(self, config: Dict, dde: DirectorDecisionEngine):
        self.config = config
        self.dde = dde
        self.word_timing_cache = {}

    def calculate_pacing(self, script: List[Dict]) -> List[Dict]:
        """Add precise timing metadata to each line"""

        paced_script = []

        for line in script:
            # Get DDE directive for this line
            directive = self.dde.build_directive(line["text"], line["speaker"])

            # Merge DDE directive with existing line data
            line["directives"] = {
                "words_per_minute": self._calculate_wpm(line, directive),
                "target_duration": self._calculate_duration(line, directive),
                "pause_after": directive["pause_after"],
                "energy_contour": self._calculate_energy_contour(line, directive),
                "emphasis_words": [(word, 0.8) for word in directive["emphasis"]],  # Convert to stress format
                "pitch_style": directive["pitch"],
                "tone": directive["tone"],
                "breath": directive["breath"]
            }

            paced_script.append(line)

        return paced_script

    def _determine_pause(self, line: Dict, speaker: str) -> float:
        """Smart pause calculation based on context"""

        # Default pause
        pause = self.config["pacing_rules"]["pause_durations"]["standard"]

        # Extend for punchlines
        if line.get("is_punchline"):
            pause = self.config["pacing_rules"]["pause_durations"]["punchline"]

        # Extend for topic transitions
        if line.get("type") == "topic_transition":
            pause = self.config["pacing_rules"]["pause_durations"]["topic_transition"]

        # Shorten if in banter mode
        if line.get("banter_mode"):
            pause *= 0.6

        # Phil likes longer pauses for emphasis
        if speaker == "phil_dandy" and "importantly" in line["text"].lower():
            pause *= 1.3

        return pause

    def _calculate_wpm(self, line: Dict, directive: Dict) -> float:
        """Calculate words per minute based on DDE directive"""
        base_wpm = self.config["pacing_rules"]["sentence_rate_words_per_minute"].get(line["speaker"], 150)

        # Adjust based on energy level (higher energy = faster)
        energy = directive["energy"]
        if energy > 0.8:
            base_wpm *= 1.2  # Excited = faster
        elif energy < 0.6:
            base_wpm *= 0.8   # Calm = slower

        # Adjust for energy level from line
        line_energy = line.get("energy_level", self.config["phil_and_jim_chemistry"]["energy_symmetry"])
        adjusted_wpm = base_wpm * (0.8 + line_energy * 0.4)

        return adjusted_wpm

    def _calculate_duration(self, line: Dict, directive: Dict) -> float:
        """Calculate target duration based on DDE directive"""
        word_count = len(line["text"].split())
        wpm = self._calculate_wpm(line, directive)
        duration_seconds = (word_count / wpm) * 60

        # Adjust for energy (higher energy = shorter duration)
        energy = directive["energy"]
        if energy > 0.8:
            duration_seconds *= 0.9
        elif energy < 0.6:
            duration_seconds *= 1.1

        return duration_seconds

    def _calculate_energy_contour(self, line: Dict, directive: Dict) -> List[Tuple[float, float]]:
        """
        Energy curve over time: [(time_offset, energy_level), ...]
        Used to modulate phonatory parameters dynamically
        """
        duration = self._calculate_duration(line, directive)

        # Base energy from directive
        base_energy = directive["energy"]

        # Adjust for emphasis words - create energy spikes
        emphasis_positions = []
        words = line["text"].split()
        for i, word in enumerate(words):
            if word.lower().strip('.,!?') in [e.lower() for e in directive["emphasis"]]:
                emphasis_positions.append(i / len(words))  # Position as fraction

        # Build contour with emphasis spikes
        contour = [(0.0, base_energy * 0.8)]  # Opening: slightly below base

        # Add emphasis spikes
        for pos in emphasis_positions:
            time_point = duration * pos
            contour.append((time_point - 0.1, base_energy))  # Build up
            contour.append((time_point, base_energy * 1.2))   # Peak at emphasis
            contour.append((time_point + 0.1, base_energy))   # Settle back

        # Peak in middle if no emphasis
        if not emphasis_positions:
            contour.extend([
                (duration * 0.3, base_energy),     # Building
                (duration * 0.6, base_energy * 1.1), # Peak energy
            ])

        # Wind down at end
        contour.append((duration * 0.9, base_energy * 0.6))

        return contour


class TransitionEngine:
    """Handles smooth topic transitions and ad breaks"""

    def __init__(self, skg, config: Dict):
        self.skg = skg
        self.config = config

    def generate_transition(self, from_topic: str, to_topic: str, transition_type: str = "pivot") -> Dict:
        """Generate a smooth transition between topics"""

        if transition_type == "pivot":
            text = random.choice(self.config["transition_patterns"]["topic_pivots"])
        elif transition_type == "ad_break":
            text = random.choice(self.config["transition_patterns"]["ad_breaks"])
        else:
            text = "Moving on..."

        return {
            "speaker": "phil_dandy",  # Usually Phil handles transitions
            "text": text,
            "type": "transition",
            "pause_after": 1.0,
            "energy_level": 0.6,
            "directives": {
                "smooth_transition": True
            }
        }