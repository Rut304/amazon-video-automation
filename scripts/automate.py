import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for modular imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tts.elevenlabs import tts_to_file

# Load environment variables from .env
load_dotenv()

def ensure_build_dirs():
    Path("build/narration").mkdir(parents=True, exist_ok=True)

def validate_env():
    required_vars = ["ELEVENLABS_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"[✗] Missing environment variables: {', '.join(missing)}")
        sys.exit(1)

def narrate(text: str, filename: str):
    try:
        voice_path = tts_to_file(
            text,
            out_path=f"build/narration/{filename}.mp3"
        )
        print(f"[✓] Narration generated: {voice_path}")
        return voice_path
    except Exception as e:
        print(f"[✗] Narration failed: {e}")
        raise

def main():
    print("[•] Starting automation pipeline...")
    ensure_build_dirs()
    validate_env()

    # 🎙️ Voice synthesis step
    try:
        narrate("This product is great for everyday use.", "product_intro")
    except Exception:
        sys.exit(1)

    # ✅ Future steps can go here (video rendering, upload, etc.)
    print("[✓] Pipeline complete.")

if __name__ == "__main__":
    main()
