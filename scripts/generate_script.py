# generate_script.py
import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_video_script(products):
    prompt = f"""Compare the following 3 Amazon products in a short YouTube script:

1. {products[0]['title']} - {products[0]['price']} - Rating: {products[0]['rating']}
2. {products[1]['title']} - {products[1]['price']} - Rating: {products[1]['rating']}
3. {products[2]['title']} - {products[2]['price']} - Rating: {products[2]['rating']}

Make it engaging and under 100 words. End with a recommendation.
"""

    response = client.chat.completions.create(
        model="GPT-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
