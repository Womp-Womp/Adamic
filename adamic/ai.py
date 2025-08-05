import os
import google.generativeai as genai
from google.generativeai import types


def get_ai_response(query: str) -> str:
    """
    Interacts with the Gemini LLM to get a response.
    """
    try:
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        model = "gemini-2.5-pro"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=query),
                ],
            ),
        ]
        tools = [
            types.Tool(googleSearch=types.GoogleSearch()),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=0,
            thinking_config=types.ThinkingConfig(
                thinking_budget=-1,
            ),
            tools=tools,
        )

        response_chunks = []
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response_chunks.append(chunk.text)

        return "".join(response_chunks)

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while processing your request."
