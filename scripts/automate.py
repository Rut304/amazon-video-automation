import os
from dotenv import load_dotenv
from fetch_products import fetch_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from generate_description import generate_video_description
from download_image import download_amazon_image
from create_video import create_video

# Load environment variables
load_dotenv()

def main():
    print("🚀 Starting automation...\n")

    # Step 1: Fetch products
    products = fetch_products()
    print("📦 Products Compared:")
    for p in products:
        print(f"- {p['title']} | ${p['price']} | Rating: {p['rating']}")
    print()

    # Step 2: Generate script
    script = generate_video_script(products)
    print("🎬 Video Script:")
    print(script + "\n")

    # Step 3: Generate voiceover
    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    # Step 4: Download product images
    image_paths = []
    for i, product in enumerate(products):
        image_path = f"assets/product{i+1}.jpg"
        result = download_amazon_image(product["url"], product["title"], image_path)
        if result:
            image_paths.append(image_path)
            print(f"✅ Saved image to {image_path}")
        else:
            print(f"❌ Failed to download image for {product['title']}")
    
    if not image_paths:
        raise RuntimeError("❌ No valid images were processed. Aborting video creation.")

    # Step 5: Create video
    video_path = create_video(voice_path, image_paths, products)
    print(f"✅ Video saved to {video_path}")

    # Step 6: Generate description
    description = generate_video_description(products)
    with open("outputs/description.txt", "w") as f:
        f.write(description)
    print("✅ Description saved to outputs/description.txt")

if __name__ == "__main__":
    main()
