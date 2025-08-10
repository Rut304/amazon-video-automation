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
                clip = AudioFileClip(mp3_path)
                if not clip.duration or clip.duration <= 0:
                    raise ValueError("Voice file has zero duration")
                print(f"[DEBUG] TTS duration: {clip.duration:.2f}s")

                wav_path = "outputs/voice.wav"
                clip.write_audiofile(
                    wav_path,
                    fps=44100,
                    nbytes=2,
                    codec="pcm_s16le"
                )
                clip.close()
                return wav_path
            except Exception as e:
                print(f"[WARN] WAV conversion failed: {e}, using MP3 fallback")
                return mp3_path
        print(f"[WARN] Attempt {attempt+1} failed: {resp.status_code} - {resp.text[:100]}")
        time.sleep(2 ** attempt)

    raise Exception("Voice generation failed after retries")
