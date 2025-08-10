# generate_voice.py
import os
import time
import requests
from moviepy.editor import AudioFileClip

def generate_voice(script_text: str, voice_id="21m00Tcm4TlvDq8ikWAM") -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise Exception("ELEVENLABS_API_KEY is missing in .env")

    os.makedirs("outputs", exist_ok=True)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": script_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": { "stability": 0.5, "similarity_boost": 0.7 }
    }

    for attempt in range(3):
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200 and resp.content:
            mp3_path = "outputs/voice.mp3"
            with open(mp3_path, "wb") as f:
                f.write(resp.content)
            try:
                clip = AudioFile
