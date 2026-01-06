# GOAT v2.1 - The Proven Teacher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.20-363636.svg)](https://soliditylang.org/)
[![DALS](https://img.shields.io/badge/DALS-Integrated-00D4AA.svg)](https://github.com/Spruked/GOAT)

**NFT Knowledge Engine with Glyph + Vault Provenance System & Digital Asset Logistics**

> Turn any NFT into a self-improving, AI-powered teacher that verifies learning on-chain.
> Every lesson is signed. Every skill is provable. Every teacher is accountable.
> Now enhanced with Digital Asset Logistics System (DALS) for comprehensive asset management and monitoring.

---

## 🌟 Features

### 📊 **Digital Asset Logistics System (DALS)**
- **Unified Dashboard**: Complete GOAT functionality accessible through DALS gateway
- **Configuration Overrides**: Runtime configuration management with monitoring
- **Host Messaging**: Push/pull messaging system for workers and GOAT integration
- **UQV Storage**: Universal Query Vault for data persistence and retrieval
- **TTS Synthesis**: Text-to-speech capabilities for audio content generation
- **Broadcast System**: Multi-channel communication and notification system
- **GOAT Proxy**: All GOAT endpoints accessible through DALS with override capabilities
- **Real-time Monitoring**: Comprehensive system status and performance tracking

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

### 🔐 **Glyph + Vault System**
- **Unique Glyph IDs**: Cryptographically signed identifiers for every NFT
- **AES-256 Encryption**: Secure vault storage with complete audit trails
- **EIP-191 Signatures**: Verifiable provenance for all data
- **Merkle Tree Anchoring**: On-chain proof anchoring to Polygon

### 🤖 **AI-Powered Teaching**
- **Adaptive Learning Paths**: Personalized recommendations based on progress
- **Auto-Generated Quizzes**: AI-created assessments from NFT content
- **Skill Tree System**: Prerequisite tracking and mastery levels
- **Progress Analytics**: Detailed learning metrics and achievements

### 🔗 **Multi-Source Collection**
- **IPFS Integration**: Direct CID ingestion with auto-pinning
- **On-Chain Reading**: ERC-721 tokenURI extraction
- **OpenSea API**: Marketplace metadata enrichment
- **Webhook Support**: Auto-ingest from mint events

### 🎓 **Verifiable Credentials**
- **Learner Badges**: Mintable NFT badges for verified skills
- **Cryptographic Proofs**: Full provenance chain for every achievement
- **Feedback Loop**: Continuous improvement from learner input

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone & Setup

```bash
git clone https://github.com/Spruked/GOAT.git
cd GOAT

# Copy environment file
cp .env.example .env

# Edit .env with your keys
nano .env
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
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **DALS Dashboard**: http://localhost:8000/dals/host/dashboard
- **Neo4j Browser**: http://localhost:7474
- **IPFS Gateway**: http://localhost:8080

---

## 📁 Project Structure

```
GOAT/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── bubble/          # Bubble host components
│   │   ├── orb/             # Orb CALI escalation components
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/                  # FastAPI backend
│   └── app/
│       ├── main.py          # FastAPI application
│       ├── api/v1/endpoints/# GOAT API endpoints
│       └── config.py        # Configuration
├── escalation/               # Orb CALI escalation system
│   ├── escalation_detector.py # AI-driven escalation detection
│   └── escalation-proxy.ts  # TypeScript IPC proxy
├── orb/                      # Orb CALI Electron components
│   ├── orb-renderer.ts      # Main orb UI component
│   ├── orb-main.ts          # Electron main process
│   └── orb-styles.css       # Orb visual styling
├── bubble/                   # Bubble host system
│   └── bubble-bridge.ts     # Bubble to Orb handoff
├── workers/                  # Background worker system
│   ├── signup_worker.py     # User signup processing
│   └── user_data_worker.py  # User data management
├── users/                    # User management system
│   └── user_store.py        # Centralized user data access
├── lib/                      # Shared libraries
│   └── user_store.py        # User data helper
├── DALS/                     # Digital Asset Logistics System
│   ├── api/
│   │   ├── host_routes.py   # Host messaging & dashboard
│   │   ├── uqv_routes.py    # Universal Query Vault
│   │   ├── tts_routes.py    # Text-to-speech
│   │   └── broadcast_routes.py # Broadcasting
│   └── registry/            # Component registry
├── vault/
│   ├── core.py              # Glyph + encryption
│   ├── glyph_svg.py         # SVG generation
│   ├── ipfs_gateway.py      # IPFS integration
│   └── onchain_anchor.py    # Merkle anchoring
├── collector/
│   ├── orchestrator.py      # Ingestion pipeline
│   └── glyph_generator.py   # Glyph creation
├── knowledge/
│   └── graph.py             # Skill tree & graph
├── learning/                # Content organization & planning
│   ├── engine.py            # Content recommendation engine
│   ├── ucm_bridge.py        # External UCM service integration
│   └── vault_bridge.py      # Vault integration
├── licenser/
│   └── verifier.py          # Badge minting
├── contracts/
│   └── GOATVaultAnchor.sol  # Solidity contract
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
uvicorn main:app --reload --port 8000
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

### DALS Dashboard
- `GET /dals/host/dashboard` - Complete GOAT + DALS dashboard
- `GET /dals/host/config` - Get DALS configuration
- `POST /dals/host/config/override` - Override configuration
- `GET /dals/host/monitoring` - Real-time monitoring
- `GET /dals/host/connections` - Connection status

### GOAT Knowledge Graph
- `POST /api/v1/triples/ingest` - Ingest triples
- `GET /api/v1/triples/search` - Search triples
- `POST /api/v1/query/sparql` - SPARQL queries
- `POST /api/v1/query/vector` - Vector search

### GOAT Analytics
- `GET /api/v1/analytics/stats` - System statistics
- `GET /api/v1/analytics/graph` - Graph analytics

### GOAT Video Generation
- `POST /api/v1/video/generate-memory` - Generate memory videos
- `GET /api/v1/video/job/{job_id}` - Check job status
- `GET /api/v1/video/templates` - Available templates

### Vault
- `GET /api/vault/stats` - Get vault statistics
- `GET /api/glyph/{id}` - Retrieve glyph by ID
- `GET /api/vault/proof/{id}` - Get cryptographic proof

### Collector
- `POST /api/collect/ipfs` - Ingest from IPFS
- `POST /api/collect/onchain` - Ingest from blockchain
- `POST /api/collect/webhook` - Handle mint webhooks

---

## 🔐 Security

### Vault Encryption
- **AES-256**: Industry-standard encryption at rest
- **EIP-191 Signatures**: Ethereum-compatible signing
- **SQLite Ledger**: Immutable audit log

### DALS Security
- **Configuration Overrides**: Runtime security settings
- **Monitoring**: Real-time security status tracking
- **Access Control**: Integrated authentication with GOAT

### Environment Variables
```bash
VAULT_ENCRYPTION_KEY=your_secret_key  # Change in production!
PRIVATE_KEY=0x...                      # For EIP-191 signing
POLYGON_RPC=https://polygon-rpc.com
ANCHOR_CONTRACT=0x...                  # Deployed contract address
OPENAI_API_KEY=sk-...                  # For AI features
DALS_ENDPOINT=http://localhost:8000    # DALS gateway
```

---

## 🎯 Use Cases

### For Educators
1. Mint educational NFTs with IPFS content
2. GOAT auto-ingests and creates glyphs
3. AI generates lessons and quizzes
4. Students earn verifiable badges
5. DALS provides monitoring and asset management

### For Learners
1. Browse recommended skills through DALS dashboard
2. Complete adaptive lessons
3. Take AI-generated quizzes
4. Mint proof-of-learning badges
5. Track progress via DALS monitoring

### For Platforms
1. Integrate via webhook for auto-ingestion
2. Embed GOAT widget in marketplace
3. Verify learner credentials on-chain
4. Track learning analytics through DALS
5. Manage assets via DALS logistics system

---

## 🌐 Deployment

### Deploy to Production

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d
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

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### DALS Dashboard
```bash
curl http://localhost:8000/dals/host/dashboard
```

### Vault Stats
```bash
curl http://localhost:8000/api/vault/stats
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

## 🔗 Links

- **Documentation**: [BUILD_SUMMARY.md](BUILD_SUMMARY.md) | [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) | [QUICK_START.md](QUICK_START.md)
- **GitHub Setup**: [GITHUB_SETUP.md](GITHUB_SETUP.md)
- **Contract**: [GOATVaultAnchor.sol](contracts/GOATVaultAnchor.sol)

---

## 🙏 Acknowledgments

- **FastAPI** for the amazing Python async framework
- **React** + **Vite** for lightning-fast frontend development
- **Web3.py** for seamless Ethereum integration
- **TailwindCSS** for utility-first styling
- **IPFS** for decentralized storage
- **Polygon** for scalable blockchain infrastructure
- **DALS** for comprehensive asset logistics

---

## 📧 Support

For issues and questions:
- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the `/docs` folder for detailed guides

---

**Built with ❤️ by the GOAT team**

*The GOAT now doesn't just teach — it **proves*. And with DALS, it **manages**.*