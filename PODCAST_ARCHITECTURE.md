# GOAT Podcast Production Architecture

## The Core Rule

> **The local GPT4All model reasons.**  
> **The SKG remembers.**  
> **The Harmonizer decides tone.**  
> **The POM speaks.**

## System Components

### 1. GPT4All (Local CPU Model)
**Location:** CPU-local (NOT Ollama, NOT Hermes, NOT OpenAI, NOT Claude)  
**Runtime:** GPT4All  
**Model:** Local CPU-optimized model selected for speed  
**Responsibility:**
- Text reasoning
- Content drafting
- Content structuring
- Symbolic intent generation
- SKG population

**NOT Responsible For:**
- Voice synthesis
- Pitch/cadence control
- Emotional audio delivery
- Raw audio output
- Tone decisions (that's Harmonizer)

### 2. SKG (Structured Knowledge Graph)
**Location:** `skg/podcast_studio_skg.json`  
**Responsibility:**
- Production bible (7 pillars)
- Configuration storage
- LLM → POM bridge
- Analytics feedback loop

**Structure:**
1. Show Identity
2. Episode Structure
3. Voice Config
4. Tone & Style
5. Audio Production
6. Content Structure
7. Distribution

### 3. POM (Phonatory Output Module)
**Location:** `Phonatory_Output_Module/`  
**Technology:** Coqui TTS (NOT generic TTS)  
**Responsibility:**
- Voice synthesis
- Pitch control
- Cadence timing
- Formant shaping
- Articulation
- Vocal tract simulation

**Biological Components:**
- Larynx simulation
- Formant filter
- Tongue articulation
- Lip control
- Uvula control

### 4. Gyro-Cortical Harmonizer
**Location:** Between SKG and POM  
**Responsibility:**
- Tone decisions
- Emotional modulation
- Pre-audio signal processing
- Cadence/pitch guidance
- Feeds parameters to POM

**NOT Responsible For:**
- Content generation (that's GPT4All)
- Audio synthesis (that's POM)

## Production Flow

```
┌─────────────────────────────────────────────────────────────┐
│ Frontend Form (Podcast Page)                                │
│ - Show title, episode details, voice selections             │
│ - Content outline, talking points                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ POST /api/podcast/create
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ Backend API (podcast_api.py)                                │
│ - Receives form data                                        │
│ - Builds SKG configuration                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ form_data → skg_config.json
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ SKG (Structured Knowledge Graph)                            │
│ - Production bible saved to disk                            │
│ - 7 pillars of podcast configuration                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ SKG → Orchestrator
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ SKG Podcast Orchestrator                                    │
│ - Reads SKG                                                 │
│ GPT4All (Local CPU Model)                                   │
│ - Generates script text                                     │
│ - Structures talking points                                 │
│ - Produces SYMBOLIC output only                             │
│ - NO AUDIO GENERATION                                       │
│ - NO TONE DECISIONS                                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Symbolic script → Orchestrator
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ SKG Orchestrator                                            │
│ - Receives symbolic script                                  │
│ - Reads voice config from SKG                               │
│ - Passes to Gyro-Cortical Harmonizer                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Script + SKG Config → Harmonizer
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ Gyro-Cortical Harmonizer                                    │
│ - Decides tone/emotion for this segment                     │
│ - Determines pitch modulation strategy                      │
│ - Calculates cadence parameters                             │
│ - Prepares phonatory instructions                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Text + Phonatory Parameters → POM        │
│ - Structures talking points                                 │
│ - Produces SYMBOLIC output only                             │
│ - NO AUDIO GENERATION                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Symbolic script → Orchestrator
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ SKG Orchestrator                                            │
│ - Receives symbolic script                                  │
│ - Reads voice config from SKG                               │
│ - Passes to POM with phonatory parameters                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Text + Voice Config → POM
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ POM (Phonatory Output Module)                               │
│ - Receives text + voice parameters                          │
│ - Uses Coqui TTS (biological voice model)                   │
│ - Applies:                                                  │
│   * PitGPT4All Does
✅ Generate text content  
✅ Structure episodes  
✅ Write dialogue  
✅ Create outlines  
✅ Populate SKG  
✅ Reason symbolically  

### What GPT4All Does NOT Do
❌ Generate voice audio  
❌ Control pitch  
❌ Control cadence  
❌ Decide tone/emotion  
❌ Direct TTS synthesis  
❌ Make audio decisions

### What Gyro-Cortical Harmonizer Does
✅ Decide tone for each segment  
✅ Determine emotional modulation  
✅ Calculate pitch parameters  
✅ Set cadence/pacing  
✅ Prepare phonatory instructions  

### What Harmonizer Does NOT Do
❌ Generate text content  
❌ Synthesize audio (that's POM)  
❌ Structure episodes (that's GPT4All) synthesis                              │
│ - Proper phonatory control                                  │
│ - Distribution-ready audio                                  │
└─────────────────────────────────────────────────────────────┘
```

## Critical Boundaries

### What LLM Does
✅ Generate text content  
✅ Structure episodes  
✅ Write dialogue  
✅ Create outlines  
✅ Populate SKG  

### What LLM Does NOT Do
❌ Generate voice audio  
❌ Control pitch  
❌ Control cadence  
❌ Control emotion in audio  
❌ Direct TTS synthesis  

### What POM Does
✅ Synthesize voice (Coqui TTS)  
✅ Control pitch (larynx simulation)  
✅ Control cadence (speaking rate)  
✅ Shape formants (vowel quality)  
✅ Articulation control  
✅ Nasalization control  

### What POM Does NOT Do
❌ Generate script text  
❌ Make content decisions  
❌ Structure episodes  
❌ Choose topics  

## Caleon's Role

**Position:** Supervisory  
**Intervention:** Only for:
- Issues/errors in production
- User escalations
- Quality control failures

**NOT Involved In:**
- Standard production flow
- Routine episode generation
- Normal SKG reading

Caleon watches. She doesn't produce routinely.

## File Structure

```
GOAT/
├── skg/
│   ├── podcast_studio_skg.json          # Base template
│   └── productions/
│       └── podcast_[uuid].json          # Per-episode SKG
├── Phonatory_Output_Module/
│   ├── phonitory_output_module.py       # Main POM entry
│   ├── larynx_sim.py                    # Pitch control
│   ├── formant_filter.py                # Vowel shaping
│   ├── tongue_artic.py                  # Articulation
│   ├── lip_control.py                   # Lip movements
│   └── uvula_control.py                 # Nasalization
├── skg_podcast_orchestrator.py          # SKG → POM bridge
├── routes/
│   └── podcast_api.py                   # API endpoint
└── frontend/src/pages/
    └── PodcastPage.jsx                  # User interface
```

## Integration Points

### 1. Frontend → Backend
**Endpoint:** `POST /api/podcast/create`  
**Payload:** Form data (show details, episode config, voice selections)  
**Returns:** `{podcast_id, skg_path, audio_path}`

### 2. Backend → SKG
**Action:** Build JSON configuration from form data  
**Output:** `skg/productions/podcast_[uuid].json`

### 3. SKG → LLM
**Action:** Orchestrator reads SKG, provides context to LLM  
**LLM Output:** Symbolic script (plain text, structure)

### 4. LLM Output → POM
**Action:** Orchestrator passes text + voice config to POM  
**POM Input:** `text, pitch_factor, speaking_rate, formant_target, articulation`  
**POM Output:** WAV audio file

## Voice Configuration in SKG

```json
{
  "voice_config": {
    "host": {
      "name": "Alex Johnson",
      "voice_id": "ljspeech",
      "pom_config": {
        "model": "tts_models/en/ljspeech/tacotron2-DDC",
        "pitch_factor": 1.0,
        "speaking_rate": 1.0,
        "formant_target": {
          "f1": 500,
          "f2": 1500
        },
        "articulation": {
          "clarity": 0.8,
          "energy": 0.7
        }
      }
    }
  }
}
```

## Analytics Feedback Loop

```
Episode Produced
    ↓
Analytics Gathered (listener retention, quality scores)
    ↓
SKG Updated (mastery_scores section)
    ↓
Next Episode Uses Updated SKG
    ↓
Production Improves Over Time
```

## Command Examples

```bash
# Produce episode using SKG + POM
pyReasoning Engine:** GPT4All (local CPU model)  
**Tone Engine:** Gyro-Cortical Harmonizer  
**Voice Engine:** Phonatory Output Module (POM + Coqui TTS)

**NOT USED:**
- ❌ Ollama
- ❌ Nous Hermes
- ❌ OpenAI for speech
- ❌ Claude for speech \
  --output deliverables/podcasts/episode.wav

# Validate SKG configuration
python skg_validator.py \
  --schema podcast_studio \
  --file skg/productions/podcast_abc123.json

# Update SKG from analytics
python skg_updater.py \
  --analytics analytics_episode_47.json \
  --update voice_performance \
  --update listener_retention
```

## Testing the Flow

1. **Frontend:** Submit podcast form
2. **API:** Receives data, builds SKG
3. **Orchestrator:** Reads SKG, calls LLM
4. **LLM:** Generates script text
5. **POM:** Synthesizes voice with Coqui TTS
6. **Output:** Professional podcast episode

All components respect boundaries:
- GPT4All reasons (text only)
- SKG stores (configuration + memory)
- Harmonizer decides (tone only)
- POM speaks (voice only)

---

**Last Updated:** 2025-12-15  
**Architecture Owner:** GOAT Platform  
**Reasoning Engine:** GPT4All (local CPU model)  
**Tone Engine:** Gyro-Cortical Harmonizer  
**Voice Engine:** Phonatory Output Module (POM + Coqui TTS)

**Hardware Strategy:** CPU-resident now, GPU drop-in upgrade later

**NOT USED:**
- ❌ Ollama
- ❌ Nous Hermes  
- ❌ OpenAI for speech
- ❌ Claude for speech
