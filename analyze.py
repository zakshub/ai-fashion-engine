from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():

    colors = [
        "#1A1A1A",
        "#F5E9EF",
        "#2A3D66",
        "#C9A227"
    ]

    result = {
        "primary_color": random.choice(colors),
        "background": "#ffffff",
        "font_color": "#000000",
        "accent": "#C9A227"
    }

    return jsonify(result)