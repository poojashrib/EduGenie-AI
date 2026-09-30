import os
import traceback
from google import genai

def get_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)

def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and recommended resources.
Include beginner, intermediate, and advanced levels where applicable.
"""
    try:
        client = get_client()
        models_to_try = [
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
                print(f"[LearningPath Debug] Model {m} failed: {e}")
                last_error = e
                continue

        return f"⚠️ Could not generate learning recommendations. Error: {last_error}"
    except Exception as e:
        traceback.print_exc()
        return f"⚠️ Learning Path Setup Error: {str(e)}"