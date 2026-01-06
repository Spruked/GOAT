import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()

    doc.close()
    return text

if __name__ == "__main__":
    pdf_path = "audiobook_engine/finalcopyhappytoes.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)

    # Save the extracted text to a file
    with open("extracted_content.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"Text extracted from PDF and saved to extracted_content.txt")
    print(f"Total characters extracted: {len(extracted_text)}")