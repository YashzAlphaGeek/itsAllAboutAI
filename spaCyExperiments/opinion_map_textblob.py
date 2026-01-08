import spacy
from textblob import TextBlob
import networkx as nx
import matplotlib.pyplot as plt

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Sentence to analyze
text = "Apple is planning to open a new office in London next year."
doc = nlp(text)

# --- Step 1: Extract entities ---
entities = {ent.text: ent.label_ for ent in doc.ents}

# --- Step 2: Extract main action and object ---
action = ""
obj = ""
for token in doc:
    if token.dep_ == "ROOT":  # main verb
        action = token.text
    if token.dep_ in ("dobj", "pobj"):  # direct or prepositional object
        obj = token.text

# --- Step 3: Extract context (location & time) ---
context = {}
for ent in doc.ents:
    if ent.label_ in ["GPE", "LOC"]:
        context["Location"] = ent.text
    elif ent.label_ in ["DATE", "TIME"]:
        context["Time"] = ent.text

# --- Step 4: Sentiment analysis ---
blob = TextBlob(text)
sentiment = "Positive" if blob.sentiment.polarity > 0.05 else \
            "Negative" if blob.sentiment.polarity < -0.05 else "Neutral"

# --- Step 5: Build Opinion Map using networkx ---
G = nx.DiGraph()

# Add nodes
for ent in entities:
    G.add_node(ent, type="entity")
if action:
    G.add_node(action, type="action")
if obj:
    G.add_node(obj, type="object")
for k, v in context.items():
    G.add_node(v, type="context")
G.add_node(f"Sentiment: {sentiment}", type="sentiment")

# Add edges
if "Apple" in entities:
    if action:
        G.add_edge("Apple", action)
if action and obj:
    G.add_edge(action, obj)
for k, v in context.items():
    G.add_edge(obj, v)
G.add_edge(obj, f"Sentiment: {sentiment}")

# --- Step 6: Draw the graph ---
pos = nx.spring_layout(G, seed=42)  # positions
colors = []
for node in G.nodes(data=True):
    if node[1]["type"] == "entity":
        colors.append("skyblue")
    elif node[1]["type"] == "action":
        colors.append("orange")
    elif node[1]["type"] == "object":
        colors.append("lightgreen")
    elif node[1]["type"] == "context":
        colors.append("violet")
    else:
        colors.append("pink")  # sentiment

plt.figure(figsize=(10,6))
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2000, font_size=10, arrowsize=20)
plt.title("Opinion Map")
plt.show()
