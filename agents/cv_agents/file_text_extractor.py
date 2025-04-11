import pdfplumber
import io
from state_schema import StateType


def extract_text_from_pdf(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_node(state: StateType) -> dict:
    """
    Node to extract text from a .docx file.
    Expects state with key 'file' containing file bytes.
    Returns dict with 'text'.
    """
    file_bytes = state.file
    extracted_text = extract_text_from_pdf(file_bytes)
    return {"extracted_text": extracted_text}



