import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from serpapi import GoogleSearch

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def download_amazon_image(product_url, product_title, output_path):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        # Step 1: Try to fetch image from Amazon product page
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find("img", {"id": "landingImage"})
        if img_tag and img_tag.get("src"):
            image_url = img_tag["src"]
            print(f"✅ Amazon image found: {image_url}")
            return _save_image(image_url, output_path)

        print("❌ Amazon image failed: No image found using dynamic-image method.")

    except Exception as e:
        print(f"❌ Error scraping Amazon: {e}")

    # Step 2: Fallback using SerpAPI
    if SERPAPI_API_KEY:
        try:
            print(f"🔍 Searching fallback image with SerpAPI for: {product_title}")
            search = GoogleSearch({
                "q": product_title,
                "tbm": "isch",
                "api_key": SERPAPI_API_KEY
            })
            results = search.get_dict()
            images = results.get("images_results", [])
            if images:
                fallback_url = images[0]["original"]
                print(f"✅ SerpAPI image found: {fallback_url}")
                return _save_image(fallback_url, output_path)
            else:
                print("❌ SerpAPI image failed: No images found in SerpAPI results.")
        except Exception as e:
            print(f"❌ SerpAPI error: {e}")
    else:
        print("❌ No SERPAPI_API_KEY set. Cannot use fallback.")

    return None


def _save_image(image_url, output_path):
    try:
        img_response = requests.get(image_url)
        if img_response.status_code != 200:
            raise Exception("Image request failed: " + str(img_response.status_code))

        img = Image.open(BytesIO(img_response.content)).convert("RGB")
        img = img.resize((1080, 1080))
        img.save(output_path)
        print(f"✅ Saved image to {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error saving image: {e}")
        return None


if __name__ == "__main__":
    test_url = "https://www.amazon.com/dp/B07YFP8KV3"
    os.makedirs("assets", exist_ok=True)
    download_amazon_image(test_url, "Logitech MX Master 3", "assets/test_image.jpg")
