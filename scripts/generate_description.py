def generate_video_description(products):
    lines = ["Here are the top 3 gaming mice on Amazon:\n"]
    for product in products:
        lines.append(f"- {product['title']}: ${product['price']} ({product['rating']}⭐)")
        lines.append(f"  Buy now: {product['url']}\n")
    return "\n".join(lines)
