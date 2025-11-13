"""
GOAT Vault Module - Immutable Data Lineage for NFT Knowledge
"""

from .core import Vault, Glyph, VaultEncryption, VaultLedger
from .glyph_svg import generate_svg, generate_badge_svg, get_glyph_color
from .ipfs_gateway import IPFSGateway, IPFSGatewaySync
from .onchain_anchor import OnChainAnchor

__all__ = [
    "Vault",
    "Glyph",
    "VaultEncryption",
    "VaultLedger",
    "generate_svg",
    "generate_badge_svg",
    "get_glyph_color",
    "IPFSGateway",
    "IPFSGatewaySync",
    "OnChainAnchor"
]

__version__ = "2.1.0"
