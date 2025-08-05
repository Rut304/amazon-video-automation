# scripts/automate.py

import os
from fetch_products import fetch_top_amazon_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from create_video import create_video
from generate_description import generate_description

def main():
    print("🚀 Starting automation...\n")

    products = fetch_top_amazon_products()
    print("📦 Products Compared:")
    for product in products:
        print(f"- {product['title']} | {product['price']} | Rating: {product['rating']}")

    script = generate_video_script(products)
    print("\n🎬 Video Script:\n" + script)

    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    product_images = [
        "assets/placeholder.jpg",
        "assets/placeholder2.jpg",
        "assets/placeholder3.jpg"
    ]

    video_path = create_video(voice_path, product_images, products)
    print(f"✅ Video saved to {video_path}")

    description = generate_description(products)
    print("\n📝 Video Description:\n" + description)

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/description.txt", "w") as f:
        f.write(description)

    print("\n✅ All steps completed!")

if __name__ == "__main__":
    main()
