"""Backward-compatible pipeline adapter."""

from llms.groq_provider import GroqLLMProvider


def rag_advanced(
    question: str,
    context_chunks: list[str],
    api_key: str | None = None,
    model_name: str = "llama-3.3-70b-versatile",
) -> str:
    provider = GroqLLMProvider(model_name=model_name, api_key=api_key)
    return provider.generate(question=question, context_chunks=context_chunks, model_name=model_name, api_key=api_key)
