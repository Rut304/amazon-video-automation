def generate_video_description(products):
    lines = ["Check out the top 3 products featured in this video:\n"]

    for product in products:
        line = f"{product['title']} – ${product['price']} – Rated {product['rating']} stars\n{product['url']}\n"
        lines.append(line)

    lines.append("\nDon't forget to like 👍, comment 💬, and subscribe 🔔 for more reviews!")

    return "\n".join(lines)
