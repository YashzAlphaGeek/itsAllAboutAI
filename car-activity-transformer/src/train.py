# src/train.py
import os
import glob
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import joblib

from src.model import build_transformer
from src.preprocess import create_windows, load_csv, resample_and_interpolate, scale_features

# ---------- CONFIG ----------
SEQ_LEN = 50
STEP = 10
FEATURE_COLS = ['speed','rpm','throttle','brake','accel_x','accel_y','gear']
LABEL_COL = 'label'
BATCH_SIZE = 64
EPOCHS = 30
# ----------------------------

# Ensure required folders exist
os.makedirs("data/processed", exist_ok=True)
os.makedirs("experiments", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)

# If no CSV exists in data/raw, create a dummy dataset
if len(glob.glob("data/raw/*.csv")) == 0:
    print("No CSV found in data/raw/. Generating dummy dataset...")
    SEQ_LEN_DUMMY = 500
    data = {'timestamp': pd.date_range(start='2025-12-12', periods=SEQ_LEN_DUMMY, freq='100ms')}
    for col in FEATURE_COLS:
        data[col] = np.random.randn(SEQ_LEN_DUMMY)
    labels = []
    for i in range(SEQ_LEN_DUMMY):
        if i < 100:
            labels.append('idle')
        elif i < 250:
            labels.append('moving')
        elif i < 400:
            labels.append('neutral')
        else:
            labels.append('parked')
    data[LABEL_COL] = labels
    df_dummy = pd.DataFrame(data)
    dummy_path = "data/raw/dummy_session.csv"
    df_dummy.to_csv(dummy_path, index=False)
    print(f"Dummy dataset created at {dummy_path}")

# 1) Load all CSV sessions in data/raw
files = glob.glob("data/raw/*.csv")
Xs, ys = [], []
for f in files:
    df = load_csv(f)
    df = resample_and_interpolate(df, freq='100ms')
    X, y = create_windows(df, FEATURE_COLS, LABEL_COL, seq_len=SEQ_LEN, step=STEP)
    Xs.append(X)
    ys.append(y)

X = np.concatenate(Xs, axis=0)
y = np.concatenate(ys, axis=0)
print(f"Total sequences: {X.shape[0]}, sequence length: {X.shape[1]}, features: {X.shape[2]}")

# 2) Train/val/test split
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

# 3) Scale features
X_train, X_val, X_test, scaler = scale_features(X_train, X_val, X_test)
joblib.dump(scaler, "data/processed/scaler.joblib")

# 4) Label encode
le = LabelEncoder()
y_train_enc = le.fit_transform(y_train)
y_val_enc = le.transform(y_val)
y_test_enc = le.transform(y_test)
joblib.dump(le, "data/processed/label_encoder.joblib")

# 5) Build transformer model
num_classes = len(le.classes_)
num_features = len(FEATURE_COLS)
model = build_transformer(SEQ_LEN, num_features, num_classes, num_heads=4, ff_dim=128, num_layers=2)
model.summary()

# 6) Callbacks
cb = [
    tf.keras.callbacks.ModelCheckpoint("experiments/best_model.h5", save_best_only=True, monitor='val_accuracy'),
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=6, restore_best_weights=True)
]

# 7) Train
history = model.fit(X_train, y_train_enc,
                    validation_data=(X_val, y_val_enc),
                    epochs=EPOCHS,
                    batch_size=BATCH_SIZE,
                    callbacks=cb)

# 8) Evaluate
loss, acc = model.evaluate(X_test, y_test_enc)
print(f"Test accuracy: {acc:.4f}")

# 9) Reports
y_pred = np.argmax(model.predict(X_test), axis=1)
print(classification_report(y_test_enc, y_pred, target_names=le.classes_))
cm = confusion_matrix(y_test_enc, y_pred)
print("Confusion matrix:\n", cm)

# 10) Save final model in native Keras format
model.save("experiments/final_model.keras")  # <-- use .keras
joblib.dump(scaler, "data/processed/scaler.joblib")
joblib.dump(le, "data/processed/label_encoder.joblib")
print("Training complete. Model saved at experiments/final_model.keras")

