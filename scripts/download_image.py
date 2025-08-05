import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def download_amazon_image(product_url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(product_url, headers=headers)
        if response.status_code != 200:
            raise Exception("Amazon page request failed.")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Attempt dynamic image
        img_tag = soup.find("img", {"id": "landingImage"})
        if img_tag and img_tag.get("src"):
            return img_tag["src"]

        # Attempt hiRes from scripts
        for script in soup.find_all("script"):
            if script.string and "ImageBlockATF" in script.string:
                matches = re.findall(r'"hiRes":"(https:[^"]+)"', script.string)
                if matches:
                    return matches[0]

        raise Exception("No image found using dynamic-image method.")

    except Exception as e:
        print(f"❌ Amazon image failed: {e}")
        return None


def download_serpapi_image(query):
    if not SERPAPI_KEY:
        print("❌ SERPAPI key not found in environment.")
        return None

    params = {
        "engine": "google",
        "q": query,
        "tbm": "isch",
        "api_key": SERPAPI_KEY,
    }

    try:
        response = requests.get("https://serpapi.com/search.json", params=params)
        data = response.json()
        images = data.get("images_results", [])
        if not images:
            raise Exception("No images found in SerpAPI results.")
        return images[0]["original"]

    except Exception as e:
        print(f"❌ SerpAPI image failed: {e}")
        return None


def save_image_from_url(url, output_path):
    try:
        img_response = requests.get(url)
        img = Image.open(BytesIO(img_response.content)).convert("RGB")
        img = img.resize((1080, 1080))
        img.save(output_path)
        print(f"✅ Saved image to {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error downloading image: {e}")
        return None


def download_product_image(product, index):
    output_path = f"assets/product{index + 1}.jpg"

    # Try Amazon first
    image_url = download_amazon_image(product["url"])
    if image_url:
        return save_image_from_url(image_url, output_path)

    # Fallback: SerpAPI
    print(f"🔍 Searching fallback image with SerpAPI for: {product['name']}")
    fallback_url = download_serpapi_image(product["name"])
    if fallback_url:
        return save_image_from_url(fallback_url, output_path)

    print(f"❌ Failed to download image for {product['name']}")
    return None


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    sample_product = {
        "name": "Logitech MX Master 3",
        "url": "https://www.amazon.com/dp/B07YFP8KV3"
    }
    download_product_image(sample_product, 0)
