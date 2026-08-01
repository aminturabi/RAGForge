"""Ollama local LLM provider plugin."""

import json
import urllib.error
import urllib.request

from core.contracts import LLMProvider
from core.registry import register_plugin


@register_plugin("llms", "ollama")
class OllamaLLMProvider(LLMProvider):
    """Local LLM provider interfacing with Ollama HTTP REST API."""

    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "llama3") -> None:
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name

    def generate(
        self,
        question: str,
        context_chunks: list[str],
        model_name: str | None = None,
        api_key: str | None = None,
    ) -> str:
        selected_model = model_name or self.model_name
        context = "\n\n---\n\n".join(context_chunks)
        system_prompt = (
            "You are a helpful assistant that answers questions using ONLY the provided context. "
            "If the answer is not in the context, say you do not know based on the document."
        )
        prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"

        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False,
        }

        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                if response.status == 200:
                    resp_data = json.loads(response.read().decode("utf-8"))
                    return resp_data.get("response", "").strip()
                raise RuntimeError(f"Ollama returned non-200 status code: {response.status}")
        except urllib.error.URLError as err:
            raise RuntimeError(
                f"Could not connect to Ollama service at {self.base_url}. Make sure Ollama is running. Error: {err}"
            ) from err
