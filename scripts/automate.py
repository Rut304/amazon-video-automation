import os
from fetch_products import fetch_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from generate_description import generate_description
from create_video import create_video
from download_image import download_amazon_image

def main():
    print("🚀 Starting automation...\n")

    # Step 1: Fetch product data
    products = fetch_products()
    if not products or len(products) < 3:
        raise ValueError("❌ Not enough products fetched. Need at least 3.")

    print("📦 Products Compared:")
    for p in products:
        print(f"- {p['name']} | ${p['price']} | Rating: {p['rating']}")

    # Step 2: Generate video script
    script = generate_video_script(products)
    print("\n🎬 Video Script:")
    print(script)

    # Step 3: Generate voiceover
    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    # Step 4: Download product images
    image_paths = []
    os.makedirs("assets", exist_ok=True)

    for i, product in enumerate(products):
        output_path = f"assets/product{i+1}.jpg"
        image_path = download_amazon_image(product["url"], output_path)
        if image_path:
            image_paths.append(image_path)

    if not image_paths:
        raise RuntimeError("❌ No valid images were processed. Aborting video creation.")

    print("🖼️ Downloaded images:")
    for img in image_paths:
        print(f"- {img}")

    # Step 5: Create video
    video_path = create_video(voice_path, image_paths, products)
    print(f"🎞️ Video saved to {video_path}")

    # Step 6: Generate YouTube description
    description = generate_description(products)
    with open("outputs/description.txt", "w") as f:
        f.write(description)
    print("📝 YouTube description saved to outputs/description.txt")

if __name__ == "__main__":
    main()
