from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import base64
import os
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(category, subcategory, idea):
    if category == "fitness":
        return f"""
You are a professional photographer creating Instagram captions for your fitness and physique photography work.

Create a caption based on this image.

Category: fitness / physique photography
Audience focus: {subcategory}
Extra direction: {idea if idea else "None"}

Style:
- confident, calm, premium
- grounded and real
- written from a marketing perspective focused on driving bookings from gym owners, apparel brands, fitness companies, PTs, and gym enthusiasts
- focused on physique, visual identity, brand presence, discipline, and commercial impact
- tailored to appeal to {subcategory}
- positions the photographer as experienced and in control of the shoot

Goal:
- encourage the reader to book a fitness or physique photoshoot

CTA:
- clear and direct
- encourage DM or enquiry
- focused only on booking a fitness or physique shoot

Avoid:
- mentioning the mindset workshop
- mentioning workshops of any kind
- using the word mindset
- sounding like a clothing brand
- clichés or generic motivational phrases
- only refer to the selected audience focus ({subcategory})
- do not mention other audience types

Structure:
1. Short strong hook
2. Body focused on progress, discipline, physique, or presence
3. Clear CTA to book a shoot
4. 10 to 15 relevant hashtags

Keep it natural and believable.
Do not mention any service outside the selected category.
"""

    elif category == "model":
        return f"""
You are a professional photographer creating Instagram captions for your model and portrait photography work.

Create a caption based on this image.

Category: model / portrait photography
Audience focus: {subcategory}
Extra direction: {idea if idea else "None"}

Style:
- confident, calm, premium
- grounded and real
- written from a marketing perspective focused on driving bookings
- focused on presence, confidence, style, energy, and visual impact
- written from the photographer’s perspective for models, designers, and brands looking for strong editorial-style images
- tailored to appeal to {subcategory}
- aligned with what agencies and casting directors expect to see

Goal:
- encourage the reader to book a model, portrait, editorial, or portfolio photoshoot

CTA:
- clear and direct
- encourage DM or enquiry
- focused only on booking a model, portrait, editorial, or portfolio shoot

Avoid:
- mentioning the mindset workshop
- mentioning workshops of any kind
- using the word mindset
- sounding like a clothing brand
- clichés or generic motivational phrases
- only refer to the selected audience focus ({subcategory})
- do not mention other audience types

Structure:
1. Short strong hook
2. Body focused on confidence, presence, editorial feel, style, or energy in the image
3. Clear CTA to book a shoot
4. 10 to 15 relevant hashtags

Hashtag guidance:
- include a mix of:
  - niche hashtags (modeldigitals, portfolioshoot)
  - broader hashtags (portraitphotography)
  - branded hashtag (#MSandsPhotography)

Keep it natural and believable.
Do not mention any service outside the selected category.
"""

    else:
        return f"""
You are promoting your Mindset Photography Workshop.

Create a caption based on this image.

Category: mindset photography workshop
Audience focus: {subcategory}
Extra direction: {idea if idea else "None"}

Style:
- calm, reflective, premium
- grounded and real
- focused on slowing down, noticing more, and feeling present
- written from a marketing perspective focused on driving workshop enquiries
- aimed at people interested in mindfulness, yoga, wellbeing, and creative ways to manage stress or anxiety
- tailored to people experiencing {subcategory}

Goal:
- encourage the reader to enquire about or book the mindset photography workshop

CTA:
- clear and direct
- encourage DM or enquiry
- focused only on the mindset workshop

Avoid:
- promoting photoshoots
- generic motivational phrases
- clichés

Structure:
1. Short strong hook
2. Body focused on calm, awareness, creativity, or presence
3. Clear CTA for the workshop
4. 10 to 15 relevant hashtags

Keep it natural and believable.
Do not mention any service outside the selected category.
"""


def encode_image(file_storage):
    return base64.b64encode(file_storage.read()).decode("utf-8")


@app.route("/generate", methods=["POST"])
def generate():
    image = request.files.get("image")
    category = request.form.get("category", "").strip().lower()
    subcategory = request.form.get("subcategory", "").strip()
    idea = request.form.get("idea", "").strip()

    if not image:
        return jsonify({"error": "No image uploaded"}), 400

    if category not in ["fitness", "model", "mindset"]:
        return jsonify({"error": "Invalid category"}), 400

    mime_type = image.mimetype or "image/jpeg"
    base64_image = encode_image(image)

    prompt = build_prompt(category, subcategory, idea)

    option_prompt = prompt + """

    Generate exactly 3 distinct caption options.

    Return the result as valid JSON only, in this format:

    {
      "captions": [
        {
          "hook": "short opening line",
          "main": "main caption body",
          "hashtags": "#tag1 #tag2 #tag3"
        },
        {
          "hook": "short opening line",
          "main": "main caption body",
          "hashtags": "#tag1 #tag2 #tag3"
        },
        {
          "hook": "short opening line",
          "main": "main caption body",
          "hashtags": "#tag1 #tag2 #tag3"
        }
      ]
    }

    Rules:
    - return only JSON
    - no markdown
    - no labels like Option 1
    - no extra commentary
    - each option must contain exactly these 3 keys: hook, main, hashtags
    - hashtags must be returned as one single string
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": option_prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{base64_image}"
                    }
                ]
            }
        ]
    )

    result_text = response.output_text.strip()

    try:
        result_json = json.loads(result_text)
        captions = result_json.get("captions", [])
    except json.JSONDecodeError:
        captions = [result_text]

    return jsonify({"captions": captions})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
