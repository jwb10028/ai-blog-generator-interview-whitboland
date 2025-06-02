# ai_generator.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# You can change this to gpt-4 if needed
MODEL = "gpt-3.5-turbo"


def generate_blog_post(keyword, seo_data):
    search_volume = seo_data["search_volume"]
    difficulty = seo_data["keyword_difficulty"]
    cpc = seo_data["avg_cpc"]

    prompt = f"""
You are an SEO copywriter. Write a well-structured blog post in Markdown about "{keyword}".

Include:
- An engaging introduction
- A subheading on why {keyword} is trending (mention the search volume: {search_volume})
- A subheading on challenges or competition (mention keyword difficulty: {difficulty})
- A section recommending 2–3 products or services, using affiliate link placeholders (like {{AFF_LINK_1}})
- A conclusion with a call to action

Ensure the tone is informative but casual. Length: ~500 words.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful AI content writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    # Replace affiliate link placeholders with dummy URLs
    for i in range(1, 4):
        content = content.replace(f"{{AFF_LINK_{i}}}", f"https://example.com/product{i}")

    return content
