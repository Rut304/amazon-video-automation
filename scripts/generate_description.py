# scripts/generate_description.py

def generate_video_description(products, affiliate_tag="1705d0-20"):
    # Sort products from highest to lowest rating
    sorted_products = sorted(products, key=lambda p: -p['rating'])

    lines = []
    for i, product in enumerate(sorted_products, start=1):
        title = product['title']
        price = product['price']
        rating = product['rating']
        asin = product['asin']

        url = f"https://www.amazon.com/dp/{asin}?tag={affiliate_tag}"
        line = f"{i}) {title} - {price} - ⭐ {rating}\n👉 {url}"
        lines.append(line)

    return "\n\n".join(lines)
