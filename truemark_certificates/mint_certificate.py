#!/usr/bin/env python3
"""
Enhanced TrueMark Certificate Generator CLI v2.0
Professional NFT Documentation System for DALS Framework

Usage:
    python mint_certificate.py [OPTIONS]

Example:
    python mint_certificate.py \
      --serial DALSM0001 \
      --owner "Bryan A. Spruk" \
      --title "Caleon Prime" \
      --wallet "0xA377665..." \
      --domain "bryan.truemark" \
      --category "Knowledge" \
      --ipfs "ipfs://QmXyZ..." \
      --description "Advanced AI knowledge system" \
      --output "DALSM0001_certificate.pdf"
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import uuid

# Add the package to path
sys.path.insert(0, str(Path(__file__).parent))

from generator import create_enhanced_truemark_certificate


def generate_stardate():
    """Generate a stardate-style timestamp"""
    now = datetime.now()
    stardate = f"{now.year}{now.month:02d}{now.day:02d}.{now.hour:02d}{now.minute:02d}"
    return stardate


def generate_sig_id():
    """Generate a unique signature verification ID"""
    return str(uuid.uuid4())[:12].upper()


def main():
    parser = argparse.ArgumentParser(
        description="Enhanced TrueMark Certificate Generator v2.0 - Professional NFT Documentation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mint_certificate.py \\
    --serial DALSM0001 \\
    --owner "Bryan A. Spruk" \\
    --title "Caleon Prime" \\
    --wallet "0xA377665..." \\
    --domain "bryan.truemark" \\
    --category "Knowledge" \\
    --ipfs "ipfs://QmXyZ..." \\
    --description "Advanced AI knowledge system" \\
    --output "DALSM0001_certificate.pdf"

Legal Disclaimer:
This certificate is for business documentation purposes only.
It is NOT a legal financial instrument, security, or government document.
"""
    )

    # Required arguments
    parser.add_argument('--serial', required=True,
                       help='DALS Serial Number (e.g., DALSM0001)')
    parser.add_argument('--owner', required=True,
                       help='Owner Full Name')
    parser.add_argument('--title', required=True,
                       help='Asset Title')
    parser.add_argument('--wallet', required=True,
                       help='Web3 Wallet Address')

    # Optional arguments
    parser.add_argument('--domain', default='',
                       help='TrueMark Web3 Domain')
    parser.add_argument('--category', default='General',
                       help='NFT Classification (KEP Category)')
    parser.add_argument('--ipfs', default='',
                       help='IPFS Hash')
    parser.add_argument('--description', default='',
                       help='Asset Description')
    parser.add_argument('--chain-id', default='1',
                       help='Chain ID (default: 1 for Ethereum)')
    parser.add_argument('--output', '-o',
                       help='Output PDF file path')
    parser.add_argument('--format', choices=['letter', 'a4'], default='letter',
                       help='Paper format (default: letter)')

    args = parser.parse_args()

    # Generate output filename if not specified
    if not args.output:
        args.output = f"{args.serial}_truemark_certificate.pdf"

    # Prepare certificate data
    certificate_data = {
        'dals_serial': args.serial,
        'owner_name': args.owner,
        'asset_title': args.title,
        'wallet': args.wallet,
        'web3_domain': args.domain,
        'kep_category': args.category,
        'ipfs_hash': args.ipfs,
        'description': args.description or f"NFT asset documentation - {args.title}",
        'chain_id': args.chain_id,
        'stardate': generate_stardate(),
        'sig_id': generate_sig_id(),
        'verification_url': f"https://truemark.verify/{args.serial}",
        'issue_date': datetime.now().strftime("%B %d, %Y")
    }

    print("🔐 Enhanced TrueMark Certificate Generator v2.0")
    print("=" * 60)
    print(f"Serial: {args.serial}")
    print(f"Owner: {args.owner}")
    print(f"Asset: {args.title}")
    print(f"Format: {args.format.upper()}")
    print(f"Output: {args.output}")
    print()

    try:
        # Create the certificate
        create_enhanced_truemark_certificate(
            data=certificate_data,
            output_path=args.output
        )

        print("\n✅ Enhanced certificate minted successfully!")
        print(f"📄 File: {args.output}")
        print(f"🔗 Verification: {certificate_data['verification_url']}")
        print(f"📏 Format: {args.format.upper()} ({'8.5×11 inches' if args.format == 'letter' else 'A4'})")
        print("\n⚠️  LEGAL NOTICE: This certificate is for business documentation only.")
        print("   It is NOT a legal financial instrument or government document.")

    except Exception as e:
        print(f"❌ Error generating certificate: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()