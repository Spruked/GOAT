# GOAT v2.1 - Greatest Of All Time

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.20-363636.svg)](https://soliditylang.org/)

**Courtroom-Grade AI Evidence Preparation System with APEX DOC Certification & TrueMark Asset Minting**

> GOAT prepares evidence. APEX certifies truth. TrueMark mints assets.
> Every observation is recorded. Every decision is reviewed. Every asset is provable.

---

## 🔒 ALIGNMENT DOCTRINE

**"GOAT observes. GOAT records. GOAT submits for certification. GOAT never claims authority."**

GOAT is a **standalone AI evidence preparation system** with human oversight.
GOAT produces structured observations and evidence bundles for external certification.
GOAT maintains strict authority separation from APEX DOC (certification) and TrueMark (assets).

---

## 🌟 Core Architecture

### 🏛️ **GOAT Field Review System**
- **Courtroom-Grade Human Oversight**: Mandatory rationale for all AI decisions
- **4D Autobiographical Memory**: Space-Field Knowledge Graph with ORB-style clutter cleaning
- **Field Observations**: Immutable audit trail of all system operations
- **Sequence Tracking**: Temporal integrity across all observations

### 🔐 **Evidence Preparation Pipeline**
- **VisiData Distiller**: Non-agentic data extraction and pattern recognition
- **Distiller Registry**: Sovereign registry for instrumental components
- **Legacy Builder Worker**: Content synthesis and multi-format output
- **ChaCha20 Vault**: Pre-storage encryption for all user data

### 🏛️ **APEX DOC Integration**
- **GOAT↔APEX Handshake Protocol v1.0**: Single integration bolt with HMAC-SHA256
- **13-Layer Certificate Generation**: Internal certificates (layers 1-11)
- **Evidence Bundle Submission**: Cryptographically signed bundles for certification
- **Callback Processing**: Certificate delivery with Ed25519 verification

### ⛓️ **TrueMark Mint Integration**
- **APEX→TrueMark Bridge**: Certified assets minted as blockchain tokens
- **Replay Protection**: Deterministic mint IDs prevent duplicate creation
- **Mint Authority Validation**: Only APEX-certified assets can be minted
- **Asset Provenance**: Full 13-layer certificate chain on-chain

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+ (for frontend development)
- Docker & Docker Compose (for full deployment)

### 1. Clone & Setup

```bash
git clone https://github.com/Spruked/GOAT.git
cd GOAT

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your keys (required for APEX/TrueMark integration)
nano .env
```

### 3. Run Development Server

```bash
# Start backend
python start_backend.py

# In another terminal, start frontend (optional)
cd frontend && npm install && npm run dev
```

### 4. Access Interfaces

- **GOAT API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:8000/admin
- **GOAT Field Review**: http://localhost:8000/field-review

---

## 📁 Project Structure

```
GOAT/
├── goat/                          # Core GOAT system
│   ├── core/                      # GOAT Field SKG & review system
│   │   ├── goat_field_skg.py      # 4D autobiographical memory
│   │   └── field_review_system.py # Human oversight
│   ├── distillers/                # Data processing engines
│   │   ├── visidata_engine.py     # VisiData distiller
│   │   └── registry.py            # Component registry
│   ├── workers/                   # Content generation
│   │   └── legacy_builder.py      # Synthesis worker
│   ├── security/                  # Encryption & certificates
│   │   ├── chacha20_vault.py      # Data encryption
│   │   └── certificate_generator.py # 13-layer certs
│   ├── output/                    # Evidence preparation
│   │   └── evidence_bundle.py     # Bundle generator
│   └── integrations/              # External system connectors
│       ├── apex_client.py         # APEX handshake client
│       ├── apex_callback_handler.py # Certificate receiver
│       └── truemark_mint_connector.py # Asset minting
├── apex/                          # APEX DOC reference implementation
│   ├── validators/                # Input validation
│   │   └── evidence_bundle.py     # Gatekeeper validator
│   ├── handlers/                  # Processing pipeline
│   │   └── certification_orchestrator.py # 13-layer processor
│   └── endpoints/                 # API endpoints
│       └── status.py              # Status polling
├── backend/                       # FastAPI application
│   └── app/
│       ├── main.py                # Application entry point
│       ├── api/v1/endpoints/      # GOAT API endpoints
│       └── config.py              # Configuration
├── frontend/                      # React dashboard (optional)
│   ├── src/
│   │   ├── components/            # UI components
│   │   ├── pages/                 # Dashboard pages
│   │   └── App.jsx
│   └── package.json
├── tests/                         # Comprehensive test suite
│   ├── test_goat_apex_handshake_protocol.py
│   ├── test_goat_apex_truemark_pipeline.py
│   └── test_goat_core_integration.py
├── docs/                          # Documentation
│   ├── BUILD_SUMMARY.md           # Architecture overview
│   ├── QUICK_START.md             # Setup guide
│   └── DEPLOYMENT.md              # Production deployment
├── Dockerfile                     # Container definition
├── docker-compose.yml             # Multi-service orchestration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🔧 Core Components

### **GOAT Field SKG (Space-Field Knowledge Graph)**
```python
from goat.core.goat_field_skg import GOATFieldSKG

field = GOATFieldSKG()
await field.observe(FieldObservation(
    operation_type="evidence_preparation",
    inputs_hash="...",
    outcome="success",
    metrics={"confidence": 0.95}
))
```

### **Evidence Bundle Generation**
```python
from goat.output.evidence_bundle import EvidenceBundleGenerator

generator = EvidenceBundleGenerator()
bundle = await generator.create_bundle(
    content_files=[...],
    provenance_log=[...],
    certification_request={
        "layer_profile": "STANDARD_13",
        "callback_url": "https://goat.gg/callback"
    }
)
```

### **APEX Handshake Protocol**
```python
from goat.integrations.apex_client import APEXClient

async with APEXClient(endpoint="https://apex.doc/v1",
                     api_key="goat_key",
                     api_secret=b"secret") as client:
    result = await client.submit_bundle(bundle)
    status = await client.get_status(result["apex_request_id"])
```

---

## 📡 API Endpoints

### GOAT Core
- `POST /api/v1/field/observe` - Record field observation
- `GET /api/v1/field/review` - Access review interface
- `POST /api/v1/bundles/generate` - Create evidence bundle
- `POST /api/v1/bundles/submit` - Submit to APEX

### APEX Integration
- `POST /api/v1/apex/submit` - Submit bundle to APEX
- `GET /api/v1/apex/status/{id}` - Check certification status
- `POST /api/v1/apex/callback` - Receive certificates

### TrueMark Integration
- `POST /api/v1/truemark/mint` - Mint certified asset
- `GET /api/v1/truemark/status/{id}` - Check mint status

### Admin Dashboard
- `GET /admin` - Complete system dashboard
- `GET /admin/field-review` - Human oversight interface
- `GET /admin/certificates` - Certificate management
- `GET /admin/integrations` - External system status

---

## 🔐 Security Model

### **Authority Separation**
- **GOAT**: Evidence preparation only (no forensic claims)
- **APEX DOC**: Certification authority (13-layer validation)
- **TrueMark**: Asset minting (blockchain bridge)

### **Cryptographic Security**
- **HMAC-SHA256**: Request signing with canonical JSON
- **Ed25519**: Certificate and callback verification
- **ChaCha20-Poly1305**: Data encryption at rest
- **Idempotency Keys**: Replay attack prevention

### **Human Oversight**
- **Mandatory Review**: All AI decisions require human rationale
- **Field Observations**: Immutable audit trail
- **Certificate Validation**: External authority verification

---

## 🏗️ Development

### **Run Tests**
```bash
# Run complete test suite
python -m pytest tests/ -v

# Run specific integration test
python -m pytest tests/test_goat_apex_handshake_protocol.py -v
```

### **Code Quality**
```bash
# Type checking
mypy goat/ --ignore-missing-imports

# Linting
flake8 goat/ --max-line-length=100

# Format code
black goat/
```

### **Build Documentation**
```bash
# Generate API docs
cd backend && python -m mkdocs build

# Serve docs locally
mkdocs serve
```

---

## 🌐 Deployment

### **Docker Deployment**
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f goat
```

### **Environment Configuration**
```bash
# Required for APEX integration
APEX_ENDPOINT=https://apex.doc/v1
APEX_API_KEY=goat_prod_xxxxxx
APEX_API_SECRET=your_hmac_secret

# Required for TrueMark integration
TRUEMARK_ENDPOINT=https://truemark.mint/v1
TRUEMARK_PRIVATE_KEY=your_ed25519_private_key

# GOAT configuration
GOAT_VERSION=2.1.0
GOAT_INSTANCE_ID=goat-prod-us-east-1
VAULT_ENCRYPTION_KEY=your_chacha20_key
```

---

## 📊 Monitoring & Health

### **Health Checks**
```bash
# System health
curl http://localhost:8000/health

# Component status
curl http://localhost:8000/health/components

# Integration status
curl http://localhost:8000/health/integrations
```

### **Metrics**
- **Field Observations**: All system operations tracked
- **Certificate Processing**: APEX integration metrics
- **Mint Success Rate**: TrueMark integration stats
- **Human Review Coverage**: Oversight compliance

---

## 🤝 Integration Partners

### **APEX DOC**
- **Role**: External certification authority
- **Integration**: GOAT↔APEX Handshake Protocol v1.0
- **Security**: HMAC-SHA256 + Ed25519 verification
- **Website**: https://apex.doc

### **TrueMark Mint**
- **Role**: Blockchain asset minting
- **Integration**: APEX→TrueMark bridge protocol
- **Security**: Ed25519 signatures + replay protection
- **Website**: https://truemark.mint

---

## 📜 Legal & Compliance

### **Copyright Notice**
Copyright © 2025-2026 PRo Prime Series and GOAT, in association with TrueMark Mint LLC. All rights reserved.

### **Patent Intent**
This software implements proprietary methods for AI evidence preparation, cryptographic certification chains, and human-AI oversight systems. Patent protection is sought for the GOAT↔APEX handshake protocol, 13-layer certificate generation, and Field Review System.

### **Trademark Protection**
"GOAT", "APEX DOC", "TrueMark", "GOAT Field", and associated logos are trademarks of PRo Prime Series. All rights reserved. Unauthorized use prohibited.

### **License**
This project is licensed under the MIT License with additional patent and trademark protections. See [LICENSE](LICENSE) for complete terms.

---

## 📖 Documentation

- **[BUILD_SUMMARY.md](docs/BUILD_SUMMARY.md)** - Complete architecture overview
- **[QUICK_START.md](docs/QUICK_START.md)** - Setup and configuration guide
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment guide
- **[GITHUB_SETUP.md](docs/GITHUB_SETUP.md)** - Repository setup instructions
- **[ALIGNMENT_DOCTRINE.md](docs/ALIGNMENT_DOCTRINE.md)** - System principles

---

## 🙏 Acknowledgments

- **FastAPI** for the exceptional async Python framework
- **React** for modern frontend development
- **Ed25519** for post-quantum signature security
- **ChaCha20-Poly1305** for authenticated encryption
- **HMAC-SHA256** for request authentication
- **APEX DOC** for certification authority
- **TrueMark Mint** for blockchain asset creation

---

## 📧 Support & Contributing

### **Issues & Questions**
- **Bug Reports**: Open GitHub issues with detailed reproduction steps
- **Security Issues**: Email security@goat.gg (do not open public issues)
- **Feature Requests**: Use GitHub Discussions
- **General Questions**: Check documentation first, then GitHub Discussions

### **Contributing**
We welcome contributions that align with our Alignment Doctrine:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/enhancement`)
3. **Implement** with comprehensive tests
4. **Document** all changes
5. **Submit** a Pull Request with detailed description

### **Code Standards**
- **Type Hints**: All Python code must have type annotations
- **Documentation**: All functions/classes must have docstrings
- **Testing**: All features must have comprehensive test coverage
- **Security**: All external integrations must maintain authority separation

---

## 🔗 Links

- **Live Demo**: https://goat.gg
- **API Documentation**: https://api.goat.gg/docs
- **APEX DOC**: https://apex.doc
- **TrueMark Mint**: https://truemark.mint
- **GitHub**: https://github.com/Spruked/GOAT

---

**Built with 🏛️ integrity by the GOAT team**

*GOAT observes. GOAT records. GOAT submits for certification. GOAT maintains truth through external authority.*

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

### 🤖 **AI-Powered Content Creation**
- **Adaptive Content Generation**: Personalized recommendations based on user needs
- **Auto-Generated Assets**: AI-created content from NFT knowledge bases
- **Knowledge Graph System**: Semantic relationships and content connections
- **Performance Analytics**: Detailed usage metrics and content insights

### 🔗 **Multi-Source Collection**
- **IPFS Integration**: Direct CID ingestion with auto-pinning
- **On-Chain Reading**: ERC-721 tokenURI extraction
- **OpenSea API**: Marketplace metadata enrichment
- **Webhook Support**: Auto-ingest from mint events

### 🎓 **Verifiable Provenance**
- **Content Badges**: Mintable NFT badges for verified creations
- **Cryptographic Proofs**: Full provenance chain for every asset
- **Feedback Loop**: Continuous improvement from user interactions

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
- **API**: http://localhost:5000
- **API Docs**: http://localhost:5000/docs
- **DALS Dashboard**: http://localhost:5000/dals/host/dashboard
- **Neo4j Browser**: http://localhost:7474
- **IPFS Gateway**: http://localhost:8080

---

## 📁 Project Structure

```
GOAT/
├── goat/                          # Core GOAT system
│   ├── core/                      # GOAT Field SKG & review system
│   │   ├── goat_field_skg.py      # 4D autobiographical memory
│   │   └── field_review_system.py # Human oversight
│   ├── distillers/                # Data processing engines
│   │   ├── visidata_engine.py     # VisiData distiller
│   │   └── registry.py            # Component registry
│   ├── workers/                   # Content generation
│   │   └── legacy_builder.py      # Synthesis worker
│   ├── security/                  # Encryption & certificates
│   │   ├── chacha20_vault.py      # Data encryption
│   │   └── certificate_generator.py # 13-layer certs
│   ├── output/                    # Evidence preparation
│   │   └── evidence_bundle.py     # Bundle generator
│   └── integrations/              # External system connectors
│       ├── apex_client.py         # APEX handshake client
│       ├── apex_callback_handler.py # Certificate receiver
│       └── truemark_mint_connector.py # Asset minting
├── apex/                          # APEX DOC reference implementation
│   ├── validators/                # Input validation
│   │   └── evidence_bundle.py     # Gatekeeper validator
│   ├── handlers/                  # Processing pipeline
│   │   └── certification_orchestrator.py # 13-layer processor
│   └── endpoints/                 # API endpoints
│       └── status.py              # Status polling
├── backend/                       # FastAPI application
│   └── app/
│       ├── main.py                # Application entry point
│       ├── api/v1/endpoints/      # GOAT API endpoints
│       └── config.py              # Configuration
├── frontend/                      # React dashboard (optional)
│   ├── src/
│   │   ├── components/            # UI components
│   │   ├── pages/                 # Dashboard pages
│   │   └── App.jsx
│   └── package.json
├── tests/                         # Comprehensive test suite
│   ├── test_goat_apex_handshake_protocol.py
│   ├── test_goat_apex_truemark_pipeline.py
│   └── test_goat_core_integration.py
├── docs/                          # Documentation
│   ├── BUILD_SUMMARY.md           # Architecture overview
│   ├── QUICK_START.md             # Setup guide
│   └── DEPLOYMENT.md              # Production deployment
├── Dockerfile                     # Container definition
├── docker-compose.yml             # Multi-service orchestration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```
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

### GOAT Core
- `POST /api/v1/field/observe` - Record field observation
- `GET /api/v1/field/review` - Access review interface
- `POST /api/v1/bundles/generate` - Create evidence bundle
- `POST /api/v1/bundles/submit` - Submit to APEX

### APEX Integration
- `POST /api/v1/apex/submit` - Submit bundle to APEX
- `GET /api/v1/apex/status/{id}` - Check certification status
- `POST /api/v1/apex/callback` - Receive certificates

### TrueMark Integration
- `POST /api/v1/truemark/mint` - Mint certified asset
- `GET /api/v1/truemark/status/{id}` - Check mint status

### Admin Dashboard
- `GET /admin` - Complete system dashboard
- `GET /admin/field-review` - Human oversight interface
- `GET /admin/certificates` - Certificate management
- `GET /admin/integrations` - External system status

---

## 🔐 Security Model

### **Authority Separation**
- **GOAT**: Evidence preparation only (no forensic claims)
- **APEX DOC**: Certification authority (13-layer validation)
- **TrueMark**: Asset minting (blockchain bridge)

### **Cryptographic Security**
- **HMAC-SHA256**: Request signing with canonical JSON
- **Ed25519**: Certificate and callback verification
- **ChaCha20-Poly1305**: Data encryption at rest
- **Idempotency Keys**: Replay attack prevention

### **Human Oversight**
- **Mandatory Review**: All AI decisions require human rationale
- **Field Observations**: Immutable audit trail
- **Certificate Validation**: External authority verification

### Environment Variables
```bash
# GOAT Configuration
GOAT_VERSION=2.1.0
GOAT_INSTANCE_ID=goat-prod-us-east-1

# APEX Integration (Required)
APEX_ENDPOINT=https://apex.doc/v1
APEX_API_KEY=goat_prod_xxxxxx
APEX_API_SECRET=your_hmac_secret

# TrueMark Integration (Required)
TRUEMARK_ENDPOINT=https://truemark.mint/v1
TRUEMARK_PRIVATE_KEY=your_ed25519_private_key

# Security
VAULT_ENCRYPTION_KEY=your_chacha20_key
HMAC_SECRET=your_request_signing_secret
```

---

## 🎯 Use Cases

### For Evidence Preparation
1. **AI System Monitoring**: GOAT observes AI operations and prepares evidence bundles
2. **Automated Review**: Human experts review GOAT observations with mandatory rationale
3. **External Certification**: APEX DOC provides independent 13-layer validation
4. **Asset Creation**: TrueMark mints certified observations as blockchain assets

### For Compliance & Audit
1. **Regulatory Compliance**: Courtroom-grade evidence preparation with external validation
2. **Audit Trails**: Complete provenance chains from observation to minted asset
3. **Authority Separation**: Independent certification prevents conflicts of interest
4. **Temporal Integrity**: Timestamp validation and sequence tracking

### For AI Governance
1. **Human Oversight**: Mandatory review of all AI decisions and observations
2. **External Validation**: APEX certification provides independent authority
3. **Blockchain Provenance**: Immutable asset records on distributed ledger
4. **Transparency**: Complete audit trail from AI observation to certified asset

### For Enterprise Integration
1. **API Integration**: RESTful APIs for evidence submission and certificate retrieval
2. **Webhook Callbacks**: Real-time certificate delivery and status updates
3. **Batch Processing**: High-volume evidence bundle processing
4. **Multi-tenant**: Isolated instances with shared certification infrastructure

---

## 🌐 Deployment

### **Docker Deployment**
```bash
# Build and run complete system
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f goat

# Scale services
docker-compose up -d --scale goat=3
```

### **Environment Configuration**
```bash
# Required for APEX integration
APEX_ENDPOINT=https://apex.doc/v1
APEX_API_KEY=goat_prod_xxxxxx
APEX_API_SECRET=your_hmac_secret

# Required for TrueMark integration
TRUEMARK_ENDPOINT=https://truemark.mint/v1
TRUEMARK_PRIVATE_KEY=your_ed25519_private_key

# GOAT configuration
GOAT_VERSION=2.1.0
GOAT_INSTANCE_ID=goat-prod-us-east-1
VAULT_ENCRYPTION_KEY=your_chacha20_key
```

### **Production Checklist**
- [ ] Configure APEX API credentials
- [ ] Set up TrueMark minting keys
- [ ] Configure ChaCha20 encryption keys
- [ ] Set up monitoring and alerting
- [ ] Configure backup and recovery
- [ ] Test integration end-to-end
- [ ] Validate certificate processing
- [ ] Confirm asset minting workflow

---

## 📊 Monitoring & Health

### **Health Checks**
```bash
# System health
curl http://localhost:8000/health

# Component status
curl http://localhost:8000/health/components

# Integration status
curl http://localhost:8000/health/integrations
```

### **Key Metrics**
- **Field Observations**: All system operations tracked
- **Certificate Processing**: APEX integration success rate
- **Mint Success Rate**: TrueMark integration statistics
- **Human Review Coverage**: Oversight compliance percentage
- **Evidence Bundle Quality**: Acceptance rate by APEX

### **Logging**
- **Structured Logging**: JSON format with correlation IDs
- **Security Events**: All authentication and authorization events
- **Integration Events**: APEX and TrueMark interaction logs
- **Audit Trail**: Complete chain from observation to asset minting

---

## 🤝 Integration Partners

### **APEX DOC**
- **Role**: External certification authority
- **Integration**: GOAT↔APEX Handshake Protocol v1.0
- **Security**: HMAC-SHA256 + Ed25519 verification
- **API**: https://apex.doc/v1
- **Status**: Production ready

### **TrueMark Mint**
- **Role**: Blockchain asset minting
- **Integration**: APEX→TrueMark bridge protocol
- **Security**: Ed25519 signatures + replay protection
- **API**: https://truemark.mint/v1
- **Status**: Production ready

### **Integration Requirements**
- **APEX API Key**: Obtain from APEX DOC
- **TrueMark Keys**: Ed25519 keypair for minting
- **HMAC Secrets**: Shared secrets for request signing
- **Callback URLs**: HTTPS endpoints for certificate delivery

## 📜 Legal & Compliance

### **Copyright Notice**
Copyright © 2025-2026 PRo Prime Series and GOAT, in association with TrueMark Mint LLC. All rights reserved.

### **Patent Intent**
This software implements proprietary methods for AI evidence preparation, cryptographic certification chains, and human-AI oversight systems. Patent protection is sought for:

- GOAT↔APEX Handshake Protocol v1.0
- 13-Layer Certificate Generation System
- GOAT Field Review System with Mandatory Human Oversight
- Authority Separation Architecture for AI Systems
- Cryptographic Evidence Bundle Generation with HMAC-SHA256

### **Trademark Protection**
"GOAT", "APEX DOC", "TrueMark", "GOAT Field", "GOAT↔APEX Handshake Protocol", and associated logos are trademarks of PRo Prime Series. All rights reserved. Unauthorized use prohibited.

### **License**
This project is licensed under the MIT License with additional patent and trademark protections. See [LICENSE](LICENSE) for complete terms.

## � Documentation

- **[BUILD_SUMMARY.md](docs/BUILD_SUMMARY.md)** - Complete architecture overview
- **[QUICK_START.md](docs/QUICK_START.md)** - Setup and configuration guide
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment guide
- **[GITHUB_SETUP.md](docs/GITHUB_SETUP.md)** - Repository setup instructions
- **[ALIGNMENT_DOCTRINE.md](docs/ALIGNMENT_DOCTRINE.md)** - System principles and philosophy
- **[DOCKER_DEPLOYMENT.md](docs/DOCKER_DEPLOYMENT.md)** - Container deployment guide

---

## 🙏 Acknowledgments

- **FastAPI** for the exceptional async Python framework
- **React** for modern frontend development
- **Ed25519** for post-quantum signature security
- **ChaCha20-Poly1305** for authenticated encryption
- **HMAC-SHA256** for request authentication
- **APEX DOC** for certification authority
- **TrueMark Mint** for blockchain asset creation
- **VisiData** for data distillation capabilities

---

## 📧 Support & Contributing

### **Issues & Questions**
- **Bug Reports**: Open GitHub issues with detailed reproduction steps
- **Security Issues**: Email security@goat.gg (do not open public issues)
- **Feature Requests**: Use GitHub Discussions
- **General Questions**: Check documentation first, then GitHub Discussions

### **Contributing**
We welcome contributions that align with our Alignment Doctrine:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/enhancement`)
3. **Implement** with comprehensive tests
4. **Document** all changes
5. **Submit** a Pull Request with detailed description

### **Code Standards**
- **Type Hints**: All Python code must have type annotations
- **Documentation**: All functions/classes must have docstrings
- **Testing**: All features must have comprehensive test coverage
- **Security**: All external integrations must maintain authority separation

---

## 🔗 Links

- **Live Demo**: https://goat.gg
- **API Documentation**: https://api.goat.gg/docs
- **APEX DOC**: https://apex.doc
- **TrueMark Mint**: https://truemark.mint
- **GitHub**: https://github.com/Spruked/GOAT

---

**Built with 🏛️ integrity by the GOAT team**

*GOAT observes. GOAT records. GOAT submits for certification. GOAT maintains truth through external authority.*