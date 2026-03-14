from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

def get_dominant_color(image_url):

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    img = img.resize((50,50))

    pixels = list(img.getdata())

    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)

    return "#{:02x}{:02x}{:02x}".format(r,g,b)


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    image_url = data.get("image")

    dominant_color = get_dominant_color(image_url)

    brightness = "light"

    r = int(dominant_color[1:3],16)
    g = int(dominant_color[3:5],16)
    b = int(dominant_color[5:7],16)

    if (r+g+b)/3 < 120:
        brightness = "dark"

    font_color = "#000000"

    if brightness == "dark":
        font_color = "#ffffff"

    result = {
        "primary_color": dominant_color,
        "background": "#ffffff",
        "font_color": font_color,
        "accent": dominant_color
    }

    return jsonify(result)


@app.route("/")
def home():
    return "AI Fashion Theme Engine Running"