# -*- coding: utf-8 -*-
import os
import requests
from PIL import Image, ImageOps
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def download_amazon_image(product_url, filename):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(product_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        img_tag = soup.select_one("#imgTagWrapperId img")

        if not img_tag or not img_tag.get("src"):
            raise Exception("No valid image found.")

        image_url = img_tag["src"]
        img_data = requests.get(image_url, headers=headers).content

        os.makedirs("images", exist_ok=True)
        image_path = os.path.join("images", filename)

        with open(image_path, "wb") as f:
            f.write(img_data)

        # Crop or pad to square using Pillow
        img = Image.open(image_path)
        img = ImageOps.fit(img, (max(img.size), max(img.size)), Image.ANTIALIAS)
        img.save(image_path)

        return image_path

    except Exception as e:
        print(f"❌ Failed to download image for {product_url}: {e}")
        return "images/placeholder.jpg"
