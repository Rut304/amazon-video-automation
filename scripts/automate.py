import os
from fetch_products import fetch_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from generate_description import generate_video_description
from create_video import create_video
from download_image import download_amazon_image


def main():
    print("🚀 Starting automation...\n")

    # Step 1: Fetch product data
    products = fetch_products()

    print("📦 Products Compared:")
    for p in products:
        print(f"- {p['title']} | ${p['price']} | Rating: {p['rating']}")
    print()

    # Step 2: Generate video script
    script = generate_video_script(products)
    print("🎬 Video Script:")
    print(script)

    # Step 3: Generate voiceover
    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    # Step 4: Download product images
    product_images = []
    for idx, product in enumerate(products):
        image_filename = f"assets/product{idx+1}.jpg"
        result = download_amazon_image(product["image"], image_filename)
        if result:
            product_images.append(image_filename)
        else:
            print(f"❌ Failed to download image for {product['title']}")

    if not product_images:
        raise RuntimeError("❌ No valid images were processed. Aborting video creation.")

    print("🎞️ Creating video...")
    video_path = create_video(voice_path, product_images, products)
    print(f"✅ Video saved to {video_path}")

    # Step 5: Generate description
    description = generate_video_description(products)
    with open("outputs/description.txt", "w") as f:
        f.write(description)
    print("✅ Description saved to outputs/description.txt")


if __name__ == "__main__":
    main()
