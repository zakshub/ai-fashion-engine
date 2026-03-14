from flask import Flask, request, jsonify
import google.generativeai as genai
import json

app = Flask(__name__)

# GEMINI API KEY
genai.configure(api_key="AIzaSyBeK-XrNL8gkpDxbRyVczonSqf8gv2UnsI")

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    image_url = data.get("image")

    prompt = f"""
Analyze this clothing product image.

Return ONLY JSON.

Fields required:
dominant_color
pattern
fabric
style
luxury_level
occasion

Example JSON:
{{
"dominant_color":"#000000",
"pattern":"floral",
"fabric":"chiffon",
"style":"luxury",
"luxury_level":"high",
"occasion":"eveningwear"
}}
"""

    response = model.generate_content([
        prompt,
        image_url
    ])

    text = response.text

    try:
        ai_data = json.loads(text)
    except:
        ai_data = {
            "dominant_color":"#000000",
            "pattern":"solid",
            "fabric":"unknown",
            "style":"modern",
            "luxury_level":"medium",
            "occasion":"casual"
        }

    # THEME ENGINE RULES

    primary_color = ai_data["dominant_color"]
    font_color = "#000000"
    background = "#ffffff"

    if ai_data["style"] == "luxury":
        font_color = "#ffffff"

    if ai_data["pattern"] == "floral":
        background = "#FCEFF5"

    result = {
        "primary_color": primary_color,
        "accent": primary_color,
        "background": background,
        "font_color": font_color,
        "pattern": ai_data["pattern"],
        "style": ai_data["style"],
        "fabric": ai_data["fabric"]
    }

    return jsonify(result)


@app.route("/")
def home():
    return "AI Fashion Engine Running"