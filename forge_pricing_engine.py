# forge_pricing_engine.py
# Updated December 18, 2025 - 30% increase for exclusive discount offers
# Allows for partner promotions without compromising bottom line

PRICE_MAP = {
    # Masterclass Builder (was $29-$189, now $38-$246)
    "Masterclass Builder Mini": 38,
    "Masterclass Builder Standard": 64,
    "Masterclass Builder Deep Dive": 116,
    "Masterclass Builder Elite": 246,
    
    # Audiobook Suite (was $29-$249, now $38-$324)
    "Audiobook Suite Mini": 38,
    "Audiobook Suite Standard": 90,
    "Audiobook Suite Premium": 168,
    "Audiobook Suite Legacy": 324,
    
    # Coaching Program (was $39-$349, now $51-$454)
    "Coaching Program System Mini": 51,
    "Coaching Program System Signature": 116,
    "Coaching Program System High-Ticket": 233,
    "Coaching Program System Empire": 454,
    
    # Vault & Storage (was $29-$299, now $38-$389)
    "GOAT Vault & Perma-Storage Basic (IPFS)": 38,
    "GOAT Vault & Perma-Storage Pro (IPFS+Arweave)": 90,
    "GOAT Vault & Perma-Storage Immortal (All Chains)": 168,
    "GOAT Vault & Perma-Storage Dynasty (TrueMark+GDIS)": 389,
    
    # Add-ons (30% increase)
    "Booklet / PDF Builder": 33,
    "Promo & Social Media Kits": 26,
    "Podcast Edition Pack": 64,
    "AI Artwork Pack": 46,
    "Merch Template Pack": 52,
    "Print-on-Demand Setup Kit": 85,
    "Domain Prep (TrueMark)": 20,
    "Complete Asset ZIP": 16,
    
    # New products
    "Course Builder Standard": 64,
    "Course Builder Premium": 116,
    "Course Builder Enterprise": 194,
    "Manual Generator Basic": 32,
    "Manual Generator Professional": 64,
    "Manual Generator Enterprise": 90,
    "Book Builder Standard": 52,
    "Book Builder Premium": 90,
    "Book Builder Elite": 116,
    "TrueMark Certificate": 65,
    "Verifiable Badge Prep": 26,
    "Graph Visualization": 52,
    "Video Memory Basic": 90,
    "Video Memory Pro": 142,
    "Video Memory Premium": 194,
    "Guest Interview Standalone": 32,
    "Legacy Assembly Custom": 299  # Starting price, custom quotes
}

# Bundle pricing (30% increase)
BUNDLES = {
    "basic": {
        "price": 103,  # was $79
        "includes": ["Book Builder Standard", "Manual Generator Basic", "GOAT Vault & Perma-Storage Basic (IPFS)"],
        "savings": "30%"
    },
    "creator": {
        "price": 194,  # was $149
        "includes": ["Book Builder Premium", "Course Builder Standard", "Podcast Edition Pack", "GOAT Vault & Perma-Storage Pro (IPFS+Arweave)"],
        "savings": "40%"
    },
    "pro": {
        "price": 324,  # was $249
        "includes": ["All content products", "GOAT Vault & Perma-Storage Immortal (All Chains)"],
        "savings": "50%"
    },
    "legacy": {
        "price": 519,  # was $399
        "includes": ["Everything", "UCM Enterprise", "GOAT Vault & Perma-Storage Dynasty (TrueMark+GDIS)"],
        "savings": "60%"
    }
}

# Partner mint pricing (GOAT does NOT mint - only refers)
PARTNER_MINTS = {
    "alpha_certsig": {
        "standard_price_eth": 0.08,
        "goat_exclusive_eth": 0.056,  # 30% discount
        "discount_code": "GOAT30",
        "features": [
            "ERC-721/ERC-1155 minting",
            "Multi-chain support (Ethereum, Polygon, Base, Arbitrum)",
            "IPFS pinning",
            "ChaCha24/128/256 encryption upgrades",
            "Permanent authorship proof"
        ]
    },
    "truemark_mint": {
        "standard_price_eth": 0.15,
        "goat_exclusive_eth": 0.105,  # 30% discount
        "discount_code": "GOAT30",
        "features": [
            "Identity-linked minting",
            ".go domain integration",
            "GDIS identity verification",
            "Royalty tracking",
            "Multi-chain support",
            "White-label options",
            "ChaCha24/128/256 encryption upgrades"
        ]
    }
}

def calculate_total(items, bundle=None):
    """Calculate total with bundle discounts"""
    if bundle and bundle in BUNDLES:
        return BUNDLES[bundle]["price"]
    
    base = sum(PRICE_MAP.get(item, 0) for item in items)
    return base

def get_partner_discount_info(partner="alpha_certsig"):
    """Get partner mint discount information"""
    if partner in PARTNER_MINTS:
        info = PARTNER_MINTS[partner]
        savings = (info["standard_price_eth"] - info["goat_exclusive_eth"]) * 100 / info["standard_price_eth"]
        return {
            "partner": partner,
            "standard_price": info["standard_price_eth"],
            "goat_price": info["goat_exclusive_eth"],
            "discount_code": info["discount_code"],
            "savings_percent": round(savings),
            "features": info["features"]
        }
    return None

def generate_referral_message(product_type, vault_tier):
    """Generate referral message for partner mints"""
    messages = {
        "basic": f"""
🎉 Your {product_type} is ready for blockchain preservation!

GOAT has prepared your content package with:
✅ Cryptographic signatures
✅ Content verification hashes
✅ Blockchain-ready metadata

Ready to make it permanent?

🔗 Alpha CertSig Mint: 30% OFF for GOAT users
   Use code: GOAT30
   Only $0.056 ETH (was $0.08 ETH) + gas

🔗 TrueMark Mint: 30% OFF for GOAT users
   Use code: GOAT30
   Only $0.105 ETH (was $0.15 ETH) + gas

WHY MINT?
• Permanent proof of authorship
• Timestamped creation record
• Decentralized storage (IPFS/Arweave)
• Transferable ownership
• Royalty tracking
• Protects your IP forever

BONUS: Upgrade to ChaCha24/128/256 encryption at checkout!
        """,
        "immortal": f"""
🏆 Your {product_type} Dynasty Package is ready!

GOAT has prepared your premium package with:
✅ Multi-chain metadata (Ethereum, Polygon, Arbitrum)
✅ 10+ year Filecoin deal preparation
✅ 3-node backup configuration
✅ ChaCha128 encryption ready

Make it immortal with our partners:

🔗 TrueMark Mint (RECOMMENDED for Dynasty):
   30% OFF - Use code: GOAT30
   Only $0.105 ETH (was $0.15 ETH) + gas
   
   Includes:
   • .go domain integration
   • GDIS identity linking
   • White-label vault options
   • ChaCha256 encryption upgrade

🔗 Alpha CertSig Mint:
   30% OFF - Use code: GOAT30
   Only $0.056 ETH (was $0.08 ETH) + gas

Your creation deserves to outlive you. 🚀
        """
    }
    
    return messages.get(vault_tier, messages["basic"])