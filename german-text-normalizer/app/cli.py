# app/cli.py

import argparse
from inference import normalize_sentence

def main():
    parser = argparse.ArgumentParser(description="German Text Normalizer CLI")
    parser.add_argument("sentence", type=str, help="Input German sentence to normalize")
    args = parser.parse_args()

    input_sentence = args.sentence
    output_sentence = normalize_sentence(input_sentence)

    print("\n✅ Normalization Result")
    print(f"Input : {input_sentence}")
    print(f"Output: {output_sentence}\n")

if __name__ == "__main__":
    main()
