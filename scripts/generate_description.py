# scripts/generate_description.py

AFFILIATE_TAG = "1705d0-20"

def generate_description(products):
    lines = ["🔥 Top 3 Amazon Picks:"]
    for i, product in enumerate(products, 1):
        title = product["title"]
        price = product["price"]
        rating = product["rating"]
        asin = product["asin"]
        url = f"https://www.amazon.com/dp/{asin}?tag={AFFILIATE_TAG}"

        lines.append(f"{i}) {title} - {price} ⭐ {rating}")
        lines.append(f"👉 {url}")
        lines.append("")  # Blank line between products

    lines.append("Disclosure: These are affiliate links. I may earn a small commission at no cost to you.")
    return "\n".join(lines)
