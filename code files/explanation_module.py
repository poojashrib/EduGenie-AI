import os
from google import genai

def get_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    return genai.Client(api_key=api_key)

def explain_topic(topic: str) -> str:
    try:
        client = get_client()
        prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
        
        models_to_try = [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
    "gemini-3.5-flash"
]
        
        for m in models_to_try:
            try:
                chat = client.chats.create(model=m)
                response = chat.send_message(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception:
                continue
                
        return "⚠️ Explanation Error: Unable to contact Gemini models."
    except Exception as e:
        return f"⚠️ Explanation Error: {e}"