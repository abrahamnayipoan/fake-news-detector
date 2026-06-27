import streamlit as st
import joblib
import os

# ======================
# APP TITLE
# ======================
st.title("📰 Fake News Detection System")

# ======================
# LOAD MODEL
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# ======================
# INPUT
# ======================
news_text = st.text_area("Enter or paste a news article")

# ======================
# PREDICTION
# ======================
if st.button("Analyze"):

    if not news_text.strip():
        st.warning("Please enter news text.")
        st.stop()

    # Transform input
    vector = vectorizer.transform([news_text])

    # Prediction
    prediction = model.predict(vector)[0]

    # Confidence (safe check)
    confidence = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(vector)[0]
        confidence = round(max(probabilities) * 100, 2)

    # ======================
    # OUTPUT
    # ======================
    if prediction == 1:
        if confidence:
            st.success(f"🟢 Real News ({confidence}%)")
        else:
            st.success("🟢 Real News")
    else:
        if confidence:
            st.error(f"🔴 Fake News ({confidence}%)")
        else:
            st.error("🔴 Fake News")