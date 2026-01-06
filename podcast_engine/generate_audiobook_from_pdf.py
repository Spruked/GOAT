import sys
from pathlib import Path
from skg.skg_manager import SpeakerKnowledgeGraph
from skg.audiobook_generator import AudiobookGenerator
import PyPDF2

# --- CONFIG ---
PDF_PATH = Path(__file__).parent.parent / "audiobook_engine" / "finalcopyhappytoes.pdf"
CONFIG = {
    "title": "Happy Toes",
    "author": "Unknown",
    "narrator_id": "fiction_narrator",  # Change to your narrator persona
    "genre": "fiction",
    "character_voice_map": {
        # Add character mappings as needed
    }
}

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    # 1. Extract text from PDF
    manuscript = extract_text_from_pdf(PDF_PATH)

    # 2. Initialize SKG
    skg = SpeakerKnowledgeGraph()

    # 3. Generate audiobook
    generator = AudiobookGenerator(skg)
    output_path = generator.generate_audiobook(manuscript, CONFIG)
    print(f"\n✅ Audiobook generated: {output_path}")
