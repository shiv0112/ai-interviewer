import fitz  # PyMuPDF
from langchain.docstore.document import Document

def load_pdf(file_path: str) -> list[Document]:
    """
    Extracts text from a PDF file and returns a list containing a single LangChain Document.
    """
    try:
        doc = fitz.open(file_path)
        full_text = "\n".join(page.get_text() for page in doc)
        return [Document(page_content=full_text)]
    except Exception as e:
        raise RuntimeError(f"Failed to load PDF: {str(e)}")
