import os
from scripts.generate_script import generate_video_script
from scripts.generate_voice import generate_voice
from scripts.create_video import create_video
from scripts.download_images import download_amazon_image

OUTPUT_DIR = "outputs"
ASSETS_DIR = "assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)


def main():
    print("🚀 Starting automation...\n")

    # Step 1: Generate product comparison script
    products, script = generate_video_script()
    print("📦 Products Compared:")
    for p in products:
        print(f"- {p['title']} | ${p['price']} | Rating: {p['rating']}")
    print("\n🎬 Video Script:")
    print(script)

    # Step 2: Generate voiceover from script
    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    # Step 3: Download images for each product
    product_images = []
    for idx, product in enumerate(products, start=1):
        image_path = os.path.join(ASSETS_DIR, f"product{idx}.jpg")
        result = download_amazon_image(product["url"], image_path)
        if result:
            product_images.append(image_path)
        else:
            print(f"❌ Skipping product image for: {product['title']}")

    # Step 4: Create video using images and voice
    if not product_images:
        raise RuntimeError("❌ No valid images were processed. Aborting video creation.")

    video_path = create_video(voice_path, product_images, products)
    print(f"✅ Video created at {video_path}")


if __name__ == "__main__":
    main()
