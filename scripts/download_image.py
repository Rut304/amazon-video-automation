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
        print(f"❌ Am
