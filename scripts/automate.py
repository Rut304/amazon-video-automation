import os
from dotenv import load_dotenv

load_dotenv()

from fetch_products import fetch_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from download_image import download_amazon_image
from create_video import create_video
from generate_description import generate_video_description

def main():
    print("🚀 Starting automation...\n")

    products = fetch_products()

    print("📦 Products Compared:")
    for p in products:
        print(f"- {p['title']} | ${p['price']} | Rating: {p['rating']}")
    print()

    script = generate_video_script(products)
    print("🎬 Video Script:")
    print(script)
    print()

    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    image_paths = []
    for i, product in enumerate(products):
        image_path = f"assets/product{i+1}.jpg"
        result = download_amazon_image(product["url"], product["title"], image_path)
        if result:
            print(f"✅ Saved image to {image_path}")
            image_paths.append(image_path)
        else:
            print(f"❌ Failed to download image for {product['title']}")

    if not image_paths:
        raise RuntimeError("❌ No valid images were processed. Aborting video creation.")

    video_path = create_video(voice_path, image_paths)
    print(f"✅ Video saved to {video_path}")

    description = generate_video_description(products)
    with open("outputs/description.txt", "w") as f:
        f.write(description)
    print("✅ Description saved to outputs/description.txt")

if __name__ == "__main__":
    main()
