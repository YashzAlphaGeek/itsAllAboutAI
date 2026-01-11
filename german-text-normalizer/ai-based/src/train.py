import os
import numpy as np
from data_loader import load_dataset
from preprocessing import Preprocessor
from model import build_seq2seq_model

import tensorflow as tf

import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "normalization_rules.txt")
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
MODEL_FILE = os.path.join(MODEL_DIR, "seq2seq_model.keras")
LATENT_DIM = 64
EPOCHS = 200
BATCH_SIZE = 1

os.makedirs(MODEL_DIR, exist_ok=True)

# Load dataset
bad_sentences, correct_sentences = load_dataset(DATA_FILE)

# Add <sos> and <eos> tokens
correct_sentences_sos = ["<sos> " + s + " <eos>" for s in correct_sentences]

# Preprocess
src_pre = Preprocessor(max_len=10)
src_seq = src_pre.fit(bad_sentences)
src_seq_padded = src_pre.transform(bad_sentences)

tgt_pre = Preprocessor(max_len=10)
tgt_seq = tgt_pre.fit(correct_sentences_sos)
tgt_seq_padded = tgt_pre.transform(correct_sentences_sos)

src_pre.save_tokenizer(os.path.join(MODEL_DIR, "src_tokenizer.pkl"))
tgt_pre.save_tokenizer(os.path.join(MODEL_DIR, "tgt_tokenizer.pkl"))

# Prepare decoder input & target
decoder_input = tgt_seq_padded[:, :-1]
decoder_target = tgt_seq_padded[:, 1:]

# Build model
src_vocab_size = len(src_pre.tokenizer.word_index) + 1
tgt_vocab_size = len(tgt_pre.tokenizer.word_index) + 1

model = build_seq2seq_model(src_vocab_size, tgt_vocab_size, LATENT_DIM)

# Compile before training
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy"
)

model.summary()

# Train
history = model.fit(
    [src_seq_padded, decoder_input],
    np.expand_dims(decoder_target, -1),
    batch_size=BATCH_SIZE,
    epochs=EPOCHS
)

# Save model
model.save(MODEL_FILE)
print("Model saved!")
