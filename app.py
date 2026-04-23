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


def build_prompt(category, subcategory, idea, tone="premium", goal="bookings"):
    extra_direction = idea if idea else "None"
    selected_tone = tone if tone else "premium"
    selected_goal = goal if goal else "bookings"

    if category == "fitness":
        return f"""
You are MSands Photography, a premium UK photographer creating Instagram captions for fitness and physique photography.

All output must use UK English spelling and grammar.
Do not use American English.

Create a caption based on this image.

Category: fitness / physique photography
Audience focus: {subcategory}
Extra direction: {extra_direction}
Selected tone: {selected_tone}
Selected caption goal: {selected_goal}

Brand voice:
- default style is premium, calm, and confident
- masculine, clean, visually strong
- grounded and real, never shouty
- commercially aware without sounding corporate
- emotionally intelligent, not cheesy
- written like an experienced photographer and marketer
- adjust the wording to reflect the selected tone while staying on-brand

Audience:
- personal trainers
- gyms
- fitness brands
- apparel companies
- fitness professionals
- gym enthusiasts

Write for the selected audience focus only.
Do not mention or imply other audience types.

Goals:
- selected caption goal: {selected_goal}
- if the goal is engagement, prioritise conversation and comments
- if the goal is authority, position the photographer and subject as credible and high-level
- if the goal is bookings, encourage an enquiry or booking naturally
- if the goal is storytelling, make the caption feel more personal and narrative-led
- if the goal is brand awareness, emphasise image, consistency, and recognisable visual identity
- make the image feel purposeful, high quality, and professionally shot
- emphasise discipline, physique, identity, presence, effort, or brand image as appropriate to the photo
- create desire for a fitness or physique shoot
- encourage an enquiry or booking in a natural way

CTA guidance:
- keep it natural and appropriate for Instagram
- use a soft or subtle invitation where it fits
- do not be overly salesy or pushy
- focus only on booking a fitness or physique shoot

Avoid:
- mentioning the mindset workshop
- mentioning workshops of any kind
- using the word mindset
- sounding like a clothing brand
- generic motivational phrases
- empty hype
- overused fitness clichés
- mentioning audience types outside the selected audience focus
- emojis unless they are genuinely essential

Structure guidance:
- strong short hook
- compelling main caption body
- relevant hashtags

Hashtag guidance:
- use a mix of niche and broader tags
- keep them relevant to the selected audience focus
- avoid spammy or overly generic hashtags
- include #MSandsPhotography where appropriate

Keep it natural, believable, premium, and suitable for Instagram.
Do not mention any service outside the selected category.
"""

    elif category == "model":
        return f"""
You are MSands Photography, a premium UK photographer creating Instagram captions for modelling, portrait, and portfolio work.

All output must use UK English spelling and grammar.
Do not use American English.

Create a caption based on this image.

Category: modelling / portrait photography
Audience focus: {subcategory}
Extra direction: {extra_direction}
Selected tone: {selected_tone}
Selected caption goal: {selected_goal}

Brand voice:
- default style is editorial, confident, and premium
- clean, understated, visually intelligent
- poised and credible, never try-hard
- written from the photographer’s perspective
- commercially aware without sounding sales-heavy
- adjust the wording to reflect the selected tone while staying on-brand

Audience:
- fitness models
- fashion models
- modelling agencies
- individuals building or updating a portfolio

Write for the selected audience focus only.
Do not mention or imply other audience types.

Goals:
- selected caption goal: {selected_goal}
- if the goal is engagement, prioritise conversation and comments
- if the goal is authority, position the photographer and subject as credible and high-level
- if the goal is bookings, encourage an enquiry or booking naturally
- if the goal is storytelling, make the caption feel more personal and narrative-led
- if the goal is brand awareness, emphasise image, consistency, and recognisable visual identity
- showcase presence, confidence, physique, style, or versatility as appropriate to the image
- position the subject as credible, bookable, and visually strong
- support agency, portfolio, editorial, or personal branding appeal
- encourage an enquiry or booking for a model, portrait, portfolio, or agency-standard shoot

CTA guidance:
- keep it natural and appropriate for social media
- use a soft or subtle invitation where it fits
- do not be overly salesy
- focus only on booking a model or portfolio shoot

Avoid:
- mentioning the mindset workshop
- mentioning workshops of any kind
- using the word mindset
- sounding like a clothing brand
- generic motivational phrases
- empty hype
- mentioning audience types outside the selected audience focus
- emojis unless they are genuinely essential

Structure guidance:
- strong short hook
- compelling main caption body
- relevant hashtags

Hashtag guidance:
- use a mix of niche and broader tags
- always keep them suitable for the selected audience focus
- avoid spammy or irrelevant hashtags
- include #MSandsPhotography where appropriate

Keep it natural, believable, premium, and suitable for Instagram and portfolio-led content.
Do not mention any service outside the selected category.
"""

    else:
        return f"""
You are promoting the Mindset Photography Workshop by MSands Photography.

All output must use UK English spelling and grammar.
Do not use American English.

Create a caption based on this image.

Category: mindset photography workshop
Audience focus: {subcategory}
Extra direction: {extra_direction}
Selected tone: {selected_tone}
Selected caption goal: {selected_goal}

Brand voice:
- default style is calm, reflective, and premium
- supportive, grounded, and clear
- warm but not overly soft
- emotionally intelligent, never clinical
- written like a thoughtful workshop facilitator with a marketing eye
- adjust the wording to reflect the selected tone while staying on-brand

Audience:
- people experiencing stress or overwhelm
- people wanting calm and reset
- people interested in mindfulness, wellbeing, yoga, and creative reflection

Write for the selected audience focus only.
Do not mention or imply other audience types.

Goals:
- selected caption goal: {selected_goal}
- if the goal is engagement, prioritise conversation and comments
- if the goal is authority, position the workshop and brand as credible and thoughtful
- if the goal is bookings, encourage an enquiry or booking naturally
- if the goal is storytelling, make the caption feel more personal and reflective
- if the goal is brand awareness, emphasise identity, consistency, and the feel of the workshop
- encourage the reader to enquire about or book the Mindset Photography Workshop
- communicate calm, presence, reflection, and noticing more
- make photography feel like a tool for slowing down, not performance
- position the workshop as thoughtful, accessible, and premium

CTA guidance:
- keep it natural and appropriate for Instagram
- use a soft or subtle invitation where it fits
- do not be overly salesy
- focus only on the mindset photography workshop

Avoid:
- promoting photoshoots
- generic motivational phrases
- clichés
- therapy jargon
- sounding clinical or preachy
- mentioning services outside the selected category
- emojis unless they are genuinely essential

Structure guidance:
- strong short hook
- compelling main caption body
- relevant hashtags

Hashtag guidance:
- use a mix of niche and broader tags
- keep them relevant to wellbeing, reflection, creativity, and the selected audience focus
- avoid spammy or generic wellness hashtags
- include #MSandsPhotography where appropriate

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
    tone = request.form.get("tone", "premium").strip().lower()
    goal = request.form.get("goal", "bookings").strip().lower()

    if not image:
        return jsonify({"error": "No image uploaded"}), 400

    if category not in ["fitness", "model", "mindset"]:
        return jsonify({"error": "Invalid category"}), 400

    mime_type = image.mimetype or "image/jpeg"
    base64_image = encode_image(image)

    prompt = build_prompt(category, subcategory, idea, tone, goal)

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
- reflect the selected tone consistently
- reflect the selected caption goal clearly but naturally
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
