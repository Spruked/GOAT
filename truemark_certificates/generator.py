# truemark_certificates/generator.py
"""
Enhanced TrueMark Certificate Generator v2.0
Professional NFT Documentation System for DALS Framework
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import qrcode
from pathlib import Path
from datetime import datetime
import textwrap

class EnhancedTrueMarkGenerator:
    """Enhanced professional certificate generator for DALS NFT assets"""

    def __init__(self):
        self.setup_styles()
        self.page_width, self.page_height = letter  # 8.5 x 11 inches

    def setup_styles(self):
        """Setup professional styling"""
        self.styles = getSampleStyleSheet()

        # Title styles
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            fontName='Helvetica-Bold',
            fontSize=36,
            leading=42,
            alignment=TA_CENTER,
            textColor=HexColor("#1a365d"),
            spaceAfter=20
        ))

        self.styles.add(ParagraphStyle(
            name='Subtitle',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            textColor=HexColor("#2d3748"),
            spaceAfter=30
        ))

        # Field styles
        self.styles.add(ParagraphStyle(
            name='FieldLabel',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=HexColor("#2d3748"),
            spaceAfter=2
        ))

        self.styles.add(ParagraphStyle(
            name='FieldValue',
            fontName='Courier',
            fontSize=10,
            leading=12,
            textColor=HexColor("#1a202c")
        ))

        # Legal styles
        self.styles.add(ParagraphStyle(
            name='LegalText',
            fontName='Helvetica',
            fontSize=7,
            leading=9,
            alignment=TA_LEFT,
            textColor=HexColor("#718096")
        ))

    def create_certificate(self, data: dict, output_path: str):
        """
        Create enhanced professional TrueMark certificate

        Args:
            data: Certificate data dictionary
            output_path: Output PDF file path
        """
        c = canvas.Canvas(output_path, pagesize=letter)

        # Draw all certificate elements
        self.draw_background(c)
        self.draw_header(c, data)
        self.draw_certificate_body(c, data)
        self.draw_security_features(c)
        self.draw_qr_and_seal(c, data)
        self.draw_signatures(c, data)
        self.draw_legal_disclaimer(c)

        c.save()
        print(f"✅ Enhanced TrueMark Certificate Generated → {output_path}")

    def draw_background(self, c):
        """Draw professional certificate background with ornate border"""
        # Elegant cream background
        c.setFillColor(HexColor("#faf7f2"))
        c.rect(0, 0, self.page_width, self.page_height, fill=1)

        # Ornate outer border with corner decorations
        c.setStrokeColor(HexColor("#d4af37"))
        c.setLineWidth(4)
        c.rect(0.4*inch, 0.4*inch, self.page_width - 0.8*inch, self.page_height - 0.8*inch, fill=0)

        # Inner decorative border
        c.setStrokeColor(HexColor("#b8860b"))
        c.setLineWidth(2)
        c.rect(0.6*inch, 0.6*inch, self.page_width - 1.2*inch, self.page_height - 1.2*inch, fill=0)

        # Corner flourishes
        c.setStrokeColor(HexColor("#d4af37"))
        c.setLineWidth(1)
        # Top-left corner
        c.line(0.4*inch, 0.8*inch, 0.4*inch, 0.6*inch)
        c.line(0.2*inch, 0.6*inch, 0.4*inch, 0.6*inch)
        # Top-right corner
        c.line(self.page_width - 0.4*inch, 0.8*inch, self.page_width - 0.4*inch, 0.6*inch)
        c.line(self.page_width - 0.2*inch, 0.6*inch, self.page_width - 0.4*inch, 0.6*inch)
        # Bottom-left corner
        c.line(0.4*inch, self.page_height - 0.8*inch, 0.4*inch, self.page_height - 0.6*inch)
        c.line(0.2*inch, self.page_height - 0.6*inch, 0.4*inch, self.page_height - 0.6*inch)
        # Bottom-right corner
        c.line(self.page_width - 0.4*inch, self.page_height - 0.8*inch, self.page_width - 0.4*inch, self.page_height - 0.6*inch)
        c.line(self.page_width - 0.2*inch, self.page_height - 0.6*inch, self.page_width - 0.4*inch, self.page_height - 0.6*inch)

    def draw_header(self, c, data):
        """Draw certificate header with branding"""
        # TrueMark logo area - use custom image with proper aspect ratio
        try:
            # Use the specific truemark_logo.png file
            logo_path = Path(__file__).parent / "truemark_logo.png"
            if not logo_path.exists():
                # Fallback to 512px transparent version
                logo_path = Path(__file__).parent / "TMlogotrans512.png"
            if not logo_path.exists():
                # Fallback to 256px version
                logo_path = Path(__file__).parent / "TMlogotrans256.png"

            if logo_path.exists():
                # Logo with proper dimensions - horizontal layout
                logo_width = 3.0 * inch
                logo_height = 1.0 * inch
                logo_x = self.page_width/2 - logo_width/2
                logo_y = self.page_height - 1.6*inch
                c.drawImage(str(logo_path), logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True, anchor='c')
            else:
                # Fallback to text if image not found
                c.setFillColor(HexColor("#1a365d"))
                c.setFont("Helvetica-Bold", 48)
                c.drawCentredString(self.page_width/2, self.page_height - 1.5*inch, "TRUEMARK®")
        except Exception as e:
            # Fallback to text if image loading fails
            c.setFillColor(HexColor("#1a365d"))
            c.setFont("Helvetica-Bold", 48)
            c.drawCentredString(self.page_width/2, self.page_height - 1.5*inch, "TRUEMARK®")

        # Certificate type
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(HexColor("#d4af37"))
        c.drawCentredString(self.page_width/2, self.page_height - 2.5*inch, "CERTIFICATE OF AUTHENTICITY")

        # DALS Framework notice
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor("#718096"))
        c.drawCentredString(self.page_width/2, self.page_height - 2.8*inch, "Digital Asset Ledger System (DALS) Official Documentation")

        # Serial number - clean, smaller text in top right corner
        serial = data.get('dals_serial', 'UNKNOWN')
        c.setFillColor(HexColor("#4a5568"))
        c.setFont("Helvetica", 9)
        c.drawRightString(self.page_width - 0.8*inch, self.page_height - 0.7*inch, f"Serial: {serial}")

    def draw_certificate_body(self, c, data):
        """Draw the main certificate content"""
        # Add essential information in clean, professional format
        y_pos = self.page_height - 4.2*inch

        # This certifies that text
        c.setFillColor(HexColor("#2d3748"))
        c.setFont("Helvetica", 14)
        c.drawCentredString(self.page_width/2, y_pos, "This certifies that")
        y_pos -= 0.4*inch

        # Owner name - prominent
        owner_name = data.get('owner_name', 'Owner')
        c.setFillColor(HexColor("#1a365d"))
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(self.page_width/2, y_pos, owner_name)
        y_pos -= 0.5*inch

        # "is the verified owner of" text
        c.setFillColor(HexColor("#2d3748"))
        c.setFont("Helvetica", 14)
        c.drawCentredString(self.page_width/2, y_pos, "is the verified owner of the digital asset")
        y_pos -= 0.4*inch

        # Asset title - prominent
        asset_title = data.get('asset_title', 'Digital Asset')
        c.setFillColor(HexColor("#1a365d"))
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(self.page_width/2, y_pos, f'"{asset_title}"')
        y_pos -= 0.6*inch

        # Additional details in smaller text
        c.setFillColor(HexColor("#4a5568"))
        c.setFont("Helvetica", 10)

        domain = data.get('web3_domain', '')
        if domain:
            c.drawCentredString(self.page_width/2, y_pos, f"Web3 Domain: {domain}")
            y_pos -= 0.25*inch

        wallet = data.get('wallet', '')
        if wallet:
            # Show abbreviated wallet
            short_wallet = f"{wallet[:6]}...{wallet[-4:]}"
            c.drawCentredString(self.page_width/2, y_pos, f"Wallet Address: {short_wallet}")
            y_pos -= 0.4*inch

        # Issue date
        c.setFont("Helvetica-Oblique", 11)
        c.drawCentredString(self.page_width/2, y_pos, f"Issued on {datetime.now().strftime('%B %d, %Y')}")

    def draw_asset_section(self, c, data):
        """Draw asset information section"""
        y_pos = self.page_height - 3.5*inch

        # Section header
        c.setFillColor(HexColor("#1a365d"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1.5*inch, y_pos, "ASSET INFORMATION")
        y_pos -= 0.3*inch

        # Asset details
        asset_fields = [
            ("Asset Title", data.get('asset_title', '')),
            ("NFT Classification", data.get('kep_category', '')),
            ("Description", data.get('description', 'Digital asset documentation')),
        ]

        for label, value in asset_fields:
            self.draw_field(c, 1.5*inch, y_pos, label, value, width=3*inch)
            y_pos -= 0.4*inch

    def draw_owner_section(self, c, data):
        """Draw owner information section"""
        y_pos = self.page_height - 5.0*inch

        # Section header
        c.setFillColor(HexColor("#1a365d"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1.5*inch, y_pos, "OWNER INFORMATION")
        y_pos -= 0.3*inch

        # Owner details
        owner_fields = [
            ("Owner Name", data.get('owner_name', '')),
            ("Web3 Wallet Address", data.get('wallet', '')),
            ("TrueMark Domain", data.get('web3_domain', '')),
        ]

        for label, value in owner_fields:
            self.draw_field(c, 1.5*inch, y_pos, label, value, width=4*inch)
            y_pos -= 0.4*inch

    def draw_technical_section(self, c, data):
        """Draw technical details section"""
        y_pos = self.page_height - 6.5*inch

        # Section header
        c.setFillColor(HexColor("#1a365d"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1.5*inch, y_pos, "TECHNICAL SPECIFICATIONS")
        y_pos -= 0.3*inch

        # Technical details in two columns
        left_fields = [
            ("Chain ID", data.get('chain_id', '1')),
            ("IPFS Hash", data.get('ipfs_hash', '')),
        ]

        right_fields = [
            ("Issue Date", data.get('stardate', datetime.now().strftime("%Y%m%d.%H%M"))),
            ("Verification ID", data.get('sig_id', 'AUTO-GENERATED')),
        ]

        # Left column
        y_left = y_pos
        for label, value in left_fields:
            self.draw_field(c, 1.5*inch, y_left, label, value, width=2.5*inch)
            y_left -= 0.4*inch

        # Right column
        y_right = y_pos
        for label, value in right_fields:
            self.draw_field(c, 5*inch, y_right, label, value, width=2.5*inch)
            y_right -= 0.4*inch

    def draw_field(self, c, x, y, label, value, width=3*inch):
        """Draw a labeled field with value"""
        # Label
        c.setFillColor(HexColor("#4a5568"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x, y + 0.05*inch, label)

        # Value background
        c.setFillColor(HexColor("#f7fafc"))
        c.setStrokeColor(HexColor("#e2e8f0"))
        c.setLineWidth(0.5)
        c.rect(x, y - 0.15*inch, width, 0.25*inch, fill=1, stroke=1)

        # Value text
        c.setFillColor(HexColor("#1a202c"))
        c.setFont("Courier", 8)
        # Truncate if too long
        display_value = value[:35] + "..." if len(value) > 35 else value
        c.drawString(x + 0.05*inch, y - 0.12*inch, display_value)

    def draw_security_features(self, c):
        """Draw security features and watermarks"""
        # Guilloche pattern border
        self.draw_guilloche_border(c)

        # Watermark
        self.draw_watermark(c)

    def draw_guilloche_border(self, c):
        """Draw complex security border pattern"""
        c.setStrokeColor(HexColor("#d4af37"))
        c.setLineWidth(0.5)
        c.setStrokeAlpha(0.3)

        # Create interlocking circular patterns
        for i in range(20, int(self.page_width) - 20, 15):
            for j in range(20, int(self.page_height) - 20, 15):
                if (i + j) % 30 == 0:
                    c.circle(i, j, 8, fill=0)

        c.setStrokeAlpha(1.0)

    def draw_watermark(self, c):
        """Draw TrueMark watermark"""
        c.setFillColor(HexColor("#1a365d"))
        c.setFillAlpha(0.08)

        # TrueMark tree symbol
        center_x = self.page_width / 2
        center_y = self.page_height / 2

        # Tree trunk
        c.rect(center_x - 3, center_y - 30, 6, 40, fill=1)

        # Tree crown (stylized)
        for i in range(5):
            y_offset = i * 8
            width = 40 - i * 6
            c.rect(center_x - width/2, center_y + y_offset, width, 8, fill=1)

        c.setFillAlpha(1.0)

    def draw_qr_and_seal(self, c, data):
        """Draw QR code and official seal"""
        # QR Code - top left corner, clean placement
        verification_url = data.get("verification_url", f"https://truemark.verify/{data.get('dals_serial', 'unknown')}")
        qr = qrcode.make(verification_url)

        qr_x = 0.9*inch  # Top left corner
        qr_y = self.page_height - 1.9*inch  # Below header area
        qr_size = 1.0*inch  # Reasonable size
        c.drawInlineImage(qr, qr_x, qr_y, width=qr_size, height=qr_size)

        # QR label
        c.setFont("Helvetica", 7)
        c.setFillColor(HexColor("#718096"))
        c.drawCentredString(qr_x + qr_size/2, qr_y - 0.15*inch, "Blockchain Verify")

        # Official seal - centered between signature lines at proper position
        seal_x = self.page_width/2 - 0.65*inch  # Centered horizontally
        seal_y = 2.8*inch   # Above signatures with space
        self.draw_official_seal(c, seal_x, seal_y, 1.3*inch)  # Properly sized seal

    def draw_official_seal(self, c, x, y, size):
        """Draw official TrueMark seal using custom image"""
        try:
            # Try transparent seal first
            seal_path = Path(__file__).parent / "truemark_seal_transparent.png"
            if not seal_path.exists():
                # Try gold seal
                seal_path = Path(__file__).parent / "goldsealtruemark1600.png"
            if not seal_path.exists():
                # Try using transparent logo as seal
                seal_path = Path(__file__).parent / "TMlogotrans.png"

            if seal_path.exists():
                # Custom seal - resize to fit the specified size
                seal_size = size  # Use the passed size parameter
                c.drawImage(str(seal_path), x, y, width=seal_size, height=seal_size)
            else:
                # Fallback to programmatic seal if image not found
                center_x = x + size/2
                center_y = y + size/2

                # Gold seal background
                c.setFillColor(HexColor("#d4af37"))
                c.circle(center_x, center_y, size/2, fill=1)

                # Inner border
                c.setStrokeColor(HexColor("#b8860b"))
                c.setLineWidth(2)
                c.circle(center_x, center_y, size/2 - 2, fill=0)

                # Star pattern
                c.setFillColor(HexColor("#ffd700"))
                star_size = size * 0.25
                self.draw_star(c, center_x, center_y, star_size)

                # Seal text
                c.setFillColor(HexColor("#b8860b"))
                c.setFont("Helvetica-Bold", 8)
                c.drawCentredString(center_x, center_y - 2, "TrueMark")
                c.setFont("Helvetica", 6)
                c.drawCentredString(center_x, center_y - 8, "Official")
        except Exception as e:
            # Fallback to programmatic seal if image loading fails
            center_x = x + size/2
            center_y = y + size/2

            # Gold seal background
            c.setFillColor(HexColor("#d4af37"))
            c.circle(center_x, center_y, size/2, fill=1)

            # Inner border
            c.setStrokeColor(HexColor("#b8860b"))
            c.setLineWidth(2)
            c.circle(center_x, center_y, size/2 - 2, fill=0)

            # Star pattern
            c.setFillColor(HexColor("#ffd700"))
            star_size = size * 0.25
            self.draw_star(c, center_x, center_y, star_size)

            # Seal text
            c.setFillColor(HexColor("#b8860b"))
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(center_x, center_y - 2, "TrueMark")
            c.setFont("Helvetica", 6)
            c.drawCentredString(center_x, center_y - 8, "Official")

    def draw_star(self, c, center_x, center_y, size):
        """Draw a star shape using lines"""
        c.setLineWidth(1)
        points = []
        for i in range(10):
            angle = (i * 36) * 3.14159 / 180
            radius = size if i % 2 == 0 else size * 0.6
            x = center_x + radius * (1 if i % 2 == 0 else 0.8) * (-1 if i < 5 else 1)
            y = center_y + radius * (0.8 if i % 2 == 0 else 1) * (-1 if i < 5 else 1)
            points.append((x, y))

        # Draw star lines
        for i in range(len(points)):
            start_point = points[i]
            end_point = points[(i + 1) % len(points)]
            c.line(start_point[0], start_point[1], end_point[0], end_point[1])

        # Fill the center (approximation)
        c.setFillColor(HexColor("#ffd700"))
        c.circle(center_x, center_y, size * 0.3, fill=1)

    def draw_signatures(self, c, data):
        """Draw signature section"""
        y_pos = 1.9*inch

        # Signature lines - properly spaced
        c.setStrokeColor(HexColor("#2d3748"))
        c.setLineWidth(1)
        c.line(1.3*inch, y_pos, 3.3*inch, y_pos)
        c.line(5.2*inch, y_pos, 7.2*inch, y_pos)

        # Signature labels
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#4a5568"))
        c.drawString(1.3*inch, y_pos - 0.2*inch, "Authorized Officer")
        c.drawString(5.2*inch, y_pos - 0.2*inch, "Date")

        # Issue date
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#2d3748"))
        c.drawString(5.2*inch, y_pos - 0.4*inch, datetime.now().strftime("%B %d, %Y"))

    def draw_legal_disclaimer(self, c):
        """Draw comprehensive legal disclaimer"""
        disclaimer_text = """
        <b>LEGAL DISCLAIMER:</b> This TrueMark Certificate is issued solely for business documentation and record-keeping purposes within the DALS (Digital Asset Ledger System) framework. This certificate does not constitute a legal title, security, financial instrument, negotiable instrument, or any form of official government documentation. It is not valid for banking transactions, legal proceedings, regulatory compliance, financial reporting, or government filings. This document is for informational purposes only and should not be used for any official or legal purposes. Consult qualified legal counsel before using this certificate for any purpose other than personal business documentation.
        """

        frame = Frame(1*inch, 0.5*inch, self.page_width - 2*inch, 1.2*inch, showBoundary=0)
        disclaimer_para = Paragraph(disclaimer_text, self.styles['LegalText'])
        frame.addFromList([disclaimer_para], c)


def create_enhanced_truemark_certificate(data: dict, output_path: str):
    """
    Convenience function to create an enhanced TrueMark certificate

    Args:
        data: Certificate data dictionary
        output_path: Output PDF path
    """
    generator = EnhancedTrueMarkGenerator()
    generator.create_certificate(data, output_path)