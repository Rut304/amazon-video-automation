import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from serpapi import GoogleSearch

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

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
        soup = BeautifulSoup(response.text, "html.parser")

        # Try to find dynamic image from Amazon
        image_tag = soup.find("img", {"id": "landingImage"})
        if image_tag and image_tag.get("src"):
            return image_tag["src"]

        # Try fallback via regex
        for script in soup.find_all("script"):
            if script.string and 'ImageBlockATF' in script.string:
                match = re.search(r'"hiRes":"(https:[^"]+)"', script.string)
                if match:
                    return match.group(1)

        print("❌ Amazon image failed: No image found using dynamic-image method.")
        return None

    except Exception as e:
        print(f"❌ Amazon image error: {e}")
        return None


def search_fallback_image(query):
    try:
        print(f"🔍 Searching fallback image with SerpAPI for: {query}")
        search = GoogleSearch({
            "q": query,
            "tbm": "isch",
            "ijn": "0",
            "api_key": SERPAPI_KEY
        })
        results = search.get_dict()
        images = results.get("images_results", [])

        for image in images:
            link = image.get("original") or image.get("thumbnail")
            if link and (".jpg" in link or ".png" in link):
                return link

        print("❌ SerpAPI image failed: No images found in SerpAPI results.")
        return None

    except Exception as e:
        print(f"❌ SerpAPI error: {e}")
        return None


def save_image_from_url(url, output_path):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Image request failed: " + str(response.status_code))
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = img.resize((1080, 1080))
        img.save(output_path)
        print(f"✅ Saved image to {output_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to save image: {e}")
        return False


def download_product_image(product_url, product_name, output_path):
    # Try Amazon first
    image_url = download_amazon_image(product_url)

    # Try SerpAPI if Amazon fails
    if not image_url:
        image_url = search_fallback_image(product_name)

    if image_url:
        return save_image_from_url(image_url, output_path)
    else:
        print(f"❌ Failed to download image for {product_name}")
        return False


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    test_url = "https://www.amazon.com/dp/B07YFP8KV3"
    test_name = "Logitech MX Master 3"
    output_file = "assets/test.jpg"
    download_product_image(test_url, test_name, output_file)
