# automate.py
from fetch_products import get_top_amazon_products
from generate_script import generate_video_script
from generate_voice import generate_voice
from create_video import create_video

def main():
    products = get_top_amazon_products()
    script = generate_video_script(products)

    print("\n🎬 Video Script:\n")
    print(script)

    voice_file = generate_voice(script)
    print(f"\n✅ Voice saved to {voice_file}")

    print("\n📦 Products Compared:")
    for p in products:
        print(f"- {p['title']} | {p['price']} | Rating: {p['rating']}")

    video_file = create_video(voice_file)
    print(f"\n🎥 Final video saved to {video_file}")

if __name__ == "__main__":
    main()
