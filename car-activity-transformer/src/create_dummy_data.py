import pandas as pd
import numpy as np
import os

os.makedirs("data/raw", exist_ok=True)

SEQ_LEN = 500
FEATURE_COLS = ['speed','rpm','throttle','brake','accel_x','accel_y','gear']
LABELS = ['moving','idle','neutral','parked']

# generate timestamps
data = {'timestamp': pd.date_range(start='2025-12-12', periods=SEQ_LEN, freq='100ms')}

# numeric features
for col in FEATURE_COLS:
    data[col] = np.random.randn(SEQ_LEN)

# labels (simple pattern)
labels = []
for i in range(SEQ_LEN):
    if i < 100:
        labels.append('idle')
    elif i < 250:
        labels.append('moving')
    elif i < 400:
        labels.append('neutral')
    else:
        labels.append('parked')
data['label'] = labels

# save CSV
df = pd.DataFrame(data)
df.to_csv("data/raw/session1.csv", index=False)
print("Dummy dataset created at data/raw/session1.csv")
