import tensorflow as tf

def build_seq2seq_model(src_vocab_size, tgt_vocab_size, latent_dim=128):
    """
    Build a simple LSTM Encoder-Decoder seq2seq model.

    Parameters:
        src_vocab_size : int : vocabulary size of source sentences
        tgt_vocab_size : int : vocabulary size of target sentences
        latent_dim : int : LSTM hidden size

    Returns:
        model : tf.keras.Model : compiled seq2seq model
        encoder_inputs : tf.keras.Input
        decoder_inputs : tf.keras.Input
    """

    # --------------------
    # Encoder
    # --------------------
    encoder_inputs = tf.keras.Input(shape=(None,), name="encoder_input")
    enc_emb = tf.keras.layers.Embedding(src_vocab_size, latent_dim, name="encoder_embedding")(encoder_inputs)
    encoder_outputs, state_h, state_c = tf.keras.layers.LSTM(
        latent_dim, return_state=True, name="encoder_lstm"
    )(enc_emb)
    encoder_states = [state_h, state_c]

    # --------------------
    # Decoder
    # --------------------
    decoder_inputs = tf.keras.Input(shape=(None,), name="decoder_input")
    dec_emb = tf.keras.layers.Embedding(tgt_vocab_size, latent_dim, name="decoder_embedding")(decoder_inputs)
    decoder_lstm = tf.keras.layers.LSTM(
        latent_dim, return_sequences=True, return_state=True, name="decoder_lstm"
    )
    decoder_outputs, _, _ = decoder_lstm(dec_emb, initial_state=encoder_states)
    decoder_dense = tf.keras.layers.Dense(tgt_vocab_size, activation="softmax", name="decoder_dense")
    decoder_outputs = decoder_dense(decoder_outputs)

    # --------------------
    # Define model
    # --------------------
    model = tf.keras.Model([encoder_inputs, decoder_inputs], decoder_outputs)

    # Compile
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    return model, encoder_inputs, decoder_inputs



if __name__ == "__main__":
    model, _, _ = build_seq2seq_model(20, 30)
    model.summary()
