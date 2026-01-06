"""
Podcast API Routes - SKG-Powered Endpoint
Receives form data from frontend and orchestrates production using SKG
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import json
import os
from pathlib import Path

# Import SKG orchestrator and POM
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    sys.path.insert(0, str(Path(__file__).parent.parent / "Phonatory_Output_Module"))
    from skg_podcast_orchestrator import SKGPodcastOrchestrator
    from phonitory_output_module import PhonatoryOutputModule
    SKG_AVAILABLE = True
    POM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Import warning: {e}")
    SKG_AVAILABLE = False
    POM_AVAILABLE = False

router = APIRouter(prefix="/api/podcast", tags=["podcast"])

# Initialize POM singleton
_pom_instance = None

def get_pom_instance():
    """Get or create POM instance (Phonatory Output Module)"""
    global _pom_instance
    if _pom_instance is None and POM_AVAILABLE:
        try:
            _pom_instance = PhonatoryOutputModule()
            print("✅ Phonatory Output Module initialized")
        except Exception as e:
            print(f"⚠️  POM initialization failed: {e}")
    return _pom_instance


# ===== Request Models =====

class PodcastCreationRequest(BaseModel):
    """Request model matching frontend form data"""
    
    # Show Identity
    showTitle: str = Field(..., min_length=3, max_length=200)
    showTagline: Optional[str] = None
    showDescription: Optional[str] = None
    showCategory: Optional[str] = None
    
    # Episode Details
    episodeTitle: str = Field(..., min_length=3)
    episodeNumber: Optional[str] = None
    seasonNumber: Optional[str] = None
    episodeType: str = Field(..., description="Episode format type")
    episodeDuration: str = Field(..., description="Episode duration range")
    
    # Voice Configuration
    hostVoice: str = Field(..., description="Host voice ID")
    hostName: str
    coHostVoice: Optional[str] = None
    coHostName: Optional[str] = None
    hasCoHost: bool = False
    guestVoice: Optional[str] = None
    guestName: Optional[str] = None
    hasGuest: bool = False
    
    # Tone & Style
    conversationStyle: Optional[str] = None
    pacing: Optional[str] = None
    energyLevel: Optional[str] = None
    formality: Optional[str] = None
    
    # Audio Production
    introMusicStyle: Optional[str] = None
    outroMusicStyle: Optional[str] = None
    transitionStyle: Optional[str] = None
    includeIntro: bool = True
    includeOutro: bool = True
    includeMusicBed: bool = False
    soundEffects: bool = False
    
    # Content Structure
    episodeOutline: str
    keyTalkingPoints: Optional[str] = None
    openingHook: Optional[str] = None
    closingStatement: Optional[str] = None
    researchSources: Optional[str] = None
    
    # Distribution
    targetAudience: Optional[str] = None
    targetListenerLevel: Optional[str] = None
    callToAction: Optional[str] = None
    sponsorMention: Optional[str] = None
    distributionChannels: List[str] = []
    explicitContent: bool = False
    episodeTags: Optional[str] = None


# ===== Helper Functions =====

def form_data_to_skg(form_data: PodcastCreationRequest) -> dict:
    """
    Convert frontend form data to SKG JSON format
    This bridges the UI to the production engine
    """
    skg_config = {
        "metadata": {
            "schema_version": "1.0.0",
            "created_at": datetime.utcnow().isoformat(),
            "last_modified": datetime.utcnow().isoformat(),
            "production_engine": "caleon",
            "mastery_score": 0
        },
        "show_identity": {
            "show_title": form_data.showTitle,
            "show_tagline": form_data.showTagline or "",
            "show_description": form_data.showDescription or "",
            "show_category": form_data.showCategory or "Society & Culture",
            "show_language": "en-US"
        },
        "episode_structure": {
            "episode_title": form_data.episodeTitle,
            "episode_number": form_data.episodeNumber or "",
            "season_number": form_data.seasonNumber or "",
            "episode_type": form_data.episodeType,
            "episode_duration": form_data.episodeDuration,
            "release_schedule": "single",
            "episode_format_rules": {
                "max_intro_duration_seconds": 30,
                "max_outro_duration_seconds": 45,
                "allow_mid_roll_breaks": False,
                "segment_count": 3
            }
        },
        "voice_config": {
            "host": {
                "name": form_data.hostName,
                "voice_id": form_data.hostVoice,
                "voice_provider": "elevenlabs",
                "speaking_rate": 1.0,
                "pitch_adjustment": 0
            },
            "dialogue_rules": {
                "min_turn_length_words": 20,
                "max_turn_length_words": 150,
                "allow_interruptions": False,
                "natural_overlap_percentage": 5
            }
        },
        "tone_style": {
            "conversation_style": form_data.conversationStyle or "Professional & Polished",
            "pacing": form_data.pacing or "Moderate",
            "energy_level": form_data.energyLevel or "Balanced",
            "formality": form_data.formality or "Semi-Formal",
            "language_rules": {
                "vocabulary_level": "conversational",
                "use_contractions": True,
                "allow_slang": False,
                "max_sentence_length_words": 25
            }
        },
        "audio_production": {
            "intro_music": {
                "style": form_data.introMusicStyle or "None",
                "duration_seconds": 15,
                "fade_duration_seconds": 3,
                "volume_db": -18
            },
            "outro_music": {
                "style": form_data.outroMusicStyle or "None",
                "duration_seconds": 20,
                "fade_duration_seconds": 5,
                "volume_db": -18
            },
            "transition_style": form_data.transitionStyle or "Smooth Fade",
            "background_music_bed": {
                "enabled": form_data.includeMusicBed,
                "volume_db": -35,
                "style": "ambient" if form_data.includeMusicBed else "none"
            },
            "sound_effects": {
                "enabled": form_data.soundEffects,
                "types_allowed": ["transition", "emphasis"] if form_data.soundEffects else []
            },
            "mastering_profile": {
                "target_lufs": -16,
                "compression_ratio": 3,
                "eq_preset": "podcast_standard",
                "noise_reduction_level": "moderate"
            }
        },
        "content_structure": {
            "opening_hook": form_data.openingHook or "",
            "episode_outline": form_data.episodeOutline,
            "key_talking_points": form_data.keyTalkingPoints or "",
            "research_sources": form_data.researchSources or "",
            "closing_statement": form_data.closingStatement or "",
            "scriptwriting_rules": {
                "write_full_script": False,
                "bullet_points_only": True,
                "allow_improvisation": True,
                "maintain_natural_flow": True
            }
        },
        "distribution": {
            "target_audience": form_data.targetAudience or "",
            "listener_experience_level": form_data.targetListenerLevel or "Mixed (All levels welcome)",
            "distribution_channels": form_data.distributionChannels,
            "episode_tags": [tag.strip() for tag in (form_data.episodeTags or "").split(",") if tag.strip()],
            "call_to_action": form_data.callToAction or "",
            "sponsor_mention": form_data.sponsorMention or "",
            "explicit_content": form_data.explicitContent
        }
    }
    
    # Add cohost if present
    if form_data.hasCoHost and form_data.coHostVoice:
        skg_config["voice_config"]["cohost"] = {
            "name": form_data.coHostName,
            "voice_id": form_data.coHostVoice,
            "voice_provider": "elevenlabs",
            "speaking_rate": 1.0,
            "pitch_adjustment": 0
        }
    
    # Add guest if present
    if form_data.hasGuest and form_data.guestVoice:
        skg_config["voice_config"]["guest"] = {
            "name": form_data.guestName,
            "voice_id": form_data.guestVoice,
            "voice_provider": "elevenlabs"
        }
    
    return skg_config


# ===== API Endpoints =====

@router.post("/create")
async def create_podcast(request: PodcastCreationRequest):
    """
    Create professional podcast using SKG + Harmonizer + POM architecture
    
    Flow:
    1. Frontend form data → SKG configuration
    2. GPT4All (local CPU) generates symbolic script from SKG
    3. SKG passes to Gyro-Cortical Harmonizer
    4. Harmonizer decides tone, pitch, cadence parameters
    5. POM (Coqui TTS) synthesizes voice with phonatory control
    6. Return audio + SKG reference
    
    GPT4All reasons. SKG remembers. Harmonizer decides tone. POM speaks.
    """
    if not SKG_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="SKG Orchestrator not available"
        )
    
    if not POM_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Phonatory Output Module not available"
        )
    
    try:
        import uuid
        podcast_id = str(uuid.uuid4())
        
        # Step 1: Build SKG from form data
        skg_config = form_data_to_skg(request)
        skg_config['metadata']['podcast_id'] = podcast_id
        
        # Step 2: Save SKG to disk (production bible)
        skg_dir = Path("skg/productions")
        skg_dir.mkdir(parents=True, exist_ok=True)
        skg_path = skg_dir / f"podcast_{podcast_id}.json"
        
        with open(skg_path, 'w', encoding='utf-8') as f:
            json.dump(skg_config, f, indent=2)
        
        print(f"✅ SKG saved: {skg_path}")
        
        # Step 3: Initialize orchestrator with this SKG
        orchestrator = SKGPodcastOrchestrator(str(skg_path))
        
        # Step 4: Generate symbolic script using GPT4All (local CPU)
        # GPT4All reads SKG and produces text/structure
        # It does NOT decide tone, pitch, or emotion - that's Harmonizer's job
        # It does NOT produce audio - that's POM's job
        script_data = orchestrator._generate_script(skg_config)
        
        print(f"✅ Symbolic script generated by GPT4All")
        
        # Step 5: Get POM instance
        pom = get_pom_instance()
        if not pom:
            raise HTTPException(
                status_code=503,
                detail="POM not initialized"
            )
        Gyro-Cortical Harmonizer decides tone/emotion
        # Harmonizer reads SKG and determines phonatory parameters
        # TODO: Initialize Harmonizer here
        # harmonizer = GyroCoricalHarmonizer(skg_config)
        
        # Step 7: POM synthesizes voice using Harmonizer's parameters
        # This is where Coqui TTS creates actual audio
        # Using proper phonatory control (pitch, cadence, formants)
        output_dir = Path(f"deliverables/podcasts/{podcast_id}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        audio_segments = []
        for segment in script_data['segments']:
            # Get voice config from SKG
            speaker = segment.get('speaker', 'host')
            voice_config = skg_config['voice_config'].get(speaker, skg_config['voice_config']['host'])
            
            # Harmonizer would determine these parameters based on context:
            # - Emotional tone for this segment
            # - Pitch modulation strategy
            # - Cadence/pacing adjustments
            # For now, using SKG config directly
            
            # POM phonates using Coqui TTS with proper vocal tract simulation
            # This is NOT generic TTS - it's biological voice synthesis
            segment_audio_path = pom.phonate(
                text=segment['text'],
                pitch_factor=voice_config.get('pitch_adjustment', 1.0),
                # Add formant/articulation if available in SKG
            )
            
            audio_segments.append(segment_GPT4All → SKG → Harmonizer → POM",
            "architecture": {
                "reasoning": "GPT4All (local CPU)",
                "memory": "Structured Knowledge Graph",
                "tone": "Gyro-Cortical HarmonizerTTS)")
        
        # Step 7: Return production data
        return JSONResponse({
            "success": True,
            "podcast_id": podcast_id,
            "skg_path": str(skg_path),
            "audio_segments": audio_segments,
            "message": "Podcast produced: LLM → SKG → POM",
            "architecture": {
                "llm": "GPT4All (Nous Hermes)",
                "skg": "Structured Knowledge Graph",
                "voice": "POM (Coqui TTS)"
            }
        })
        
    except Exception as e:
        print(f"❌ Production failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Podcast production failed: {str(e)}"
        )
    Flow:
    1. Convert form data to SKG format
    2. Save SKG config to file
    3. Initialize orchestrator with SKG
    4. Produce episode
    5. Return production result
    """
    
    if not SKG_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="SKG Orchestrator not available"
        )
    
    try:
        # Convert form data to SKG format
        skg_config = form_data_to_skg(request)
        
        # Save SKG config
        config_dir = Path("skg/configs/podcasts")
        config_dir.mkdir(parents=True, exist_ok=True)
        
        episode_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        config_file = config_dir / f"podcast_{episode_id}.json"
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(skg_config, f, indent=2, ensure_ascii=False)
        
        # Initialize orchestrator
        orchestrator = SKGPodcastOrchestrator(str(config_file))
        
        # Produce episode
        output_path = f"podcasts/{request.showTitle.replace(' ', '_')}_{episode_id}.wav"
        result_file = orchestrator.produce_episode(output_path=output_path)
        
        return JSONResponse(content={
            "success": True,
            "episode_id": episode_id,
            "skg_config_path": str(config_file),
            "output_file": result_file,
            "episode_title": request.episodeTitle,
            "show_title": request.showTitle,
            "message": "Podcast episode produced successfully"
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Podcast production failed: {str(e)}"
        )


@router.get("/voices")
async def get_available_voices():
    """
    Get list of available voices for podcast production
    """
    # TODO: Integrate with actual voice provider API
    voices = [
        {"id": "voice_1", "name": "Alex", "gender": "male", "style": "professional"},
        {"id": "voice_2", "name": "Sarah", "gender": "female", "style": "warm"},
        {"id": "voice_3", "name": "Marcus", "gender": "male", "style": "authoritative"},
        {"id": "voice_4", "name": "Emma", "gender": "female", "style": "conversational"},
        {"id": "voice_5", "name": "David", "gender": "male", "style": "friendly"},
        {"id": "voice_6", "name": "Sofia", "gender": "female", "style": "energetic"}
    ]
    
    return {"voices": voices}


@router.get("/config/{episode_id}")
async def get_episode_config(episode_id: str):
    """
    Retrieve SKG configuration for a specific episode
    """
    config_file = Path(f"skg/configs/podcasts/podcast_{episode_id}.json")
    
    if not config_file.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episode configuration not found"
        )
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config
