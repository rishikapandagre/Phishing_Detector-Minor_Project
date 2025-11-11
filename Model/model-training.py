# model-training.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Ensure models directory exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "../models")
DATA_DIR = os.path.join(BASE_DIR, "../data")

os.makedirs(MODEL_DIR, exist_ok=True)

def train_model(file_path, model_name, analyzer_type='char', ngram_range=(3, 5)):
    """
    Train a RandomForest phishing detection model.
    file_path: path to the training data file
    model_name: name to save model and vectorizer
    """
    print(f"🔹 Training {model_name} model...")

    # Load data
    data = pd.read_csv(file_path, names=["Input", "Label"])
    data['Label'] = data['Label'].apply(lambda x: 1 if str(x).strip().lower() == 'phishing' else 0)

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(analyzer=analyzer_type, ngram_range=ngram_range)
    X = vectorizer.fit_transform(data['Input'])
    y = data['Label']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"{model_name.capitalize()} Model Accuracy: {accuracy:.2f}")

    # Save model and vectorizer
    joblib.dump(model, os.path.join(MODEL_DIR, f"{model_name}_model.pkl"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, f"{model_name}_vectorizer.pkl"))
    print(f"Saved {model_name}_model.pkl and {model_name}_vectorizer.pkl\n")

if __name__ == "__main__":
    # Train URL phishing model
    train_model(os.path.join(DATA_DIR, "phishing-links.txt"), "url", analyzer_type='char', ngram_range=(3,5))

    # Train Email phishing model
    train_model(os.path.join(DATA_DIR, "email-links.txt"), "email", analyzer_type='char', ngram_range=(3,5))

    print("Training complete! Models saved in /models directory.")
