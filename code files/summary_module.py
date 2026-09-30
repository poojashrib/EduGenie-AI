import os
from google import genai

def get_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)

def summarize_text(text: str) -> str:
    try:
        client = get_client()
        prompt = f"Summarize the following text clearly and concisely in simple language:\n\n{text}"
        
        models_to_try = models_to_try = [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
    "gemini-3.5-flash"
]
        last_error = None

        for m in models_to_try:
            try:
                chat = client.chats.create(model=m)
                response = chat.send_message(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[Summary Debug] Model {m} failed: {e}")
                last_error = e
                continue
                
        return f"⚠️ Summary Error: Unable to generate summary. Detail: {last_error}"
    except Exception as e:
        print(f"[Summary Debug] Setup error: {e}")
        return f"⚠️ Summary Setup Error: {e}"