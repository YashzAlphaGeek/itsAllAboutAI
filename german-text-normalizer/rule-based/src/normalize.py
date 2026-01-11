from preprocessing import clean_text

UMLAUTS = {
    "ae": "ä",
    "oe": "ö",
    "ue": "ü",
    "Ae": "Ä",
    "Oe": "Ö",
    "Ue": "Ü",
    "ss": "ß",
}

class Normalizer:
    def __init__(self, rules_file: str):
        self.rules = {}
        self.load_rules(rules_file)

    def load_rules(self, rules_file: str):
        with open(rules_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "|||" not in line:
                    continue
                bad, correct = line.split("|||")
                bad = clean_text(bad)
                correct = correct.strip()
                self.rules[bad] = correct

    def replace_umlauts(self, text: str) -> str:
        for k, v in UMLAUTS.items():
            text = text.replace(k, v)
        return text

    def normalize(self, sentence: str) -> str:
        # Clean sentence
        sentence_clean = clean_text(sentence)

        if sentence_clean in self.rules:
            return self.rules[sentence_clean]

        words = sentence_clean.split()
        normalized_words = [self.replace_umlauts(w) for w in words]

        if normalized_words:
            normalized_words[0] = normalized_words[0].capitalize()

        return " ".join(normalized_words)


normalizer = None

def normalize_sentence(sentence: str, rules_file: str = "../data/normalization_rules.txt") -> str:
    global normalizer
    if normalizer is None:
        normalizer = Normalizer(rules_file)
    return normalizer.normalize(sentence)
