# -*- coding: utf-8 -*-
import os
import logging
from dotenv import load_dotenv
from fetch_products import fetch_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from generate_description import generate_video_description
from download_image import download_amazon_image
from create_video import create_video

# Load environment variables
load_dotenv()

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/automate.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("🚀 Starting automation...\n")
    logging.info("Automation started.")

    try:
        # Step 1: Fetch products
        products = fetch_products()
        print("📦 Products Compared:")
        for p in products:
            print(f"- {p['title']} | ${p['price']} | Rating: {p['rating']}")
        print()

        # Step 2: Generate video script
        script = generate_video_script(products)
        print("🎬 Video Script:")
        print(script)
        print()

        # Step 3: Generate voiceover
        voice_path = generate_voice(script)
        print(f"✅ Voice saved to {voice_path}")

        # Step 4: Download images
        for i, product in enumerate(products):
            image_path = download_amazon_image(product['url'], f"product_{i+1}.jpg")
            product['image_path'] = image_path
            print(f"🖼️ Image downloaded for: {product['title']}")

        # Step 5: Create video
        video_path = create_video(products, voice_path)
        print(f"📹 Video created: {video_path}")

        # Step 6: Generate YouTube description
        description = generate_video_description(products)
        print("📝 Description:\n" + description)

        logging.info("Automation finished successfully.")

    except Exception as e:
        logging.error(f"Automation failed: {str(e)}")
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
