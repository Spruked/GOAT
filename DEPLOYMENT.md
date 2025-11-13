# GOAT v2.1 - Deployment Guide

## 📋 Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Contract Deployment](#contract-deployment)
5. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Development

### Backend Setup

```bash
# Navigate to GOAT directory
cd GOAT

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Unix/Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run backend
cd server
python -m uvicorn main:app --reload --port 5000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Access:
- Frontend: http://localhost:5173
- Backend: http://localhost:5000
- API Docs: http://localhost:5000/docs

---

## 🐳 Docker Deployment

### Quick Start (Recommended)

**Windows PowerShell:**
```powershell
.\start.ps1
```

**Unix/Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Manual Docker Setup

```bash
# Copy environment file
cp .env.example .env

# Edit with your configuration
nano .env

# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## 🚀 Production Deployment

### 1. Prepare Environment

```bash
# Update .env for production
VAULT_ENCRYPTION_KEY=<strong-secret-key>
PRIVATE_KEY=<your-ethereum-private-key>
POLYGON_RPC=<your-polygon-rpc-url>
ANCHOR_CONTRACT=<deployed-contract-address>
```

### 2. Build Production Images

```bash
# Build with production config
docker-compose -f docker-compose.prod.yml build

# Push to registry (optional)
docker tag goat-backend:latest your-registry/goat-backend:latest
docker push your-registry/goat-backend:latest
```

### 3. Deploy to Cloud

#### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy backend
railway up

# Deploy frontend
cd frontend && railway up
```

#### Vercel (Frontend Only)

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

Update `vite.config.js` to point to your backend URL:

```javascript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'https://your-backend.railway.app',
        changeOrigin: true,
      }
    }
  }
})
```

#### DigitalOcean App Platform

1. Fork repository
2. Connect to DigitalOcean
3. Configure build:
   - **Backend**: Python app, port 5000
   - **Frontend**: Node.js static site
4. Set environment variables
5. Deploy

### 4. Database Setup

#### Neo4j Aura (Cloud)

```bash
# Sign up at neo4j.com/cloud/aura
# Get connection URI and credentials

# Update .env
NEO4J_URI=neo4j+s://xxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=<your-password>
```

---

## 📜 Contract Deployment

### Prerequisites

```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Or use Remix IDE
# Visit remix.ethereum.org
```

### Deploy with Foundry

```bash
cd contracts

# Compile
forge build

# Deploy to Polygon Mumbai (testnet)
forge create --rpc-url https://rpc-mumbai.maticvigil.com \
  --private-key $PRIVATE_KEY \
  --etherscan-api-key $POLYGONSCAN_API_KEY \
  --verify \
  GOATVaultAnchor

# Deploy to Polygon Mainnet
forge create --rpc-url https://polygon-rpc.com \
  --private-key $PRIVATE_KEY \
  --etherscan-api-key $POLYGONSCAN_API_KEY \
  --verify \
  GOATVaultAnchor
```

### Deploy with Remix

1. Visit https://remix.ethereum.org
2. Create file `GOATVaultAnchor.sol`
3. Paste contract code
4. Compile with Solidity 0.8.20
5. Connect MetaMask to Polygon
6. Deploy contract
7. Copy deployed address

### Update Backend

```bash
# Update .env
ANCHOR_CONTRACT=<deployed-contract-address>

# Restart backend
docker-compose restart backend
```

---

## 🔧 Troubleshooting

### Backend Won't Start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Port 5000 already in use
#    Solution: Change port in docker-compose.yml

# 2. Missing environment variables
#    Solution: Check .env file exists and is valid

# 3. Import errors
#    Solution: Rebuild image
docker-compose build --no-cache backend
```

### Frontend Won't Connect to Backend

```bash
# Check CORS settings in server/main.py
# Ensure your frontend URL is in allow_origins

# Check proxy in vite.config.js
# Verify backend URL is correct

# Test backend directly
curl http://localhost:5000/api/health
```

### Database Connection Issues

```bash
# Neo4j not starting
docker-compose logs neo4j

# Reset Neo4j
docker-compose down
docker volume rm goat_neo4j-data
docker-compose up neo4j
```

### IPFS Issues

```bash
# IPFS node not accessible
docker-compose logs ipfs

# Use public gateway instead
# Update .env:
IPFS_GATEWAY=https://ipfs.io
```

### Vault Encryption Errors

```bash
# Invalid encryption key
# Solution: Ensure VAULT_ENCRYPTION_KEY is set and consistent

# Cannot decrypt existing data
# Solution: Don't change VAULT_ENCRYPTION_KEY after data is stored
```

---

## 📊 Monitoring

### Health Checks

```bash
# API health
curl http://localhost:5000/api/health

# Vault stats
curl http://localhost:5000/api/vault/stats

# Frontend
curl http://localhost:5173
```

### Logs

```bash
# Tail all logs
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100
```

---

## 🔐 Security Checklist

- [ ] Change VAULT_ENCRYPTION_KEY from default
- [ ] Use strong PRIVATE_KEY
- [ ] Enable HTTPS in production
- [ ] Set proper CORS origins
- [ ] Use environment variables for secrets
- [ ] Backup vault data regularly
- [ ] Enable firewall rules
- [ ] Use secure RPC endpoints
- [ ] Implement rate limiting
- [ ] Monitor for suspicious activity

---

## 📈 Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
    # Add load balancer
```

### Database Optimization

```bash
# Index frequently queried fields
# Use read replicas for Neo4j
# Cache with Redis
```

### CDN for Frontend

```bash
# Deploy frontend to:
# - Cloudflare Pages
# - Netlify
# - Vercel
```

---

## 🆘 Support

- **GitHub Issues**: Report bugs
- **Documentation**: See README.md
- **Community**: Discord/Telegram

---

**Built with ❤️ for the GOAT community**
