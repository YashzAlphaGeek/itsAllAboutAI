# Opinion Map - NLP Visualization

This project demonstrates how to create an **Opinion Map** from a sentence using **spaCy**, **TextBlob**, and **NetworkX**. The opinion map visually represents the relationships between entities, actions, objects, context, and sentiment.

<img width="750" height="450" alt="image" src="https://github.com/user-attachments/assets/371e32a7-9206-48ab-b3fd-c9e919e9106b" />

---

## Features

- **Named Entity Recognition (NER)**: Extracts entities such as organizations, locations, and dates.
- **Dependency Parsing**: Identifies the main action (verb) and objects.
- **Context Extraction**: Captures location and time references.
- **Sentiment Analysis**: Determines the sentiment (positive, neutral, negative) of the sentence.
- **Graph Visualization**: Uses NetworkX and Matplotlib to visualize the opinion map.

---

## Requirements

- Python 3.8+
- Libraries:
  - spaCy
  - textblob
  - networkx
  - matplotlib

### Install Dependencies
```bash
pip install spacy textblob networkx matplotlib
python -m spacy download en_core_web_sm
```

---

## Usage

1. Clone the repository or download the files.
2. Ensure dependencies are installed.
3. Run the script `opinion_map.py` (the Python code provided):

```bash
python opinion_map.py
```

4. The program will:
   - Analyze the input sentence.
   - Extract entities, actions, objects, and context.
   - Compute sentiment.
   - Display a visual opinion map using Matplotlib.

### Example
Input Sentence:
```text
Apple is planning to open a new office in London next year.
```

Output Graph:
```
    (Apple)
       |
  planning to open
       |
   (New Office)
    /        \
(London)   (Next Year)
       |
  Sentiment: Neutral/Slightly Positive
```

Nodes are color-coded:
- Skyblue: Entities
- Orange: Actions
- Light Green: Objects
- Violet: Context (Location/Time)
- Pink: Sentiment

---

