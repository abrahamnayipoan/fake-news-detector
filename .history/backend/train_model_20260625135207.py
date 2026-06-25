import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

fake_path = os.path.join(BASE_DIR, "..", "dataset", "Fake.csv")
true_path = os.path.join(BASE_DIR, "..", "dataset", "True.csv")

fake = pd.read_csv(fake_path)
true = pd.read_csv(true_path)

fake["label"] = 0
true["label"] = 1

data = pd.concat([fake, true], ignore_index=True)

data["content"] = data["title"].fillna("") + " " + data["text"].fillna("")

X = data["content"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    shuffle=True
)

vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)

X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=200)
model.fit(X_train_vectorized, y_train)

y_pred = model.predict(X_test_vectorized)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(model, os.path.join(BASE_DIR, "model.pkl"))
joblib.dump(vectorizer, os.path.join(BASE_DIR, "vectorizer.pkl"))

print("Model trained and saved successfully!")
