import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "seq2seq_model.keras")
SRC_TOKENIZER_PATH = os.path.join(MODEL_DIR, "src_tokenizer.pkl")
TGT_TOKENIZER_PATH = os.path.join(MODEL_DIR, "tgt_tokenizer.pkl")
LATENT_DIM = 64
MAX_LEN = 10

# Load model
seq2seq_model = load_model(MODEL_PATH)
print("Seq2Seq model loaded.")

# Load tokenizers
with open(SRC_TOKENIZER_PATH, "rb") as f:
    src_tokenizer = pickle.load(f)
with open(TGT_TOKENIZER_PATH, "rb") as f:
    tgt_tokenizer = pickle.load(f)

index_to_word = {v: k for k, v in tgt_tokenizer.word_index.items()}

# Build encoder model
encoder_inputs = seq2seq_model.input[0]
encoder_embedding = seq2seq_model.get_layer("encoder_embedding")(encoder_inputs)
encoder_outputs, state_h, state_c = seq2seq_model.get_layer("encoder_lstm")(encoder_embedding)
encoder_model = tf.keras.Model(encoder_inputs, [state_h, state_c])

# Build decoder model
decoder_inputs_inf = tf.keras.Input(shape=(1,), name="decoder_input_inf")
decoder_state_h = tf.keras.Input(shape=(LATENT_DIM,), name="decoder_h")
decoder_state_c = tf.keras.Input(shape=(LATENT_DIM,), name="decoder_c")

dec_emb_layer = seq2seq_model.get_layer("decoder_embedding")(decoder_inputs_inf)
dec_lstm_layer = seq2seq_model.get_layer("decoder_lstm")
dec_dense_layer = seq2seq_model.get_layer("decoder_dense")

dec_outputs, state_h_dec, state_c_dec = dec_lstm_layer(
    dec_emb_layer, initial_state=[decoder_state_h, decoder_state_c]
)
dec_outputs = dec_dense_layer(dec_outputs)

decoder_model = tf.keras.Model(
    [decoder_inputs_inf, decoder_state_h, decoder_state_c],
    [dec_outputs, state_h_dec, state_c_dec]
)

# Rule fallback for unseen sentences
RULES = {
    "ich bin muede": "Ich bin müde",
    "hunger": "Hunger",
    "guten morgen": "Guten Morgen",
    "ich gehe in die schule": "Ich gehe in die Schule"
}

def normalize_sentence(sentence: str) -> str:
    # Rule-based fallback
    sentence_clean = " ".join(sentence.lower().split())
    if sentence_clean in RULES:
        return RULES[sentence_clean]

    # AI-based inference
    seq = src_tokenizer.texts_to_sequences([sentence])
    seq = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=MAX_LEN, padding="post")
    state_h_val, state_c_val = encoder_model.predict(seq, verbose=0)

    decoder_input = np.array([[tgt_tokenizer.word_index.get("<sos>", 1)]])
    result = []

    for _ in range(MAX_LEN):
        output_tokens, state_h_val, state_c_val = decoder_model.predict(
            [decoder_input, state_h_val, state_c_val], verbose=0
        )
        next_id = np.argmax(output_tokens[0, -1, :])
        if next_id == tgt_tokenizer.word_index.get("<eos>", 2):
            break
        word = index_to_word.get(next_id, "")
        if word:
            result.append(word)
        decoder_input = np.array([[next_id]])

    return " ".join(result)
