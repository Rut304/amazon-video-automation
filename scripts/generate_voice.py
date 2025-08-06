import os
import requests

def generate_voice(script_text):
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    if not elevenlabs_key:
        raise Exception("ELEVENLABS_API_KEY is missing from environment.")

    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"  # Use a real voice ID
    headers = {
        "xi-api-key": elevenlabs_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": script_text,
        "model_id": "eleven_monolingual_v1"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        voice_path = "outputs/voice.mp3"
        with open(voice_path, "wb") as f:
            f.write(response.content)
        return voice_path
    else:
        raise Exception(f"Voice generation failed: {response.text}")
