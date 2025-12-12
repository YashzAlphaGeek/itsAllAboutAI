import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

# ---- Positional Encoding ----
class PositionalEncoding(layers.Layer):
    def __init__(self, seq_len=None, d_model=None, **kwargs):
        """
        Positional Encoding layer for Transformer.
        Compatible with Keras H5 or native .keras format.
        """
        super().__init__(**kwargs)
        self.seq_len = seq_len
        self.d_model = d_model
        self.pos_encoding = None
        if self.seq_len is not None and self.d_model is not None:
            self._build_pos_encoding(self.seq_len, self.d_model)

    def _build_pos_encoding(self, seq_len, d_model):
        pos = np.arange(seq_len)[:, None]
        i = np.arange(d_model)[None, :]
        angle_rates = 1 / np.power(10000, (2 * (i // 2)) / float(d_model))
        angle_rads = pos * angle_rates
        angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
        angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
        self.pos_encoding = tf.cast(angle_rads[None, :, :], dtype=tf.float32)

    def call(self, x):
        if self.pos_encoding is None:
            self._build_pos_encoding(x.shape[1], x.shape[2])
        return x + self.pos_encoding[:, :tf.shape(x)[1], :]

    def get_config(self):
        config = super().get_config()
        config.update({
            "seq_len": self.seq_len,
            "d_model": self.d_model
        })
        return config

# ---- Transformer Encoder Block ----
def transformer_encoder_block(x, num_heads, ff_dim, dropout=0.1):
    attn = layers.MultiHeadAttention(num_heads=num_heads, key_dim=ff_dim)(x, x)
    attn = layers.Dropout(dropout)(attn)
    out1 = layers.LayerNormalization(epsilon=1e-6)(x + attn)
    ff = layers.Dense(ff_dim, activation='relu')(out1)
    ff = layers.Dense(x.shape[-1])(ff)
    ff = layers.Dropout(dropout)(ff)
    out2 = layers.LayerNormalization(epsilon=1e-6)(out1 + ff)
    return out2

# ---- Build Transformer Model ----
def build_transformer(seq_len, num_features, num_classes,
                      num_heads=4, ff_dim=128, num_layers=2, dropout=0.1, mlp_units=[64]):
    inputs = layers.Input(shape=(seq_len, num_features))
    x = layers.Dense(num_features)(inputs)
    x = PositionalEncoding(seq_len=seq_len, d_model=num_features)(x)  # use keyword args

    for _ in range(num_layers):
        x = transformer_encoder_block(x, num_heads=num_heads, ff_dim=ff_dim, dropout=dropout)

    x = layers.GlobalAveragePooling1D()(x)
    for u in mlp_units:
        x = layers.Dense(u, activation='relu')(x)
        x = layers.Dropout(dropout)(x)

    outputs = layers.Dense(num_classes, activation='softmax')(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model
