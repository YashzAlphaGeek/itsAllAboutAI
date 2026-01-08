import spacy
from transformers import pipeline
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# Step 0: Load NLP Models
# -----------------------------
nlp = spacy.load("en_core_web_sm")

# Use PyTorch framework to avoid TensorFlow/Keras issues
sentiment_pipeline = pipeline("sentiment-analysis", framework="pt")  # Transformer model

# -----------------------------
# Step 1: Input Sentence
# -----------------------------
text = "Apple is planning to open a new office in London next year."
doc = nlp(text)

# -----------------------------
# Step 2: Extract Entities
# -----------------------------
entities = {ent.text: ent.label_ for ent in doc.ents}

# -----------------------------
# Step 3: Extract Main Action & Object
# -----------------------------
action = ""
obj = ""
for token in doc:
    if token.dep_ == "ROOT":
        action = token.text
    if token.dep_ in ("dobj", "pobj"):
        obj_tokens = [child.text for child in token.lefts if child.dep_ in ("amod", "det")]
        obj_tokens.append(token.text)
        obj = " ".join(obj_tokens)

# -----------------------------
# Step 4: Extract Context (Location & Time)
# -----------------------------
context = {}
for ent in doc.ents:
    if ent.label_ in ["GPE", "LOC"]:
        context["Location"] = ent.text
    elif ent.label_ in ["DATE", "TIME"]:
        context["Time"] = ent.text

# -----------------------------
# Step 5: Transformer Sentiment
# -----------------------------
def get_sentiment_label(text):
    result = sentiment_pipeline(text)
    return result[0]["label"]  # POSITIVE / NEGATIVE

sentiment = get_sentiment_label(text)

# -----------------------------
# Step 6: Build Opinion Map Graph
# -----------------------------
G = nx.DiGraph()

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
if "Apple" in entities and action:
    G.add_edge("Apple", action)
if action and obj:
    G.add_edge(action, obj)
for k, v in context.items():
    G.add_edge(obj, v)
G.add_edge(obj, f"Sentiment: {sentiment}")

# -----------------------------
# Step 7: Visualize Graph
# -----------------------------
pos = nx.spring_layout(G, seed=42)
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
        colors.append("pink")

plt.figure(figsize=(12,6))
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2500, font_size=10, arrowsize=20)
plt.title("Opinion Map with Transformer Sentiment (PyTorch)", fontsize=14)
plt.show()