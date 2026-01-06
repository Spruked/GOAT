"""
SKG Podcast Orchestrator - Production Engine for Podcast Studio
Uses Structured Knowledge Graph to produce professional podcast episodes
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from podcast_engine.podcast_engine import PodcastEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SKGPodcastOrchestrator:
    """
    Orchestrates podcast production using SKG configuration
    This is the production bible that Caleon reads
    """
    
    def __init__(self, skg_config_path: str):
        """
        Initialize orchestrator with SKG configuration
        
        Args:
            skg_config_path: Path to podcast studio SKG JSON
        """
        self.skg_config = self._load_skg(skg_config_path)
        self.validate_skg()
        
        # Initialize podcast engine
        self.engine = PodcastEngine()
        
        logger.info(f"SKG Podcast Orchestrator initialized")
    
    def _load_skg(self, config_path: str) -> Dict[str, Any]:
        """Load SKG configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"Loaded SKG config from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"SKG config not found: {config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in SKG config: {e}")
            raise
    
    def validate_skg(self) -> bool:
        """
        Validate SKG configuration against schema
        Ensures all required fields are present
        """
        required_sections = [
            'metadata',
            'show_identity',
            'episode_structure',
            'voice_config',
            'tone_style',
            'audio_production',
            'content_structure',
            'distribution'
        ]
        
        for section in required_sections:
            if section not in self.skg_config:
                raise ValueError(f"Missing required SKG section: {section}")
        
        # Validate episode type matches voice config
        episode_type = self.skg_config['episode_structure']['episode_type']
        has_cohost = self.skg_config['voice_config'].get('cohost') is not None
        has_guest = self.skg_config['voice_config'].get('guest') is not None
        
        if episode_type == 'cohosted_conversation' and not has_cohost:
            logger.warning("Episode type is 'cohosted_conversation' but no cohost configured")
        
        if episode_type == 'interview' and not has_guest:
            logger.warning("Episode type is 'interview' but no guest configured")
        
        logger.info("SKG validation passed")
        return True
    
    def produce_episode(self, user_content: Optional[Dict[str, Any]] = None, output_path: str = None) -> str:
        """
        Produce complete podcast episode using SKG configuration
        
        Args:
            user_content: Optional additional content from user submission
            output_path: Where to save the final audio file
            
        Returns:
            Path to produced audio file
        """
        logger.info("Starting podcast production...")
        
        # Merge user content with SKG config
        production_config = self._prepare_production_config(user_content)
        
        # Generate script
        script = self._generate_script(production_config)
        
        # Synthesize voices
        audio_segments = self._synthesize_voices(script, production_config)
        
        # Apply audio production (music, effects, mastering)
        final_audio = self._apply_audio_production(audio_segments, production_config)
        
        # Export final episode
        output_file = self._export_episode(final_audio, output_path)
        
        # Update SKG with production metadata
        self._update_production_metadata(output_file)
        
        logger.info(f"Podcast production complete: {output_file}")
        return output_file
    
    def _prepare_production_config(self, user_content: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge SKG configuration with user-provided content
        User content overrides SKG for this specific episode
        """
        config = self.skg_config.copy()
        
        if user_content:
            # User content can override episode-specific fields
            if 'episode_title' in user_content:
                config['episode_structure']['episode_title'] = user_content['episode_title']
            
            if 'opening_hook' in user_content:
                config['content_structure']['opening_hook'] = user_content['opening_hook']
            
            if 'episode_outline' in user_content:
                config['content_structure']['episode_outline'] = user_content['episode_outline']
            
            if 'key_talking_points' in user_content:
                config['content_structure']['key_talking_points'] = user_content['key_talking_points']
            
            logger.info("Merged user content with SKG config")
        
        return config
    
    def _generate_script(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate podcast script
        Follows tone, style, and content structure from SKG
        """
        logger.info("Generating script...")
        
        # Extract configuration for script generation
        episode_type = config['episode_structure']['episode_type']
        conversation_style = config['tone_style']['conversation_style']
        pacing = config['tone_style'].get('pacing', 'Moderate')
        
        # Build prompt context
        prompt_context = {
            'show_title': config['show_identity']['show_title'],
            'episode_title': config['episode_structure']['episode_title'],
            'episode_type': episode_type,
            'conversation_style': conversation_style,
            'pacing': pacing,
            'formality': config['tone_style'].get('formality', 'Semi-Formal'),
            'opening_hook': config['content_structure'].get('opening_hook', ''),
            'episode_outline': config['content_structure'].get('episode_outline', ''),
            'key_talking_points': config['content_structure'].get('key_talking_points', ''),
            'closing_statement': config['content_structure'].get('closing_statement', ''),
            'host_name': config['voice_config']['host']['name'],
            'cohost_name': config['voice_config'].get('cohost', {}).get('name'),
            'guest_name': config['voice_config'].get('guest', {}).get('name'),
            'duration': config['episode_structure']['episode_duration']
        }
        
        # Generate script using engine
        script = self.engine.generate_script(prompt_context)
        
        logger.info(f"Script generated: {len(script.get('segments', []))} segments")
        return script
    
    def _synthesize_voices(self, script: Dict[str, Any], config: Dict[str, Any]) -> list:
        """
        Synthesize voice audio for each script segment
        Uses voice configuration from SKG
        """
        logger.info("Synthesizing voices...")
        
        audio_segments = []
        voice_config = config['voice_config']
        
        for segment in script.get('segments', []):
            speaker = segment.get('speaker', 'host')
            text = segment.get('text', '')
            
            # Get voice config for this speaker
            if speaker == 'host':
                voice_id = voice_config['host']['voice_id']
                speaking_rate = voice_config['host'].get('speaking_rate', 1.0)
            elif speaker == 'cohost' and voice_config.get('cohost'):
                voice_id = voice_config['cohost']['voice_id']
                speaking_rate = voice_config['cohost'].get('speaking_rate', 1.0)
            elif speaker == 'guest' and voice_config.get('guest'):
                voice_id = voice_config['guest']['voice_id']
                speaking_rate = 1.0
            else:
                logger.warning(f"Unknown speaker: {speaker}, using host voice")
                voice_id = voice_config['host']['voice_id']
                speaking_rate = 1.0
            
            # Synthesize audio
            audio = self.engine.synthesize_speech(
                text=text,
                voice_id=voice_id,
                speaking_rate=speaking_rate
            )
            
            audio_segments.append({
                'audio': audio,
                'speaker': speaker,
                'text': text,
                'duration': len(audio) / 44100  # Assuming 44.1kHz
            })
        
        logger.info(f"Synthesized {len(audio_segments)} audio segments")
        return audio_segments
    
    def _apply_audio_production(self, segments: list, config: Dict[str, Any]) -> bytes:
        """
        Apply audio production elements:
        - Intro/outro music
        - Transitions
        - Background music bed
        - Sound effects
        - Mastering (compression, EQ, normalization)
        """
        logger.info("Applying audio production...")
        
        audio_prod = config['audio_production']
        
        # Build final audio sequence
        final_sequence = []
        
        # Add intro music
        intro_config = audio_prod.get('intro_music', {})
        if intro_config.get('style') != 'None':
            logger.info(f"Adding intro music: {intro_config.get('style')}")
        
        # Add voice segments
        for segment in segments:
            final_sequence.append(('voice', segment['audio']))
        
        # Add outro music
        outro_config = audio_prod.get('outro_music', {})
        if outro_config.get('style') != 'None':
            logger.info(f"Adding outro music: {outro_config.get('style')}")
        
        # Combine and master
        combined_audio = self._combine_audio_segments(final_sequence)
        mastered_audio = self._apply_mastering(combined_audio, audio_prod.get('mastering_profile', {}))
        
        logger.info("Audio production complete")
        return mastered_audio
    
    def _combine_audio_segments(self, sequence: list) -> bytes:
        """Combine audio segments into single stream"""
        logger.info(f"Combining {len(sequence)} audio segments")
        # TODO: Use pydub or similar
        return b''  # Placeholder
    
    def _apply_mastering(self, audio: bytes, mastering_profile: Dict[str, Any]) -> bytes:
        """Apply mastering profile to final audio"""
        target_lufs = mastering_profile.get('target_lufs', -16)
        logger.info(f"Applying mastering: LUFS={target_lufs}")
        # TODO: Integrate with audio processing library
        return audio
    
    def _export_episode(self, audio: bytes, output_path: Optional[str]) -> str:
        """Export final episode to file"""
        if not output_path:
            episode_title = self.skg_config['episode_structure']['episode_title']
            safe_title = "".join(c for c in episode_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_path = f"podcasts/{safe_title.replace(' ', '_')}.wav"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(audio)
        
        logger.info(f"Episode exported to: {output_path}")
        return output_path
    
    def _update_production_metadata(self, output_file: str):
        """Update SKG with production metadata"""
        self.skg_config['metadata']['last_modified'] = datetime.utcnow().isoformat()
        
        if 'production_history' not in self.skg_config:
            self.skg_config['production_history'] = []
        
        self.skg_config['production_history'].append({
            'timestamp': datetime.utcnow().isoformat(),
            'output_file': output_file,
            'episode_title': self.skg_config['episode_structure']['episode_title']
        })
        
        logger.info("Production metadata updated")


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SKG Podcast Orchestrator')
    parser.add_argument('--skg-studio', action='store_true', help='Use SKG Studio mode')
    parser.add_argument('--config', required=True, help='Path to SKG config JSON')
    parser.add_argument('--content', help='Path to user content JSON (optional)')
    parser.add_argument('--output', help='Output audio file path')
    
    args = parser.parse_args()
    
    # Load user content if provided
    user_content = None
    if args.content:
        with open(args.content, 'r') as f:
            user_content = json.load(f)
    
    # Initialize orchestrator
    orchestrator = SKGPodcastOrchestrator(args.config)
    
    # Produce episode
    output_file = orchestrator.produce_episode(user_content, args.output)
    
    print(f"\n✅ Podcast episode produced!")
    print(f"📁 Output: {output_file}")


if __name__ == '__main__':
    main()
