from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import requests

# ======================
# APP SETUP
# ======================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ======================
# LOAD MODEL
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("✓ Model loaded successfully")
    print("✓ Vectorizer loaded successfully")
except Exception as e:
    print("Model loading failed:", e)
    raise

# ======================
# HOME ROUTE
# ======================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Fake News Detection API is running"
    })

# ======================
# PREDICT ROUTE
# ======================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json() or {}
        text = data.get("text", "").strip()

        if not text:
            return jsonify({
                "error": "No text provided"
            }), 400

        vector = vectorizer.transform([text])
        prediction = model.predict(vector)[0]

        label = "Likely Real News" if prediction == 1 else "Likely Fake News"

        return jsonify({
            "prediction": label
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# ======================
# NEWS API ROUTE
# ======================
NEWS_API_KEY = "YOUR_NEWSAPI_KEY_HERE"

@app.route("/latest-news", methods=["GET"])
def latest_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={NEWS_API_KEY}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        articles = response.json().get("articles", [])

        results = []

        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            content = f"{title} {description}".strip()

            if not content:
                continue

            vector = vectorizer.transform([content])
            prediction = model.predict(vector)[0]

            label = "Real News" if prediction == 1 else "Fake News"

            confidence = 0
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(vector)[0]
                confidence = round(max(probabilities) * 100, 2)

            results.append({
                "headline": title,
                "description": description,
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url"),
                "image": article.get("urlToImage"),
                "publishedAt": article.get("publishedAt"),
                "prediction": label,
                "confidence": confidence
            })

        return jsonify({"articles": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    print("Server running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)