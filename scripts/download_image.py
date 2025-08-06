import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

def download_amazon_image(url: str, title: str, output_path: str) -> bool:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        image_tag = soup.find("img", {"id": "landingImage"}) or soup.find("img", {"data-old-hires": True})

        if image_tag and image_tag.get("src"):
            image_url = image_tag["src"]
            img_data = requests.get(image_url).content
            with open(output_path, "wb") as f:
                f.write(img_data)
            return True
        else:
            print("❌ Amazon image failed: No image found using dynamic-image method.")
            return download_fallback_image(title, output_path)
    except Exception as e:
        print(f"❌ Error downloading image: {e}")
        return download_fallback_image(title, output_path)

def download_fallback_image(title: str, output_path: str) -> bool:
    serp_api_key = os.getenv("SERPAPI_API_KEY")
    if not serp_api_key:
        print("❌ No SERPAPI_API_KEY set. Cannot use fallback.")
        return False

    print(f"🔍 Searching fallback image with SerpAPI for: {title}")
    try:
        search = GoogleSearch({
            "q": title,
            "tbm": "isch",
            "api_key": serp_api_key
        })
        results = search.get_dict()
        images = results.get("images_results", [])
        if not images:
            print("❌ SerpAPI image failed: No images found in SerpAPI results.")
            return False

        img_url = images[0]["original"]
        img_data = requests.get(img_url).content
        with open(output_path, "wb") as f:
            f.write(img_data)
        return True
    except Exception as e:
        print(f"❌ Fallback image error: {e}")
        return False
