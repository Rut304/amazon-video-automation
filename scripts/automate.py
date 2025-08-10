import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from tts.elevenlabs import tts_to_file

# Load environment variables from .env
load_dotenv()

def ensure_build_dirs():
    Path("build/narration").mkdir(parents=True, exist_ok=True)

def narrate_product_intro():
    try:
        voice_path = tts_to_file(
            "This product is great for everyday use.",
            out_path="build/narration/product_intro.mp3"
        )
        print(f"[✓] Narration generated: {voice_path}")
        return voice_path
    except Exception as e:
        print(f"[✗] Narration failed: {e}")
        sys.exit(1)

def main():
    print("[•] Starting automation pipeline...")
    ensure_build_dirs()

    # 🎙️ Voice synthesis step
    narrate_product_intro()

    # ✅ Future steps can go here (video rendering, upload, etc.)
    print("[✓] Pipeline complete.")

if __name__ == "__main__":
    main()
