import os
from pathlib import Path
from dotenv import load_dotenv
from tts.elevenlabs import tts_to_file

# Load environment variables
load_dotenv()

def ensure_dirs():
    Path("build/narration").mkdir(parents=True, exist_ok=True)

def main():
    ensure_dirs()

    try:
        # 🎤 Voice generation step
        voice_path = tts_to_file(
            "This product is great for everyday use.",
            out_path="build/narration/product_intro.mp3"
        )
        print(f"[✓] Voice narration saved to {voice_path}")

    except Exception as e:
        print(f"[✗] Voice generation failed: {e}")
        return

    # 🔁 Extendable pipeline steps
    # e.g., video generation, thumbnail creation, upload...
    print("[•] Pipeline complete ✅")

if __name__ == "__main__":
    main()
