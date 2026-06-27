import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

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