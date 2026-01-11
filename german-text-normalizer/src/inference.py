import numpy as np
import tensorflow as tf
import pickle
import os

MODEL_DIR = "../models"
MODEL_PATH = os.path.join(MODEL_DIR, "seq2seq_model.keras")
SRC_TOKENIZER_PATH = os.path.join(MODEL_DIR, "src_tokenizer.pkl")
TGT_TOKENIZER_PATH = os.path.join(MODEL_DIR, "tgt_tokenizer.pkl")
LATENT_DIM = 128

# -----------------------------
# 1. Load trained Seq2Seq model
# -----------------------------
seq2seq_model = tf.keras.models.load_model(MODEL_PATH)
print("Seq2Seq model loaded.")

# -----------------------------
# 2. Load tokenizers
# -----------------------------
with open(SRC_TOKENIZER_PATH, "rb") as f:
    src_tokenizer = pickle.load(f)

with open(TGT_TOKENIZER_PATH, "rb") as f:
    tgt_tokenizer = pickle.load(f)

# Reverse mapping for target tokens
index_to_word = {v: k for k, v in tgt_tokenizer.word_index.items()}

# -----------------------------
# 3. Build inference models
# -----------------------------
# Encoder
encoder_inputs = seq2seq_model.input[0]
encoder_embedding = seq2seq_model.get_layer("encoder_embedding")(encoder_inputs)
encoder_outputs, state_h, state_c = seq2seq_model.get_layer("encoder_lstm")(encoder_embedding)
encoder_model = tf.keras.Model(encoder_inputs, [state_h, state_c])

# Decoder
decoder_inputs = seq2seq_model.input[1]
decoder_state_input_h = tf.keras.Input(shape=(LATENT_DIM,))
decoder_state_input_c = tf.keras.Input(shape=(LATENT_DIM,))
dec_emb = seq2seq_model.get_layer("decoder_embedding")(decoder_inputs)
decoder_outputs, state_h_dec, state_c_dec = seq2seq_model.get_layer("decoder_lstm")(
    dec_emb, initial_state=[decoder_state_input_h, decoder_state_input_c]
)
decoder_dense = seq2seq_model.get_layer("decoder_dense")
decoder_outputs = decoder_dense(decoder_outputs)

decoder_model = tf.keras.Model(
    [decoder_inputs, decoder_state_input_h, decoder_state_input_c],
    [decoder_outputs, state_h_dec, state_c_dec]
)

# -----------------------------
# 4. Inference function
# -----------------------------
def normalize_sentence(sentence, max_len=20):
    """
    Takes a "bad" German sentence and returns the corrected version.
    """
    prepped = f"<sos> {sentence} <eos>"
    seq = src_tokenizer.texts_to_sequences([prepped])
    seq_padded = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=max_len, padding="post")

    # Encode input
    state_h, state_c = encoder_model.predict(seq_padded)

    decoder_input = np.array([[tgt_tokenizer.word_index["<sos>"]]])
    result = []

    for _ in range(max_len):
        output_tokens, state_h, state_c = decoder_model.predict([decoder_input, state_h, state_c])
        next_id = np.argmax(output_tokens[0, -1, :])

        if next_id == tgt_tokenizer.word_index.get("<eos>", 0):
            break

        word = index_to_word.get(next_id, "")
        if word:
            result.append(word)

        decoder_input = np.array([[next_id]])

    return " ".join(result)

# -----------------------------
# 5. Test examples
# -----------------------------
if __name__ == "__main__":
    test_sentences = [
        "ich bin muede",
        "hunger",
        "guten morgen ich habe hunger",
        "glucklich",
        "ich  bin   muede",
        "hallo zusammen",
        "bin muede",
        "ich gehe in die schule"
    ]

    for sent in test_sentences:
        normalized = normalize_sentence(sent)
        print(f"Input : {sent}")
        print(f"Output: {normalized}")
        print("-" * 50)
