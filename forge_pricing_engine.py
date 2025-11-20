# forge_pricing_engine.py
PRICE_MAP = {
    "Masterclass Builder Mini": 29,
    "Masterclass Builder Standard": 49,
    "Masterclass Builder Deep Dive": 89,
    "Masterclass Builder Elite": 189,
    "Audiobook Suite Mini": 29,
    "Audiobook Suite Standard": 69,
    "Audiobook Suite Premium": 129,
    "Audiobook Suite Legacy": 249,
    "Coaching Program System Mini": 39,
    "Coaching Program System Signature": 89,
    "Coaching Program System High-Ticket": 179,
    "Coaching Program System Empire": 349,
    "GOAT Vault & Perma-Storage Basic (IPFS)": 29,
    "GOAT Vault & Perma-Storage Pro (IPFS+Arweave)": 69,
    "GOAT Vault & Perma-Storage Immortal (All Chains)": 129,
    "GOAT Vault & Perma-Storage Dynasty (TrueMark+GDIS)": 299,
    "Booklet / PDF Builder": 25,
    "Promo & Social Media Kits": 20,
    "Podcast Edition Pack": 49,
    "AI Artwork Pack": 35,
    "Merch Template Pack": 40,
    "Print-on-Demand Setup Kit": 65,
    "Domain Prep (TrueMark)": 15,
    "Complete Asset ZIP": 12
}

def calculate_total(items, bundle=None):
    base = sum(PRICE_MAP.get(item, 0) for item in items)
    if bundle == "legacy":
        return 399
    elif bundle == "pro":
        return 249
    elif bundle == "creator":
        return 149
    elif bundle == "basic":
        return 79
    # Automatic max-tier upgrades for bundles
    return base