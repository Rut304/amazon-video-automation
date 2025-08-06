import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_voice(script: str) -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # default "Rachel"

    if not api_key:
        raise Exception("❌ ELEVENLABS_API_KEY is not set.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    data = {
        "text": script,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Voice generation failed: {response.text}")

    output_path = "outputs/voice.mp3"
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
