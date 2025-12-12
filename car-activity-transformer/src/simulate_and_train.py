# simulate_and_train.py (very small demo)
import numpy as np
from src.model import build_transformer
from sklearn.preprocessing import LabelEncoder
# create synthetic dataset: 3 classes, 1000 samples
SEQ_LEN = 50; FEATURES = 7; SAMPLES = 1000
X = np.random.randn(SAMPLES, SEQ_LEN, FEATURES)
# make class-dependent pattern: add offset to speed column for class 0
y = np.random.randint(0,3,size=(SAMPLES,))
for i in range(SAMPLES):
    if y[i]==0:
        X[i,:,0] += 2.0
    elif y[i]==1:
        X[i,:,0] += -1.5
# encode
le = LabelEncoder(); y_enc = le.fit_transform(y)
model = build_transformer(SEQ_LEN, FEATURES, num_classes=3)
model.fit(X, y_enc, epochs=5, batch_size=32, validation_split=0.2)
