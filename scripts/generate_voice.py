from dotenv import load_dotenv
import os
import sys

load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    print("❌ ELEVENLABS_API_KEY is missing in environment variables or `.env` file.")
    api_key = input("🔑 Paste your ElevenLabs API Key: ").strip()
    if not api_key:
        print("🚫 No API key provided. Exiting.")
        sys.exit(1)
