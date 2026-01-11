from normalize import normalize_sentence

def run_demo():
    test_sentences = [
        "ich bin muede",
        "hunger",
        "guten morgen",
        "glucklich",
        "ich  bin   muede",
        "hallo zusammen",
        "bin muede",
        "ich gehe in die schule"
    ]

    print("=== German Text Normalizer Demo ===\n")
    for sentence in test_sentences:
        normalized = normalize_sentence(sentence)
        print(f"Input  : {sentence}")
        print(f"Output : {normalized}")
        print("-" * 50)

if __name__ == "__main__":
    run_demo()
