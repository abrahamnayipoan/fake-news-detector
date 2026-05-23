import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

fake_path = os.path.join(BASE_DIR, "..", "dataset", "Fake.csv")
true_path = os.path.join(BASE_DIR, "..", "dataset", "True.csv")

# Load dataset
fake = pd.read_csv(fake_path)
true = pd.read_csv(true_path)

# Label data
fake["label"] = 0   # FAKE
true["label"] = 1   # REAL

# Combine datasets
data = pd.concat([fake, true])

# Use only text column
X = data["text"]
y = data["label"]

# Convert text to numbers (IMPORTANT NLP step)
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
X_vectorized = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model saved successfully!")

