import os
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

def tts_to_file(
    text: str,
    out_path: str = "output.mp3",
    voice_id: str | None = None,
    stability: float = 0.5,
    similarity: float = 0.7,
) -> str:
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY is not set in environment or .env")

    vid = voice_id or DEFAULT_VOICE_ID
    if not vid:
        raise RuntimeError("No voice_id provided and ELEVENLABS_VOICE_ID not set")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "voice_settings": {"stability": stability, "similarity_boost": similarity},
    }

    with requests.post(url, headers=headers, json=data, stream=True) as r:
        r.raise_for_status()
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    size = Path(out_path).stat().st_size
    if size < 1024:
        raise RuntimeError(f"TTS output seems too small ({size} bytes). Check API key/voice/text.")

    return out_path

if __name__ == "__main__":
    import sys

    text = sys.argv[1] if len(sys.argv) > 1 else "Your automated narration is ready."
    out = sys.argv[2] if len(sys.argv) > 2 else "output.mp3"
    path = tts_to_file(text, out)
    print(f"Wrote {path}")
