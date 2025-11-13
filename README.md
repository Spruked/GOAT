# GOAT v2.1 - The Proven Teacher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.20-363636.svg)](https://soliditylang.org/)

**NFT Knowledge Engine with Glyph + Vault Provenance System**

> Turn any NFT into a self-improving, AI-powered teacher that verifies learning on-chain.  
> Every lesson is signed. Every skill is provable. Every teacher is accountable.

---

## 🌟 Features

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
- **API**: http://localhost:5000
- **API Docs**: http://localhost:5000/docs
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
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── server/
│   └── main.py              # FastAPI backend
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
├── teacher/
│   └── engine.py            # Adaptive learning
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
cd server
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

### Vault
- `GET /api/vault/stats` - Get vault statistics
- `GET /api/glyph/{id}` - Retrieve glyph by ID
- `GET /api/vault/proof/{id}` - Get cryptographic proof
- `GET /glyph/svg/{id}` - Get glyph SVG image
- `GET /glyph/badge/{id}` - Get verification badge

### Collector
- `POST /api/collect/ipfs` - Ingest from IPFS
- `POST /api/collect/onchain` - Ingest from blockchain
- `POST /api/collect/webhook` - Handle mint webhooks

### Teacher
- `GET /api/teach/recommend/{user_id}` - Get personalized lesson
- `GET /api/teach/quiz/{skill_id}` - Generate quiz
- `POST /api/teach/submit-quiz` - Submit quiz answers
- `GET /api/teach/progress/{user_id}` - Get user progress

### Verifier
- `POST /api/verify/mint-badge` - Mint learner badge
- `POST /api/verify/feedback` - Submit feedback

### On-Chain Anchor
- `POST /api/anchor/batch` - Anchor glyph batch
- `GET /api/anchor/verify/{root}` - Verify anchor
- `GET /api/anchor/proof` - Get Merkle proof

---

## 🔐 Security

### Vault Encryption
- **AES-256**: Industry-standard encryption at rest
- **EIP-191 Signatures**: Ethereum-compatible signing
- **SQLite Ledger**: Immutable audit log

### Environment Variables
```bash
VAULT_ENCRYPTION_KEY=your_secret_key  # Change in production!
PRIVATE_KEY=0x...                      # For EIP-191 signing
POLYGON_RPC=https://polygon-rpc.com
ANCHOR_CONTRACT=0x...                  # Deployed contract address
```

---

## 🎯 Use Cases

### For Educators
1. Mint educational NFTs with IPFS content
2. GOAT auto-ingests and creates glyphs
3. AI generates lessons and quizzes
4. Students earn verifiable badges

### For Learners
1. Browse recommended skills
2. Complete adaptive lessons
3. Take AI-generated quizzes
4. Mint proof-of-learning badges

### For Platforms
1. Integrate via webhook for auto-ingestion
2. Embed GOAT widget in marketplace
3. Verify learner credentials on-chain
4. Track learning analytics

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

- **Documentation**: [BUILD_SUMMARY.md](BUILD_SUMMARY.md) | [DEPLOYMENT.md](DEPLOYMENT.md) | [QUICK_START.md](QUICK_START.md)
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

*The GOAT now doesn't just teach — it **proves**.*
