import os
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from src.preprocess import resample_and_interpolate, create_windows
from src.model import PositionalEncoding

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

@st.cache_resource
def load_model_artifacts():
    try:
        model = load_model(
            "experiments/final_model.keras",
            custom_objects={"PositionalEncoding": PositionalEncoding},
            compile=False
        )
        le = joblib.load("data/processed/label_encoder.joblib")
        scaler = joblib.load("data/processed/scaler.joblib")
        return model, le, scaler
    except FileNotFoundError as e:
        st.error(f"Model or artifacts not found: {e}")
        return None, None, None

model, le, scaler = load_model_artifacts()
if model is None:
    st.stop()

st.title("🚗 Car Activity Recognition")
st.write("Upload a CSV file with car telemetry (speed, rpm, throttle, brake, accel_x/y, gear)")

uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
    if df.empty:
        st.warning("Uploaded CSV is empty!")
    else:
        df = resample_and_interpolate(df, freq='100ms')
        SEQ_LEN = 50
        FEATURE_COLS = ['speed', 'rpm', 'throttle', 'brake', 'accel_x', 'accel_y', 'gear']
        X, _ = create_windows(df, FEATURE_COLS, 'label', seq_len=SEQ_LEN, step=10)

        if len(X) == 0:
            st.warning("Not enough data for creating windows. Try a longer CSV or smaller SEQ_LEN/step.")
        else:
            n_features = X.shape[-1]
            X_scaled = scaler.transform(X.reshape(-1, n_features)).reshape(X.shape)

            y_pred = model.predict(X_scaled)
            y_pred_labels = le.inverse_transform(np.argmax(y_pred, axis=1))

            st.subheader("Predicted Activities")
            st.write(y_pred_labels)

            st.subheader("Activity Timeline")
            timeline_df = pd.DataFrame({
                'Window': np.arange(len(y_pred_labels)),
                'Activity': y_pred_labels
            })
            activity_map = {v: i for i, v in enumerate(le.classes_)}
            timeline_df['Activity_Num'] = timeline_df['Activity'].map(activity_map)
            st.line_chart(timeline_df[['Window', 'Activity_Num']].set_index('Window'))
