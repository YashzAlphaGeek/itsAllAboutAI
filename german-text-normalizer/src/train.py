import os
import numpy as np
from data_loader import load_dataset
from preprocessing import Preprocessor
from model import build_seq2seq_model
import tensorflow as tf

# -----------------------------
# Configuration
# -----------------------------
DATA_FILE = "../data/raw/german_normalization_v1.txt"
MODEL_DIR = "../models"
LATENT_DIM = 32
EMBED_DIM = 32
BATCH_SIZE = 1
EPOCHS = 500
REPEAT_FACTOR = 10

os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# 1. Load dataset
# -----------------------------
bad_sentences, correct_sentences = load_dataset(DATA_FILE)
print(f"Loaded {len(bad_sentences)} sentence pairs.")

# Repeat dataset to give the model enough examples
bad_sentences = bad_sentences * REPEAT_FACTOR
correct_sentences = correct_sentences * REPEAT_FACTOR
print(f"Dataset repeated: {len(bad_sentences)} sentence pairs")

# -----------------------------
# 2. Preprocess dataset
# -----------------------------
src_pre = Preprocessor()
src_seq = src_pre.fit(bad_sentences)
src_seq_padded = src_pre.transform(bad_sentences)

tgt_pre = Preprocessor()
tgt_seq = tgt_pre.fit(correct_sentences)
tgt_seq_padded = tgt_pre.transform(correct_sentences)

# Save tokenizers for inference
src_pre.save_tokenizer(os.path.join(MODEL_DIR, "src_tokenizer.pkl"))
tgt_pre.save_tokenizer(os.path.join(MODEL_DIR, "tgt_tokenizer.pkl"))

# -----------------------------
# 3. Prepare decoder input & target
# -----------------------------
decoder_input = tgt_seq_padded[:, :-1]  # all tokens except last
decoder_target = tgt_seq_padded[:, 1:]  # all tokens except first

# -----------------------------
# 4. Build model
# -----------------------------
src_vocab_size = len(src_pre.tokenizer.word_index) + 1
tgt_vocab_size = len(tgt_pre.tokenizer.word_index) + 1

model, _, _ = build_seq2seq_model(
    src_vocab_size, tgt_vocab_size, LATENT_DIM
)

model.summary()

# -----------------------------
# 5. Train model
# -----------------------------
history = model.fit(
    [src_seq_padded, decoder_input],
    np.expand_dims(decoder_target, -1),
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    verbose=1,
    shuffle=True
)

# -----------------------------
# 6. Save model
# -----------------------------
model.save(os.path.join(MODEL_DIR, "seq2seq_model.keras"))
print(f"Model saved to {MODEL_DIR}/seq2seq_model.keras")
