# Speaker Knowledge Graph (SKG) - Phil & Jim Dandy Show

The SKG system manages voice personas and conversation flow for authentic podcast generation using the Phonatory Output Module.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  GOAT Content   │───▶│  Dandy Show      │───▶│  Phonatory TTS  │
│   Ingestor      │    │  Generator       │    │   Engine        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Speaker KG      │
                       │  (JSON Graph)    │
                       └──────────────────┘
```

## Core Components

### 1. `skg_core.json` - Persona Knowledge Graph
- **Primary Personas**: Phil Dandy, Jim Dandy (cloned voices)
- **Standby Personas**: Tech Expert, Creative Director, Community Manager (Coqui presets)
- **Voice Profiles**: Pitch, rate, formant shifts, reference audio
- **Persona Traits**: Expertise, tone, catchphrases, conversation style

### 2. `skg_manager.py` - SKG Controller
- Loads and manages the persona graph
- Initializes voice cloning and caching
- Provides persona-aware speech synthesis
- Handles dynamic persona activation

### 3. `dandy_show_generator.py` - Podcast Director
- Generates conversation segments based on topics
- Manages dialogue flow between personas
- Activates relevant guest experts automatically
- Produces structured podcast content

### 4. `goat_podcast_pipeline.py` - Main Pipeline
- Integrates with GOAT content system
- Orchestrates full podcast production
- Handles audio concatenation and packaging

## Quick Start

### 1. Setup Environment
```bash
# Linux/Mac
./setup_skg.sh

# Windows
setup_skg.bat
```

### 2. Add Voice Reference Audio
Place high-quality voice samples in `podcast_engine/coqui/reference_audio/`:
- `phil_sample1.wav` (2-3 minutes)
- `phil_sample2.wav` (different context)
- `jim_sample1.wav` (2-3 minutes)
- `jim_sample2.wav` (different context)

### 3. Test the System
```bash
cd podcast_engine
python goat_podcast_pipeline.py --test
```

### 4. Generate Podcast
```bash
python goat_podcast_pipeline.py
```

## Persona Tuning

Use the CLI tuner for quick adjustments:

```bash
# Adjust Phil's pitch
python persona_tuner.py phil_dandy base_pitch 0.98

# Make Jim speak faster
python persona_tuner.py jim_dandy speaking_rate 1.05

# Fine-tune formants
python persona_tuner.py phil_dandy formant_f1 1.02

# List all personas
python persona_tuner.py list

# Show persona details
python persona_tuner.py show phil_dandy
```

## Integration with GOAT

The SKG system integrates seamlessly with the existing GOAT podcast engine:

```python
from podcast_engine import PodcastEngine

# Initialize with SKG support
engine = PodcastEngine(use_ucm=True, use_dals=True)

# Generate podcast with SKG personas
result = engine.create_legacy(user_input)
```

## Voice Cloning Best Practices

### Reference Audio Requirements
- **Duration**: 2-3 minutes per sample
- **Quality**: 48kHz, 24-bit WAV
- **Content**: Natural conversation, varied emotions
- **Environment**: Quiet recording space
- **Multiple Samples**: Different contexts/speaking styles

### Coqui XTTS v2 Features Used
- Native multi-speaker support
- Voice cloning with reference audio
- Persistent voice caching
- Real-time synthesis optimization

## Advanced Features

### Dynamic Persona Activation
The system automatically activates guest personas based on topic keywords:
- "AI", "machine learning" → Tech Expert
- "design", "brand" → Creative Director
- "community", "users" → Community Manager

### Conversation Flow Control
- **Phil**: Challenger style, analytical tone
- **Jim**: Supporter style, enthusiastic tone
- **Guests**: Domain-specific expertise with contextual insights

### Audio Production Pipeline
1. Generate individual voice segments
2. Concatenate with transition audio
3. Add intro/outro music
4. Export final podcast with metadata

## Troubleshooting

### Common Issues

**"Phonatory Output Module not available"**
- Ensure Phonatory_Output_Module is cloned in the parent directory
- Check Python path and imports

**"Reference audio not found"**
- Verify audio files are in `coqui/reference_audio/`
- Ensure proper WAV format (48kHz, 24-bit)

**"Voice cloning failed"**
- Check reference audio quality and duration
- Verify Coqui TTS installation

### Performance Optimization
- Voice caching reduces synthesis time for repeated personas
- Batch processing for multiple segments
- Memory management for long-form content

## API Reference

### SpeakerKnowledgeGraph
```python
skg = SpeakerKnowledgeGraph()
audio_path = skg.synthesize_as_persona(text, persona_id)
persona = skg.get_persona(persona_id)
guest = skg.activate_standby_persona(keywords)
```

### DandyShowGenerator
```python
generator = DandyShowGenerator(skg)
segments = generator.generate_episode_segment(topic_dict)
```

### Pipeline Functions
```python
output_file = generate_weekly_podcast(topics, test_mode=False)
setup_skg_environment()
```

## Future Enhancements

- **Web-based Persona Editor**: GUI for voice tuning
- **Conversation Templates**: Pre-built dialogue structures
- **Real-time Adaptation**: Dynamic persona switching
- **Multi-language Support**: Extended language personas
- **Emotion Modeling**: Context-aware emotional expression