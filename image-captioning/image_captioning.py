# ================================
# Image Captioning using TensorFlow / Keras
# CNN (InceptionV3) + LSTM
# ================================

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, Add

# ================================
# 1. Load CNN Encoder
# ================================
cnn = InceptionV3(weights="imagenet")
cnn = Model(cnn.input, cnn.layers[-2].output)

def extract_features(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    feature = cnn.predict(img, verbose=0)
    return feature

# ================================
# 2. Prepare Caption Data
# ================================
captions = [
    "start a dog running in the park end",
    "start a man riding a bike end",
    "start a child playing with a ball end"
]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(captions)

vocab_size = len(tokenizer.word_index) + 1
max_length = max(len(c.split()) for c in captions)

# ================================
# 3. Create Training Sequences
# ================================
def create_sequences(tokenizer, max_length, captions, image_feature):
    X1, X2, y = [], [], []
    for caption in captions:
        seq = tokenizer.texts_to_sequences([caption])[0]
        for i in range(1, len(seq)):
            in_seq = pad_sequences([seq[:i]], maxlen=max_length)[0]
            out_seq = tf.keras.utils.to_categorical(seq[i], vocab_size)

            X1.append(image_feature[0])
            X2.append(in_seq)
            y.append(out_seq)

    return np.array(X1), np.array(X2), np.array(y)

# Dummy image feature (for demo training)
dummy_image_feature = np.random.rand(1, 2048)

X1, X2, y = create_sequences(
    tokenizer,
    max_length,
    captions,
    dummy_image_feature
)

# ================================
# 4. Build Captioning Model
# ================================
image_input = Input(shape=(2048,))
image_dense = Dense(256, activation="relu")(image_input)
image_dense = Dropout(0.5)(image_dense)

text_input = Input(shape=(max_length,))
text_embed = Embedding(vocab_size, 256, mask_zero=True)(text_input)
text_lstm = LSTM(256)(text_embed)

decoder = Add()([image_dense, text_lstm])
decoder = Dense(256, activation="relu")(decoder)
output = Dense(vocab_size, activation="softmax")(decoder)

model = Model([image_input, text_input], output)
model.compile(loss="categorical_crossentropy", optimizer="adam")

print(model.summary())

# ================================
# 5. Train Model
# ================================
model.fit(
    [X1, X2],
    y,
    epochs=20,
    batch_size=8,
    verbose=1
)

# ================================
# 6. Generate Caption
# ================================
def generate_caption(photo_feature):
    caption = "start"
    for _ in range(max_length):
        seq = tokenizer.texts_to_sequences([caption])[0]
        seq = pad_sequences([seq], maxlen=max_length)

        yhat = model.predict([photo_feature, seq], verbose=0)
        word_id = np.argmax(yhat)
        word = tokenizer.index_word.get(word_id)

        if word is None:
            break

        caption += " " + word
        if word == "end":
            break
    return caption

# ================================
# 7. Test with Image
# ================================
image_path = "test.jpg"   # image in the same folder
image_feature = extract_features(image_path)

print("Generated Caption:")
print(generate_caption(image_feature))
