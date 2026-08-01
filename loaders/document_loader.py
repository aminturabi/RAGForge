"""Legacy-compatible document loader APIs built on modular components."""

import os

from chunking.recursive_character import RecursiveCharacterChunker
from core.contracts import DocumentLoader
from core.registry import register_plugin
from loaders.pdf_loader import PDFLoader
from loaders.text_loader import TextLoader
from loaders.csv_loader import CSVLoader
from loaders.markdown_loader import MarkdownLoader
from loaders.web_loader import WebLoader
from loaders.docx_loader import DOCXLoader


@register_plugin("loaders", "composite")
class CompositeDocumentLoader(DocumentLoader):
    """Loader dispatching by file extension."""

    def __init__(self) -> None:
        self._pdf_loader = PDFLoader()
        self._text_loader = TextLoader()
        self._csv_loader = CSVLoader()
        self._markdown_loader = MarkdownLoader()
        self._web_loader = WebLoader()
        self._docx_loader = DOCXLoader()

    def load(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at: {file_path}")

        _, ext = os.path.splitext(file_path.lower())
        if ext == ".pdf":
            return self._pdf_loader.load(file_path)
        elif ext == ".docx":
            return self._docx_loader.load(file_path)
        elif ext == ".csv":
            return self._csv_loader.load(file_path)
        elif ext == ".md":
            return self._markdown_loader.load(file_path)
        elif ext in {".html", ".htm"}:
            return self._web_loader.load(file_path)
        elif ext in {".txt", ".json"}:
            return self._text_loader.load(file_path)

        # Default fallback to plain text loader for unknown text files
        return self._text_loader.load(file_path)


def load_document(file_path: str) -> str:
    """Backward-compatible function wrapper."""
    return CompositeDocumentLoader().load(file_path)


def split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    """Backward-compatible function wrapper."""
    return RecursiveCharacterChunker(chunk_size=chunk_size, overlap=overlap).chunk(text)
