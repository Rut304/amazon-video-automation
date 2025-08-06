import os
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def download_amazon_image(product_url, product_title, save_path):
    try:
        # Attempt 1: Get image directly from Amazon page
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        image_tag = soup.find("img", {"class": "a-dynamic-image"})
        if image_tag and image_tag.get("src"):
            img_url = image_tag["src"]
            img_data = requests.get(img_url).content
            with open(save_path, "wb") as handler:
                handler.write(img_data)
            return True
        else:
            print("❌ Amazon image failed: No image found using dynamic-image method.")
    except Exception as e:
        print(f"❌ Amazon image error: {e}")

    # Attempt 2: Fallback to SerpAPI
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_key:
        print("❌ No SERPAPI_API_KEY set. Cannot use fallback.")
        return False

    try:
        print(f"🔍 Searching fallback image with SerpAPI for: {product_title}")
        params = {
            "engine": "google_images",
            "q": product_title,
            "api_key": serpapi_key,
            "num": 1
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        if "images_results" in results and len(results["images_results"]) > 0:
            img_url = results["images_results"][0]["original"]
            img_data = requests.get(img_url).content
            with open(save_path, "wb") as handler:
                handler.write(img_data)
            return True
        else:
            print("❌ SerpAPI image failed: No images found in SerpAPI results.")
    except Exception as e:
        print(f"❌ SerpAPI error: {e}")
    return False
