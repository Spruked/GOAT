"""
SKG Validator - Ensures podcast configuration integrity
Validates SKG JSON against schema before production
"""

import json
import jsonschema
from pathlib import Path
from typing import Dict, Any
import sys


class SKGValidator:
    """Validates SKG configuration files against schema"""
    
    def __init__(self, schema_file: str = "skg/podcast_studio_schema.json"):
        """
        Initialize validator with schema
        
        Args:
            schema_file: Path to JSON schema file
        """
        self.schema = self._load_schema(schema_file)
    
    def _load_schema(self, schema_file: str) -> Dict[str, Any]:
        """Load JSON schema"""
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            return schema
        except FileNotFoundError:
            print(f"❌ Schema file not found: {schema_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in schema: {e}")
            sys.exit(1)
    
    def validate(self, config_file: str) -> bool:
        """
        Validate SKG configuration file
        
        Args:
            config_file: Path to SKG config JSON
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Load config
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate against schema
            jsonschema.validate(instance=config, schema=self.schema)
            
            # Additional validation rules
            self._validate_business_rules(config)
            
            print(f"✅ SKG configuration is valid: {config_file}")
            return True
            
        except FileNotFoundError:
            print(f"❌ Config file not found: {config_file}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in config: {e}")
            return False
        except jsonschema.ValidationError as e:
            print(f"❌ Schema validation failed:")
            print(f"   {e.message}")
            print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
            return False
        except ValueError as e:
            print(f"❌ Business rule validation failed: {e}")
            return False
    
    def _validate_business_rules(self, config: Dict[str, Any]):
        """
        Validate business rules beyond schema
        """
        # Rule: Episode type must match voice configuration
        episode_type = config['episode_structure']['episode_type']
        has_cohost = config['voice_config'].get('cohost') is not None
        has_guest = config['voice_config'].get('guest') is not None
        
        if episode_type == 'cohosted_conversation' and not has_cohost:
            raise ValueError("Episode type 'cohosted_conversation' requires cohost configuration")
        
        if episode_type == 'interview' and not has_guest:
            raise ValueError("Episode type 'interview' requires guest configuration")
        
        # Rule: Duration must be reasonable for episode type
        duration = config['episode_structure']['episode_duration']
        if episode_type == 'narrative_storytelling' and duration in ['5-10', '15-20']:
            print(f"⚠️  Warning: Narrative storytelling typically needs more than {duration} minutes")
        
        # Rule: Voice IDs must be different if multiple speakers
        host_voice = config['voice_config']['host']['voice_id']
        if has_cohost:
            cohost_voice = config['voice_config']['cohost']['voice_id']
            if host_voice == cohost_voice:
                print("⚠️  Warning: Host and cohost have the same voice ID")
        
        if has_guest:
            guest_voice = config['voice_config']['guest']['voice_id']
            if host_voice == guest_voice:
                print("⚠️  Warning: Host and guest have the same voice ID")
        
        # Rule: Explicit content flag vs distribution channels
        if config['distribution'].get('explicit_content', False):
            channels = config['distribution'].get('distribution_channels', [])
            if 'YouTube' in channels:
                print("⚠️  Warning: Explicit content may have restrictions on YouTube")


def main():
    """Command-line interface for SKG validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SKG Podcast Configuration Validator')
    parser.add_argument('--schema', default='skg/podcast_studio_schema.json', help='Path to schema file')
    parser.add_argument('--file', required=True, help='Path to SKG config JSON to validate')
    
    args = parser.parse_args()
    
    # Validate
    validator = SKGValidator(args.schema)
    is_valid = validator.validate(args.file)
    
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
