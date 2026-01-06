
---
**GOAT Eternal**

Copyright (c) 2025 GOAT Contributors

This project is licensed under the MIT License. See the LICENSE file for details.

> This software is provided "AS IS", without warranty of any kind, express or implied. See the full MIT license in LICENSE for details.

# GOAT v2.1 - Minting Minds, Its Worth More Than You Think!

**GOAT = Greatest Of All Time**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.20-363636.svg)](https://soliditylang.org/)
[![UCM](https://img.shields.io/badge/UCM-Plugin-FF6B6B.svg)](https://github.com/Spruked/Unified-Cognition-Module-Caleon-Prime-full-System)
[![DALS](https://img.shields.io/badge/DALS-Integrated-00D4AA.svg)](https://github.com/Spruked/GOAT)

**AI + Web3 Content Creation & Organization Platform with Adaptive Formatting & Immutable Vaulting**

> GOAT transforms user data into professionally formatted content (books, manuals, podcasts, scripts) with blockchain-ready certificates.
> Every creation is signed. Every format is optimized. Every certificate is prepared for minting.
> Now powered by Unified Cognition Module for advanced content cognition and Digital Asset Logistics System for comprehensive asset management.

---

---

## 🌟 Features

### 🧠 **Unified Cognition Module (UCM) Plugin**
- **External AI Cognition**: Connects to separate Unified Cognition Module service for advanced AI reasoning
- **Plugin Architecture**: UCM runs as independent service, GOAT connects via API
- **Adaptive Intelligence**: Real-time cognitive analysis and personalized learning adaptation
- **Smart Quiz Generation**: AI-crafted assessments based on cognitive understanding
- **Personalized Explanations**: Context-aware content delivery using advanced cognition

### 🤖 **Caleon Overlay - AI Guardian**
- **Persistent AI Assistant**: Floating AI companion that provides context-aware help throughout the platform
- **Voice Interaction**: Full speech recognition and text-to-speech capabilities
- **Panel Awareness**: Intelligent understanding of current user context and active panels
- **UCM-Connected Responses**: Integration with external Unified Cognition Module for advanced reasoning
- **Workflow Guidance**: Step-by-step assistance for complex tasks and processes
- **Real-time Status Updates**: Live UCM cognition status and system monitoring
- **Custom Avatar**: Uses CaleoniA.jpeg as the AI assistant's visual representation

### 🎯 **Orb CALI Escalation System**
- **Intelligent Escalation Detection**: Advanced AI-driven analysis of user needs and frustration levels
- **Dramatic Orb Entrance**: Spectacular animated orb appearance with particle effects and sound
- **Secure Screen Access**: Permission-based screen capture for comprehensive assistance
- **Cursor-Aware Positioning**: Smart orb placement that avoids interfering with user workflow
- **Seamless Handoff**: Smooth transition from bubble assistant to advanced Orb CALI support
- **Performance Optimized**: Lightweight escalation detection with minimal system impact
- **Enterprise-Ready**: Scalable architecture supporting multiple concurrent escalations

### 🫧 **Bubble Host Architecture**
- **Contextual Assistance**: Intelligent floating bubbles that provide immediate help
- **Multi-Panel Support**: Simultaneous assistance across different application panels
- **Voice-Enabled Interaction**: Speech recognition and synthesis for natural communication
- **Real-time Adaptation**: Dynamic adjustment based on user behavior and context
- **Seamless Escalation**: Automatic handoff to Orb CALI when advanced support needed
- **Customizable Appearance**: Themed bubbles with configurable colors and animations
- **Unified Dashboard**: Complete GOAT functionality accessible through DALS gateway
- **Configuration Overrides**: Runtime configuration management with monitoring
- **Host Messaging**: Push/pull messaging system for workers and GOAT integration
- **UQV Storage**: Universal Query Vault for data persistence and retrieval
- **TTS Synthesis**: Text-to-speech capabilities for audio content generation
- **Broadcast System**: Multi-channel communication and notification system
- **GOAT Proxy**: All GOAT endpoints accessible through DALS with override capabilities
- **Real-time Monitoring**: Comprehensive system status and performance tracking

### �🔐 **Glyph + Vault System**
- **Unique Glyph IDs**: Cryptographically signed identifiers for every NFT
- **AES-256 Encryption**: Secure vault storage with complete audit trails
- **EIP-191 Signatures**: Verifiable provenance for all data
- **Merkle Tree Anchoring**: On-chain proof anchoring to Polygon

### 🤖 **AI-Powered Content Creation**
- **Adaptive Formatting**: Personalized content structure based on user data and requirements
- **Auto-Generated Content**: AI-created books, manuals, and multimedia from user input
- **Format Optimization**: Professional formatting for various output types
- **Content Analytics**: Detailed metrics and quality assessments
- **Manual Generation**: Create user manuals, owner's manuals, and training manuals as separate offerings from books

### 🎧 **Audiobook Creation System**
- **POM 2.0 Voice Synthesis**: Professional voice synthesis with phonatory output modules
- **Character Voice Mapping**: Unique voices for each character with emotional modulation
- **Narrator Optimization**: Content-aware voice adjustment for fiction, nonfiction, and technical content
- **Multi-Format Export**: WAV, MP3, M4B audiobook production with chapter markers
- **Voice Vault Security**: Encrypted voice profiles with cryptographic provenance
- **Batch Processing**: Automated audiobook production pipeline

### 🔗 **Multi-Source Content Organization**
- **Data Ingestion**: Direct content ingestion with auto-organization
- **Content Structuring**: Automatic categorization and formatting
- **Webhook Support**: Auto-ingest from data sources
- **Content Vaulting**: Secure storage with encryption and audit trails

### 🎓 **Certificate Preparation & Referral**
- **Certificate Creation**: Prepares blockchain-ready certificates for external minting
- **Partner Referrals**: Exclusive 30% discounts at Alpha CertSig Mint and TrueMark Mint
- **Cryptographic Proofs**: Full provenance chain preparation for certificates
- **Minting Packages**: Ready-to-mint certificate bundles with all metadata
- **External Minting**: GOAT does NOT mint - only prepares and refers to professional minting services

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)
- **No GPU/CUDA required** - This application runs on CPU only

### 1. Clone & Setup

```bash
git clone https://github.com/Spruked/GOAT.git
cd GOAT

# Copy environment file
cp .env.example .env

# Edit .env with your keys
nano .env

# Place Caleon avatar image (optional)
# Copy CaleoniA.jpeg to frontend/public/ for custom Caleon avatar
cp /path/to/CaleoniA.jpeg frontend/public/
```

### 2. Deploy with Docker

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **API**: http://localhost:5000
- **API Docs**: http://localhost:5000/docs
- **Neo4j Browser**: http://localhost:7474
- **IPFS Gateway**: http://localhost:8080

---

## 📁 Project Structure

```
GOAT/
├── frontend/                    # React + Vite frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── bubble/             # Bubble host components
│   │   ├── orb/                # Orb CALI escalation components
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/                     # FastAPI backend
│   └── app/
│       ├── main.py             # FastAPI application
│       ├── api/                # API endpoints
│       ├── models/             # Database models
│       └── core/               # Core functionality
├── escalation/                  # Orb CALI escalation system
│   ├── escalation_detector.py  # AI-driven escalation detection
│   └── escalation-proxy.ts     # TypeScript IPC proxy
├── orb/                        # Orb CALI Electron components
│   ├── orb-renderer.ts         # Main orb UI component
│   ├── orb-main.ts             # Electron main process
│   └── orb-styles.css          # Orb visual styling
├── bubble/                     # Bubble host system
│   └── bubble-bridge.ts        # Bubble to Orb handoff
├── workers/                    # Background worker system
│   ├── signup_worker.py        # User signup processing
│   └── user_data_worker.py     # User data management
├── users/                      # User management system
│   └── user_store.py           # Centralized user data access
├── lib/                        # Shared libraries
│   └── user_store.py           # User data helper
├── marketing/                  # Marketing and analytics
├── vault/
│   ├── core.py                 # Glyph + encryption system
│   ├── glyph_svg.py            # SVG generation
│   ├── ipfs_gateway.py         # IPFS integration
│   └── onchain_anchor.py       # Merkle anchoring
├── vault/
│   ├── core.py                 # Glyph + encryption system
│   ├── glyph_svg.py            # SVG generation
│   ├── ipfs_gateway.py         # IPFS integration
│   └── onchain_anchor.py       # Merkle anchoring
├── collector/
│   ├── orchestrator.py         # Ingestion pipeline
│   └── glyph_generator.py      # Glyph creation
├── config/
│   └── voice_config.py         # Voice synthesis configuration
├── audiobook_engine/          # Audiobook production system
│   ├── voice_engine.py         # POM 2.0 voice synthesis
│   ├── character_voice_mapper.py # Character voice mapping
│   ├── narrator_optimizer.py   # Content-aware narrator optimization
│   └── audiobook_renderer.py   # Complete audiobook pipeline
├── engines/                     # AI content creation engines
│   ├── voice_engine.py         # POM 2.0 voice synthesis engine
│   ├── character_voice_mapper.py # Character voice mapping system
│   ├── narrator_optimizer.py   # Content-aware narrator optimization
│   ├── audiobook_renderer.py   # Complete audiobook production pipeline
│   ├── manual_engine.py        # Manual generation system
│   ├── graph_engine.py         # Content visualization engine
│   ├── deep_parser.py          # Text analysis engine
│   ├── summarization_engine.py # Content summarization
│   └── contradiction_detector.py # Logic analysis
├── routes/                     # API route handlers
│   ├── voice_management.py     # Voice synthesis and audiobook API
│   ├── manuals.py              # Manual generation endpoints
│   ├── graph_visualization.py  # Content visualization API
│   ├── podcast_engine.py       # Podcast/audio generation
│   └── certificate_prep.py     # Certificate preparation
├── DALS/                       # Distributed AI Content System
│   ├── api/                    # DALS API endpoints
│   │   ├── host_routes.py      # Host messaging
│   │   ├── broadcast_routes.py # Worker broadcasting
│   │   ├── uqv_routes.py       # UQV API
│   │   └── tts_routes.py       # Text-to-speech
│   └── registry/               # Worker registry
├── knowledge/
│   └── graph.py                # Skill tree & progress tracking
├── learning/                   # Content organization & planning
│   ├── engine.py               # Content recommendation engine
│   ├── difficulty_engine.py    # Content complexity scaling
│   ├── ucm_bridge.py           # External UCM service integration
│   ├── event_logger.py         # Content creation event tracking
│   ├── learning_package_builder.py  # Content package building
│   ├── glyph_forge.py          # Certificate preparation
│   └── vault_bridge.py         # Vault integration
├── licenser/
│   └── verifier.py             # Badge minting & verification
├── contracts/
│   └── GOATVaultAnchor.sol     # Solidity contract
├── voices/                     # Voice profiles and samples
│   ├── profiles/               # Character voice profiles
│   ├── samples/                # Voice sample storage
│   └── vault/                  # Encrypted voice vault
├── vault_forge/                # Multi-tier vault packaging
├── Unified-Cognition-Module-Caleon-Prime-full-System/  # UCM (external plugin)
├── docker-compose.yml
├── Dockerfile.backend
└── requirements.txt
```

---

## 🔧 Development

### Run Backend Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
cd backend/app
uvicorn main:app --reload --port 5000
```

### Run Frontend Locally

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

### Build Frontend

```bash
cd frontend
npm run build
```

---

## 📡 API Endpoints

### Authentication Required (API Key)
All endpoints require `X-API-Key` header for access.

### Vault
- `GET /api/vault/stats` - Get vault statistics
- `GET /api/glyph/{id}` - Retrieve glyph by ID
- `GET /api/vault/proof/{id}` - Get cryptographic proof
- `GET /api/vault/list` - List all glyphs (with pagination)
- `GET /glyph/svg/{id}` - Get glyph SVG image
- `GET /glyph/badge/{id}` - Get verification badge

### Collector
- `POST /api/collect/ipfs` - Ingest from IPFS
- `POST /api/collect/onchain` - Ingest from blockchain
- `POST /api/collect/manual` - Process manual knowledge
- `POST /api/collect/webhook` - Handle mint webhooks

### Content Creation (UCM-Connected)
- `POST /api/content/book` - Generate complete books from user data
- `POST /api/content/manual` - Create user/owner/training manuals
- `POST /api/content/podcast` - Generate podcast scripts and audio content
- `POST /api/content/script` - Create professional scripts
- `GET /api/content/status/{job_id}` - Check content generation status

### Audiobook Creation (POM 2.0 Voice Synthesis)
- `POST /api/voice/profiles/create` - Create voice profile with POM phonatory modules
- `GET /api/voice/profiles` - List all voice profiles
- `POST /api/voice/characters/create` - Create character with unique voice mapping
- `POST /api/voice/characters/{name}/audio` - Generate character dialogue audio
- `POST /api/voice/narrator/create` - Create content-optimized narrator profile
- `POST /api/voice/narrator/audio` - Generate narrator audio with clarity enhancement
- `POST /api/voice/audiobook/render` - Render complete audiobook from book data
- `POST /api/voice/audiobook/preview` - Generate voice preview samples
- `POST /api/voice/audiobook/batch` - Batch render multiple audio segments
- `GET /api/voice/status` - Get voice system status and POM integration

### Certificate Preparation
- `POST /api/certificate/prepare` - Prepare certificate for external minting
- `GET /api/certificate/partners` - Get minting partner options with discounts
- `POST /api/certificate/referral` - Generate referral package for partner minting
- `GET /api/certificate/discounts` - Check available discounts and promotions

### Knowledge Graph
- `GET /api/knowledge/skills` - List all skills
- `GET /api/knowledge/skill/{skill_id}` - Get skill tree
- `GET /api/knowledge/path/{skill_id}` - Get learning path
- `GET /api/knowledge/export` - Export complete graph

### Vault Forge
- `POST /api/vault-forge/create` - Create immutable vault package

### On-Chain Anchor
- `POST /api/anchor/batch` - Anchor glyph batch
- `GET /api/anchor/verify/{root}` - Verify anchor
- `GET /api/anchor/proof` - Get Merkle proof

### Background Jobs
- `GET /api/jobs/{job_id}` - Check job status
- `GET /api/jobs` - List active jobs

---

## 🔐 Security

### Vault Encryption
- **AES-256**: Industry-standard encryption at rest
- **EIP-191 Signatures**: Ethereum-compatible signing
- **SQLite Ledger**: Immutable audit log

### Environment Variables
```bash
# Security
API_KEY=your_api_key_here                    # Required for all API access
VAULT_ENCRYPTION_KEY=your_secret_key         # AES-256 encryption key

# UCM Plugin (External Service)
UCM_ENDPOINT=http://external-ucm:8080        # External UCM service endpoint
UCM_API_KEY=your_ucm_key                     # UCM API key (optional)
# Note: GOAT connects to UCM as external plugin - no local GPU/CUDA required

# Web3
PRIVATE_KEY=0x...                            # For EIP-191 signing
POLYGON_RPC=https://polygon-rpc.com          # Polygon RPC endpoint
ANCHOR_CONTRACT=0x...                        # Deployed contract address

# Optional
IPFS_GATEWAY=https://ipfs.io                 # IPFS gateway
OPENSEA_API_KEY=your_opensea_key             # OpenSea API access
```

---

## 🎯 Use Cases

### For Content Creators
1. Upload data and requirements to GOAT
2. GOAT creates formatted content (books, manuals, podcasts, scripts)
3. AI optimizes structure and formatting
4. Export in multiple professional formats
5. Optional: Prepare certificates for external minting with 30% discount

### For Users
1. Provide data and content specifications
2. GOAT builds professional content packages
3. Review and approve AI-generated content
4. Export finished products
5. Optional: Mint certificates through GOAT's partner referral program

### For Platforms
1. Integrate via API for automated content creation
2. Embed GOAT widget for content building
3. Use referral system for certificate minting
4. Access formatted content packages
5. Leverage AI content optimization

---

## 🌐 Deployment

### Deploy to Production

```bash
# Build optimized images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### Deploy Contract

```bash
cd contracts

# Compile
forge build

# Deploy to Polygon
forge create --rpc-url $POLYGON_RPC \
  --private-key $PRIVATE_KEY \
  GOATVaultAnchor
```

---

## 🎯 Usage Guide

### 🧠 Caleon Overlay - Your AI Guardian

The Caleon Overlay is your persistent AI assistant that floats above all panels and provides context-aware help throughout the GOAT platform.

#### Features:
- **Persistent Presence**: Always available in the bottom-right corner with a glowing crest
- **Voice Interaction**: Click the microphone to speak commands or questions
- **Context Awareness**: Automatically understands which panel you're on and what you're doing
- **UCM Connection**: Connects to external Unified Cognition Module for intelligent responses
- **Workflow Guidance**: Get step-by-step help for complex tasks

#### Quick Actions:
1. **Click the Caleon Crest** to expand the quick actions menu
2. **Voice Commands**: Click the microphone icon for voice input
3. **Text Chat**: Type questions directly in the chat interface
4. **Panel-Specific Help**: Caleon automatically detects your current panel and offers relevant assistance

#### Voice Commands Examples:
- "Help me understand what I'm looking at"
- "Guide me through this workflow"
- "Analyze my recent files"
- "What's my current progress?"
- "Explain the vault system"

#### Context Indicators:
- **Panel Awareness**: Shows current panel (Dashboard, Vault, Learn, etc.)
- **Active Bundle**: Displays currently selected knowledge bundle
- **File Context**: Indicates selected files for analysis
- **UCM Status**: Real-time connection status to the external cognition engine

---

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Vault Stats
```bash
curl http://localhost:5000/api/vault/stats
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## � Links

- **Documentation**: [BUILD_SUMMARY.md](BUILD_SUMMARY.md) | [DEPLOYMENT.md](DEPLOYMENT.md) | [QUICK_START.md](QUICK_START.md) | [Manual Generation Docs](docs/manuals.md) | [Manual README](MANUAL_GENERATION_README.md) | [Audiobook System](AUDIOBOOK_README.md)
 - **Vault System Integration**: See [docs/vault_integration.md](docs/vault_integration.md) for steps to integrate Caleon's Vault System (Vault_System_1.0) into GOAT.
- **GitHub Setup**: [GITHUB_SETUP.md](GITHUB_SETUP.md)
- **Contract**: [GOATVaultAnchor.sol](contracts/GOATVaultAnchor.sol)

---

## �🙏 Acknowledgments

- **FastAPI** for the amazing Python async framework
- **React** + **Vite** for lightning-fast frontend development
- **Web3.py** for seamless Ethereum integration
- **TailwindCSS** for utility-first styling
- **IPFS** for decentralized storage
- **Polygon** for scalable blockchain infrastructure

---

## 📧 Support

For issues and questions:
- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the `/docs` folder for detailed guides

---

**Built with ❤️ by the GOAT team**

*The GOAT now doesn't just create — it **builds professional content & prepares certificates for minting**.*
