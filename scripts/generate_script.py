# scripts/generate_script.py

import os
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_video_script(products):
    prompt = f"""
You're a YouTube video script writer. Write a 30-second engaging script comparing these 3 Amazon products. Start with a hook. End with a call-to-action to check links in the description.

Products:
{products[0]['title']} - {products[0]['price']} - Rating: {products[0]['rating']}
{products[1]['title']} - {products[1]['price']} - Rating: {products[1]['rating']}
{products[2]['title']} - {products[2]['price']} - Rating: {products[2]['rating']}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
