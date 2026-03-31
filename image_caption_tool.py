from openai import OpenAI
import base64

client = OpenAI(api_key="PASTE_YOUR_API_KEY_HERE")

image_path = "/Users/mark/path/to/your/image.jpg"
category = "fitness"
idea = "client transformation"

def encode_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(image_path)

prompt = f"""
You are a premium photography content creator.

Create an Instagram caption based on this image.

Category: {category}
Extra direction: {idea}

Write in a calm, confident, premium tone.
Do not be cheesy or overhyped.

Please include:
1. A hook
2. A body
3. A CTA
4. A relevant set of hashtags

Keep it suitable for Instagram.
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]
)

print(response.output_text)