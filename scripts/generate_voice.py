# generate_voice.py
import requests
import os

def generate_voice(script_text, filename="outputs/voice.mp3"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = "EXAVITQu4vr4xnSDxMaL"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": script_text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Voice generation failed: {response.text}")

    # Save the MP3 file
    os.makedirs("outputs", exist_ok=True)
    with open(filename, "wb") as f:
        f.write(response.content)

    return filename
