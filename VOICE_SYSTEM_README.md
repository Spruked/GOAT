# GOAT Voice System - POM 2.0 Integration

## Professional Audiobook Creation with Advanced Voice Synthesis

The GOAT Voice System integrates Phonatory Output Module (POM) 2.0 with Coqui TTS to deliver professional-grade audiobook production with character voice mapping, narrator optimization, and emotional modulation.

## 🎯 Key Features

### Voice Engine (`engines/voice_engine.py`)
- **POM 2.0 Integration**: Advanced phonatory processing with formant filtering, larynx simulation, lip control, tongue articulation, and uvula control
- **Dual Creation Methods**: Sample-based voice cloning and parameter-based voice synthesis
- **Emotional Modulation**: Dynamic voice adjustments for different emotional states
- **Secure Voice Vault**: Cryptographic provenance tracking with glyph integration

### Character Voice Mapper (`engines/character_voice_mapper.py`)
- **Automatic Voice Assignment**: Creates matching voices based on character traits
- **Emotional Range Mapping**: Supports multiple emotions per character
- **Dialogue Processing**: Parses scripts and assigns appropriate voices
- **Personality-Based Synthesis**: Adjusts voice parameters based on character personality

### Narrator Optimizer (`engines/narrator_optimizer.py`)
- **Content-Type Optimization**: Specialized profiles for fiction, nonfiction, poetry, and technical content
- **Text Analysis**: Automatic complexity assessment and pacing optimization
- **Technical Term Handling**: Pronunciation guides and clarity enhancements
- **Reading Speed Adaptation**: Dynamic speed adjustment based on content difficulty

### Audiobook Renderer (`engines/audiobook_renderer.py`)
- **Complete Pipeline**: From book data to final audiobook file
- **Multi-Track Assembly**: Combines narrator and character voices
- **Format Support**: WAV, MP3, M4B export with metadata
- **Batch Processing**: Efficient rendering of multiple segments

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
# Note: POM 2.0 and Coqui TTS require additional setup
```

### 2. Run the Demo
```bash
python demo_voice_system.py
```

### 3. Run Tests
```bash
python test_voice_system.py
```

### 4. Start API Server
```bash
uvicorn routes.voice_management:app --host 0.0.0.0 --port 8000
```

## 📖 API Usage

### Create Voice Profile
```python
from engines.voice_engine import VoiceEngine

engine = VoiceEngine()
result = await engine.create_voice_profile(
    creation_method="parameter",
    name="Narrator",
    description="Professional narrator voice",
    voice_type="narrator",
    param_config={
        "tension": 0.6,
        "breathiness": 0.2,
        "articulation_precision": 0.9
    }
)
```

### Create Character Profile
```python
from engines.character_voice_mapper import CharacterVoiceMapper

mapper = CharacterVoiceMapper(engine)
character = await mapper.create_character_profile(
    name="Detective Chen",
    description="Sharp-witted detective",
    gender="female",
    age_range="adult",
    personality_traits=["confident", "intelligent"]
)
```

### Generate Audiobook
```python
from engines.audiobook_renderer import AudiobookRenderer

renderer = AudiobookRenderer(engine, mapper, optimizer)
result = await renderer.render_audiobook_from_book(
    book_data=your_book_data,
    output_path="./output/audiobook.wav"
)
```

## 🎵 Voice Configuration

### POM Modules
- **Formant Filter**: Voice color and timbre adjustment
- **Larynx Simulation**: Vocal texture (tension, breathiness)
- **Lip Control**: Articulation precision
- **Tongue Articulation**: Speech clarity and accents
- **Uvula Control**: Nasalization for specific languages

### Emotional Profiles
- **Neutral**: Baseline voice characteristics
- **Angry**: Increased tension and speed
- **Weary**: Reduced intensity and slower pace
- **Excited**: Higher pitch variation and faster speech
- **Calm**: Steady rhythm and moderate intensity

### Quality Presets
- **Draft**: Fast processing, basic quality
- **Standard**: Balanced quality and speed
- **Professional**: Highest quality with post-processing

## 🔧 Configuration

Voice synthesis settings are managed in `config/voice_config.py`:

```python
VOICE_CONFIG = {
    "engine": {
        "pom_integration": True,
        "sample_rate": 22050,
        "channels": 1
    },
    "directories": {
        "voices": "./voices",
        "profiles": "./voices/profiles",
        "temp": "./voices/temp"
    }
}
```

## 📊 API Endpoints

### Voice Profiles
- `POST /api/voice/profiles/create` - Create voice profile
- `GET /api/voice/profiles/{id}` - Get voice profile
- `GET /api/voice/profiles` - List all profiles
- `DELETE /api/voice/profiles/{id}` - Delete profile

### Characters
- `POST /api/voice/characters/create` - Create character
- `POST /api/voice/characters/{name}/audio` - Generate character audio
- `GET /api/voice/characters` - List characters

### Narrator
- `POST /api/voice/narrator/create` - Create narrator profile
- `POST /api/voice/narrator/analyze` - Analyze text
- `POST /api/voice/narrator/audio` - Generate narrator audio

### Audiobooks
- `POST /api/voice/audiobook/render` - Render audiobook
- `POST /api/voice/audiobook/preview` - Generate preview
- `POST /api/voice/audiobook/batch` - Batch render segments

## 🏗️ Architecture

```
GOAT Voice System
├── engines/
│   ├── voice_engine.py          # Core synthesis engine
│   ├── character_voice_mapper.py # Character management
│   ├── narrator_optimizer.py     # Content optimization
│   └── audiobook_renderer.py     # Final rendering
├── routes/
│   └── voice_management.py       # API endpoints
├── config/
│   └── voice_config.py          # Configuration
├── voices/
│   ├── profiles/                # Voice profiles
│   ├── models/                  # Model files
│   └── temp/                    # Temporary files
└── data/vault/                  # Secure storage
```

## 🔒 Security & Provenance

- **Voice Vault**: Secure storage with cryptographic hashing
- **Glyph System**: Provenance tracking for voice assets
- **Access Control**: Profile-based permissions
- **Audit Trail**: Usage logging and monitoring

## 📈 Performance

- **Concurrent Processing**: Multiple voices rendered simultaneously
- **Caching**: Voice profile and audio segment caching
- **Memory Management**: Efficient memory usage for long audiobooks
- **Quality Optimization**: Adaptive quality based on content complexity

## 🎯 Use Cases

### Fiction Audiobooks
- Character voice differentiation
- Emotional dialogue rendering
- Atmospheric narration

### Nonfiction Content
- Clear technical explanations
- Professional narration
- Educational content optimization

### Poetry & Literature
- Expressive verse rendering
- Emotional depth enhancement
- Rhythmic speech patterns

### Technical Documentation
- Precise term pronunciation
- Clarity optimization
- Structured content pacing

## 🔄 Integration Status

- ✅ Voice Engine with POM 2.0 integration
- ✅ Character voice mapping
- ✅ Narrator optimization
- ✅ Audiobook rendering pipeline
- ✅ RESTful API
- ✅ Test suite
- ✅ Demo application
- 🔄 Production deployment (requires POM 2.0 installation)
- 🔄 Multi-format export (MP3, M4B)

## 📝 Requirements

- Python 3.8+
- Coqui TTS
- POM 2.0 Phonatory Modules (when available)
- FastAPI (for API server)
- NumPy, SciPy (for audio processing)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This implementation is part of the GOAT system. See LICENSE file for details.

---

**Note**: This system uses mock implementations for POM 2.0 modules during development. Full functionality requires the actual POM 2.0 library installation.

---

## 📄 Copyright

Copyright © 2025-2026 PRo Prime Series and GOAT, in association with TrueMark Mint LLC. All rights reserved.