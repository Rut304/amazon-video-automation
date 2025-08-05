# scripts/automate.py

from fetch_products import fetch_top_amazon_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from create_video import create_video
from generate_description import generate_video_description

import os

def main():
    # Step 1: Get top 3 products (mocked or real)
    products = fetch_top_amazon_products()
    
    print("\n📦 Products Compared:")
    for p in products:
        print(f"- {p['title']} | {p['price']} | Rating: {p['rating']}")

    # Step 2: Generate YouTube video script using OpenAI
    script = generate_video_script(products)
    print("\n🎬 Video Script:\n" + script)

    # Step 3: Generate voiceover from script using ElevenLabs
    voice_file = generate_voice(script)
    print(f"✅ Voice saved to {voice_file}")

    # Step 4: Create video with placeholder or product image
    video_file = create_video(voice_file)
    print(f"🎥 Final video saved to {video_file}")

    # Step 5: Generate YouTube description with affiliate links
    description = generate_video_description(products, affiliate_tag="1705d0-20")
    print("\n📝 YouTube Description:\n" + description)

if __name__ == "__main__":
    main()
