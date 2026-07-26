"""Groq LLM provider plugin."""

import os

from groq import Groq

from core.contracts import LLMProvider
from core.registry import register_plugin


@register_plugin("llms", "groq")
class GroqLLMProvider(LLMProvider):
    def __init__(self, model_name: str = "llama-3.3-70b-versatile", api_key: str | None = None) -> None:
        self.model_name = model_name
        self.api_key = api_key

    def generate(
        self,
        question: str,
        context_chunks: list[str],
        model_name: str | None = None,
        api_key: str | None = None,
    ) -> str:
        final_api_key = api_key or self.api_key or os.environ.get("GROQ_API_KEY")
        if not final_api_key:
            raise ValueError(
                "Groq API Key is missing. Please set the GROQ_API_KEY environment variable or supply it in config."
            )

        client = Groq(api_key=final_api_key)
        context = "\n\n---\n\n".join(context_chunks)
        system_prompt = (
            "You are a helpful assistant that answers questions using ONLY the provided context. "
            "If the answer is not in the context, say you do not know based on the document."
        )
        user_prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"

        response = client.chat.completions.create(
            model=model_name or self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
