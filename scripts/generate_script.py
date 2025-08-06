# -*- coding: utf-8 -*-
def generate_video_script(products):
    for p in products:
        if not all(key in p for key in ['title', 'price', 'rating', 'url']):
            raise ValueError(f"Missing field in product: {p}")

    script = "🔥 Top 3 Amazon Picks Over $40!\n\n"

    for i, product in enumerate(products, start=1):
        script += f"🔹 {i}. {product['title']}\n"
        script += f"💲 Price: ${product['price']}\n"
        script += f"⭐ Rating: {product['rating']} stars\n"
        script += f"👉 Check it out: {product['url']}\n\n"

    script += "💬 Comment below which one you'd choose!\n"
    script += "🔔 Follow for more daily Amazon finds!"
    return script
