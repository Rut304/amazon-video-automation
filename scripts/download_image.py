# -*- coding: utf-8 -*-
import os
import re
import requests
from PIL import Image, ImageOps
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_KEY")

def crop_to_square(image_path):
    img = Image.open(image_path)
    img = ImageOps.fit(img, (max(img.size), max(img.size)), Image.ANTIALIAS)
    img.save(image_path)

def extract_asin(url):
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    return match.group(1) if match else None

def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        with open(save_path, "wb") as f:
            f.write(response.content)
        crop_to_square(save_path)
        return True
    except Exception as e:
        print(f"❌ Failed to download image from {url}: {e}")
        return False

def get_image_from_amazon(product_url, save_path):
    try:
        response = requests.get(product_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        selectors = [
            "#imgTagWrapperId img",
            "#landingImage",
            "img[data-old-hires]",
            "img.a-dynamic-image"
        ]

        for selector in selectors:
            img_tag = soup.select_one(selector)
            if img_tag:
                img_url = img_tag.get("src") or img_tag.get("data-old-hires")
                if img_url:
                    print(f"✅ Amazon image found using selector '{selector}'")
                    if download_image(img_url, save_path):
                        return True
        return False
    except Exception as e:
        print(f"❌ Error scraping Amazon page: {e}")
        return False

def get_image_from_cdn(asin, save_path):
    try:
        cdn_url = f"https://m.media-amazon.com/images/I/{asin}.jpg"
        print(f"➡️ Trying CDN image: {cdn_url}")
        return download_image(cdn_url, save_path)
    except:
        return False

def get_image_from_serpapi(query, save_path):
    try:
        print(f"🔍 Searching SerpAPI for: {query}")
        search_url = "https://serpapi.com/search"
        params = {
            "q": query,
            "tbm": "isch",
            "api_key": SERP_API_KEY
        }
        response = requests.get(search_url, params=params, timeout=10)
        results = response.json()
        if "images_results" in results:
            for result in results["images_results"]:
                if download_image(result["original"], save_path):
                    print("✅ Image found via SerpAPI.")
                    return True
    except Exception as e:
        print(f"❌ SerpAPI image fetch failed: {e}")
    return False

def download_amazon_image(product_url, filename):
    os.makedirs("images", exist_ok=True)
    image_path = os.path.join("images", filename)
    asin = extract_asin(product_url)

    print(f"📥 Downloading image for: {product_url}")

    if get_image_from_amazon(product_url, image_path):
        return image_path

    if asin and get_image_from_cdn(asin, image_path):
        return image_path

    title_query = asin if not asin else f"amazon {asin}"
    if get_image_from_serpapi(title_query, image_path):
        return image_path

    raise FileNotFoundError("❌ No valid product image found from any method.")
