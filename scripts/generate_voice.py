from dotenv import load_dotenv
import os
import sys
import requests

load_dotenv()

# Check or prompt for API key
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    print("❌ ELEVENLABS_API_KEY is missing in environment variables or `.env` file.")
    api_key = input("🔑 Paste your ElevenLabs API Key: ").strip()
    if not api_key:
        print("🚫 No API key provided. Exiting.")
        sys.exit(1)

def generate_voice(text, voice_id="default"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Voice generation failed: {response.text}")

    with open("output.mp3", "wb") as f:
        f.write(response.content)
    print("✅ Voice generated and saved to output.mp3")
