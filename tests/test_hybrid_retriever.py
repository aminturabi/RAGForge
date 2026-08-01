from unittest.mock import MagicMock

from retrievers.hybrid_retriever import HybridSearchRetriever


def test_hybrid_search_retriever():
    mock_vector_store = MagicMock()
    mock_vector_store.query.return_value = [
        "Python is a high-level programming language.",
        "RAGForge is a modular RAG framework written in Python.",
        "Machine learning models are trained on datasets.",
    ]

    mock_embedding_model = MagicMock()
    mock_embedding_model.embed.return_value = [0.1, 0.2, 0.3]

    retriever = HybridSearchRetriever(
        vector_store=mock_vector_store,
        embedding_model=mock_embedding_model,
        rrf_k=60,
    )

    results = retriever.retrieve(
        collection_name="test_col",
        query="modular framework Python",
        top_k=2,
    )

    assert len(results) == 2
    # The document mentioning "modular RAG framework written in Python" has highest keyword match + high dense rank
    assert "RAGForge is a modular RAG framework written in Python." in results


def test_hybrid_search_empty_query():
    mock_vector_store = MagicMock()
    mock_embedding_model = MagicMock()

    retriever = HybridSearchRetriever(
        vector_store=mock_vector_store,
        embedding_model=mock_embedding_model,
    )

    results = retriever.retrieve("test_col", "   ", top_k=4)
    assert results == []
