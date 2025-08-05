import os
import requests
from PIL import Image
from io import BytesIO

def download_amazon_image(image_url, output_path):
    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            raise Exception(f"Image request failed: {response.status_code}")
        
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = img.resize((1080, 1080))
        img.save(output_path)
        print(f"✅ Saved image to {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error downloading image: {e}")
        return None

if __name__ == "__main__":
    test_url = "https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SL1500_.jpg"
    os.makedirs("assets", exist_ok=True)
    download_amazon_image(test_url, "assets/test_image.jpg")
