from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

# Create Flask app
app = Flask(__name__)
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS (IMPORTANT for frontend connection)
CORS(app)

# Get current backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained model
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))

# Load vectorizer
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))


# Home route (test API)
@app.route("/")
def home():
    return "Fake News Detection API is running!"


# Prediction route
@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Get JSON from frontend
        data = request.get_json()

        # Extract text
        text = data.get("text", "")

        if not text.strip():
            return jsonify({"prediction": "No text provided!"})

        # Convert text to features
        vector = vectorizer.transform([text])

        # Predict
        if prediction == 1:
    result = "🟢 Real News"
else:
    result = "🔴 Fake News"

return jsonify({"prediction": result})

        # Response
        if prediction == 0:
            result = "FAKE NEWS ⚠️"
        else:
            result = "REAL NEWS ✅"

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({
            "prediction": "Error occurred",
            "error": str(e)
        })


# Run server
if __name__ == "__main__":
    app.run(debug=True)