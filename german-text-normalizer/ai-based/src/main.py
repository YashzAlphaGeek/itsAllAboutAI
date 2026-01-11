from inference import normalize_sentence

def run_demo():
    print("=== German Text Normalizer (AI) ===")
    print("Type 'exit' to quit.\n")

    while True:
        sentence = input("Enter a sentence: ").strip()
        if sentence.lower() == "exit":
            break
        normalized = normalize_sentence(sentence)
        print(f"Normalized: {normalized}\n")

if __name__ == "__main__":
    run_demo()
