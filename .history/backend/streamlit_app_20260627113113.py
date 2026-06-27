import streamlit as st
import joblib

# Load model
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.title("Fake News Detection System")

news_text = st.text_area(
    "Enter or paste a news article"
)

if st.button("Analyze"):

    if news_text.strip():

        vector = vectorizer.transform([news_text])

        prediction = model.predict(vector)[0]

        probabilities = model.predict_proba(vector)[0]
        confidence = round(max(probabilities) * 100, 2)

        if prediction == 1:
            st.success(
                f"🟢 Real News ({confidence}%)"
            )
        else:
            st.error(
                f"🔴 Fake News ({confidence}%)"
            )
    else:
        st.warning("Please enter news text.")