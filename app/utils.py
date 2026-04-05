# app/utils.py

import pdfplumber
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract all text from a PDF given its raw bytes.
    pdfplumber is more reliable than PyPDF2 for formatted/multi-column PDFs.
    
    We use io.BytesIO to treat the bytes as a file-like object,
    so we don't need to save the uploaded file to disk first.
    """
    text = ""
    
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Some pages might be images with no extractable text
                text += page_text + "\n"
    
    return text.strip()


def clean_text(text: str) -> str:
    """
    Remove excessive whitespace and normalize the text.
    Raw PDF extraction often has double spaces, weird newlines, etc.
    """
    import re
    # Replace multiple whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()