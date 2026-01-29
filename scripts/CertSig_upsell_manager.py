# partner_referral_manager.py (formerly CertSig_upsell_manager.py)
"""
GOAT Partner Referral Manager
Handles referrals to Alpha CertSig Mint and TrueMark Mint with exclusive 30% discounts
Updated December 18, 2025 - GOAT does NOT mint NFTs, only prepares and refers
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional

class PartnerReferralManager:
    """Manages referrals to partner minting services with exclusive discounts"""

    def __init__(self):
        self.partner_services = {
            "alpha_certsig": {
                "name": "Alpha CertSig Mint",
                "description": "Blockchain minting with multi-chain support",
                "referral_url": "https://alphamint.certsig.io?ref=GOAT30",
                "features": [
                    "ERC-721/ERC-1155 minting",
                    "Multi-chain support (Ethereum, Polygon, Base, Arbitrum)",
                    "IPFS pinning included",
                    "ChaCha24/128/256 encryption upgrades",
                    "Permanent authorship proof",
                    "Timestamped creation records"
                ],
                "standard_price_eth": 0.08,
                "goat_discount_eth": 0.056,
                "discount_code": "GOAT30",
                "discount_percent": 30
            },
            "truemark": {
                "name": "TrueMark Mint",
                "description": "Identity-linked permanent blockchain records",
                "referral_url": "https://mint.truemark.com?ref=GOAT30",
                "features": [
                    "Identity-linked minting",
                    ".go domain integration",
                    "GDIS identity verification",
                    "Royalty tracking built-in",
                    "Multi-chain support",
                    "White-label branding options",
                    "ChaCha24/128/256 encryption upgrades",
                    "Enterprise compliance ready"
                ],
                "standard_price_eth": 0.15,
                "goat_discount_eth": 0.105,
                "discount_code": "GOAT30",
                "discount_percent": 30
            }
        }

    def get_referral_options(self) -> Dict[str, Any]:
        """Get available partner minting options with GOAT discounts"""
        return {
            "partners": self.partner_services,
            "goat_benefits": [
                "✅ 30% exclusive discount at both partners",
                "✅ Package already prepared by GOAT",
                "✅ No additional metadata work needed",
                "✅ One-click export to partner",
                "✅ Bonus encryption upgrades available",
                "✅ Support from both GOAT and partner teams"
            ],
            "revenue_model": "GOAT + Partner revenue sharing (win-win-win)"
        }

    def prepare_referral_package(self, legacy_data: Dict[str, Any], partner: str, vault_tier: str = "basic") -> Dict[str, Any]:
        """Prepare data package for partner minting (GOAT does not mint)"""
        
        metadata = legacy_data.get("nft_metadata", {})
        
        # Generate content hash for verification
        content_hash = self._generate_content_hash(legacy_data)
        
        # Prepare partner-specific package
        referral_package = {
            "goat_package_version": "2.1",
            "prepared_by": "GOAT",
            "partner": partner,
            "referral_code": self.partner_services[partner]["discount_code"],
            "discount_applied": "30%",
            "metadata": metadata,
            "content_hash": content_hash,
            "vault_tier": vault_tier,
            "timestamp": datetime.utcnow().isoformat(),
            "export_format": "zip",  # Always provide ZIP
            "encryption_ready": self._get_encryption_level(vault_tier),
            "blockchain_ready": True,
            "ipfs_ready": True,
            "instructions": self._get_minting_instructions(partner, vault_tier)
        }

        return referral_package

    def _generate_content_hash(self, legacy_data: Dict[str, Any]) -> str:
        """Generate SHA-256 hash of legacy content for verification"""
        import hashlib
        content_str = json.dumps(legacy_data, sort_keys=True, default=str)
        return hashlib.sha256(content_str.encode()).hexdigest()

    def _get_encryption_level(self, vault_tier: str) -> Dict[str, Any]:
        """Get encryption options based on vault tier"""
        encryption_levels = {
            "basic": {
                "included": "AES-256",
                "upgrade_options": ["ChaCha24"]
            },
            "pro": {
                "included": "AES-256",
                "upgrade_options": ["ChaCha24", "ChaCha128"]
            },
            "immortal": {
                "included": "AES-256 + ChaCha128 option",
                "upgrade_options": ["ChaCha128", "ChaCha256"]
            },
            "dynasty": {
                "included": "AES-256 + ChaCha256",
                "upgrade_options": []  # Already has highest level
            }
        }
        return encryption_levels.get(vault_tier, encryption_levels["basic"])

    def _get_minting_instructions(self, partner: str, vault_tier: str) -> str:
        """Get detailed instructions for minting at partner"""
        
        partner_info = self.partner_services[partner]
        
        instructions = f"""
🎯 READY TO MINT AT {partner_info['name'].upper()}

Your GOAT package is prepared and ready. Here's what happens next:

STEP 1: Download Your Package
- Click "Download ZIP Package" below
- Your package includes all metadata, hashes, and content
- Everything is blockchain-ready

STEP 2: Visit {partner_info['name']}
- URL: {partner_info['referral_url']}
- Your 30% discount is automatically applied with code: {partner_info['discount_code']}

STEP 3: Upload & Mint
- Upload your GOAT ZIP package
- {partner_info['name']} will handle:
  • IPFS pinning
  • Blockchain transaction
  • Smart contract deployment
  • Certificate generation

PRICING:
- Standard: {partner_info['standard_price_eth']} ETH + gas
- GOAT Exclusive: {partner_info['goat_discount_eth']} ETH + gas (30% OFF!)
- Savings: {partner_info['standard_price_eth'] - partner_info['goat_discount_eth']} ETH

BONUS OPTIONS AT CHECKOUT:
"""
        
        encryption = self._get_encryption_level(vault_tier)
        if encryption["upgrade_options"]:
            instructions += "\n".join([f"- {opt} encryption upgrade" for opt in encryption["upgrade_options"]])
        else:
            instructions += "- Your Dynasty package already includes ChaCha256 encryption!"
        
        instructions += f"""

WHY MINT?
✅ Permanent proof of authorship
✅ Timestamped creation record on blockchain
✅ Decentralized storage (IPFS/Arweave)
✅ Transferable ownership
✅ Royalty tracking (TrueMark)
✅ Protects your intellectual property forever
✅ Cannot be altered or deleted

SUPPORT:
- GOAT Support: support@goat.gg
- {partner_info['name']} Support: Available at their platform

Your creation deserves to be immortal. 🚀
        """
        
        return instructions

    def get_caleon_referral_dialogue(self, phase: str, partner: str = "alpha_certsig") -> str:
        """Get Caleon dialogue for different referral phases"""

        partner_name = self.partner_services[partner]["name"]
        discount = self.partner_services[partner]["discount_code"]

        dialogues = {
            "project_complete": f"""Your work is complete and packaged beautifully.

If you'd like to preserve this on the blockchain — timestamped, verifiable, and permanent — I can prepare everything for {partner_name}.

GOAT users get 30% off. Use code {discount}.

This is optional. Your content is already secure here. But blockchain preservation means no one can ever alter it, delete it, or claim it as their own.

Would you like me to prepare the export package?""",

            "export_ready": f"""Your package is ready for blockchain minting.

I've prepared everything {partner_name} needs:
✅ Metadata
✅ Content hash
✅ Cryptographic signatures
✅ Blockchain-ready format

Download your ZIP package, then visit {partner_name}.
Your 30% discount is already included with code {discount}.

This makes your work immortal. Literally.""",

            "why_mint": """Minting doesn't change your work. It protects it.

Here's what happens:
• Your content gets a permanent timestamp
• It's stored on IPFS (decentralized, uncensorable)
• A blockchain record proves you created it
• No one can alter the original
• You can transfer or sell ownership
• Royalties can be tracked automatically

Think of it as a birth certificate for your creation.

And with GOAT's 30% discount, the cost is minimal compared to the permanent protection.""",

            "partner_choice": f"""Both partners are excellent. Here's the difference:

ALPHA CERTSIG MINT:
• Multi-chain (Ethereum, Polygon, Base, Arbitrum)
• Fast and simple
• Great for content creators
• $0.056 ETH with your GOAT discount

TRUEMARK MINT:
• Identity-linked (ties to your .go domain)
• GDIS verification
• Royalty tracking built-in
• White-label options
• $0.105 ETH with your GOAT discount

For most creators: Alpha CertSig
For professionals building a brand: TrueMark

Either way, you save 30% as a GOAT user.""",

            "post_export": """Package downloaded. You're all set.

Visit the partner site (link in your email), upload the ZIP, and mint.

Your discount code is already applied. The process takes about 5 minutes.

After minting, you'll get:
• A certificate
• Your blockchain transaction hash
• IPFS CID for your content
• Proof of ownership

Your creation is about to become permanent. Well done."""
        }

        return dialogues.get(phase, "Your work is ready for the next step.")

def show_referral_modal(title: str, partner: str, package_data: Dict[str, Any], cta: str):
    """Show referral modal in UI (to be implemented in frontend)"""
    print(f"Showing referral modal: {title}")
    print(f"Partner: {partner}")
    print(f"Package ready: {package_data.get('blockchain_ready', False)}")

def redirect_to_partner_mint(partner: str, referral_code: str):
    """Redirect to partner mint site with referral code"""
    partner_urls = {
        "alpha_certsig": f"https://alphamint.certsig.io?ref={referral_code}",
        "truemark": f"https://mint.truemark.com?ref={referral_code}"
    }
    url = partner_urls.get(partner, partner_urls["alpha_certsig"])
    print(f"Redirecting to: {url}")
    # In frontend, this would be: window.location.href = url

# Global instance
partner_referral_manager = PartnerReferralManager()
minting_manager = PartnerReferralManager()