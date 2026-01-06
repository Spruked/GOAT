from .skg_manager import SpeakerKnowledgeGraph
from typing import List, Dict, Any
import random
import sys
from pathlib import Path

class DandyShowGenerator:
    def __init__(self, skg_manager: SpeakerKnowledgeGraph):
        self.skg = skg_manager

    def generate_episode_segment(self, topic: Dict[str, Any]) -> List[Dict]:
        """
        Generate a complete podcast segment for a topic

        topic: {
            "title": "User's AI Tool",
            "description": "Description...",
            "submitter": "@username",
            "category": "AI/ML",
            "key_points": ["machine learning", "automation"]
        }
        """
        # 1. Activate relevant guest persona
        self.skg.activate_standby_persona(topic.get("key_points", []))

        active_personas = self.skg.data["episode_state"]["active_personas"]

        # 2. Generate script segments
        segments = []

        # Opening: Phil introduces topic
        segments.append({
            "speaker": "phil_dandy",
            "text": self._generate_opening(topic),
            "type": "opening"
        })

        # Jim responds with enthusiasm
        segments.append({
            "speaker": "jim_dandy",
            "text": self._generate_response(topic, "phil_dandy"),
            "type": "reaction"
        })

        # Guest expert segment (if activated)
        if len(active_personas) > 2:
            guest_id = active_personas[2]
            segments.append({
                "speaker": guest_id,
                "text": self._generate_expert_insight(topic, guest_id),
                "type": "expert_commentary"
            })

            # Hosts react
            segments.append({
                "speaker": "phil_dandy",
                "text": f"Great point, {self.skg.get_persona(guest_id)['name']}. That connects to...",
                "type": "expert_reaction"
            })

        # Closing: Jim wraps up
        segments.append({
            "speaker": "jim_dandy",
            "text": self._generate_closing(topic),
            "type": "closing"
        })

        # 3. Generate audio for all segments
        audio_segments = []
        for segment in segments:
            try:
                audio_path = self.skg.synthesize_as_persona(
                    text=segment["text"],
                    persona_id=segment["speaker"]
                )
                audio_segments.append({
                    **segment,
                    "audio_path": audio_path,
                    "duration": self._get_audio_duration(audio_path)
                })
            except Exception as e:
                print(f"⚠️  Failed to generate audio for {segment['speaker']}: {e}")
                # Continue without audio for this segment
                audio_segments.append({
                    **segment,
                    "audio_path": None,
                    "duration": 0
                })

        return audio_segments

    def _generate_opening(self, topic: Dict) -> str:
        """Generate Phil's opening for the topic"""
        templates = [
            f"Jim, check this out—{topic['title']} from {topic.get('submitter', 'our community')}. This is right in our wheelhouse.",
            f"Welcome back! Today we're looking at {topic['title']}. Jim, you've got to see what {topic.get('submitter', 'someone')} built.",
            f"Oh man, Jim, this next one is a doozy. {topic['title']} - {topic.get('description', '')[:100]}..."
        ]
        return random.choice(templates)

    def _generate_response(self, topic: Dict, previous_speaker: str) -> str:
        """Generate Jim's enthusiastic response"""
        templates = [
            f"That's incredible! I love how {topic.get('submitter', 'they')} approached this.",
            f"Whoa, that's some next-level stuff. Tell me more about the {topic.get('category', 'technical')} side of it.",
            f"I'm already thinking about how we could apply this in our own work. The {topic.get('key_points', ['innovation'])[0]} aspect is brilliant!"
        ]
        return random.choice(templates)

    def _generate_expert_insight(self, topic: Dict, guest_id: str) -> str:
        """Generate guest expert commentary"""
        guest = self.skg.get_persona(guest_id)
        expertise = guest["persona_traits"]["expertise"][0]

        templates = [
            f"As someone who specializes in {expertise}, I can tell you that {topic['title']} represents a significant advancement in the field.",
            f"From a {expertise} perspective, what's really impressive about {topic['title']} is how it addresses the core challenges.",
            f"I've been following developments in this area, and {topic['title']} does something quite unique with {topic.get('key_points', ['the approach'])[0]}."
        ]
        return random.choice(templates)

    def _generate_closing(self, topic: Dict) -> str:
        """Generate Jim's closing remarks"""
        return f"Fantastic stuff from {topic.get('submitter', 'the community')}. If you're working on something cool, submit it at our website. Phil, what else we got?"

    def _get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_wav(audio_path)
            return len(audio) / 1000.0  # Convert ms to seconds
        except ImportError:
            print("⚠️  pydub not available for duration calculation")
            return 0.0
        except Exception as e:
            print(f"⚠️  Could not get duration for {audio_path}: {e}")
            return 0.0