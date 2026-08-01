"""DOCX document loader plugin."""

import os
import xml.etree.ElementTree as ET
import zipfile

from core.contracts import DocumentLoader
from core.exceptions import DocumentLoadError
from core.registry import register_plugin


@register_plugin("loaders", "docx")
class DOCXLoader(DocumentLoader):
    """Loads text from Microsoft Word .docx documents."""

    def load(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise DocumentLoadError(f"DOCX file not found: {file_path}")

        # Try using python-docx if installed
        try:
            import docx

            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs if para.text]
            return "\n".join(full_text)
        except (ImportError, Exception):
            # Fallback to standard library zipfile + xml parsing if python-docx is not installed or fails
            try:
                return self._load_via_zipfile(file_path)
            except Exception as err:
                raise DocumentLoadError(f"Failed to read DOCX document {file_path}: {err}") from err

    def _load_via_zipfile(self, file_path: str) -> str:
        try:
            with zipfile.ZipFile(file_path, "r") as zf:
                if "word/document.xml" not in zf.namelist():
                    raise DocumentLoadError(f"Invalid DOCX file structure: {file_path}")
                xml_content = zf.read("word/document.xml")

            root = ET.fromstring(xml_content)
            # Namespace map for WordprocessingML
            namespaces = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            
            paragraphs = []
            for p in root.findall(".//w:p", namespaces):
                texts = [node.text for node in p.findall(".//w:t", namespaces) if node.text]
                if texts:
                    paragraphs.append("".join(texts))

            return "\n".join(paragraphs)
        except DocumentLoadError:
            raise
        except Exception as err:
            raise DocumentLoadError(f"Failed to read DOCX XML from {file_path}: {err}") from err
