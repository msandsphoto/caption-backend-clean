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


def encode_image(file_storage):
    return base64.b64encode(file_storage.read()).decode("utf-8")


def build_prompt(category, subcategory, idea):
    if category == "fitness":
        return f"""
You are a professional photographer creating Instagram captions for fitness and physique photography.

All output must use UK English spelling and grammar.
Do not use American English.

Create a caption based on this image.

Category: fitness / physique photography
Audience focus: {subcategory}
Extra direction: {idea if idea else "None"}

Audience:
- personal trainers
- gyms
- fitness brands
- apparel companies
- fitness professionals
- gym enthusiasts

Style:
- confident, calm, premium
- grounded and real
- commercially aware
- written from a marketing perspective focused on driving bookings
- focused on physique, discipline, brand presence, visual identity, and impact
- tailored to appeal only to the selected audience focus

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
- mentioning audience types outside the selected audience focus

Structure guidance:
- strong short hook
- compelling main caption body
- relevant hashtags

Keep it natural, believable, premium, and suitable for Instagram.
Do not mention any service outside the selected category.
"""

    elif category == "model":
        return f"""
You are a professional photographer creating Instagram captions for modelling and portfolio work.

All output must use UK English spelling and grammar.
Do not use American English.

Create a caption based on this image.

Category: modelling / portrait photography
Audience focus: {subcategory}
Extra direction: {idea if idea else "None"}

Audience:
- fitness models
- fashion models
- modelling agencies
- individuals building or updating a portfolio

Style:
- editorial and confident
- clean and premium
- not overly sales-focused
- focused on image quality, physique, presence, confidence, and visual impact
- written from the photographer’s perspective
- tailored only to the selected audience focus

Goal:
- showcase presence, confidence, physique, and aesthetic
- attract agency attention or portfolio bookings
- position the subject as credible and commercially usable
- encourage a booking for a model, portrait, portfolio, or agency-standard shoot

CTA:
- clear and direct
- encourage DM or enquiry
- focused only on booking a model or portfolio shoot

Avoid:
- mentioning the mindset workshop
- mentioning workshops of any kind
- using the word mindset
- sounding like a clothing brand
- clichés or generic motivational phrases
- mentioning audience types outside the selected audience focus

Structure guidance:
- strong short hook
- compelling main caption body
- relevant hashtags

Hashtag guidance:
- use a mix of niche and broader tags
- always keep them suitable for the selected audience focus
- include #MSandsPhotography where appropriate

Keep it natural, believable, premium, and suitable for Instagram and portfolio-led content.
Do not mention any service outside the selected category.
"""

    else:
        return f"""
You are promoting a Mindset Photography Workshop.

All output must use UK English spelling and grammar.
Do not use American English.

Create a caption based on this image.

Category: mindset photography workshop
Audience focus: {subcategory}
Extra direction: {idea if idea else "None"}

Audience:
- people experiencing stress or overwhelm
- people wanting calm and reset
- people interested in mindfulness, wellbeing, yoga, and creative reflection

Style:
- calm, reflective, premium
- grounded and real
- focused on slowing down, noticing more, and feeling present
- written from a marketing perspective focused on driving workshop enquiries
- tailored only to the selected audience focus

Goal:
- encourage the reader to enquire about or book the mindset photography workshop

CTA:
- clear and direct
- encourage DM or enquiry
- focused only on the workshop

Avoid:
- promoting photoshoots
- generic motivational phrases
- clichés
- mentioning services outside the selected category

Structure guidance:
- strong short hook
- compelling main caption body
- relevant hashtags

Keep it natural, believable, calm, and suitable for Instagram.
Do not mention any service outside the selected category.
"""


@app.route("/", methods=["GET"])
def home():
    return "Caption backend is running"


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
- each option must be clearly different in wording and angle
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
        captions = [
            {
                "hook": "",
                "main": result_text,
                "hashtags": ""
            }
        ]

    return jsonify({"captions": captions})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)