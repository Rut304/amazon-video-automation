import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def resize_and_save(img_data, output_path):
    img = Image.open(BytesIO(img_data)).convert("RGB")
    img = img.resize((1080, 1080))
    img.save(output_path)
    print(f"✅ Saved image to {output_path}")
    return output_path

def fetch_amazon_image(product_url):
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
            raise Exception(f"Failed to fetch product page: {product_url}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for high-res image
        image_url = None
        for script in soup.find_all("script"):
            if script.string and 'ImageBlockATF' in script.string:
                matches = re.findall(r'"hiRes":"(https:[^\"]+?)"', script.string)
                if matches:
                    image_url = matches[0]
                    break

        # Fallback: try data-dynamic-image tag
        if not image_url:
            img_tag = soup.find("img", {"data-dynamic-image": True})
            if img_tag:
                dynamic_data = img_tag["data-dynamic-image"]
                urls = re.findall(r'"(https:[^"]+)"', dynamic_data)
                if urls:
                    image_url = urls[0]

        if not image_url:
            raise Exception("No image found using dynamic-image method.")

        print(f"📸 Found Amazon image URL: {image_url}")
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        return img_response.content

    except Exception as e:
        print(f"❌ Amazon image failed: {e}")
        return None

def fetch_image_from_serpapi(query):
    print(f"🔍 Searching fallback image with SerpAPI for: {query}")
    try:
        params = {
            "engine": "google",
            "q": query,
            "tbm": "isch",
            "api_key": SERPAPI_KEY
        }
        resp = requests.get("https://serpapi.com/search", params=params)
        data = resp.json()

        if "images_results" in data and len(data["images_results"]) > 0:
            image_url = data["images_results"][0]["original"]
            print(f"📸 Found SerpAPI image URL: {image_url}")
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            return img_response.content
        else:
            raise Exception("No images found in SerpAPI results.")
    except Exception as e:
        print(f"❌ SerpAPI image failed: {e}")
        return None

def download_amazon_image(product_url, product_name, output_path):
    img_data = fetch_amazon_image(product_url)

    if not img_data:
        img_data = fetch_image_from_serpapi(product_name)

    if img_data:
        return resize_and_save(img_data, output_path)
    else:
        print(f"❌ Failed to download image for {product_name}")
        return None


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    test_url = "https://www.amazon.com/dp/B07YFP8KV3"
    test_name = "Logitech MX Master 3"
    download_amazon_image(test_url, test_name, "assets/test_image.jpg")
