# automate.py
import os
import logging
from dotenv import load_dotenv
from fetch_products import fetch_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from generate_description import generate_video_description
from download_image import download_amazon_image
from create_video import create_video
from verify_video import verify_video
from upload_to_youtube import upload_to_youtube

# Ensure logs directory exists at project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

# Load environment variables
load_dotenv()

# Setup logging
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "automate.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    print("🚀 Starting automation...\n")
    logging.info("Automation started.")

    try:
        # Step 1: Fetch products
        products = fetch_products()
        print("📦 Products Compared:")
        for p in products:
            print(f"- {p['title']} | ${p['price']} | Rating: {p['rating']}")
        print()

        # Step 2: Generate video script
        script = generate_video_script(products)
        print("🎬 Video Script:")
        print(script)
        print()

        # Step 3: Generate voiceover
        voice_path = generate_voice(script)
        print(f"✅ Voice saved to: {voice_path}")

        # Step 4: Download product images
        for i, product in enumerate(products):
            image_path = download_amazon_image(product["url"], f"product_{i+1}.jpg", product["title"])
            product["image_path"] = image_path
            print(f"🖼️ Image downloaded: {image_path}")

        # Step 5: Create video with attached voiceover
        video_path = create_video(products, voice_path)
        print(f"📹 Video created: {video_path}")

        # Step 6: Generate YouTube description
        description = generate_video_description(products)
        print("📝 Description:")
        print(description)
        print()

        # Step 7: Verify video before upload
        print("🔍 Verifying video/audio integrity...")
        if verify_video(video_path):
            print("✅ Verification passed. Proceeding to upload...")

            # Step 8: Upload to YouTube
            video_id = upload_to_youtube(
                video_path=video_path,
                title="Top Amazon Picks — Quick Showcase",
                description=description,
                tags=["Amazon", "Deals", "Shopping", "Tech"],
                privacy_status="unlisted"
            )
            print(f"🎉 Video uploaded successfully: https://youtu.be/{video_id}")
        else:
            print("🚫 Verification failed — skipping upload.")

        logging.info("Automation completed successfully.")

    except Exception as e:
        logging.error(f"Automation failed: {str(e)}")
        print(f"❌ Error during automation: {str(e)}")


if __name__ == "__main__":
    main()
