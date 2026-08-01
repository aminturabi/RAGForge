"""Plugin package discovery."""

import importlib
import pkgutil

_DISCOVERED = False


def discover_plugins() -> None:
    global _DISCOVERED
    if _DISCOVERED:
        return

    packages = [
        "chunking.recursive_character",
        "loaders.document_loader",
        "loaders.docx_loader",
        "embeddings.sentence_transformer",
        "vectorstores.chroma_store",
        "retrievers.vector_retriever",
        "retrievers.hybrid_retriever",
        "rerankers.noop_reranker",
        "llms.groq_provider",
        "llms.ollama_provider",
        "formatters.json_formatter",
    ]
    for module_name in packages:
        importlib.import_module(module_name)

    for module in pkgutil.iter_modules(__path__):
        importlib.import_module(f"{__name__}.{module.name}")

    _DISCOVERED = True

