from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

NEWS_API_KEY = "ca9cf9c6c15a48218cb035490a2b2068"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


@app.route("/")
def home():
    return jsonify({
        "message": "Fake News Detection API is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text", "").strip()

        if not text:
            return jsonify({
                "prediction": None,
                "message": "No text provided"
            }), 400

        vector = vectorizer.transform([text])
        prediction = model.predict(vector)[0]

        result = "Likely Real News" if prediction == 1 else "Likely Fake News"

        return jsonify({
            "prediction": result
        })

    except Exception as e:
        return jsonify({
            "prediction": None,
            "message": "Error occurred while making prediction",
            "error": str(e)
        }), 500


@app.route("/latest-news", methods=["GET"])
def latest_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={NEWS_API_KEY}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        news_data = response.json()
        articles = news_data.get("articles", [])

        results = []

        for article in articles:
            title = article.get("title") or ""
            description = article.get("description") or ""

            content = f"{title} {description}".strip()

            if not content:
                continue

            vector = vectorizer.transform([content])
            prediction = model.predict(vector)[0]

            probabilities = model.predict_proba(vector)[0]
            confidence = round(max(probabilities) * 100, 2)

            label = "Real News" if prediction == 1 else "Fake News"
            source = article.get("source") or {}

            results.append({
    "headline": title,
    "description": description,
    "source": source.get("name", "Unknown source"),
    "url": article.get("url"),
    "image": article.get("urlToImage"),
    "publishedAt": article.get("publishedAt"),
    "prediction": label,
    "confidence": confidence
})

        return jsonify({
            "articles": results
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5000")
    print("Make sure the frontend is accessing this URL...")
    app.run(host="127.0.0.1", port=5000, debug=True)
