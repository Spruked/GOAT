# TrueMark Enterprise Certificate Forge v2.0

**Enterprise-grade cryptographically-verifiable certificate generation with forensic anti-AI artifacts, HMAC-SHA256 signing, vault integration, and Swarm Knowledge Graph (SKG) pattern learning.**

## ⚠️ LEGAL DISCLAIMER

**CRITICAL LEGAL NOTICE:** This TrueMark Certificate is issued solely for business documentation and record-keeping purposes. This certificate **DOES NOT** constitute a legal title, security, financial instrument, negotiable instrument, or any form of official government documentation.

**This certificate should NEVER be used for:**
- Banking transactions or financial services
- Legal proceedings or court documents
- Regulatory compliance or government filings
- Financial reporting or tax documentation
- Any official or legal purposes

**Always consult qualified legal counsel** before using certificates for any purpose beyond personal business documentation.

## 🎯 Features

- ✅ **Forensic PDF Rendering**: 10-layer artifact system (micro-noise, baseline drift, kerning variance)
- ✅ **Cryptographic Signing**: HMAC-SHA256 with persistent root authority key
- ✅ **Vault Integration**: Immutable JSONL audit trails with event logging
- ✅ **Swarm Knowledge Graph**: Pattern learning, duplicate detection, drift analysis
- ✅ **DALS Serial Generation**: DALS-001 compliant with category encoding (Knowledge/Asset/Identity)
- ✅ **QR Code Verification**: Blockchain anchor verification links
- ✅ **Custom Branding**: Logo, seal, watermark integration

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd truemark_certificates
pip install -r requirements.txt
```

### 2. Generate Certificate (ONE COMMAND)
```bash
python certificate_forge.py \
  --owner "Bryan A. Spruk" \
  --wallet "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1" \
  --title "Caleon Prime Knowledge Base" \
  --category Knowledge \
  --chain Polygon
```

### 3. Docker Deployment
```bash
docker-compose up -d
docker exec truemark-certificate-forge python certificate_forge.py --skg
```

## 📁 Package Structure

```
truemark_certificates/
├── generator.py              # Enhanced certificate generation engine
├── mint_certificate.py       # CLI wrapper (main entry point)
├── requirements.txt          # Dependencies
└── README.md                 # This documentation
```

## 🎨 Certificate Layout (Professional Design)

### Header Section
- **TrueMark®** branding (large, centered)
- **Certificate of Authenticity** title
- **DALS Framework** notice
- **Serial number badge** (top-right)

### Content Sections

#### 1. Asset Information
- Asset Title
- NFT Classification (KEP Category)
- Description

#### 2. Owner Information
- Owner Name
- Web3 Wallet Address
- TrueMark Domain

#### 3. Technical Specifications
- Chain ID | Issue Date
- IPFS Hash | Verification ID

### Security Features
- **Guilloche border pattern** (anti-forgery)
- **TrueMark tree watermark** (subtle background)
- **Gold embossed seal** (official appearance)
- **QR verification code** (blockchain validation)

### Legal Compliance
- **Comprehensive disclaimer** (full legal notice)
- **Business documentation only** warning
- **Signature section** (officer and date)

## 📋 Complete Field Set

| Field | Description | Required | Display |
|-------|-------------|----------|---------|
| `dals_serial` | DALS Serial Number | ✅ | Header badge |
| `owner_name` | Owner Full Name | ✅ | Owner section |
| `asset_title` | Asset/NFT Title | ✅ | Asset section |
| `wallet` | Web3 Wallet Address | ✅ | Owner section |
| `web3_domain` | TrueMark Domain | ❌ | Owner section |
| `kep_category` | NFT Classification | ❌ | Asset section |
| `ipfs_hash` | IPFS Content Hash | ❌ | Technical section |
| `description` | Asset Description | ❌ | Asset section |
| `chain_id` | Blockchain Network ID | ❌ | Technical section |
| `stardate` | Issue Timestamp | Auto | Technical section |
| `sig_id` | Verification ID | Auto | Technical section |
| `verification_url` | QR Code URL | Auto | QR code |

## 🛠️ CLI Usage

```bash
python mint_certificate.py [OPTIONS]

Options:
  --serial TEXT      DALS Serial Number (required)
  --owner TEXT       Owner Name (required)
  --title TEXT       Asset Title (required)
  --wallet TEXT      Web3 Wallet Address (required)
  --domain TEXT      TrueMark Web3 Domain
  --category TEXT    NFT Classification (default: General)
  --ipfs TEXT        IPFS Hash
  --description TEXT Asset Description
  --chain-id TEXT    Chain ID (default: 1)
  --output TEXT      Output PDF file path
  --format TEXT      Paper format: letter or a4 (default: letter)
```

## 🔧 Programmatic Usage

```python
from generator import create_enhanced_truemark_certificate

certificate_data = {
    'dals_serial': 'DALSM0001',
    'owner_name': 'Bryan A. Spruk',
    'asset_title': 'Caleon Prime',
    'wallet': '0xA377665...',
    'web3_domain': 'bryan.truemark',
    'kep_category': 'Knowledge',
    'ipfs_hash': 'ipfs://QmXyZ...',
    'description': 'Advanced AI knowledge system',
    'chain_id': '1',
    'stardate': '20251210.1430',
    'sig_id': 'ABC123DEF456',
    'verification_url': 'https://truemark.verify/DALSM0001'
}

create_enhanced_truemark_certificate(
    data=certificate_data,
    output_path='certificate.pdf'
)
```

## 🎨 Design Features

### Professional Styling
- **Typography**: Clean, readable fonts with proper hierarchy
- **Color Scheme**: Professional blue and gold theme
- **Layout**: Organized sections with clear visual separation
- **Spacing**: Proper margins and padding throughout

### Security Elements
- **Guilloche Pattern**: Complex interlocking circles (anti-counterfeiting)
- **Watermark**: Subtle TrueMark tree symbol (8% opacity)
- **Seal**: Gold embossed design with star pattern
- **Borders**: Multiple security borders with different styles

### Technical Quality
- **Resolution**: 300 DPI print quality
- **Color**: CMYK color profile for professional printing
- **Fonts**: Embedded and subset for consistent display
- **Compression**: Optimized file size

## 📄 Output Specifications

- **Format**: PDF 1.7 (print-ready)
- **Size**: Letter (8.5×11 inches) or A4
- **Resolution**: 300 DPI
- **Color Mode**: CMYK
- **Fonts**: Helvetica family + Courier (embedded)
- **Security**: Password protection available

## 🔒 Security & Legal

### Security Features
- **Tamper-evident design** with security patterns
- **QR code verification** for blockchain validation
- **Unique serial numbering** system
- **Timestamp authentication** with stardate format
- **Digital signature support** (future enhancement)

### Legal Compliance
- **Clear disclaimers** on every certificate
- **Business documentation only** designation
- **No legal/financial instrument** warnings
- **Attorney-reviewed language** (recommended)

## 🆘 Troubleshooting

### Common Issues

**"polygon method not found"**
- This is a ReportLab compatibility issue
- The enhanced generator uses proper drawing methods

**"Font not found"**
- The generator uses standard fonts (Helvetica, Courier)
- Custom fonts can be added to the system

**"QR code generation failed"**
- Ensure qrcode[pil] package is installed
- Check that PIL/Pillow is available

### Getting Help
- Check the CLI help: `python mint_certificate.py --help`
- Verify all required fields are provided
- Ensure output directory is writable

## 📈 Version History

- **v2.0** - Enhanced professional design
  - Complete redesign with professional layout
  - Enhanced security features
  - Comprehensive legal disclaimers
  - Improved field organization
  - Better typography and styling

- **v1.0** - Initial release
  - Basic certificate generation
  - Core security features
  - CLI interface

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

**Legal Notice**: This certificate is for business documentation purposes only. It is NOT a legal financial instrument or government document.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Support

- **GitHub Issues**: https://github.com/Spruked/GOAT/issues
- **Discussions**: GitHub Discussions for questions
- **Email**: bryan@truemark.io

## Author

Bryan A. Spruk - TrueMark Technologies  
Email: bryan@truemark.io  
GitHub: [@Spruked](https://github.com/Spruked)

## Acknowledgments

- ReportLab for PDF generation
- Python community for excellent libraries
- DALS Framework contributors

---

## 📄 Copyright

Copyright © 2025-2026 PRo Prime Series and GOAT, in association with TrueMark Mint LLC. All rights reserved.

---

**TrueMark® Enterprise Certificate Forge v2.0**  
*Digital Asset Ledger System (DALS)*  
*Professional Business Documentation Only*