# 🐐 GOAT v2.1 - Quick Reference Card

## 🚀 One-Command Start

```bash
# Windows PowerShell
.\start.ps1

# Mac/Linux
./start.sh
```

## 📍 Access Points

| What | URL | Credentials |
|------|-----|-------------|
| **Frontend** | http://localhost:5173 | - |
| **Backend API** | http://localhost:5000 | - |
| **API Docs** | http://localhost:5000/docs | - |
| **Neo4j** | http://localhost:7474 | neo4j / goatpassword123 |

## 🔑 Key Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Rebuild
docker-compose up --build

# Reset everything
docker-compose down -v
docker-compose up --build
```

## 📂 Project Structure

```
GOAT/
├── frontend/          # React + Vite UI
├── server/            # FastAPI backend
├── vault/             # Glyph + encryption
├── collector/         # NFT ingestion
├── knowledge/         # Skill graph
├── teacher/           # AI teaching
├── licenser/          # Badge minting
└── contracts/         # Solidity contracts
```

## 🎯 Test Flow

1. **Start App**: `docker-compose up`
2. **Visit**: http://localhost:5173
3. **Collect**: Go to "Collect" → Enter IPFS CID
4. **View**: Check "Vault" for glyph
5. **Learn**: Try "Learn" for quizzes
6. **Profile**: See progress at /profile/user_demo

## 🔧 Environment Setup

```bash
# Copy template
cp .env.example .env

# Edit required vars
VAULT_ENCRYPTION_KEY=your_secret_key
POLYGON_RPC=https://polygon-rpc.com
ANCHOR_CONTRACT=0x... (after deploying contract)
```

## 🎨 Frontend Development

```bash
cd frontend
npm install
npm run dev     # Start dev server
npm run build   # Production build
```

## 🐍 Backend Development

```bash
pip install -r requirements.txt
cd server
python -m uvicorn main:app --reload
```

## 📡 Key API Endpoints

### Vault
```bash
GET  /api/vault/stats           # Vault statistics
GET  /api/glyph/{id}            # Get glyph
GET  /api/vault/proof/{id}      # Get proof
```

### Collector
```bash
POST /api/collect/ipfs          # Ingest from IPFS
POST /api/collect/onchain       # Ingest from chain
```

### Teacher
```bash
GET  /api/teach/recommend/{id}  # Get lesson
GET  /api/teach/quiz/{skill}    # Generate quiz
POST /api/teach/submit-quiz     # Submit answers
```

## 📜 Deploy Smart Contract

```bash
# Using Foundry
cd contracts
forge create --rpc-url $POLYGON_RPC \
  --private-key $PRIVATE_KEY \
  GOATVaultAnchor

# Or use Remix
# Visit remix.ethereum.org
# Deploy to Polygon Mumbai testnet
```

## 🐛 Troubleshooting

### Docker Issues
```bash
# Rebuild
docker-compose build --no-cache

# Check logs
docker-compose logs backend
docker-compose logs frontend

# Reset volumes
docker-compose down -v
```

### Port Conflicts
```bash
# Change ports in docker-compose.yml
ports:
  - "5001:5000"  # Backend
  - "3000:80"    # Frontend
```

### Frontend Can't Reach Backend
```bash
# Check vite.config.js proxy
# Verify CORS in server/main.py
# Test backend: curl http://localhost:5000/api/health
```

## 📚 Documentation Files

- `README.md` - Complete guide
- `BUILD_SUMMARY.md` - What was built
- `DEPLOYMENT.md` - Deploy instructions
- `BUILD_SUMMARY.md` - Features overview

## 🎁 What You Get

✅ Complete React frontend (5 pages)
✅ FastAPI backend (25+ endpoints)
✅ Glyph + Vault cryptographic system
✅ IPFS + blockchain integration
✅ AI teaching engine
✅ Badge minting system
✅ Docker deployment ready
✅ Production-ready architecture

## ⚡ Quick Test

```bash
# Test backend
curl http://localhost:5000/api/health

# Should return:
# {"status":"healthy","vault":{"total_glyphs":0,...}}
```

## 🔒 Security Notes

⚠️ **Change these in production:**
- `VAULT_ENCRYPTION_KEY`
- `PRIVATE_KEY`
- Neo4j password
- Add HTTPS
- Set proper CORS origins

## 🚢 Production Deploy

```bash
# Build frontend
cd frontend && npm run build

# Deploy backend to Railway
railway up

# Deploy frontend to Vercel
vercel --prod

# Or use Docker
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 Tech Stack at a Glance

**Backend**: Python 3.11 + FastAPI
**Frontend**: React 18 + Vite + Tailwind
**Database**: SQLite (+ Neo4j optional)
**Blockchain**: Web3.py + Polygon
**Storage**: IPFS + encrypted vault
**Deploy**: Docker + Docker Compose

---

**💡 Pro Tip**: Check `BUILD_SUMMARY.md` for complete feature list!

**The GOAT is ready to teach. Let's go! 🚀**
