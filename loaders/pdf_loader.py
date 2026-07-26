import os
from pypdf import PdfReader

from core.contracts import DocumentLoader
from core.exceptions import DocumentLoadError
from core.registry import register_plugin


@register_plugin("loaders", "pdf")
class PDFLoader(DocumentLoader):
    """Loads text from PDF documents using PyPDF."""

    def load(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise DocumentLoadError(f"PDF file not found: {file_path}")
        try:
            reader = PdfReader(file_path)
            return "\n".join((page.extract_text() or "") for page in reader.pages)
        except Exception as err:
            raise DocumentLoadError(f"Failed to read PDF document {file_path}: {err}") from err


