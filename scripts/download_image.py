import os
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

def download_amazon_image(product_url, product_name, output_path):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        # Try to scrape the Amazon image first
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tag = soup.find("img", {"id": "landingImage"})
        image_url = image_tag["src"] if image_tag else None

        if not image_url:
            print("❌ Amazon image failed: No image found using dynamic-image method.")
            raise Exception("Amazon image not found.")

        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data)).convert("RGB")
        img = img.resize((1080, 1080))
        img.save(output_path)
        print(f"✅ Saved Amazon image: {output_path}")
        return output_path

    except Exception:
        # Fallback to SerpAPI
        try:
            print(f"🔍 Searching fallback image with SerpAPI for: {product_name}")
            search = GoogleSearch({
                "q": product_name,
                "tbm": "isch",
                "api_key": SERPAPI_KEY
            })
            results = search.get_dict()
            image_results = results.get("images_results", [])
            if not image_results:
                raise Exception("No images found in SerpAPI results.")
            image_url = image_results[0]["original"]

            img_data = requests.get(image_url).content
            img = Image.open(BytesIO(img_data)).convert("RGB")
            img = img.resize((1080, 1080))
            img.save(output_path)
            print(f"✅ Saved SerpAPI fallback image: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ SerpAPI image failed: {e}")
            return None
