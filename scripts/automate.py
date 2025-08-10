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

# Load environment variables
load_dotenv()

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/automate.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("🚀 Starting automation...\n")
    logging.info("Automation started.")

    try:
        # Step 1: Fetch products
        products = fetch_products()
        print("📦 Products Compared:")
        for p in products:
            print(f"- {p['title']}
