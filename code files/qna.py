import os
from google import genai

def get_client():
    # Retrieve the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)

def answer_question_with_gemini(question: str) -> str:
    try:
        client = get_client()
        
        # Updated to active model endpoints
        models_to_try =  [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
    "gemini-3.5-flash"
]
        
        last_error = None
        for model_name in models_to_try:
            try:
                # client.chats avoids AFC warnings and supports streaming/chats
                chat = client.chats.create(model=model_name)
                response = chat.send_message(question)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[QnA Debug] Model {model_name} failed: {e}")
                last_error = e
                continue

        return f"⚠️ Error in QnA: {last_error}"
    except Exception as e:
        print(f"[QnA Debug] Client setup failed: {e}")
        return f"⚠️ Error in QnA Setup: {e}"