import os
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def download_amazon_image(url, title, save_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        img_tag = soup.select_one("img[data-a-dynamic-image]")
        if img_tag:
            dynamic_image = img_tag["data-a-dynamic-image"]
            image_url = list(eval(dynamic_image).keys())[0]
            image_data = requests.get(image_url).content
            with open(save_path, "wb") as f:
                f.write(image_data)
            return True
        else:
            print("❌ Amazon image failed: No image found using dynamic-image method.")
    except Exception as e:
        print(f"❌ Amazon image error: {e}")

    # Fallback: use SerpAPI
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_key:
        print("❌ No SERPAPI_API_KEY set. Cannot use fallback.")
        return False

    try:
        print(f"🔍 Searching fallback image with SerpAPI for: {title}")
        search = GoogleSearch({
            "q": title,
            "tbm": "isch",
            "api_key": serpapi_key
        })
        results = search.get_dict()
        if "images_results" in results and results["images_results"]:
            image_url = results["images_results"][0]["original"]
            image_data = requests.get(image_url).content
            with open(save_path, "wb") as f:
                f.write(image_data)
            return True
        else:
            print("❌ SerpAPI image failed: No images found in SerpAPI results.")
            return False
    except Exception as e:
        print(f"❌ SerpAPI fallback failed: {e}")
        return False
