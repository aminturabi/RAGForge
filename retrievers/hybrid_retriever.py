"""Hybrid search retriever combining dense vector retrieval with keyword search via RRF."""

import re
from collections import defaultdict

from core.contracts import EmbeddingModel, Retriever, VectorStoreBackend
from core.registry import register_plugin


@register_plugin("retrievers", "hybrid")
class HybridSearchRetriever(Retriever):
    """Retriever combining dense vector search and BM25/keyword search using Reciprocal Rank Fusion (RRF)."""

    def __init__(
        self,
        vector_store: VectorStoreBackend,
        embedding_model: EmbeddingModel,
        rrf_k: int = 60,
    ) -> None:
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.rrf_k = rrf_k

    def _tokenize(self, text: str) -> set[str]:
        return set(re.findall(r"\w+", text.lower()))

    def retrieve(self, collection_name: str, query: str, top_k: int = 4) -> list[str]:
        if not query.strip():
            return []

        # 1. Dense retrieval
        query_embedding = self.embedding_model.embed(query)
        dense_results = self.vector_store.query(collection_name, [query_embedding], n_results=top_k * 3)

        if not dense_results:
            return []

        # 2. Keyword scoring over candidates
        query_tokens = self._tokenize(query)
        
        def keyword_score(doc: str) -> float:
            doc_tokens = self._tokenize(doc)
            if not doc_tokens or not query_tokens:
                return 0.0
            overlap = query_tokens.intersection(doc_tokens)
            return len(overlap) / (len(query_tokens) ** 0.5)

        keyword_ranked = sorted(dense_results, key=keyword_score, reverse=True)

        # 3. Reciprocal Rank Fusion (RRF)
        rrf_scores: dict[str, float] = defaultdict(float)

        for rank, doc in enumerate(dense_results, start=1):
            rrf_scores[doc] += 1.0 / (self.rrf_k + rank)

        for rank, doc in enumerate(keyword_ranked, start=1):
            rrf_scores[doc] += 1.0 / (self.rrf_k + rank)

        # Sort documents by fused RRF score
        fused = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
        return [doc for doc, _ in fused[:top_k]]
