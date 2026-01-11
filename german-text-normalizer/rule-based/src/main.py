"""
Command-line interface for testing German text normalization.
"""

from normalize import Normalizer
import os

def main():
    rules_file = os.path.join("..", "data", "normalization_rules.txt")
    normalizer = Normalizer(rules_file)

    print("German Text Normalizer (Beginner Version)")
    print("Type 'exit' to quit.\n")

    while True:
        sentence = input("Enter a sentence: ")
        if sentence.lower() == "exit":
            break
        normalized = normalizer.normalize(sentence)
        print("Normalized:", normalized)
        print("-" * 40)

if __name__ == "__main__":
    main()
