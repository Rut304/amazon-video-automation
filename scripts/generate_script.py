def generate_video_script(products):
    hook = (
        "[Hook] \"Looking for the perfect gaming weapon to level up your skills? "
        "Let's dive into a quick comparison of the top 3 gaming mice that are dominating Amazon right now!\"\n"
    )

    body_lines = []
    for product in products:
        line = (
            f"{product['name']} - ${product['price']} - Rating: {product['rating']}"
        )
        body_lines.append(line)

    body = "\n".join([f"[Body] \"{line}\"" for line in body_lines])

    call_to_action = (
        "\n[Call-to-action] \"So, whether you're into precision, speed, or wireless freedom, "
        "there's something for everyone! Check the links in the description to explore these "
        "gaming mice and see which one ticks all your boxes. Game on!\""
    )

    return f"{hook}\n{body}{call_to_action}"
