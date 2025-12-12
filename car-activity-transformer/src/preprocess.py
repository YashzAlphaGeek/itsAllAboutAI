import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

def load_csv(path):
    return pd.read_csv(path, parse_dates=['timestamp'])


def resample_and_interpolate(df, freq='100ms'):
    df = df.set_index('timestamp')

    # Separate numeric and non-numeric columns
    numeric_cols = df.select_dtypes(include='number').columns
    non_numeric_cols = df.select_dtypes(exclude='number').columns

    # Resample numeric columns: mean + interpolate
    df_numeric = df[numeric_cols].resample(freq).mean().interpolate()

    # Resample non-numeric columns: forward-fill (labels, categories)
    df_non_numeric = df[non_numeric_cols].resample(freq).ffill()

    # Combine both
    df_resampled = pd.concat([df_numeric, df_non_numeric], axis=1).reset_index()
    return df_resampled


def create_windows(df, feature_cols, label_col, seq_len=50, step=10):
    X, y = [], []
    data = df[feature_cols].values
    labels = df[label_col].values if label_col in df.columns else None
    n = len(df)
    for start in range(0, n - seq_len + 1, step):
        end = start + seq_len
        X.append(data[start:end])
        if labels is not None:
            # Use majority vote of labels in window or label at last timestep
            window_labels = labels[start:end]
            # choose mode
            vals, counts = np.unique(window_labels, return_counts=True)
            y.append(vals[np.argmax(counts)])
    X = np.array(X)
    y = np.array(y) if labels is not None else None
    return X, y

def scale_features(X_train, X_val, X_test):
    # X shape: (samples, seq_len, features)
    n_features = X_train.shape[-1]
    scaler = StandardScaler()
    # fit on flattened training
    X_train_flat = X_train.reshape(-1, n_features)
    scaler.fit(X_train_flat)
    def transform(X):
        s = X.reshape(-1, n_features)
        s = scaler.transform(s)
        return s.reshape(X.shape)
    return transform(X_train), transform(X_val), transform(X_test), scaler

def encode_labels(y):
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    return y_enc, le

# Example flow for a single CSV
if __name__ == "__main__":
    path = "data/raw/session1.csv"
    df = load_csv(path)
    df = resample_and_interpolate(df, freq='100ms')   # adjust frequency
    feature_cols = ['speed','rpm','throttle','brake','accel_x','accel_y','gear']
    label_col = 'label'
    X, y = create_windows(df, feature_cols, label_col, seq_len=50, step=10)
    print("X shape:", X.shape, "y shape:", y.shape)

