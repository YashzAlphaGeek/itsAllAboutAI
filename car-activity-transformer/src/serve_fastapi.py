# src/serve_fastapi.py
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import tensorflow as tf

app = FastAPI()
scaler = joblib.load("data/processed/scaler.joblib")
le = joblib.load("data/processed/label_encoder.joblib")
model = tf.keras.models.load_model("experiments/best_model.h5", compile=False)

class WindowRequest(BaseModel):
    window: list  # list of lists: seq_len x features

@app.post("/predict")
def predict(req: WindowRequest):
    window = np.array(req.window, dtype=float)
    # basic validation
    if window.ndim != 2:
        return {"error": "window must be 2D array (seq_len x features)"}
    s = window.reshape(-1, window.shape[-1])
    s = scaler.transform(s).reshape(window.shape)
    probs = model.predict(s[None, ...])[0]
    label = le.inverse_transform([int(np.argmax(probs))])[0]
    return {"label": label, "confidence": float(np.max(probs))}

# Run with: uvicorn src.serve_fastapi:app --reload --port 8000
