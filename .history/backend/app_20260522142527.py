@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")

    if text.strip() == "":
        return jsonify({"prediction": "No text provided!"})

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)[0]

    # 🔥 Confidence score
    probability = model.predict_proba(vector)[0]
    confidence = max(probability) * 100

    if prediction == 0:
        result = "FAKE NEWS ⚠️"
    else:
        result = "REAL NEWS ✅"

    return jsonify({
        "prediction": result,
        "confidence": f"{confidence:.2f}%"
    })