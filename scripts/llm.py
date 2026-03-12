from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def _extract_text(response) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text

    parts: list[str] = []
    for item in getattr(response, "output", []):
        for content in getattr(item, "content", []):
            if getattr(content, "type", None) == "output_text" and getattr(content, "text", None):
                parts.append(content.text)

    return "\n".join(parts).strip()


def run_prompt(prompt_text: str) -> str:
    client = _get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o")

    response = client.responses.create(
        model=model,
        input=prompt_text,
    )

    output = _extract_text(response)
    if not output:
        raise RuntimeError("Model returned an empty response.")

    return output
