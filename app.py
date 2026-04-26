from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import base64
import os
import json
import uuid
import urllib.request
import urllib.parse
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "/tmp/caption_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
Write in a clean, direct style.
Avoid over-describing or sounding poetic.
Keep language simple, confident, and natural.
Prefer short, punchy sentences. Say less, mean more.
Write like a real photographer, not a marketing agency.
Keep it understated, specific, and believable.
Do not default to sales language unless the image genuinely supports it.

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
- avoid trying to sound impressive; keep it natural and direct
- write like a working UK photographer posting on Instagram
- captions should feel written in the moment, not carefully constructed
- avoid sounding polished or overly considered
- use natural phrasing
- it’s fine if sentences are slightly imperfect
- short is better than complete

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
- only include a CTA if it feels completely natural for the image
- it is better to have no CTA than a forced one

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
- overly flowery or poetic phrasing
- dramatic or exaggerated wording
- long, complex sentences
- starting captions with generic phrases like "this image", "this shot", or "this moment"

Structure guidance:
- strong short hook
- compelling main caption body
- relevant hashtags
- keep sentences short and punchy
- prefer short statements over long paragraphs
- include at least one specific visual detail from the image (e.g. lighting, colour, expression, styling)

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
Write in a clean, direct style.
Avoid over-describing or sounding poetic.
Keep language simple, confident, and natural.
Prefer short, punchy sentences. Say less, mean more.

Create a caption based on this image.

Category: modelling / portrait photography
Audience focus: {subcategory}
Extra direction: {extra_direction}
Selected tone: {selected_tone}
Selected caption goal: {selected_goal}

Brand voice:
- default style is understated, confident, and premium
- calm, observant, and visually aware
- clean, direct, and believable
- written from the photographer’s perspective
- grounded, not hyped
- specific rather than generic
- adjust the wording to reflect the selected tone while staying on-brand
- avoid trying to sound impressive; keep it natural and direct
- write like a working UK photographer posting on Instagram
- captions should feel written in the moment, not carefully constructed
- avoid sounding polished or overly considered
- use natural phrasing
- it’s fine if sentences are slightly imperfect
- short is better than complete

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
- if the goal is authority, position the photographer and subject as credible and visually strong
- if the goal is bookings, encourage an enquiry or booking only in a subtle, natural way
- if the goal is storytelling, make the caption feel personal, specific, and image-led
- if the goal is brand awareness, emphasise consistency, identity, and recognisable style
- respond to the actual image, not a generic model brief
- highlight mood, styling, expression, attitude, colour, light, or presence as appropriate
- keep the caption grounded in what is visible in the image
- avoid assuming this is for an agency, portfolio update, or career pitch unless the image clearly supports that

CTA guidance:
- keep it natural and appropriate for social media
- a CTA is optional, not required
- if used, keep it soft and brief
- do not force a booking angle if the image feels more editorial or observational
- never sound like an advert
- only include a CTA if it feels completely natural for the image
- it is better to have no CTA than a forced one

Avoid:
- mentioning the mindset workshop
- mentioning workshops of any kind
- using the word mindset
- sounding like a clothing brand
- generic motivational phrases
- empty hype
- mentioning audience types outside the selected audience focus
- emojis unless they are genuinely essential
- overly flowery or poetic phrasing
- dramatic or exaggerated wording
- long, complex sentences
- starting captions with generic phrases like "this image", "this shot", or "this moment"
- generic portfolio language
- agency or career talk unless clearly relevant
- empty power words like "impact", "elevate", or "command" unless truly earned
- phrases like "own your story", "command the frame", or "your look demands"

Structure guidance:
- strong short hook
- compelling main caption body
- relevant hashtags
- keep sentences short and punchy
- prefer short statements over long paragraphs
- let the image lead the caption
- make at least one detail feel specific to the photo
- include at least one specific visual detail from the image (e.g. lighting, colour, expression, styling)

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
Write in a clean, direct style.
Avoid over-describing or sounding poetic.
Keep language simple, confident, and natural.
Prefer short, punchy sentences. Say less, mean more.

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
- avoid trying to sound impressive; keep it natural and direct

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
- overly flowery or poetic phrasing
- dramatic or exaggerated wording
- long, complex sentences
- starting captions with generic phrases like "this image", "this shot", or "this moment"

Structure guidance:
- strong short hook
- compelling main caption body
- relevant hashtags
- keep sentences short and punchy
- prefer short statements over long paragraphs
- include at least one specific visual detail from the image (e.g. lighting, colour, expression, styling)

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
    image_url = request.form.get("image_url", "").strip()
    category = request.form.get("category", "").strip().lower()
    subcategory = request.form.get("subcategory", "").strip()
    idea = request.form.get("idea", "").strip()
    tone = request.form.get("tone", "premium").strip().lower()
    goal = request.form.get("goal", "bookings").strip().lower()

    if not image and not image_url:
        return jsonify({"error": "No image provided"}), 400

    if category not in ["fitness", "model", "mindset"]:
        return jsonify({"error": "Invalid category"}), 400

    if image:
        mime_type = image.mimetype or "image/jpeg"
        base64_image = encode_image(image)
    else:
        try:
            parsed_url = urllib.parse.urlparse(image_url)
            filename = os.path.basename(parsed_url.path)

            if "/uploaded-image/" in parsed_url.path and filename:
                file_path = os.path.join(UPLOAD_FOLDER, filename)

                if not os.path.exists(file_path):
                    return jsonify({"error": "Uploaded image file was not found on the server"}), 400

                extension = os.path.splitext(filename)[1].lower()
                if extension in [".jpg", ".jpeg"]:
                    mime_type = "image/jpeg"
                elif extension == ".png":
                    mime_type = "image/png"
                elif extension == ".webp":
                    mime_type = "image/webp"
                else:
                    mime_type = "image/jpeg"

                with open(file_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            else:
                with urllib.request.urlopen(image_url, timeout=20) as image_response:
                    mime_type = image_response.headers.get("Content-Type", "image/jpeg")
                    image_bytes = image_response.read()
                    base64_image = base64.b64encode(image_bytes).decode("utf-8")
        except Exception as e:
            return jsonify({"error": f"Could not retrieve image from image_url: {str(e)}"}), 400

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
- hooks should be short (ideally under 8 words)
- avoid opening with generic phrases like "this image", "this shot", or "this moment"
- prefer a statement, observation, or point of view over scene-setting
- for model captions, avoid generic portfolio or agency language unless clearly supported by the image
- make at least one line feel specific to the uploaded photo rather than interchangeable
"""

    try:
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
    except Exception as e:
        return jsonify({"error": f"OpenAI request failed: {str(e)}"}), 500

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


# Helper function and new route for generating from image path
def build_option_prompt(prompt):
    return prompt + """

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
- hooks should be short (ideally under 8 words)
- avoid opening with generic phrases like "this image", "this shot", or "this moment"
- prefer a statement, observation, or point of view over scene-setting
- for model captions, avoid generic portfolio or agency language unless clearly supported by the image
- make at least one line feel specific to the uploaded photo rather than interchangeable
"""


@app.route("/generate-from-path", methods=["POST"])
def generate_from_path():
    data = request.get_json(silent=True) or {}

    image_path = data.get("image_path", "")
    category = data.get("category", "model").strip().lower()
    subcategory = data.get("subcategory", "").strip()
    idea = data.get("idea", "").strip()
    tone = data.get("tone", "premium").strip().lower()
    goal = data.get("goal", "bookings").strip().lower()

    if not image_path:
        return jsonify({"error": "No image path provided"}), 400

    if not os.path.exists(image_path):
        return jsonify({"error": "Image path does not exist"}), 400

    if category not in ["fitness", "model", "mindset"]:
        return jsonify({"error": "Invalid category"}), 400

    image_extension = os.path.splitext(image_path)[1].lower()
    if image_extension in [".jpg", ".jpeg"]:
        mime_type = "image/jpeg"
    elif image_extension == ".png":
        mime_type = "image/png"
    elif image_extension == ".webp":
        mime_type = "image/webp"
    else:
        return jsonify({"error": "Unsupported image type. Use JPG, PNG, or WEBP."}), 400

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    prompt = build_prompt(category, subcategory, idea, tone, goal)
    option_prompt = build_option_prompt(prompt)

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


@app.route("/image")
def get_image():
    image_path = request.args.get("path")

    if not image_path or not os.path.exists(image_path):
        return "Image not found", 400

    return send_file(image_path)


@app.route("/preview")
def preview():
    image_path = request.args.get("path")

    if not image_path or not os.path.exists(image_path):
        return "Image not found", 400

    return f"""
    <html>
    <head>
        <title>AI Caption Creator</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f7f5ef;
                color: #2e2e2e;
                margin: 0;
                padding: 40px 20px;
            }}
            .card {{
                max-width: 760px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 18px;
                padding: 34px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            }}
            h1 {{
                font-size: 42px;
                margin: 0 0 24px;
                letter-spacing: -1px;
            }}
            .image-preview {{
                width: 180px;
                height: 180px;
                object-fit: cover;
                border-radius: 14px;
                display: block;
                margin-bottom: 26px;
                border: 1px solid #ddd;
            }}
            label {{
                display: block;
                font-size: 20px;
                color: #5b6b82;
                margin: 22px 0 8px;
            }}
            select, textarea {{
                width: 100%;
                font-size: 20px;
                padding: 14px;
                border-radius: 10px;
                border: 1px solid #ddd;
                background: #f1f1f1;
                box-sizing: border-box;
            }}
            textarea {{
                min-height: 90px;
                resize: vertical;
            }}
            button {{
                margin-top: 26px;
                width: 100%;
                padding: 16px;
                font-size: 20px;
                border: none;
                border-radius: 12px;
                background: #2e2e2e;
                color: #ffffff;
                cursor: pointer;
            }}
            .caption-card {{
                margin-top: 22px;
                padding: 18px;
                border-radius: 12px;
                background: #f7f5ef;
                text-align: left;
                white-space: pre-wrap;
            }}
            .caption-card h3 {{
                margin: 0 0 8px;
            }}
            .copy-button {{
                margin-top: 12px;
                width: auto;
                padding: 10px 14px;
                font-size: 14px;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>AI Caption Creator</h1>

            <label>Exported image</label>
            <img class="image-preview" src="/image?path={image_path}" />

            <label>Category</label>
            <select id="category" onchange="updateAudienceOptions()">
                <option value="fitness">Fitness</option>
                <option value="model">Model / Portrait</option>
                <option value="mindset">Mindset</option>
            </select>

            <label>Audience focus</label>
            <select id="subcategory"></select>

            <label>Tone</label>
            <select id="tone">
                <option value="premium">Premium</option>
                <option value="direct">Direct</option>
                <option value="editorial">Editorial</option>
                <option value="commercial">Commercial</option>
                <option value="soft">Soft</option>
            </select>

            <label>Caption goal</label>
            <select id="goal">
                <option value="bookings">Bookings</option>
                <option value="engagement">Engagement</option>
                <option value="authority">Authority</option>
                <option value="storytelling">Storytelling</option>
                <option value="brand awareness">Brand awareness</option>
            </select>

            <label>Extra direction (optional)</label>
            <textarea id="idea" placeholder="e.g. stripped back, commercial, no hard sell"></textarea>

            <button type="button" onclick="generateCaption()">Generate Caption</button>

            <div id="output"></div>
        </div>

        <script>
        const audienceOptions = {{
            fitness: [
                'PTs',
                'Fitness brands / apparel',
                'Gyms / fitness businesses',
                'Athletes / transformation',
                'Fitness professionals',
                'Gym enthusiasts'
            ],
            model: [
                'Editorial',
                'Portfolio',
                'Fashion model',
                'Fitness model',
                'Commercial / brand',
                'Portrait'
            ],
            mindset: [
                'Individuals',
                'Groups',
                'Corporate wellness',
                'Stress / overwhelm',
                'Mindfulness / wellbeing',
                'Creative reflection'
            ]
        }};

        function updateAudienceOptions() {{
            const category = document.getElementById('category').value;
            const subcategory = document.getElementById('subcategory');
            subcategory.innerHTML = '';

            audienceOptions[category].forEach(optionText => {{
                const option = document.createElement('option');
                option.value = optionText;
                option.textContent = optionText;
                subcategory.appendChild(option);
            }});
        }}

        function formatCaption(option, index) {{
            const hook = option.hook || '';
            const main = option.main || '';
            const hashtags = option.hashtags || '';
            const fullCaption = `${{hook}}\n\n${{main}}\n\n${{hashtags}}`.trim();

            return `
                <div class="caption-card">
                    <h3>Option ${{index + 1}}</h3>
                    <div>${{fullCaption}}</div>
                    <button type="button" id="copyButton${{index}}" class="copy-button" onclick="copyCaption(${{index}})">Copy caption</button>
                </div>
            `;
        }}

        let latestCaptions = [];

        function copyCaption(index) {{
            const option = latestCaptions[index];
            const hook = option.hook || '';
            const main = option.main || '';
            const hashtags = option.hashtags || '';
            const fullCaption = `${{hook}}\n\n${{main}}\n\n${{hashtags}}`.trim();

            navigator.clipboard.writeText(fullCaption).then(() => {{
                const button = document.getElementById(`copyButton${{index}}`);
                if (button) {{
                    button.textContent = 'Copied';
                    setTimeout(() => {{
                        button.textContent = 'Copy caption';
                    }}, 2000);
                }}
            }});
        }}

        function generateCaption() {{
            document.getElementById('output').innerHTML = '<div class="caption-card">Generating captions...</div>';

            fetch('/generate-from-path', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    image_path: "{image_path}",
                    category: document.getElementById('category').value,
                    subcategory: document.getElementById('subcategory').value,
                    tone: document.getElementById('tone').value,
                    goal: document.getElementById('goal').value,
                    idea: document.getElementById('idea').value
                }})
            }})
            .then(res => res.json())
            .then(data => {{
                latestCaptions = data.captions || [];
                if (latestCaptions.length === 0) {{
                    document.getElementById('output').innerHTML = '<div class="caption-card">No captions were returned. Try generating again.</div>';
                }} else {{
                    document.getElementById('output').innerHTML = latestCaptions.map(formatCaption).join('');
                }}
            }});
        }}

        updateAudienceOptions();
        </script>
    </body>
    </html>
    """


@app.route("/uploaded-image/<filename>")
def uploaded_image(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return "Image not found", 404

    return send_file(file_path)



@app.route("/upload-preview", methods=["POST"])
def upload_preview():
    image = request.files.get("image")

    if not image:
        return jsonify({"error": "No image uploaded"}), 400

    original_filename = secure_filename(image.filename or "upload.jpg")
    extension = os.path.splitext(original_filename)[1].lower() or ".jpg"

    if extension not in [".jpg", ".jpeg", ".png", ".webp"]:
        return jsonify({"error": "Unsupported image type"}), 400

    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(file_path)

    image_url = f"{request.host_url.rstrip('/')}/uploaded-image/{filename}"
    page_url = f"https://msands.photography/caption-generator?image_url={image_url}"

    return jsonify({
        "image_url": image_url,
        "page_url": page_url
    })


# New upload-base64 route
@app.route("/upload-base64", methods=["POST"])
def upload_base64():
    data = request.get_json(silent=True) or {}
    image_base64 = data.get("image", "")

    if not image_base64:
        return jsonify({"error": "No image provided"}), 400

    try:
        if "," in image_base64:
            image_base64 = image_base64.split(",")[-1]

        image_data = base64.b64decode(image_base64)
    except Exception:
        return jsonify({"error": "Invalid base64 image"}), 400

    filename = f"{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as f:
        f.write(image_data)

    image_url = f"{request.host_url.rstrip('/')}/uploaded-image/{filename}"
    page_url = f"https://msands.photography/caption-generator?image_url={image_url}"

    return jsonify({
        "image_url": image_url,
        "page_url": page_url
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
