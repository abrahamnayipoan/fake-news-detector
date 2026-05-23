import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

fake_path = os.path.join(BASE_DIR, "..", "dataset", "Fake.csv")
true_path = os.path.join(BASE_DIR, "..", "dataset", "True.csv")

fake = pd.read_csv(fake_path)
true = pd.read_csv(true_path)

fake["label"] = 0
true["label"] = 1

data = pd.concat([fake, true])

# 🔥 FIX: combine title + text (VERY IMPORTANT)
data["content"] = data["title"] + " " + data["text"]

X = data["content"]
y = data["label"]

vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model re-trained successfully!")