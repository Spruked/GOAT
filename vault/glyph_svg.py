"""
Glyph SVG Generator - Creates unique visual identifiers for each glyph
"""

import hashlib
from typing import Tuple


def generate_svg(glyph_id: str, size: int = 100) -> str:
    """
    Generate a unique SVG visual identifier based on glyph hash
    
    Args:
        glyph_id: The glyph ID (0x... format)
        size: SVG viewBox size (default 100)
    
    Returns:
        SVG string
    """
    # Extract color from hash
    hash_color = int(glyph_id[-6:], 16) if glyph_id.startswith("0x") else 0x4ECDC4
    
    # Generate secondary color
    hash_int = int(glyph_id[-12:-6], 16) if len(glyph_id) > 12 else 0xFFE66D
    
    # Create gradient colors
    color1 = f"#{hash_color:06x}"
    color2 = f"#{hash_int:06x}"
    
    # Generate pattern based on hash
    pattern_seed = int(glyph_id[-8:], 16) if len(glyph_id) > 8 else 0
    
    svg = f'''<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad_{glyph_id[-8:]}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1};stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:{color2};stop-opacity:0.9" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background circle -->
  <circle cx="{size/2}" cy="{size/2}" r="{size*0.4}" 
          fill="url(#grad_{glyph_id[-8:]})" 
          filter="url(#glow)" />
  
  <!-- Pattern overlay -->
  <circle cx="{size/2}" cy="{size/2}" r="{size*0.25}" 
          fill="none" 
          stroke="white" 
          stroke-width="2" 
          opacity="0.5" />
  
  <!-- GOAT "G" symbol -->
  <text x="{size/2}" y="{size/2 + 8}" 
        text-anchor="middle" 
        fill="white" 
        font-size="{size*0.4}" 
        font-weight="bold"
        font-family="Arial, sans-serif"
        filter="url(#glow)">G</text>
  
  <!-- Verification checkmark -->
  <path d="M {size*0.7} {size*0.25} L {size*0.75} {size*0.3} L {size*0.85} {size*0.2}" 
        stroke="white" 
        stroke-width="3" 
        fill="none" 
        stroke-linecap="round" 
        opacity="0.8" />
</svg>'''
    
    return svg


def generate_badge_svg(glyph_id: str, label: str = "Verified", size: int = 200) -> str:
    """
    Generate a verification badge with glyph identifier
    
    Args:
        glyph_id: The glyph ID
        label: Badge text
        size: Badge size
    
    Returns:
        SVG badge string
    """
    hash_color = int(glyph_id[-6:], 16) if glyph_id.startswith("0x") else 0x4ECDC4
    color = f"#{hash_color:06x}"
    
    # Truncated glyph ID for display
    short_id = glyph_id[:10] + "..." if len(glyph_id) > 10 else glyph_id
    
    svg = f'''<svg viewBox="0 0 {size} {size/2}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="badge-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#4ECDC4;stop-opacity:1" />
      <stop offset="100%" style="stop-color:{color};stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Badge background -->
  <rect x="0" y="0" width="{size}" height="{size/2}" 
        rx="15" 
        fill="url(#badge-grad)" />
  
  <!-- Glyph circle -->
  <circle cx="{size/6}" cy="{size/4}" r="{size/8}" 
          fill="white" 
          opacity="0.3" />
  
  <text x="{size/6}" y="{size/4 + 8}" 
        text-anchor="middle" 
        fill="white" 
        font-size="{size/10}" 
        font-weight="bold">G</text>
  
  <!-- Label text -->
  <text x="{size/2 + 20}" y="{size/4 - 5}" 
        text-anchor="middle" 
        fill="white" 
        font-size="{size/12}" 
        font-weight="bold">{label}</text>
  
  <!-- Glyph ID -->
  <text x="{size/2 + 20}" y="{size/4 + 15}" 
        text-anchor="middle" 
        fill="white" 
        font-size="{size/20}" 
        opacity="0.8">{short_id}</text>
</svg>'''
    
    return svg


def generate_qr_glyph(glyph_id: str, vault_url: str = "https://goat.vault") -> str:
    """
    Generate a QR code-style glyph for mobile verification
    (Simplified version - use qrcode library for real QR codes)
    
    Args:
        glyph_id: The glyph ID
        vault_url: Base URL for verification
    
    Returns:
        SVG with verification URL pattern
    """
    verification_url = f"{vault_url}/verify/{glyph_id}"
    
    # Generate pattern from hash
    pattern_data = []
    for i in range(0, min(len(glyph_id), 16), 2):
        try:
            val = int(glyph_id[i:i+2], 16)
            pattern_data.append(val > 128)
        except ValueError:
            pattern_data.append(False)
    
    size = 200
    grid_size = 4
    cell_size = size / grid_size
    
    svg = f'''<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{size}" height="{size}" fill="white"/>
  '''
    
    # Create pattern grid
    for i, active in enumerate(pattern_data[:16]):
        row = i // grid_size
        col = i % grid_size
        if active:
            svg += f'''<rect x="{col * cell_size}" y="{row * cell_size}" 
                       width="{cell_size}" height="{cell_size}" 
                       fill="#4ECDC4" />
  '''
    
    # Center GOAT logo
    center = size / 2
    svg += f'''
  <circle cx="{center}" cy="{center}" r="{size/6}" fill="white" stroke="#4ECDC4" stroke-width="4"/>
  <text x="{center}" y="{center + 10}" 
        text-anchor="middle" 
        fill="#4ECDC4" 
        font-size="{size/8}" 
        font-weight="bold">G</text>
</svg>'''
    
    return svg


def get_glyph_color(glyph_id: str) -> Tuple[str, str]:
    """
    Extract primary and secondary colors from glyph ID
    
    Returns:
        Tuple of (primary_hex, secondary_hex)
    """
    if glyph_id.startswith("0x"):
        primary = int(glyph_id[-6:], 16)
        secondary = int(glyph_id[-12:-6], 16) if len(glyph_id) > 12 else 0xFFE66D
    else:
        primary = 0x4ECDC4
        secondary = 0xFFE66D
    
    return f"#{primary:06x}", f"#{secondary:06x}"


# Example usage
if __name__ == "__main__":
    example_glyph = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    
    print("=== Standard Glyph SVG ===")
    print(generate_svg(example_glyph))
    
    print("\n=== Verification Badge ===")
    print(generate_badge_svg(example_glyph, "Verified Knowledge"))
    
    print("\n=== Colors ===")
    primary, secondary = get_glyph_color(example_glyph)
    print(f"Primary: {primary}, Secondary: {secondary}")
