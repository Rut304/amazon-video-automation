import os
from fetch_products import fetch_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from generate_description import generate_video_description
from create_video import create_video
from download_image import download_product_image

OUTPUT_DIR = "outputs"
ASSETS_DIR = "assets"

def main():
    print("🚀 Starting automation...")

    # Step 1: Fetch Products
    products = fetch_products()

    # Step 2: Display Products
    print("📦 Products Compared:")
    for p in products:
        print(f"- {p['title']} | ${p['price']} | Rating: {p['rating']}")

    # Step 3: Generate Script
    script = generate_video_script(products)
    print("🎬 Video Script:")
    print(script)

    # Step 4: Generate Voiceover
    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    # Step 5: Download Images
    product_images = []
    os.makedirs(ASSETS_DIR, exist_ok=True)

    for i, product in enumerate(products):
        image_path = os.path.join(ASSETS_DIR, f"product{i+1}.jpg")
        result = download_product_image(product["url"], product["title"], image_path)
        if result:
            product_images.append(image_path)
        else:
            print(f"❌ Failed to download image for {product['title']}")

    if not product_images:
        raise RuntimeError("❌ No valid images were processed. Aborting video creation.")

    # Step 6: Create Video
    video_path = create_video(voice_path, product_images, products)
    print(f"✅ Video saved to {video_path}")

    # Step 7: Generate Description
    description = generate_video_description(products)
    desc_path = os.path.join(OUTPUT_DIR, "description.txt")
    with open(desc_path, "w") as f:
        f.write(description)
    print(f"✅ Description saved to {desc_path}")


if __name__ == "__main__":
    main()
