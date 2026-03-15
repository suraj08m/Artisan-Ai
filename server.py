from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from market_analysis import analyze_market
from nova_engine import generate_advice

app = Flask(__name__, static_folder="static")
CORS(app)


# Serve frontend
@app.route("/")
def index():
    return send_from_directory("static", "artisanai.html")


# API route
@app.route("/analyze", methods=["POST"])
def analyze():
    try:

        data = request.get_json()

        product = data.get("product", "")
        material = data.get("material", "")
        region = data.get("region", "")

        # Market analytics
        market = analyze_market(product)

        # AI advice
        advice = generate_advice(
            product,
            region,
            material,
            market["best_platform"],
            market["suggested_price"],
            market["demand"],
            market["competition"]
        )

        return jsonify({
            "platform": market["best_platform"],
            "price": market["suggested_price"],
            "profit": market["estimated_profit"],
            "demand": market["demand"],
            "competition": market["competition"],
            "market_fit": market["market_fit"],
            "advice": advice
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)