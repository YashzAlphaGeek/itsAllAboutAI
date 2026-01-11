def load_dataset(file_path):
    bad_sentences = []
    correct_sentences = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|||" not in line:
                continue
            bad, correct = line.split("|||")
            bad_sentences.append(bad.strip())
            correct_sentences.append(correct.strip())

    return bad_sentences, correct_sentences
