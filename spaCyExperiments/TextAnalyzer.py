import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is planning to open a new office in London next year.")

## Tokenization + POS + dependency → Grammatical structure of the sentence
for token in doc:
    print(token.text, token.pos_, token.dep_)

## Named Entity Recognition (NER)
for ent in doc.ents:
    print(ent.text, ent.label_)
