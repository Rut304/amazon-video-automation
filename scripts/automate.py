# scripts/automate.py

import os
from fetch_products import fetch_top_amazon_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from create_video import create_video
from generate_description import generate_description

def main():
    print("🚀 Starting automation...\n")

    # Step 1: Fetch product data
    products = fetch_top_amazon_products()

    print("📦 Products Compared:")
    for product in products:
        print(f"- {product['title']} | {product['price']} | Rating: {product['rating']}")

    # Step 2: Generate video script
    script = generate_video_script(products)
    print("\n🎬 Video Script:\n" + script)

    # Step 3: Generate voiceover
    voice_file = generate_voice(script)
    print(f"✅ Voice saved to {voice_file}")

    # Step 4: Generate video
    video_file = create_video(voice_file)
    print(f"✅ Video saved to {video_file}")

    # Step 5: Generate description with affiliate links
    description = generate_description(products)
    print("\n📝 Video Description:\n" + description)

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/description.txt", "w") as f:
        f.write(description)
