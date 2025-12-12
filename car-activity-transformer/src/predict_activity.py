# predict_activity.py
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
from src.preprocess import load_csv, resample_and_interpolate, create_windows, scale_features

# ----- Config -----
SEQ_LEN = 50
FEATURE_COLS = ['speed','rpm','throttle','brake','accel_x','accel_y','gear']
LABEL_COL = 'label'

# 1) Load model and encoder
model = load_model("experiments/final_model.h5")
le = joblib.load("data/processed/label_encoder.joblib")
scaler = joblib.load("data/processed/scaler.joblib")

# 2) Load new CSV
path = "data/raw/session_new.csv"  # replace with your file
df = load_csv(path)
df = resample_and_interpolate(df, freq='100ms')

# 3) Create windows
X, _ = create_windows(df, FEATURE_COLS, LABEL_COL, seq_len=SEQ_LEN, step=10)

# 4) Scale features
n_features = X.shape[-1]
X_flat = X.reshape(-1, n_features)
X_scaled = scaler.transform(X_flat).reshape(X.shape)

# 5) Predict
y_pred_probs = model.predict(X_scaled)
y_pred_classes = np.argmax(y_pred_probs, axis=1)
y_pred_labels = le.inverse_transform(y_pred_classes)

# 6) Output predictions
for i, label in enumerate(y_pred_labels):
    print(f"Window {i}: {label}")
