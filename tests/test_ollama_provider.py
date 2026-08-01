import json
from unittest.mock import MagicMock, patch
import pytest

from llms.ollama_provider import OllamaLLMProvider


def test_ollama_provider_successful_generate():
    provider = OllamaLLMProvider(base_url="http://localhost:11434", model_name="llama3")

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = json.dumps({"response": "This is Ollama's answer."}).encode("utf-8")
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        res = provider.generate(
            question="What is RAGForge?",
            context_chunks=["RAGForge is a modular Python framework for building RAG applications."],
        )
        assert res == "This is Ollama's answer."


def test_ollama_provider_connection_error():
    provider = OllamaLLMProvider(base_url="http://localhost:11434", model_name="llama3")

    import urllib.error
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
        with pytest.raises(RuntimeError) as exc_info:
            provider.generate(
                question="What is RAGForge?",
                context_chunks=["RAGForge context"],
            )
        assert "Could not connect to Ollama service" in str(exc_info.value)
