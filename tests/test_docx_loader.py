import os
import tempfile
import zipfile
import pytest

from core.exceptions import DocumentLoadError
from loaders.docx_loader import DOCXLoader
from loaders.document_loader import CompositeDocumentLoader


def create_dummy_docx(file_path: str, text: str = "Hello from DOCX test!"):
    """Helper to create a minimal valid .docx file structure via zipfile."""
    content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="xml" ContentType="application/xml"/>
</Types>"""

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        <w:p>
            <w:r>
                <w:t>{text}</w:t>
            </w:r>
        </w:p>
    </w:body>
</w:document>"""

    with zipfile.ZipFile(file_path, "w") as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("word/document.xml", document_xml)


def test_docx_loader_load():
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp_path = tmp.name
        tmp.close()

    try:
        create_dummy_docx(tmp_path, "RAGForge DOCX Test Document")
        loader = DOCXLoader()
        extracted = loader.load(tmp_path)
        assert "RAGForge DOCX Test Document" in extracted
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_docx_loader_file_not_found():
    loader = DOCXLoader()
    with pytest.raises(DocumentLoadError):
        loader.load("non_existent_file_xyz.docx")


def test_composite_loader_with_docx():
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp_path = tmp.name
        tmp.close()

    try:
        create_dummy_docx(tmp_path, "Composite loader docx test content")
        composite = CompositeDocumentLoader()
        extracted = composite.load(tmp_path)
        assert "Composite loader docx test content" in extracted
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
