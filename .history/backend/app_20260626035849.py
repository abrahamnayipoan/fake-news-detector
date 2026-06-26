from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import requests
NEWS_API_KEY = "ca9cf9c6c15a48218cb035490a2b2068"

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

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

        if prediction == 1:
            result = "Real News"
        else:
            result = "Fake News"

        return jsonify({
            "prediction": result
        })

    except Exception as e:
        return jsonify({
            "prediction": None,
            "message": "Error occurred while making prediction",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
@app.route("/latest-news")
def latest_news():

    try:

        url = (
            f"https://newsapi.org/v2/top-headlines"
            f"?country=us"
            f"&pageSize=10"
            f"&apiKey={NEWS_API_KEY}"
        )

        response = requests.get(url)
        news_data = response.json()

        results = []

        for article in news_data.get("articles", []):

            title = article.get("title", "")

            if not title:
                continue

            vector = vectorizer.transform([title])

            prediction = model.predict(vector)[0]

            probabilities = model.predict_proba(vector)[0]
            confidence = round(max(probabilities) * 100, 2)

            label = (
                "🟢 Real News"
                if prediction == 1
                else "🔴 Fake News"
            )

            results.append({
                "headline": title,
                "source": article["source"]["name"],
                "prediction": label,
                "confidence": confidence
            })

        return jsonify(results)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })