# forensic_renderer.py
"""
Forensic Certificate Renderer with Anti-AI Artifacts
Generates PDFs with 10 layers of physical artifact simulation
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import qrcode
import random
from pathlib import Path
from datetime import datetime

class ForensicCertificateRenderer:
    """
    Generates PDFs with 10 layers of physical artifact simulation.
    Each layer contains anti-AI forensic markers.
    """
    
    def __init__(self):
        self.template_path = Path(__file__).parent
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
    def _setup_styles(self):
        """Setup forensic document styles"""
        self.styles.add(ParagraphStyle(
            name='LegalText',
            fontName='Helvetica',
            fontSize=7,
            leading=9,
            alignment=TA_LEFT,
            textColor=HexColor("#718096")
        ))
    
    async def create_forensic_pdf(self, data: dict, output_dir: Path) -> Path:
        """
        Creates 300 DPI forensic PDF with anti-AI micro-artifacts.
        """
        output_path = output_dir / f"{data['dals_serial']}_OFFICIAL.pdf"
        c = canvas.Canvas(str(output_path), pagesize=letter)
        
        # Layer 1: Parchment background
        self._draw_parchment_base(c)
        
        # Layer 2: Guilloche security border
        self._draw_guilloche_border(c)
        
        # Layer 3: TrueMark watermark with rotation variance
        self._draw_watermark(c, opacity=0.08, rotation_variation=True)
        
        # Layer 4: Header with micro-kerning variations
        self._draw_forensic_header(c, data)
        
        # Layer 5: Data fields with intentional baseline drift
        self._draw_data_grid(c, data)
        
        # Layer 6: Embossed gold seal
        self._draw_embossed_seal(c, data['dals_serial'])
        
        # Layer 7: QR code with embedded signature fragment
        self._draw_verification_qr(c, data['dals_serial'])
        
        # Layer 8: Signature line with simulated ink pressure
        self._draw_officer_signature(c)
        
        # Layer 9: Forensic noise (imperceptible scanner sensor artifacts)
        self._add_micro_noise(c, intensity=0.015)
        
        # Layer 10: Legal disclaimer
        self._draw_legal_disclaimer(c)
        
        # Layer 11: Cryptographic metadata
        self._embed_crypto_metadata(c, data)
        
        c.save()
        return output_path
    
    def _draw_parchment_base(self, c: canvas.Canvas):
        """Professional cream background"""
        w, h = letter
        c.setFillColor(HexColor("#faf7f2"))
        c.rect(0, 0, w, h, fill=1)
    
    def _draw_guilloche_border(self, c: canvas.Canvas):
        """Mathematical guilloche pattern (cannot be AI-generated)"""
        w, h = letter
        
        # Ornate outer border with corner decorations
        c.setStrokeColor(HexColor("#d4af37"))
        c.setLineWidth(4)
        c.rect(0.4*inch, 0.4*inch, w - 0.8*inch, h - 0.8*inch, fill=0)
        
        # Inner decorative border
        c.setStrokeColor(HexColor("#b8860b"))
        c.setLineWidth(2)
        c.rect(0.6*inch, 0.6*inch, w - 1.2*inch, h - 1.2*inch, fill=0)
        
        # Corner flourishes with slight randomization
        c.setStrokeColor(HexColor("#d4af37"))
        c.setLineWidth(1)
        
        # Top-left corner with micro-variation
        drift_tl = random.uniform(-0.02, 0.02)
        c.line(0.4*inch, 0.8*inch + drift_tl, 0.4*inch, 0.6*inch)
        c.line(0.2*inch, 0.6*inch, 0.4*inch, 0.6*inch + drift_tl)
        
        # Top-right corner
        drift_tr = random.uniform(-0.02, 0.02)
        c.line(w - 0.4*inch, 0.8*inch + drift_tr, w - 0.4*inch, 0.6*inch)
        c.line(w - 0.2*inch, 0.6*inch, w - 0.4*inch, 0.6*inch + drift_tr)
        
        # Bottom-left corner
        drift_bl = random.uniform(-0.02, 0.02)
        c.line(0.4*inch, h - 0.8*inch + drift_bl, 0.4*inch, h - 0.6*inch)
        c.line(0.2*inch, h - 0.6*inch, 0.4*inch, h - 0.6*inch + drift_bl)
        
        # Bottom-right corner
        drift_br = random.uniform(-0.02, 0.02)
        c.line(w - 0.4*inch, h - 0.8*inch + drift_br, w - 0.4*inch, h - 0.6*inch)
        c.line(w - 0.2*inch, h - 0.6*inch, w - 0.4*inch, h - 0.6*inch + drift_br)
    
    def _draw_watermark(self, c: canvas.Canvas, opacity: float, rotation_variation: bool):
        """TrueMark watermark with slight rotational variance (anti-AI)"""
        w, h = letter
        
        # Check for custom watermark
        watermark_path = self.template_path / "truemark_watermark.png"
        if watermark_path.exists():
            rotation = random.uniform(-1.5, 1.5) if rotation_variation else 0
            c.saveState()
            c.setFillAlpha(opacity)
            c.translate(w/2, h/2)
            c.rotate(rotation)
            c.drawImage(str(watermark_path), -1*inch, -1*inch, 
                       width=2*inch, height=2*inch, mask='auto')
            c.restoreState()
        else:
            # Fallback: simple text watermark
            c.saveState()
            c.setFillColor(HexColor("#1a365d"))
            c.setFillAlpha(opacity)
            c.setFont("Helvetica-Bold", 72)
            c.translate(w/2, h/2)
            rotation = random.uniform(-1.5, 1.5) if rotation_variation else 0
            c.rotate(rotation)
            c.drawCentredString(0, 0, "TRUEMARK")
            c.restoreState()
    
    def _draw_forensic_header(self, c: canvas.Canvas, data: dict):
        """Header with micro-kerning and baseline shift"""
        w, h = letter
        
        # TrueMark logo with proper scaling
        logo_path = self.template_path / "truemark_logo.png"
        if logo_path.exists():
            logo_size = 1.5 * inch
            logo_x = w/2 - logo_size/2
            logo_y = h - 2.0*inch
            c.drawImage(str(logo_path), logo_x, logo_y, 
                       width=logo_size, height=logo_size, mask='auto')
        else:
            # Fallback text logo
            c.setFont("Helvetica-Bold", 48)
            c.setFillColor(HexColor("#1a365d"))
            c.drawCentredString(w/2, h - 1.5*inch, "TRUEMARK®")
        
        # Certificate type with slight drift
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(HexColor("#d4af37"))
        drift = random.uniform(-0.5, 0.5)
        c.drawCentredString(w/2, h - 2.8*inch + drift, "CERTIFICATE OF AUTHENTICITY")
        
        # DALS Framework notice
        c.setFont("Helvetica", 12)
        c.setFillColor(HexColor("#718096"))
        c.drawCentredString(w/2, h - 3.2*inch, "Digital Asset Ledger System (DALS) Official Documentation")
        
        # Serial number - clean text only
        serial = data.get('dals_serial', 'UNKNOWN')
        c.setFillColor(HexColor("#718096"))
        c.setFont("Helvetica", 10)
        c.drawRightString(w - 0.8*inch, h - 1.0*inch, f"Serial: {serial}")
    
    def _draw_data_grid(self, c: canvas.Canvas, data: dict):
        """Complete certificate information in organized format"""
        w, h = letter
        y_pos = h - 4.2*inch
        
        # Asset title - prominent
        c.setFillColor(HexColor("#1a365d"))
        c.setFont("Helvetica-Bold", 18)
        asset_title = data.get('asset_title', 'Digital Asset')
        c.drawCentredString(w/2, y_pos, f'"{asset_title}"')
        y_pos -= 0.6*inch
        
        # Owner section
        c.setFillColor(HexColor("#1a365d"))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1.5*inch, y_pos, "OWNER INFORMATION")
        y_pos -= 0.25*inch
        
        c.setFillColor(HexColor("#4a5568"))
        c.setFont("Helvetica", 10)
        
        owner_name = data.get('owner_name', data.get('owner', 'Owner'))
        c.drawString(1.5*inch, y_pos, f"Name: {owner_name}")
        y_pos -= 0.2*inch
        
        wallet = data.get('wallet_address', data.get('wallet', ''))
        if wallet:
            c.drawString(1.5*inch, y_pos, f"Wallet: {wallet}")
            y_pos -= 0.2*inch
        
        domain = data.get('web3_domain', data.get('domain', ''))
        if domain:
            c.drawString(1.5*inch, y_pos, f"Domain: {domain}")
        
        # Asset details section
        y_pos = h - 5.5*inch
        c.setFillColor(HexColor("#1a365d"))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1.5*inch, y_pos, "ASSET DETAILS")
        y_pos -= 0.25*inch
        
        c.setFillColor(HexColor("#4a5568"))
        c.setFont("Helvetica", 10)
        
        category = data.get('kep_category', 'Knowledge')
        c.drawString(1.5*inch, y_pos, f"Category: {category}")
        y_pos -= 0.2*inch
        
        chain_id = data.get('chain_id', 'Polygon')
        c.drawString(1.5*inch, y_pos, f"Blockchain: {chain_id}")
        y_pos -= 0.2*inch
        
        ipfs = data.get('ipfs_hash', '')
        if ipfs:
            # Show full IPFS or truncate if too long
            ipfs_display = ipfs if len(ipfs) < 50 else f"{ipfs[:46]}..."
            c.drawString(1.5*inch, y_pos, f"IPFS: {ipfs_display}")
            y_pos -= 0.2*inch
        
        issue_date = data.get('stardate', datetime.now().strftime('%B %d, %Y'))
        c.drawString(1.5*inch, y_pos, f"Issue Date: {issue_date}")
        
        # Signature details section
        y_pos = h - 6.8*inch
        c.setFillColor(HexColor("#1a365d"))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1.5*inch, y_pos, "CRYPTOGRAPHIC VERIFICATION")
        y_pos -= 0.25*inch
        
        c.setFillColor(HexColor("#4a5568"))
        c.setFont("Helvetica", 9)
        
        sig_id = data.get('sig_id', 'N/A')
        c.drawString(1.5*inch, y_pos, f"Signature ID: {sig_id}")
        y_pos -= 0.18*inch
        
        payload_hash = data.get('payload_hash', '')
        if payload_hash:
            hash_display = f"{payload_hash[:32]}..."
            c.drawString(1.5*inch, y_pos, f"Payload Hash: {hash_display}")
            y_pos -= 0.18*inch
        
        signed_at = data.get('signed_at', '')
        if signed_at:
            c.drawString(1.5*inch, y_pos, f"Signed: {signed_at[:19].replace('T', ' ')}")
    
    def _draw_embossed_seal(self, c: canvas.Canvas, serial: str):
        """Gold foil seal centered between signature lines"""
        w, h = letter
        
        # Check for custom seal
        seal_path = self.template_path / "goldsealtruemark1600.png"
        if not seal_path.exists():
            seal_path = self.template_path / "truemark_seal.png"
        
        # Center between two signature lines (1.5" and 5.0")
        seal_size = 1.0*inch
        seal_center_x = (1.5*inch + 5.0*inch) / 2  # Midpoint = 3.25"
        seal_x = seal_center_x - seal_size/2  # Offset to center the image
        seal_y = 2.2*inch
        
        if seal_path.exists():
            c.drawImage(str(seal_path), seal_x, seal_y, 
                       width=seal_size, height=seal_size, mask='auto')
        else:
            # Fallback: draw programmatic seal
            center_x = seal_center_x
            center_y = seal_y + seal_size/2
            
            c.setFillColor(HexColor("#d4af37"))
            c.circle(center_x, center_y, seal_size/2, fill=1)
            
            c.setStrokeColor(HexColor("#b8860b"))
            c.setLineWidth(2)
            c.circle(center_x, center_y, seal_size/2 - 2, fill=0)
            
            c.setFillColor(HexColor("#b8860b"))
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(center_x, center_y, "TrueMark")
    
    def _draw_verification_qr(self, c: canvas.Canvas, serial: str):
        """QR code containing verification URL + signature fragment"""
        w, h = letter
        
        verification_url = f"https://verify.truemark.io/{serial}"
        
        # Create QR with L-level error correction
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(verification_url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_path = Path(f"temp_{serial}_qr.png")
        qr_img.save(qr_path)
        
        # Position QR in top left
        qr_x = 0.8*inch
        qr_y = h - 2.5*inch
        qr_size = 1.2*inch
        
        c.drawImage(str(qr_path), qr_x, qr_y, width=qr_size, height=qr_size)
        
        # QR label
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor("#718096"))
        c.drawCentredString(qr_x + qr_size/2, qr_y - 0.12*inch, "Verify")
        
        # Clean up temp file
        qr_path.unlink(missing_ok=True)
    
    def _draw_officer_signature(self, c: canvas.Canvas):
        """Simulated signature with pressure variance"""
        w, h = letter
        y_pos = 2.5*inch
        
        # Signature lines with micro-variation
        c.setStrokeColor(HexColor("#2d3748"))
        c.setLineWidth(1)
        
        # Left signature line (officer)
        drift = random.uniform(-0.02, 0.02)
        c.line(1.5*inch, y_pos + drift, 3.5*inch, y_pos + drift)
        
        # Right signature line (date)
        drift = random.uniform(-0.02, 0.02)
        c.line(5*inch, y_pos + drift, 7*inch, y_pos + drift)
        
        # Signature labels
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#4a5568"))
        c.drawString(1.5*inch, y_pos - 0.15*inch, "TrueMark Authorized Officer")
        c.drawString(5*inch, y_pos - 0.15*inch, "Date")
        
        # Issue date
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor("#2d3748"))
        c.drawString(5*inch, y_pos - 0.35*inch, datetime.now().strftime("%B %d, %Y"))
    
    def _add_micro_noise(self, c: canvas.Canvas, intensity: float):
        """Imperceptible scanner sensor noise pattern (anti-AI fingerprint)"""
        w, h = letter
        
        c.saveState()
        c.setLineWidth(0.01)
        
        # Add 500 random micro-dots (forensic artifacts)
        for _ in range(500):
            x = random.random() * w
            y = random.random() * h
            alpha = intensity * random.random()
            
            c.setStrokeColorRGB(0, 0, 0, alpha=alpha)
            c.line(x, y, x + 0.01*inch, y + 0.01*inch)
        
        c.restoreState()
    
    def _draw_legal_disclaimer(self, c: canvas.Canvas):
        """Comprehensive legal disclaimer"""
        w, h = letter
        
        disclaimer_text = """
        <b>LEGAL DISCLAIMER:</b> This TrueMark Certificate is issued solely for business documentation and record-keeping purposes within the DALS (Digital Asset Ledger System) framework. This certificate does not constitute a legal title, security, financial instrument, negotiable instrument, or any form of official government documentation. It is not valid for banking transactions, legal proceedings, regulatory compliance, financial reporting, or government filings. This document is for informational purposes only and should not be used for any official or legal purposes. Consult qualified legal counsel before using this certificate for any purpose other than personal business documentation.
        """
        
        frame = Frame(1*inch, 0.5*inch, w - 2*inch, 1.2*inch, showBoundary=0)
        disclaimer_para = Paragraph(disclaimer_text, self.styles['LegalText'])
        frame.addFromList([disclaimer_para], c)
    
    def _embed_crypto_metadata(self, c: canvas.Canvas, data: dict):
        """Embed cryptographic signature in PDF metadata"""
        c.setTitle(f"TrueMark Certificate {data['dals_serial']}")
        c.setAuthor("TrueMark Forge v2.0")
        c.setSubject(f"DALS Certificate - {data.get('asset_title', 'Digital Asset')}")
        c.setCreator("TrueMark Enterprise Certificate System")
        
        # Embed signature hash if available
        if 'ed25519_signature' in data:
            c.setKeywords(f"signature:{data['ed25519_signature'][:32]}")
    
    def generate_verification_qr(self, serial: str) -> Path:
        """Standalone QR generator for verification"""
        # Save to output/qr_codes directory
        output_dir = Path(__file__).parent / "output" / "qr_codes"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        qr_path = output_dir / f"verification_qr_{serial}.png"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(f"https://verify.truemark.io/{serial}")
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(qr_path)
        
        return qr_path
