"""Utilities for interacting with the Gemini AI models."""

import os

from google import genai
from google.genai import types


# Initialize the client using the API key provided via environment variable.
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def get_ai_response(query: str) -> str:
    """Generate a response from the Gemini model for a text query.

    Args:
        query: Prompt text sent to the model.

    Returns:
        The model's response text if successful, otherwise an error message.
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=query)],
                )
            ],
        )
        return response.text
    except Exception as exc:  # pragma: no cover - best effort error handling
        return f"Error: {exc}"

