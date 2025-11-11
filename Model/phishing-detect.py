# phishing-detect.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

# Base and model directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "../models")

# Load trained models and vectorizers
print("🔹 Loading models...")
url_model = joblib.load(os.path.join(MODEL_DIR, "url_model.pkl"))
url_vectorizer = joblib.load(os.path.join(MODEL_DIR, "url_vectorizer.pkl"))
email_model = joblib.load(os.path.join(MODEL_DIR, "email_model.pkl"))
email_vectorizer = joblib.load(os.path.join(MODEL_DIR, "email_vectorizer.pkl"))
print("✅ Models loaded successfully!\n")

@app.route("/")
def home():
    return jsonify({
        "message": "Phishing Detector API is running!",
        "usage": "POST /predict with JSON {'input': '<text>', 'type': 'url' or 'email'}"
    })

@app.route("/predict", methods=["POST"])
def predict():
    """
    POST JSON:
    {
        "input": "some URL or email text",
        "type": "url" or "email"
    }
    """
    data = request.get_json()

    if not data or "input" not in data or "type" not in data:
        return jsonify({"error": "Please provide 'input' and 'type' (url/email)."}), 400

    text_input = data["input"].strip()
    input_type = data["type"].strip().lower()

    if input_type == "email":
        features = email_vectorizer.transform([text_input])
        prediction = email_model.predict(features)[0]
    elif input_type == "url":
        features = url_vectorizer.transform([text_input])
        prediction = url_model.predict(features)[0]
    else:
        return jsonify({"error": "Invalid type. Must be 'url' or 'email'."}), 400

    result = "Phishing" if prediction == 1 else "Legitimate"

    return jsonify({
        "input": text_input,
        "type": input_type,
        "result": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
