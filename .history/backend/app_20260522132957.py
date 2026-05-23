from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

# Create Flask app
app = Flask(__name__)

# Enable CORS (IMPORTANT for frontend connection)
CORS(app)

# Get backend folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained model
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))

# Load vectorizer
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))


# Home route
@app.route("/")
def home():
    return "Fake News Detection API is running!"


# Prediction route
@app.route("/predict", methods=["POST"])
def predict():

    # Get data from frontend
    data = request.get_json()
    text = data.get("text", "")

    if text.strip() == "":
        return jsonify({"prediction": "No text provided!"})

    # Convert text using vectorizer
    text_vector = vectorizer.transform([text])

    # Predict
    prediction = model.predict(text_vector)[0]

    # Convert result
    if prediction == 0:
        result = "FAKE NEWS ⚠️"
    else:
        result = "REAL NEWS ✅"

    return jsonify({"prediction": result})


# Run server
if __name__ == "__main__":
    app.run(debug=True)