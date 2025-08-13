"""Utilities for interacting with the Gemini AI models."""

from __future__ import annotations

import os
import time
from typing import Iterator

from google import genai
from google.genai import types

# Initialize the client using the API key provided via environment variable.
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def stream_ai_response(query: str, timeout: float | None = 15) -> Iterator[str]:
    """Yield incremental responses from the Gemini model.

    Args:
        query: The user's prompt.
        timeout: Maximum number of seconds to stream for. ``None`` means no
            explicit timeout.

    Yields:
        Chunks of text from the model as they arrive.
    """

    model = "gemini-2.5-pro"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(query)],
        )
    ]

    start = time.time()
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
    ):
        if timeout is not None and time.time() - start > timeout:
            break

        text = getattr(chunk, "text", "")
        if text:
            yield text


def get_ai_response(query: str, timeout: float | None = 15) -> str:
    """Return a full response for ``query`` by streaming the result."""

    try:
        return "".join(stream_ai_response(query, timeout))
    except Exception as exc:  # pragma: no cover - best effort error handling
        return f"Error: {exc}"
