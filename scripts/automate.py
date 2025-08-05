import os
from generate_script import generate_video_script
from generate_voice import generate_voice
from create_video import create_video
from fetch_products import fetch_products
from generate_description import generate_video_description
from download_image import download_amazon_image

OUTPUT_DIR = "outputs"
ASSETS_DIR = "assets"

def main():
    print("🚀 Starting automation...")

    # Fetch product data
    products = fetch_products()

    print("📦 Products Compared:")
    for p in products:
        print(f"- {p['name']} | ${p['price']} | Rating: {p['rating']}")

    # Generate video script
    script = generate_video_script(products)
    print("🎬 Video Script:")
    print(script)

    # Generate voice
    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    # Download product images
    product_images = []
    for i, product in enumerate(products):
        image_path = os.path.join(ASSETS_DIR, f"product{i+1}.jpg")
        result = download_amazon_image(product["url"], product["name"], image_path)
        if result:
            product_images.append(result)

    if not product_images:
        raise RuntimeError("❌ No valid images were processed. Aborting video creation.")

    # Create the video
    video_path = create_video(voice_path, product_images, products)
    print(f"✅ Video saved to {video_path}")

    # Generate and save description
    description = generate_video_description(products)
    description_path = os.path.join(OUTPUT_DIR, "description.txt")
    with open(description_path, "w") as f:
        f.write(description)
    print(f"✅ Description saved to {description_path}")


if __name__ == "__main__":
    main()
