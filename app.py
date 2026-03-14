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

    color = get_dominant_color(image_url)

    result = {
        "primary_color": color,
        "background": "#ffffff",
        "font_color": "#000000",
        "accent": color
    }

    return jsonify(result)


@app.route("/")
def home():
    return "AI Fashion Theme Engine Running"