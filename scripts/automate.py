import os
from generate_script import generate_video_script
from generate_voice import generate_voice
from create_video import create_video
from download_images import download_amazon_image

def main():
    print("🚀 Starting automation...\n")

    # 3 example products — replace URLs/prices/ratings as needed
    products = [
        {
            "title": "Logitech MX Master 3",
            "url": "https://www.amazon.com/dp/B07YFP8KV3",
            "price": "$89.99",
            "rating": "4.7"
        },
        {
            "title": "Razer DeathAdder V2",
            "url": "https://www.amazon.com/dp/B082G5SPR5",
            "price": "$59.00",
            "rating": "4.6"
        },
        {
            "title": "Corsair Harpoon RGB Wireless",
            "url": "https://www.amazon.com/dp/B07RM39V5F",
            "price": "$49.99",
            "rating": "4.4"
        }
    ]

    print("📦 Products Compared:")
    for p in products:
        print(f"- {p['title']} | {p['price']} | Rating: {p['rating']}")
    print()

    # Step 1: Generate the video script
    script = generate_video_script(products)
    print("🎬 Video Script:\n" + script)

    # Step 2: Generate the voiceover
    voice_path = generate_voice(script)
    print(f"✅ Voice saved to {voice_path}")

    # Step 3: Download product images from Amazon
    os.makedirs("assets", exist_ok=True)
    product_images = []
    for i, product in enumerate(products):
        filename = f"assets/product{i+1}.jpg"
        image_path = download_amazon_image(product["url"], filename)
        if image_path:
            product_images.append(image_path)

    # Step 4: Create the video
    video_path = create_video(voice_path, product_images, products)
    print(f"✅ Video created at: {video_path}")

if __name__ == "__main__":
    main()
