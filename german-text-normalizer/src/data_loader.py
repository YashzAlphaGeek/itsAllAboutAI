import os

def load_dataset(file_path):
    """
    Load German normalization dataset.
    Returns two lists:
      - bad_sentences: what learners wrote
      - correct_sentences: normalized sentences
    Ignores comments (#) and empty lines.
    """
    bad_sentences = []
    correct_sentences = []

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found: {file_path}")

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "|||" not in line:
                continue

            bad, correct = line.split("|||")
            bad_sentences.append(bad.strip())
            correct_sentences.append(correct.strip())

    return bad_sentences, correct_sentences


# TEST
if __name__ == "__main__":
    file_path = "../data/raw/german_normalization_v1.txt"
    bad, correct = load_dataset(file_path)
    print("Bad Sentences:", bad[:5])
    print("Correct Sentences:", correct[:5])
