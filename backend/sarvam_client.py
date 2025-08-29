# sarvam_client.py
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # take environment variables from .env

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_BASE = os.getenv("SARVAM_BASE", "https://api.sarvam.ai/v1")  # adjust if needed

class SarvamError(Exception):
    pass

def summarize_with_sarvam(text: str, max_tokens=300):
    """
    Summarizes text using Sarvam AI's chat completion API.
    """
    if not SARVAM_API_KEY:
        raise SarvamError("No API key found in environment. Set SARVAM_API_KEY.")

    url = f"{SARVAM_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        # ⚠️ CHANGE THIS: Replace with correct Sarvam model from docs
        "model": "sarvam-m",
        "messages": [
            {"role": "system", "content": "You are a helpful summarizer."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ],
        "max_tokens": max_tokens,
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=40)
        print("Sarvam raw response:", resp.text)  # Debug print
        resp.raise_for_status()
        data = resp.json()

        # Try OpenAI-style parsing
        if "choices" in data:
            choice = data["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"].strip()
            elif "text" in choice:  # fallback to text field
                return choice["text"].strip()

        # If response shape is different, raise error
        raise SarvamError(f"Unexpected response format: {data}")

    except Exception as e:
        print("Sarvam API error:", str(e))
        return None
