from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

class Preprocessor:
    def __init__(self, sos_token="<sos>", eos_token="<eos>"):
        self.sos_token = sos_token
        self.eos_token = eos_token
        self.tokenizer = None
        self.max_len = None

    def fit(self, sentences):
        """
        Fit tokenizer on the list of sentences.
        Adds <sos> and <eos> to each sentence.
        """
        sentences_with_tokens = [
            f"{self.sos_token} {s} {self.eos_token}" for s in sentences
        ]
        self.tokenizer = Tokenizer(filters="")
        self.tokenizer.fit_on_texts(sentences_with_tokens)
        sequences = self.tokenizer.texts_to_sequences(sentences_with_tokens)
        self.max_len = max(len(seq) for seq in sequences)
        return sequences

    def transform(self, sentences):
        """
        Convert sentences to padded sequences with <sos> and <eos>.
        """
        if self.tokenizer is None:
            raise ValueError("Tokenizer not fitted yet. Call fit() first.")

        sentences_with_tokens = [
            f"{self.sos_token} {s} {self.eos_token}" for s in sentences
        ]
        sequences = self.tokenizer.texts_to_sequences(sentences_with_tokens)
        padded = pad_sequences(sequences, maxlen=self.max_len, padding="post")
        return padded

    def save_tokenizer(self, path):
        """Save tokenizer for later use"""
        with open(path, "wb") as f:
            pickle.dump(self.tokenizer, f)

    def load_tokenizer(self, path):
        """Load tokenizer"""
        with open(path, "rb") as f:
            self.tokenizer = pickle.load(f)

# -----------------------------
# Quick test
if __name__ == "__main__":
    from data_loader import load_dataset
    file_path = "../data/raw/german_normalization_v1.txt"
    bad_sentences, correct_sentences = load_dataset(file_path)

    pre = Preprocessor()
    sequences = pre.fit(correct_sentences)
    padded = pre.transform(correct_sentences)

    print("Tokenizer word index:", pre.tokenizer.word_index)
    print("Max sentence length:", pre.max_len)
    print("Padded sequences (first 5):\n", padded[:5])