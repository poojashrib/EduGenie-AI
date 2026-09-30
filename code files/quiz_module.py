import os
import re
import json
from google import genai

def get_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)

def clean_json_block(text: str) -> str:
    return re.sub(r"```(?:json)?\n?(.*?)```", r"\1", text, flags=re.DOTALL).strip()

def generate_quiz(text: str) -> list:
    try:
        client = get_client()
        prompt = f"""
You are a quiz generator.

From the following topic or passage, create 3 multiple-choice questions. Each question must include:
- A "question" string
- An "options" array containing 4 string choices
- An "answer" string matching one of the options exactly

Format your output strictly as a **valid JSON array** like this:
[
  {{
    "question": "What is ...?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A"
  }}
]

Passage/Topic:
{text}
"""
        models_to_try = [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
    "gemini-3.5-flash"]
        quiz_text = None
        last_error = None
        
        for m in models_to_try:
            try:
                chat = client.chats.create(model=m)
                response = chat.send_message(prompt)
                if response and response.text:
                    quiz_text = response.text.strip()
                    break
            except Exception as e:
                print(f"[Quiz Debug] Model {m} failed: {e}")
                last_error = e
                continue

        if not quiz_text:
            return [{"error": f"Failed to connect to Gemini models. Detail: {last_error}"}]

        cleaned = clean_json_block(quiz_text)
        return json.loads(cleaned)

    except Exception as e:
        print(f"[Quiz Debug] Exception: {e}")
        return [{"error": f"Quiz generation error: {str(e)}"}]