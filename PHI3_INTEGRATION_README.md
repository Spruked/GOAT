# Phi-3 Mini Integration with Caleon Prime

## Overview

This document describes the integration of Microsoft's Phi-3 Mini as Caleon Prime's articulation engine. Phi-3 Mini serves as Caleon's "speech cortex" - a local, fast, controllable language model that turns structured thoughts into natural language while maintaining Caleon's sovereign personality.

## Architecture

```
Caleon UCM (Reasoning) → Structured Plan → Phi-3 Mini (Articulation) → Tone Harmonizer → ScribeCore Output

Where:
- UCM: Unified Cognition Module (Helices, Resonator, EchoStack, Vaults)
- Phi-3 Mini: Local language model for text generation
- Tone Harmonizer: GOAT voice harmonizer layer
- ScribeCore: Continuity and quality management
```

## Key Benefits

### ✅ Sovereignty Maintained
- Phi-3 Mini is local and controllable
- No external API dependencies
- Caleon's reasoning remains in UCM
- Personality conditioning prevents override

### ✅ Performance Optimized
- Fast inference (4K context, optimized for local hardware)
- Low resource requirements
- Deterministic output with controlled parameters
- Streaming capability for real-time responses

### ✅ Perfect for Articulation
- Excellent at structured writing (sections, outlines, explanations)
- Maintains strong continuity across long content
- Great at expanding structured plans
- High coherence in constrained contexts

## Installation

### 1. Install Phi-3 Dependencies

```bash
pip install -r phi3_requirements.txt
```

### 2. Download Phi-3 Mini Model

Choose one of the following options:

#### Option A: Transformers (Recommended)
```python
# Automatic download via Hugging Face
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
```

#### Option B: GGUF Format (Faster Inference)
```bash
# Download from Hugging Face
wget https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf

# Set environment variable
export PHI3_MODEL_PATH="./models/Phi-3-mini-4k-instruct-q4.gguf"
```

### 3. Environment Variables

```bash
# Model path (if using GGUF)
export PHI3_MODEL_PATH="./models/Phi-3-mini-4k-instruct-q4.gguf"

# UCM endpoint (for reasoning)
export CALEON_UCM_ENDPOINT="http://localhost:8000/v1/caleon/invoke"
export CALEON_AUTH_TOKEN="your-auth-token"
```

## Usage

### Basic Articulation

```python
from phi3_driver import get_articulator

# Get articulator instance
articulator = get_articulator()

# Create writing plan
plan = {
    "chapter_title": "AI Sovereignty",
    "section_title": "Local Intelligence",
    "goals": "Explain benefits of local AI models",
    "tone": "technical_clear",
    "continuity_context": "Previous section covered AI dependencies",
    "target_length": "600-800 words"
}

# Generate articulated content
content = await articulator.articulate(plan)
print(content)
```

### Streaming Output

```python
# Real-time streaming
async for chunk in articulator.articulate_stream(plan):
    print(chunk, end="", flush=True)
```

### Integration with ScribeCore

```python
from goat_core.draft_engine.caleon_bridge import CaleonBridge

bridge = CaleonBridge()

# Generate section with UCM reasoning + Phi-3 articulation
content = bridge.generate_section(
    chapter_title="Sovereign AI",
    section_title="Phi-3 Integration",
    tone="technical_explanation",
    continuity_context="Building on previous architecture discussion",
    goals="Demonstrate Phi-3 as articulation engine"
)
```

## Personality Conditioning

Phi-3 Mini is conditioned with Caleon's personality through a comprehensive prompt that includes:

- **Direct and confident** communication style
- **Warm but not soft** interpersonal tone
- **Traditional wisdom + forward drive** perspective
- **Active voice, short paragraphs** structure
- **Zero AI-speak, zero hedging** language patterns
- **Purpose-driven, mission-focused** content approach

## Parameters Optimized for Caleon

```python
# Phi-3 parameters tuned for consistent Caleon voice
{
    "temperature": 0.4,      # Low for consistency, not zero for naturalness
    "top_p": 0.9,           # Focused but creative
    "top_k": 40,            # Good balance
    "repetition_penalty": 1.15,  # Prevent repetition
    "max_tokens": 2048,     # Generous but controlled
    "context_window": 4096, # Phi-3 Mini 4K context
}
```

## API Endpoints

### Generate Response
```http
POST /api/caleon/generate
Content-Type: application/json

{
  "message": "Explain Phi-3 integration",
  "context": {"interface": "bubble_assistant"}
}
```

### Stream Response
```http
POST /api/caleon/stream
Content-Type: application/json

{
  "message": "Live streaming demo",
  "context": {"interface": "bubble_assistant"}
}
```

## Testing

Run the integration tests:

```bash
python test_phi3_integration.py
```

This will test:
- Phi-3 articulator functionality
- Personality conditioning
- Streaming capabilities
- Fallback behavior

## Fallback Behavior

If Phi-3 Mini is unavailable, the system gracefully falls back to:
- Structured output with validated plans
- Continuity maintenance
- Clear indication of offline status
- Automatic resumption when model comes online

## Performance Characteristics

### Speed
- Local inference: ~50-100 tokens/second
- Streaming: Real-time token delivery
- Context switching: Minimal latency

### Quality
- Deterministic output with controlled variance
- Strong adherence to personality conditioning
- Excellent continuity maintenance
- High coherence in structured writing tasks

### Resource Usage
- RAM: ~2-4GB for 4K context
- CPU: 4-8 threads optimal
- Disk: ~2GB for model storage
- No internet required for inference

## Security & Privacy

- **Local execution**: No data leaves your environment
- **Sovereign control**: Complete authority over model behavior
- **No telemetry**: Microsoft Phi-3 runs without external communication
- **Private keys**: All authentication handled locally

## Troubleshooting

### Common Issues

1. **Model not found**: Check PHI3_MODEL_PATH environment variable
2. **CUDA not available**: Install torch with CUDA support or use CPU
3. **Memory errors**: Reduce context window or use quantized model
4. **Slow inference**: Use llama-cpp backend for better performance

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- **Fine-tuning**: Custom training on Caleon-specific content
- **Multi-pass articulation**: Draft → expand → refine pipeline
- **Voice variants**: Different personality modes for different contexts
- **Hybrid reasoning**: Phi-3 assisting UCM with complex planning

## Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Caleon UCM    │ -> │  Structured Plan  │ -> │   Phi-3 Mini    │
│   (Reasoning)   │    │   (JSON/Plan)     │    │ (Articulation)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐             │
│ Tone Harmonizer │ <- │   Continuity     │ <- - - - - -
│ (GOAT Voice)    │    │   Manager        │
└─────────────────┘    └──────────────────┘
         │
         v
┌─────────────────┐
│   Final Output  │
│ (Caleon Voice)  │
└─────────────────┘
```

This architecture ensures Caleon remains sovereign while leveraging Phi-3 Mini's excellent language generation capabilities.