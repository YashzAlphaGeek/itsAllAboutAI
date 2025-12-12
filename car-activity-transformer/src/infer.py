# src/infer.py
import numpy as np
import joblib
import tensorflow as tf
from src.model import build_transformer

scaler = joblib.load("data/processed/scaler.joblib")
le = joblib.load("data/processed/label_encoder.joblib")
model = tf.keras.models.load_model("experiments/best_model.h5", compile=False)

def preprocess_single_window(window):  # window: (seq_len, features)
    # scale using saved scaler (note: scaler expects 2D)
    s = window.reshape(-1, window.shape[-1])
    s = scaler.transform(s)
    return s.reshape(window.shape)

def predict_window(window):
    x = preprocess_single_window(window)[None, ...]
    probs = model.predict(x)[0]
    label = le.inverse_transform([np.argmax(probs)])[0]
    return label, probs[np.argmax(probs)]

# Example usage
if __name__ == "__main__":
    # simulate a window or load one
    sample_window = np.random.randn(50, 7)  # replace with real data
    label, conf = predict_window(sample_window)
    print("Predicted:", label, "confidence:", conf)
