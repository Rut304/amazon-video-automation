import os
from fetch_products import fetch_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from create_video import create_video
from download_image import download_amazon_image


def main():
    print("🚀 Starting automation...\n")

    # Step 1: Fetch products
    products = fetch_products()
    for p in products:
        print(f"📦 {p['name']} | ${p['price']} | Rating: {p['rating']}")

    print()

    # Step 2: Generate script
    script = generate_video_script(products)
    print("🎬 Video Script:")
    print(script)

    # Step 3: Generate voice
    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    # Step 4: Download product images
    os.makedirs("assets", exist_ok=True)
    product_images = []
    for i, product in enumerate(products):
        image_path = f"assets/product{i+1}.jpg"
        downloaded = download_amazon_image(product["url"], image_path)
        if downloaded:
            product_images.append(image_path)

    # Step 5: Create video
    if product_images:
        print("🎞️ Creating video...")
        video_path = create_video(voice_path, product_images, products)
        print(f"✅ Video saved to {video_path}")
    else:
        raise RuntimeError("❌ No valid images were processed. Check image URLs or fallback logic.")


if __name__ == "__main__":
    main()
