# automate.py
from generate_voice import generate_voice
from fetch_products import get_top_amazon_products
from generate_script import generate_video_script

def main():
    products = get_top_amazon_products()
    script = generate_video_script(products)
    
    print("\n🎬 Video Script:\n")
    print(script)
    voice_file = generate_voice(script)
print(f"✅ Voice saved to {voice_file}")

    
    print("\n📦 Products Compared:")
    for p in products:
        print(f"- {p['title']} | {p['price']} | Rating: {p['rating']}")

if __name__ == "__main__":
    main()
