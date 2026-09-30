import os
from pathlib import Path

from google import genai

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# Updated to valid, supported model identifiers
MODEL_CANDIDATES = (
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest",
)

if load_dotenv is not None:
    load_dotenv(Path(__file__).resolve().parent / ".env")


def get_api_key() -> str | None:
    return (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("API_KEY")
    )


def get_gemini_client():
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in your environment."
        )
    return genai.Client(api_key=api_key)


def generate_text(prompt: str) -> str:
    client = get_gemini_client()
    last_error = None

    for model in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            if response.text:
                return response.text.strip()
        except Exception as exc:
            last_error = exc

    if last_error is not None:
        raise RuntimeError(f"Gemini request failed: {last_error}") from last_error

    raise RuntimeError("Gemini response was empty.")