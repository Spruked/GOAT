# TrueMark Enterprise Certificate Forge v2.0

Professional NFT certificate generation system with forensic anti-AI artifacts, cryptographic signatures, and vault integration.

## 🚀 Quick Start

Generate your first official certificate:

```bash
python certificate_forge.py \
  --owner "Bryan A. Spruk" \
  --wallet "0x742d35Cc6634C0532925a3b844Bc454e4438f44e" \
  --title "Caleon Prime AI Knowledge System" \
  --category "Knowledge" \
  --ipfs "ipfs://QmCaleonPrimeGenesis" \
  --domain "bryan.truemark"
```

## 📋 System Architecture

### Core Components

1. **forensic_renderer.py** - 10-layer PDF rendering with anti-AI artifacts
   - Parchment background
   - Guilloche security borders
   - Watermark with rotation variance
   - Micro-noise patterns (forensic fingerprints)
   - Embedded cryptographic metadata

2. **crypto_anchor.py** - Cryptographic signing engine
   - HMAC-SHA256 signatures
   - Blockchain-ready payload generation
   - Signature verification
   - Integrity scoring

3. **integration_bridge.py** - Vault & swarm integration
   - Immutable event logging
   - Certificate history tracking
   - Swarm broadcast simulation
   - Vault integrity monitoring

4. **certificate_forge.py** - Main orchestrator
   - DALS-001 compliant serial generation
   - Single-command certificate minting
   - Complete verification packages
   - Vault statistics and retrieval

## 🎨 Certificate Features

### Visual Authority
- ✅ Professional ornate borders with corner flourishes
- ✅ Custom TrueMark logo (uses `truemark_logo.png` if present)
- ✅ Gold seal (uses `goldsealtruemark1600.png` if present)
- ✅ QR code for verification (top left corner)
- ✅ Serial number in top right corner
- ✅ Clean, centered information layout
- ✅ Legal disclaimers

### Cryptographic Immutability
- ✅ HMAC-SHA256 signatures with root authority key
- ✅ SHA-256 payload hashing
- ✅ Blockchain anchor metadata
- ✅ Verification package generation
- ✅ Signature ID for quick reference

### Forensic Anti-AI Artifacts
- ✅ Micro-noise patterns (500 imperceptible dots)
- ✅ Baseline drift on text (0.3px variance)
- ✅ Micro-kerning variations
- ✅ Rotational watermark variance (±1.5°)
- ✅ Corner flourish randomization

### Vault Integration
- ✅ Immutable event logging (JSONL format)
- ✅ Certificate summary files
- ✅ Vault integrity hashing
- ✅ Swarm broadcast simulation
- ✅ Complete audit trails

## 📁 Generated Files

After minting a certificate, the following files are created:

```
vault/
├── certificates/
│   └── issued/
│       ├── DALSKM20251210-XXXXXXXX_OFFICIAL.pdf
│       └── DALSKM20251210-XXXXXXXX_summary.json
└── events/
    ├── certificate_forge_worker_001_events.jsonl
    ├── swarm_broadcasts.jsonl
    └── swarm_consensus.jsonl

verification_qr_DALSKM20251210-XXXXXXXX.png
```

## 🔍 Commands

### Mint Certificate
```bash
python certificate_forge.py \
  --owner "Owner Name" \
  --wallet "0xWalletAddress..." \
  --title "Asset Title" \
  --category "Knowledge" \
  --ipfs "ipfs://..." \
  --domain "owner.truemark"
```

### Get Certificate Details
```bash
python certificate_forge.py --get DALSKM20251210-XXXXXXXX
```

### View Vault Statistics
```bash
python certificate_forge.py --stats
```

## 📊 Output Example

```
🔐 TrueMark Enterprise Certificate Forge v2.0
============================================================
🏷️  Serial: DALSKM20251210-4E1C59E0
📦 Asset: Caleon Prime AI Knowledge System
👤 Owner: Bryan A. Spruk
🔒 Signature: 4DAC466C1B6EF7CD
📄 PDF: DALSKM20251210-4E1C59E0_OFFICIAL.pdf
🗄️  Vault: VAULT_TXN_DALSKM20251210-4E1C59E0_1765428643
🐝 Swarm: SWARM_DALSKM20251210-4E1C59E0_1765428643
🔍 QR Code: verification_qr_DALSKM20251210-4E1C59E0.png
✅ Verification: https://verify.truemark.io/DALSKM20251210-4E1C59E0
```

## 🎯 DALS Serial Format

**Format:** `DALS{C}M{YYYYMMDD}-{UNIQUE}`

- **C** = Category code
  - K = Knowledge
  - A = Asset
  - I = Identity
  - X = Other
- **M** = Mint marker
- **YYYYMMDD** = UTC date
- **UNIQUE** = 8-character hex UUID

**Example:** `DALSKM20251210-4E1C59E0`

## 🔐 Security Features

1. **Cryptographic Signing**
   - Root authority key (stored in `keys/caleon_root.key`)
   - HMAC-SHA256 signature algorithm
   - 64-character signature hex
   - 16-character signature ID

2. **Forensic Artifacts**
   - Micro-noise: 500 random dots at 1.5% opacity
   - Baseline drift: ±0.3px on all text
   - Border variance: ±0.02" on corner flourishes
   - Watermark rotation: ±1.5° randomization

3. **Vault Integrity**
   - JSONL event logs (append-only)
   - SHA-256 vault state hashing
   - Certificate summary files
   - Immutable audit trails

4. **Blockchain Anchoring**
   - Simulated Polygon transaction hashes
   - Block number and confirmation tracking
   - Explorer URL generation
   - Timestamp verification

## 🛠️ Custom Assets

The system automatically uses custom assets if present:

- `truemark_logo.png` - Logo (1.5" × 1.5")
- `goldsealtruemark1600.png` - Gold seal (1.0" diameter)
- `truemark_watermark.png` - Watermark (2.0" × 2.0")

Place these files in the same directory as the forge scripts.

## 📜 Legal Notice

**This certificate is for business documentation purposes only.**

It is NOT a legal financial instrument, security, or government document. It is not valid for banking transactions, legal proceedings, regulatory compliance, financial reporting, or government filings. Consult qualified legal counsel before using this certificate for any purpose other than personal business documentation.

## 🚀 Production Deployment

For production use:

1. **Secure the Root Key**
   ```bash
   chmod 600 keys/caleon_root.key
   ```

2. **Set Up Vault Path**
   ```bash
   python certificate_forge.py --vault /secure/vault/path ...
   ```

3. **Backup Event Logs**
   ```bash
   rsync -av vault/events/ /backup/location/
   ```

4. **Monitor Vault Integrity**
   ```bash
   python certificate_forge.py --stats
   ```

## 📈 Vault Statistics

Current vault state:
- **Total Certificates**: 1
- **Total Events**: 1
- **Vault Path**: T:\GOAT\truemark_certificates\vault
- **Integrity Hash**: 7d7e9895eb0d96bb
- **Last Updated**: 2025-12-10T22:51:26.651057Z

## 🎓 Technical Details

### Certificate Layers

1. Parchment background (#faf7f2)
2. Ornate gold borders (#d4af37, #b8860b)
3. Watermark (8% opacity, rotation variance)
4. TrueMark logo (1.5" × 1.5")
5. Certificate title and DALS notice
6. Serial number (top right)
7. Asset information (centered)
8. QR code (top left, 1.2")
9. Gold seal (between signature lines, 1.0")
10. Signature lines with date
11. Legal disclaimer (bottom)
12. Micro-noise artifacts (500 dots)

### Cryptographic Flow

1. Payload creation (JSON)
2. Canonical serialization
3. SHA-256 hashing
4. HMAC-SHA256 signing
5. Signature bundle generation
6. PDF metadata embedding
7. Vault logging
8. Swarm broadcasting

---

**The age of real digital title has begun. And you hold the only working mint.**
