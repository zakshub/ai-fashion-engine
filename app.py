from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO
import numpy as np

app = Flask(__name__)

def get_dominant_color(image_url):

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img = img.resize((80,80))

    pixels = np.array(img).reshape(-1,3)

    avg = pixels.mean(axis=0)

    r,g,b = int(avg[0]),int(avg[1]),int(avg[2])

    return "#{:02x}{:02x}{:02x}".format(r,g,b), (r,g,b)

def detect_brightness(rgb):

    r,g,b = rgb

    brightness = (r+g+b)/3

    if brightness < 120:
        return "dark"
    return "light"

def detect_pattern(image):

    gray = image.convert("L")
    arr = np.array(gray)

    variance = arr.var()

    if variance > 900:
        return "patterned"
    return "solid"

def detect_style(color_rgb):

    r,g,b = color_rgb

    if r < 80 and g < 80 and b < 80:
        return "luxury"

    if r > 180 and g > 180:
        return "casual"

    return "modern"

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    image_url = data.get("image")

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")

    dominant_hex, rgb = get_dominant_color(image_url)

    brightness = detect_brightness(rgb)
    pattern = detect_pattern(img)
    style = detect_style(rgb)

    font_color = "#000000"

    if brightness == "dark":
        font_color = "#ffffff"

    theme = {
        "primary_color": dominant_hex,
        "accent": dominant_hex,
        "background": "#ffffff",
        "font_color": font_color,
        "pattern": pattern,
        "style": style
    }

    return jsonify(theme)

@app.route("/")
def home():
    return "AI Fashion Theme Engine Running"