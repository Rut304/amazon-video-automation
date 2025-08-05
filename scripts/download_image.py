import os
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


def download_amazon_image(product_url, output_path):
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

        # Find all script tags and search for image URL in JSON
        image_url = None
        for script in soup.find_all("script"):
            if script.string and 'ImageBlockATF' in script.string:
                matches = re.findall(r'"hiRes":"(https:[^\"]+?)"', script.string)
                if matches:
                    image_url = matches[0]
                    break

        if not image_url:
            raise Exception("No high-res image URL found on product page.")

        print(f"📸 Found image URL: {image_url}")

        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content)).convert("RGB")
        img = img.resize((1080, 1080))
        img.save(output_path)
        print(f"✅ Saved image to {output_path}")

        return output_path

    except Exception as e:
        print(f"❌ Error downloading image from {product_url}: {e}")
        return None


if __name__ == "__main__":
    # Example usage for manual testing
    test_url = "https://www.amazon.com/dp/B07YFP8KV3"
    os.makedirs("assets", exist_ok=True)
    download_amazon_image(test_url, "assets/test_image.jpg")
