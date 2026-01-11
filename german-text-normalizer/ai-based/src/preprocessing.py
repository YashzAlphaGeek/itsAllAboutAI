import tensorflow as tf
import pickle

class Preprocessor:
    def __init__(self, max_len=10):
        self.max_len = max_len
        self.tokenizer = None

    def fit(self, sentences):
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(
            filters='', oov_token='<unk>')
        self.tokenizer.fit_on_texts(sentences)
        return self.texts_to_sequences(sentences)

    def transform(self, sentences):
        seq = self.tokenizer.texts_to_sequences(sentences)
        return tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=self.max_len, padding='post')

    def texts_to_sequences(self, sentences):
        return self.tokenizer.texts_to_sequences(sentences)

    def save_tokenizer(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.tokenizer, f)
