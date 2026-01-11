from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense

def build_seq2seq_model(src_vocab, tgt_vocab, latent_dim=64, embed_dim=32):
    # Encoder
    enc_inputs = Input(shape=(None,), name="encoder_input")
    enc_emb = Embedding(src_vocab, embed_dim, mask_zero=True, name="encoder_embedding")(enc_inputs)
    enc_outputs, state_h, state_c = LSTM(latent_dim, return_state=True, name="encoder_lstm")(enc_emb)

    # Decoder
    dec_inputs = Input(shape=(None,), name="decoder_input")
    dec_emb = Embedding(tgt_vocab, embed_dim, mask_zero=True, name="decoder_embedding")(dec_inputs)
    dec_lstm = LSTM(latent_dim, return_sequences=True, return_state=True, name="decoder_lstm")
    dec_outputs, _, _ = dec_lstm(dec_emb, initial_state=[state_h, state_c])
    dec_dense = Dense(tgt_vocab, activation="softmax", name="decoder_dense")
    dec_outputs = dec_dense(dec_outputs)

    model = Model([enc_inputs, dec_inputs], dec_outputs)
    return model
